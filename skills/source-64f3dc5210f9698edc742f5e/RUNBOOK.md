# Scribe 5-Minute Preflight Runbook

Use this before deep debugging.

## 1) Confirm the Right Product

- Generic live audio, file-based, or storage-based transcription -> stay on `scribe`.
- Zoom meeting-native audio/video/transcript/share/chat streams -> use `rtms` instead.
- Meeting bot that joins and records before transcription -> chain Meeting SDK Linux first.

## 2) Confirm Credentials

- Build-platform issuer credential pair available.
- JWT generation uses `HS256` with one-hour-or-less expiry.
- Secret stays server-side.
- Live Mode JWT and Build credentials stay in the backend relay, never browser code.
- Reject placeholder values such as `${ZOOM_API_KEY}` and `${ZOOM_API_SECRET}`. They can make a naive health check look configured while every real call still fails.

## 3) Confirm Mode Selection

- **Live mode** for continuous voice-agent, caption, or microphone audio.
- **Fast mode** for one short file and immediate JSON response.
- **Batch mode** for many files, long recordings, or archive-style processing.
- **Browser microphone pseudo-streaming** only as a fallback when a Live Mode relay is unavailable.
- Live Mode connection contract:
  - endpoint: `wss://api.zoom.us/v2/aiservices/scribe/live`
  - subprotocol: `live-asr`
  - auth: AI Services JWT bearer header from a trusted backend
  - audio: binary PCM16 little-endian, 16 kHz, mono, approximately 100 ms frames
  - close: send `session.close`, drain final events through `session.closed`, then disconnect
- Fast mode current limits from the API spec:
  - maximum file size: `100 MB`
  - maximum duration: `2 hours`
- If fast mode is exposed through a hosted browser UI, prefer an async wrapper:
  - browser uploads once
  - backend returns `202` with a request ID
  - frontend polls for completion
  This avoids losing successful transcriptions to edge/client timeout races.
- Observed hosted timing from the deployed sample:
  - ~17.2 MB MP4 completed in ~26s
  - ~38.6 MB MP4 completed in ~26-37s
  - ~59.2 MB MP4 completed in ~32-34s on the backend
  - some ~59.2 MB requests still surfaced as frontend `504` even though the backend later completed with `200`
  Treat these as deployment observations, not hard API guarantees.
- Recommended starting browser mic cadence:
  - chunk size: `5 seconds`
  - acceptable range: `5-10 seconds`
  - keep only `2-3` chunks in flight at once
  This gives incremental transcript updates without trying to hold a single long browser request open.
- For browser mic capture, rotate the recorder per chunk so each uploaded blob is a standalone file.
  Do not assume `MediaRecorder.start(timeslice)` later chunks will always be independently transcribable.
- Do not treat chunked Fast Mode as the default production solution for live transcription.
  Prefer Scribe Live Mode for generic continuous audio and `rtms` for Zoom meeting-native streams.

## 4) Confirm Storage / Webhook Inputs

- Fast mode file URL or upload path resolves.
- Batch input/output URIs are valid.
- AWS or pre-signed access is set correctly for S3 mode.
- Webhook URL is public HTTPS if you expect notifications.

## 5) Confirm Post-Processing Contract

- Decide whether downstream code expects `text_display`, segments, or word-level timings.
- Decide whether channel separation or diarization is required before shipping.

## 6) Quick Probes

- JWT generation works locally.
- Live Mode handshake succeeds with `live-asr` and backend bearer auth.
- Live Mode emits `session.created`, accepts `session.update`, and returns
  `transcription.completed` for a known PCM16 sample.
- Graceful close produces `session.closed` after remaining final transcript segments.
- `POST /aiservices/scribe/transcribe` succeeds with a known small file.
- For normal browser-uploaded files, backend forwarding should use `multipart/form-data` to Zoom.
- Special-case demo path: short browser microphone chunks may be wrapped as JSON `data:` URLs if you intentionally choose a pseudo-streaming transport, but do not generalize that to your main file-upload flow.
- Batch submit returns `201` with `job_id`.
- Webhook signature verification works with the configured secret.

## 7) Fast Decision Tree

- `401`/auth failure -> wrong credential pair or expired JWT.
- Fast mode returns schema error -> wrong request body or config fields.
- Fast mode returns `413 Request Entity Too Large` before the app logs anything -> reverse proxy limit, not Scribe.
- Frontend returns `504` but backend logs later show `200` -> browser/edge timeout race; poll by request ID instead of assuming failure.
- Generic browser/voice-agent audio needs continuous transcription -> use Scribe Live Mode.
- Zoom meeting-native media or participant context is required -> switch to `rtms`.
- Live handshake returns `401`/`403` -> verify Build JWT; `404` -> verify AI Services provisioning; `429` -> enforce account concurrency.
- Live socket opens but returns no transcript -> verify `session.update` and binary PCM16 16 kHz mono frames.
- Final words are missing -> send `session.close` and wait for `session.closed` before disconnecting.
- Browser mic chunk 1 works but chunk 2 onward is empty -> recorder/container boundary issue; restart the recorder for each chunk.
- Batch jobs queue but never complete -> storage auth / URI / webhook issues.
- Missing transcripts for some files -> inspect `/jobs/{jobId}/files` before re-submitting whole batch.

## 8) Source Checkpoints

### Official docs

- https://developers.zoom.us/docs/ai-services/
- https://developers.zoom.us/docs/ai-services/scribe/
- https://developers.zoom.us/docs/ai-services/scribe/live-mode/
- https://developers.zoom.us/api-hub/ai-services/methods/endpoints.json

### Raw docs in repo tooling output

- `tools/zoom-crawler/raw-docs/developers.zoom.us/docs/ai-services/`
