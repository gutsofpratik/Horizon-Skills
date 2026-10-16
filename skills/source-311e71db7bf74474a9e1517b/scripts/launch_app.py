#!/usr/bin/env python3
"""Launch the FiftyOne App for Playwright automation with trigger-file IPC.

This implements "option A" from the fiftyone-app-playwright skill: the App is
launched with ``remote=True`` and the process stays alive in a watcher loop
*instead of* ``session.wait()``. Touching the trigger file makes this process
reload the dataset and push a refresh event over the EXISTING WebSocket.

Why this matters: the most common way to crash a FiftyOne automation session is
to ``browser_navigate`` / ``location.reload()`` after an operator that calls
``ctx.ops.reload_dataset()`` -- that closes the active WebSocket mid-reload and
``session.wait()`` exits, silently killing the server. ``session.refresh()``
does NOT close the socket, so driving refreshes through this trigger file lets
you update the grid/sidebar without ever navigating.

Run it detached so it survives the launching shell, e.g.::

    nohup python scripts/launch_app.py \
        --source quickstart --clone verify_clone --port 5151 \
        > /tmp/fo_app.log 2>&1 &

Then, from the automation side, request a reload + refresh with::

    touch /tmp/fo_refresh.trigger

The trigger path, port, and dataset names are all parameters -- nothing here is
specific to any one project. Extend ``watch()`` if you need the loop to perform
other side effects (mutate samples, create views, etc.) on each trigger.
"""

from __future__ import annotations

import argparse
import os
import time

import fiftyone as fo


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Launch the FiftyOne App with a trigger-file refresh loop.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Existing dataset to clone for the session (e.g. 'quickstart').",
    )
    parser.add_argument(
        "--clone",
        required=True,
        help="Name for the working clone. A leftover non-persistent clone of "
        "this name is recreated on each run; a persistent one is never touched.",
    )
    parser.add_argument(
        "--port", type=int, default=5151, help="Port for the App server."
    )
    parser.add_argument(
        "--address",
        default=None,
        help="Bind address (default: FiftyOne's default, usually localhost).",
    )
    parser.add_argument(
        "--trigger",
        default="/tmp/fo_refresh.trigger",
        help="Touch this file to trigger a reload + refresh.",
    )
    parser.add_argument(
        "--persistent",
        action="store_true",
        help="Persist the clone. Omit for a throwaway (non-persistent) clone.",
    )
    parser.add_argument(
        "--poll",
        type=float,
        default=0.5,
        help="Trigger-file poll interval, in seconds.",
    )
    return parser.parse_args()


def prepare_clone(source: str, clone_name: str, persistent: bool) -> fo.Dataset:
    """Clone ``source`` into ``clone_name``, clearing a prior throwaway first.

    Non-persistent clones do NOT auto-delete on an ungraceful crash -- they
    linger in MongoDB until something removes them. We clear a leftover only
    when it is itself non-persistent, so a real (persistent) dataset that
    happens to share the name is never silently destroyed.
    """
    if fo.dataset_exists(clone_name):
        existing = fo.load_dataset(clone_name)
        if existing.persistent:
            raise SystemExit(
                f"Refusing to overwrite persistent dataset '{clone_name}'. "
                "Pick a different --clone name, or delete it deliberately first."
            )
        print(f"Removing leftover non-persistent clone '{clone_name}'", flush=True)
        fo.delete_dataset(clone_name)

    print(
        f"Cloning '{source}' -> '{clone_name}' (persistent={persistent})",
        flush=True,
    )
    return fo.load_dataset(source).clone(clone_name, persistent=persistent)


def watch(clone: fo.Dataset, session: fo.Session, trigger: str, poll: float) -> None:
    """Block forever, reloading + refreshing whenever ``trigger`` appears."""
    print(
        f"Watching trigger file: {trigger} (touch it to reload + refresh)", flush=True
    )
    while True:
        if os.path.exists(trigger):
            try:
                os.remove(trigger)
            except FileNotFoundError:
                pass  # consumed by something else; still do the refresh
            clone.reload()  # refresh this process's view of MongoDB
            session.refresh()  # push a refresh over the existing WebSocket
            print("Reloaded + refreshed.", flush=True)
        time.sleep(poll)


def main() -> None:
    args = parse_args()
    clone = prepare_clone(args.source, args.clone, args.persistent)
    session = fo.launch_app(clone, port=args.port, address=args.address, remote=True)
    print(f"App live on port {args.port} (remote=True).", flush=True)
    try:
        watch(clone, session, args.trigger, args.poll)
    except KeyboardInterrupt:
        print("\nShutting down.", flush=True)


if __name__ == "__main__":
    main()
