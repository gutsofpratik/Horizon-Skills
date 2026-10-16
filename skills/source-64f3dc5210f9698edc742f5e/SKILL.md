---
name: scribe
description: "Reference skill for Zoom AI Services Scribe. Use after routing to a transcription workflow when handling live audio, uploaded or stored media, Build-platform JWT auth, Live/Fast/Batch processing modes, or transcript pipeline design."
user-invocable: false
triggers:
  - "scribe"
  - "ai services scribe"
  - "zoom scribe"
  - "transcribe audio file"
  - "transcribe video file"
  - "batch transcription"
  - "fast mode transcription"
  - "live transcription"
  - "live mode transcription"
  - "voice agent transcription"
  - "build platform jwt"
---

# Zoom AI Services Scribe

Background reference for Zoom AI Services Scribe across:
- real-time audio transcription over WebSocket (`wss://api.zoom.us/v2/aiservices/scribe/live`)
- synchronous single-file transcription (`POST /aiservices/scribe/transcribe`)
- asynchronous batch jobs (`/aiservices/scribe/jobs*`)
- webhook-driven batch status updates
- Build-platform JWT generation and credential handling

Official docs:
- https://developers.zoom.us/docs/ai-services/
- https://developers.zoom.us/docs/ai-services/scribe/
- https://developers.zoom.us/docs/ai-services/scribe/live-mode/
- https://developers.zoom.us/docs/api/ai-services/
- https://developers.zoom.us/api-hub/ai-services/methods/endpoints.json
- Quickstart sample: https://github.com/zoom/ai-services-quickstart/

## Routing Guardrail

- If the user needs **live audio, uploaded media, or stored media transcribed into text**, route here first.
- If the user needs **transcript text summarized**, route to [../summarizer/SKILL.md](../summarizer/SKILL.md).
- If the user needs **plain text translated**, route to [../translator/SKILL.md](../translator/SKILL.md).
- If the user needs **generic live audio** for voice agents, captions, or microphone transcription, use Scribe Live Mode.
- If the user needs **Zoom meeting-native audio, video, screen share, chat, or transcript streams**, route to [../rtms/SKILL.md](../rtms/SKILL.md).
- If the user needs **Zoom REST API inventory** for AI Services paths, chain [../rest-api/SKILL.md](../rest-api/SKILL.md).
- If the user needs webhook signature patterns or generic HMAC receiver hardening, optionally chain [../webhooks/SKILL.md](../webhooks/SKILL.md).

## Quick Links

1. [concepts/auth-and-processing-modes.md](concepts/auth-and-processing-modes.md)
2. [scenarios/high-level-scenarios.md](scenarios/high-level-scenarios.md)
3. [examples/live-mode-node.md](examples/live-mode-node.md)
4. [examples/fast-mode-node.md](examples/fast-mode-node.md)
5. [examples/batch-webhook-pipeline.md](examples/batch-webhook-pipeline.md)
6. [references/api-reference.md](references/api-reference.md)
7. [references/environment-variables.md](references/environment-variables.md)
8. [references/samples-validation.md](references/samples-validation.md)
9. [references/versioning-and-drift.md](references/versioning-and-drift.md)
10. [troubleshooting/common-drift-and-breaks.md](troubleshooting/common-drift-and-breaks.md)
11. [RUNBOOK.md](RUNBOOK.md)

## Core Workflow

1. Get Build-platform credentials and generate an HS256 JWT.
2. Choose **live mode** for continuous audio, **fast mode** for one short file, or **batch mode** for stored archives / large sets.
3. Open the Live WebSocket or submit the Fast/Batch request.
4. Handle Live events, a synchronous Fast response, or Batch polling/webhooks.
5. Persist and post-process transcript JSON.

## Hosted Fast-Mode Guardrail

- The formal fast-mode API limits are `100 MB` and `2 hours`, but hosted browser flows can still time out before the upstream response returns.
- Current deployed-sample observations:
  - ~17.2 MB MP4 completed in about `26s`
  - ~38.6 MB MP4 completed in about `26-37s`
  - ~59.2 MB MP4 completed in about `32-34s` on the backend
  - some ~59.2 MB browser requests still surfaced as frontend `504` while backend logs later showed `200`
- Treat frontend `504` plus backend `200` as a browser/edge timeout race, not an automatic transcription failure.
- For hosted UIs, prefer an async request/polling wrapper for fast mode instead of holding the browser open for the full upstream response.
- For larger or less predictable media, prefer batch mode even when the file is still within the formal fast-mode size limit.

## Live Mode Guardrails

- Connect from a trusted backend with the `live-asr` WebSocket subprotocol and a Zoom AI Services JWT in the `Authorization` header.
- Configure the session with `session.update`, then stream binary PCM16 little-endian, 16 kHz, mono audio in approximately 100 ms frames.
- Keep control messages as JSON text. Do not Base64-encode audio or wrap binary frames in JSON.
- Browser WebSocket clients cannot set the required authorization header. Relay browser audio through a backend that adds the JWT; never expose Build credentials or JWTs in client code.
- Treat `transcription.completed` as the documented final segment event. Handle every `error`, especially `error.fatal`.
- On shutdown, stop audio, send `session.close`, continue reading final events through `session.closed`, then close the socket.
- Live Mode defaults: 60-minute maximum session duration and 30-second no-audio idle timeout. Concurrent limits are account-tier dependent.
- Use repeated Fast Mode microphone uploads only as a legacy fallback when a WebSocket relay is impossible; Live Mode is the preferred continuous transcription path.

## Endpoint Surface

| Mode | Method | Path | Use |
|------|--------|------|-----|
| Live | WebSocket | `wss://api.zoom.us/v2/aiservices/scribe/live` | Continuous PCM16 audio and segment-level transcription events |
| Fast | `POST` | `/aiservices/scribe/transcribe` | Synchronous transcription for one file |
| Batch | `POST` | `/aiservices/scribe/jobs` | Submit asynchronous batch job |
| Batch | `GET` | `/aiservices/scribe/jobs` | List jobs |
| Batch | `GET` | `/aiservices/scribe/jobs/{jobId}` | Inspect job summary/state |
| Batch | `DELETE` | `/aiservices/scribe/jobs/{jobId}` | Cancel queued/processing job |
| Batch | `GET` | `/aiservices/scribe/jobs/{jobId}/files` | Inspect per-file results |
| Batch | `GET` | `/aiservices/scribe/jobs/{jobId}/files/{fileId}` | Inspect one per-file result |

## High-Level Scenarios

- On-demand clip transcription after a user uploads one recording.
- Real-time transcription for voice agents, live captions, and browser microphones through a backend relay.
- Batch transcription of stored S3 call archives.
- Webhook-driven ETL pipeline that writes transcripts to your database/search index.
- Re-transcription of Zoom-managed recordings after exporting them to your own storage.
- Offline compliance or QA workflows that need timestamps, channel separation, and speaker hints.

## Chaining

- Stored Zoom recordings -> [../rest-api/SKILL.md](../rest-api/SKILL.md) + `scribe`
- Transcribe then summarize -> `scribe` + [../summarizer/SKILL.md](../summarizer/SKILL.md)
- Transcribe then translate -> `scribe` + [../translator/SKILL.md](../translator/SKILL.md)
- Webhook verification hardening -> [../webhooks/SKILL.md](../webhooks/SKILL.md)
- Generic live audio transcription -> Scribe Live Mode
- Zoom meeting-native media/transcript streams -> [../rtms/SKILL.md](../rtms/SKILL.md)
- Cross-product routing -> [../general/SKILL.md](../general/SKILL.md)

## Operations

- [RUNBOOK.md](RUNBOOK.md) - 5-minute preflight and debugging checklist.
