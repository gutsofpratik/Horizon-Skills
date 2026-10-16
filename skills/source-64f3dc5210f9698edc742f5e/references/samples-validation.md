# Samples Validation

Validated against:
- https://github.com/zoom/ai-services-quickstart/
- Live Mode quickstart commit `3daa38378b8171bbba24b75ced5afba5f25216eb` (2026-07-31)
- official docs pages under `docs/ai-services/`
- AI Services OpenAPI inventory at `api-hub/ai-services/methods/endpoints.json`
- Zoom blog context:
  - `introducing-zoom-ai-services`
  - `voice-insights-modernize-customer-support-with-scribe`

## What the official quickstart confirms

- Node/Express proxy architecture is a valid implementation model.
- The current official quickstart covers Scribe, Summarizer, and Translator from one AI Services app.
- The current quickstart includes Scribe Live Mode through a backend WebSocket relay at
  `/live/scribe`; the relay connects upstream with `live-asr` and injects a fresh Build JWT.
- Its browser path uses an `AudioWorklet` to emit PCM16 little-endian, 16 kHz, mono audio in
  approximately 100 ms frames.
- Its relay preserves text/binary frame types, queues frames until the upstream opens, and maps
  upstream handshake failures into actionable client errors.
- Fast mode can be proxied as multipart upload handling on your server even though the docs show JSON examples.
- Batch mode commonly injects AWS credentials into request payloads.
- Webhook verification uses `x-zm-signature` + `x-zm-request-timestamp` with HMAC-SHA256 and `sha256=` prefix.
- The quickstart uses `ZOOM_API_KEY` / `ZOOM_API_SECRET` naming.

## Useful implementation details from the sample

- `multer` memory storage is enough for a small fast-mode demo.
- Batch helper routes are naturally expressed as:
  - `POST /batch/jobs`
  - `GET /batch/jobs`
  - `GET /batch/jobs/:jobId`
  - `GET /batch/jobs/:jobId/files`
  - `DELETE /batch/jobs/:jobId`
- It is practical to keep one `generateJWT()` helper and inject the bearer token per request.
- Live Mode clients should send `session.update`, process completed segment/error events, and
  send `session.close` before disconnecting.
- The quickstart also handles `transcription.delta`, but the current Live Mode event table does
  not document it. Treat delta events as optional and build correctness around
  `transcription.completed`.

## Caveats from the sample

- The README setup command still says to clone `zoom/scribe-quickstart.git`; the current repo name is `zoom/ai-services-quickstart.git`.
- It assumes Node `>=24`, which is stricter than many deployment environments actually need. Verify your runtime before copying that constraint unchanged.
- It uses environment-injected AWS credentials. Production pipelines may prefer pre-signed URLs or short-lived STS credentials only.
- The sample is an app demo, not a complete production reference for job retry policy, durable queues, or transcript storage.
- The sample relay uses an in-memory pre-open frame queue. Production relays should bound that
  queue, apply backpressure, authenticate clients, and enforce per-user/session limits.

## What the blog posts add

- They reinforce the highest-value downstream use cases:
  - post-call summaries
  - ticket enrichment
  - compliance/audit logging
  - searchable archives
  - customer-support QA workflows
- They are useful for scenario framing, but not as authoritative API surface documentation.
- Keep endpoint and request-shape decisions anchored to the AI Services docs and API Hub inventory, not the blog wording.
