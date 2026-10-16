# Zoom AI Services Scribe API Reference

Canonical sources:
- OpenAPI JSON: https://developers.zoom.us/api-hub/ai-services/methods/endpoints.json
- Docs overview: https://developers.zoom.us/docs/ai-services/scribe/
- Live Mode: https://developers.zoom.us/docs/ai-services/scribe/live-mode/
- Base URL: `https://api.zoom.us/v2`

## Endpoint Inventory

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| WebSocket | `wss://api.zoom.us/v2/aiservices/scribe/live` | Live audio transcription | Not a REST operation |
| POST | `/aiservices/scribe/transcribe` | Scribe (Synchronous) | `createFastAsr` |
| POST | `/aiservices/scribe/jobs` | Submit Batch Scribe Job | `submitBatchAsr` |
| GET | `/aiservices/scribe/jobs` | List Batch Jobs | `listBatchJobs` |
| GET | `/aiservices/scribe/jobs/{jobId}` | Get Batch Job Status | `getBatchJobStatus` |
| DELETE | `/aiservices/scribe/jobs/{jobId}` | Cancel Batch Job | `cancelBatchJob` |
| GET | `/aiservices/scribe/jobs/{jobId}/files` | List Batch Job Files | `listBatchJobFiles` |
| GET | `/aiservices/scribe/jobs/{jobId}/files/{fileId}` | Get Batch Scribe Job File | `getBatchScribeJobFile` |

## Live Mode Contract

Connection requirements:
- WebSocket endpoint: `wss://api.zoom.us/v2/aiservices/scribe/live`
- subprotocol: `live-asr`
- header: `Authorization: Bearer <Zoom AI Services JWT>`
- connect from a trusted backend; browsers cannot set the required WebSocket authorization header

Session configuration:

```json
{
  "type": "session.update",
  "language": "en-US",
  "audio": {
    "format": "pcm16"
  }
}
```

Audio requirements:
- binary PCM16 frames, not JSON or Base64
- little-endian, 16 kHz, mono
- approximately 100 ms per frame

Documented server events:

| Event | Important fields |
|-------|------------------|
| `session.created` | `session_id` |
| `session.updated` | none |
| `input_audio_buffer.speech_started` | `item_id`, `audio_start_ms` |
| `input_audio_buffer.speech_stopped` | `item_id`, `audio_end_ms` |
| `transcription.completed` | `item_id`, `transcript`, `audio_start_ms`, `audio_end_ms`, `transcription_latency_ms` |
| `error` | `error.code`, `error.message`, `error.fatal` |
| `session.closed` | `reason` |

Close by stopping audio, sending `{ "type": "session.close" }`, draining remaining final
transcription events through `session.closed`, and then closing the socket.

Live Mode defaults:
- maximum session duration: 60 minutes
- idle timeout: 30 seconds without audio
- concurrent sessions per account: Default 20, Enterprise 100, Large Contact Center 1,000,
  Custom 5,000+

## Request Shapes

### `POST /aiservices/scribe/transcribe`

Required top-level fields:
- `file`
- `config`

Common config fields:
- `language`
- `word_time_offsets`
- `channel_separation`
- `timestamps`
- `output_format`
- `profanity_filter`
- `diarization`

Response keys:
- `request_id`
- `duration_sec`
- `model`
- `result`

### `POST /aiservices/scribe/jobs`

Required top-level fields:
- `input`
- `output`
- `config`

Input subfields:
- `mode` (`SINGLE`, `PREFIX`, `MANIFEST`)
- `source` (`S3` in current spec)
- `uri`
- `manifest`
- `filters.include_globs`
- `filters.exclude_globs`
- `auth.aws.access_key_id`
- `auth.aws.secret_access_key`
- `auth.aws.session_token`

Output subfields:
- `destination`
- `uri`
- `layout` (`SINGLE`, `PREFIX`, `ADJACENT`)
- `auth.aws.*`

Config subfields:
- `language`
- `word_time_offsets`
- `channel_separation`
- `diarization`
- `profanity_filter`
- `output_format`
- `segmentation_mode`

Optional:
- `reference_id`
- `notifications.webhook_url`
- `notifications.secret`

Response keys:
- `job_id`
- `state`
- `submitted_at`

### `GET /aiservices/scribe/jobs`

Query params:
- `state`
- `page_size`
- `next_page_token`

Response keys:
- `jobs`
- `next_page_token`

### `GET /aiservices/scribe/jobs/{jobId}`

Path params:
- `jobId`

Response keys:
- `job_id`
- `state`
- `submitted_at`
- `summary`

### `GET /aiservices/scribe/jobs/{jobId}/files`

Path params:
- `jobId`

Query params:
- `page_size`
- `next_page_token`

Response keys:
- `files`
- `next_page_token`

### `GET /aiservices/scribe/jobs/{jobId}/files/{fileId}`

Path params:
- `jobId`
- `fileId`

Response keys:
- `file_id`
- `input_uri`
- `output_uri`
- `state`
- `duration_sec`
- `error`

## Current Limits and Constraints Observed in Sources

- Batch manifest max: `1000` file URIs.
- `include_globs` max items: `10`.
- `exclude_globs` max items: `10`.
- Audio/media formats called out in docs: `WAV`, `MP3`, `M4A`, `MP4`.
- Batch job rate limit label in the OpenAPI description: `LIGHT`.
