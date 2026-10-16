# Scribe Transcription Pipeline

Use AI Services Scribe when live audio, a file, or a storage object should become transcript
segments, a transcript JSON payload, or transcript files.

## Skill Chain

- Primary: [../../scribe/SKILL.md](../../scribe/SKILL.md)
- Optional storage/download source: [../../rest-api/SKILL.md](../../rest-api/SKILL.md)
- Optional webhook hardening: [../../webhooks/SKILL.md](../../webhooks/SKILL.md)

## When to Use Scribe

Use `scribe` for:
- generic continuous audio for voice agents, captions, or microphone transcription
- one uploaded file that should be transcribed immediately
- S3 archive transcription in the background
- post-processing exported media files into searchable transcript data

Do not use `scribe` for:
- Zoom meeting-native multi-modal stream ingestion
- bot-style participant join and raw recording

For those, use:
- [../../rtms/SKILL.md](../../rtms/SKILL.md) for live media streams
- [../../meeting-sdk/linux/SKILL.md](../../meeting-sdk/linux/SKILL.md) for visible meeting bots

## Minimal Flow

```text
live audio, input file, or storage prefix
  -> generate Build JWT
  -> choose live, fast, or batch mode
  -> stream audio or submit Scribe request
  -> receive transcript events, JSON, or batch job state
  -> persist transcript output
```

## Typical Variants

1. Live mode
   - continuous PCM16 audio
   - authenticated backend WebSocket relay
   - `wss://api.zoom.us/v2/aiservices/scribe/live`

2. Fast mode
   - one short file
   - immediate response needed
   - `POST /aiservices/scribe/transcribe`

3. Batch mode
   - long recordings or many files
   - `POST /aiservices/scribe/jobs`
   - monitor with polling or webhook notifications

4. Zoom recording re-transcription
   - use REST API to download or export recording files
   - feed those files into Scribe for your own transcript settings

## Common Failure Points

- wrong credential type (Build JWT vs normal OAuth token)
- exposing the Build JWT in browser code instead of using a backend relay
- sending encoded/JSON audio instead of binary PCM16 little-endian, 16 kHz, mono frames
- choosing RTMS for offline archive transcription
- expired S3 credentials for batch jobs
- webhook signature verification implemented after JSON parsing instead of on raw body
