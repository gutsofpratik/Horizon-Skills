# High-Level Scenarios

## Scenario 1: On-Demand Upload Transcription

Use fast mode when a user uploads one file and expects a transcript immediately.

Flow:
1. Browser uploads file to your backend.
2. Backend generates Build JWT.
3. Backend calls `POST /aiservices/scribe/transcribe`.
4. Backend returns transcript JSON to the caller.

Common downstream uses:
- post-call summaries
- ticket enrichment
- searchable clip libraries
- internal review or handoff notes

## Scenario 2: Batch S3 Archive Transcription

Use batch mode when call archives or media libraries already live in S3.

Flow:
1. Build a batch request with input prefix and output prefix.
2. Submit `POST /aiservices/scribe/jobs`.
3. Track state by webhook or polling.
4. Read `/jobs/{jobId}/files` for per-file success/failure.
5. Ingest outputs into search, analytics, or storage.

Common downstream uses:
- compliance and audit logging
- searchable webinar or podcast archives
- bulk transcript backfills
- QA scoring inputs

## Scenario 3: Zoom Recording Export + Re-Transcription

Use when you must re-process Zoom-managed recordings with your own transcript settings.

Skill chain:
- `zoom-rest-api` to fetch/download recordings
- `scribe` to transcribe exported media

Typical reasons:
- you need your own retention/search pipeline
- you need different transcript settings than Zoom-managed defaults
- you want to enrich recordings with your own summarization or tagging flow

## Scenario 4: Compliance / QA Processing

Use batch mode when transcripts must be generated offline for audits, QA scoring, or archival search.

Prefer:
- `word_time_offsets=true` when reviewers need precise excerpts
- `channel_separation=true` for stereo call recordings
- webhook + queue ingestion instead of synchronous polling for large volumes

## Scenario 5: Customer Support Voice-to-Insights Pipeline

Use when support call recordings should feed operational analytics instead of stopping at raw transcript text.

Flow:
1. Ingest call recordings from storage or exported meeting assets.
2. Transcribe with `scribe`.
3. Store transcript plus speaker/timing metadata.
4. Run downstream sentiment, keyword, escalation, or QA logic in your own pipeline.

Guardrail:
- keep `scribe` focused on transcription
- do sentiment analysis, keyword detection, or scoring in downstream services after transcript generation

## Scenario 6: Live Voice Agent or Browser Captions

Use Live Mode when a voice agent, caption UI, or browser microphone flow needs continuous
segment-level transcription without waiting for file uploads.

Flow:
1. Browser or audio source sends PCM16 frames to your authenticated backend relay.
2. Relay connects to `wss://api.zoom.us/v2/aiservices/scribe/live` with `live-asr` and a Build JWT.
3. Relay sends `session.update` and forwards binary 16 kHz mono PCM16 frames.
4. Application consumes `transcription.completed` events and persists completed segments.
5. Application sends `session.close` and drains final events before disconnecting.

Guardrail:
- keep the Zoom JWT and Build credentials on the backend
- use RTMS instead when the source is a Zoom meeting and the workflow needs meeting-native media,
  participant context, video, screen share, chat, or transcript streams

## Scenario 7: Legacy Browser Microphone Chunking

Use repeated Fast Mode uploads only when a backend WebSocket relay cannot be deployed.

Flow:
1. Browser records standalone `5-10` second files.
2. Backend submits each file through an async Fast Mode wrapper.
3. Frontend polls by request ID and appends results in order.

This fallback has upload overhead, file-container boundaries, and transcript stitching drift.
Do not choose it over Live Mode for new continuous-audio products.
