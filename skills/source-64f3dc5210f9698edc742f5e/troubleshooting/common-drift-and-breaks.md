# Common Drift and Breaks

## 1. Auth fails even though credentials look correct

Likely causes:
- wrong credential pair from the portal
- expired JWT
- mixing Build-platform credentials with non-Build Zoom app credentials
- valid-looking key/secret pair that is not authorized for AI Services Scribe

Check:
- `iss` value
- `exp` window
- current credential labels in portal
- if the API responds with `{"code":124,"message":"Invalid Access token"}`, treat that as a real upstream auth failure, not a transport problem

## 2. Fast mode request shape mismatch

Docs show JSON with `file` URL, but the official quickstart also proxies multipart upload and forwards a `FormData` request.

Use one clear model per service boundary:
- client upload -> your backend multipart
- backend upload proxy -> `multipart/form-data` to `/aiservices/scribe/transcribe`
- backend URL-based submit -> JSON body with `file` URL

Symptoms:
- browser request stays pending for a long time
- backend eventually returns timeout or empty upstream reply

Preferred fix:
- treat uploaded files and URL-based files as two separate request paths instead of forcing both through one JSON shape
- exception: a browser microphone demo may intentionally wrap short chunks as JSON `data:` URLs to avoid multipart edge behavior, but treat that as a demo-specific transport choice, not the default upload design

## 3. Fast mode returns `413 Request Entity Too Large`

Likely cause:
- reverse proxy rejected the upload before the request reached your app

Known deployment check:
- if nginx fronts the app, raise `client_max_body_size` to match or exceed your server-side upload limit

Current Scribe fast-mode API limits:
- maximum file size: `100 MB`
- maximum duration: `2 hours`

## 4. Fast mode returns `504 Gateway time-out`

Likely cause:
- the request reached your backend, but synchronous processing took too long for the edge/proxy path

Observed deployment behavior:
- public HTTPS can time out even when the same request path is valid and the backend is healthy
- observed hosted sample timings:
  - ~17.2 MB MP4: ~26s
  - ~38.6 MB MP4: ~26-37s
  - ~59.2 MB MP4: ~32-34s backend completion, but some browser requests still timed out first

Guardrail:
- use fast mode for smaller, interactive files
- use batch mode for large uploads or longer media where waiting synchronously through the web UI is brittle
- add request-level logging for:
  - file name
  - file size
  - mime type
  - upstream elapsed time
  - response payload size and top-level keys
  so you can tell whether the origin completed successfully while the browser/edge timed out
- for hosted UIs, wrap fast mode in an async request/polling flow instead of holding the browser open for the entire upstream response
- if nginx access logs show `499` while app logs later show `zoom_request_finished status: 200`, the transcription succeeded and only the browser-side request path was lost

## 5. Batch job accepted but outputs never appear

Likely causes:
- S3 URI/auth mismatch
- expired STS credentials
- output layout/URI mismatch
- webhook endpoint unreachable if you rely on callbacks

Check:
- `/jobs/{jobId}` summary
- `/jobs/{jobId}/files`
- cloud storage permissions

## 6. Webhook verification fails

Current sample pattern uses:
- `x-zm-signature`
- `x-zm-request-timestamp`
- HMAC-SHA256 with `sha256=` prefix

If verification fails:
- confirm raw body capture before JSON parsing
- confirm timestamp header was included in the signed string
- confirm the shared secret matches the job notification config

## 7. Health check says credentials exist, but API calls still fail

Likely cause:
- environment file contains literal placeholders such as `${ZOOM_API_KEY}` or `${ZOOM_API_SECRET}`

Guardrail:
- only treat credentials as present if they are real values, not unresolved shell placeholders
- fail fast with a clear credential error before attempting Zoom calls

## 8. Wrong product chosen

Symptoms:
- trying to use Scribe Live Mode when the workflow needs Zoom meeting-native participant/media context
- trying to use RTMS for offline archive transcription

Guardrail:
- file/storage transcription -> `scribe`
- generic continuous audio transcription -> Scribe Live Mode
- Zoom meeting-native audio/video/transcript/share/chat streams -> `rtms`

## 9. Browser microphone chunk 1 works but later chunks are empty

Likely cause:
- the browser emitted a valid first container chunk, but later `MediaRecorder` timeslice blobs were partial WebM/Opus clusters without fresh container headers

Symptoms:
- chunk 1 transcribes normally
- chunk 2 onward returns empty transcript text or much weaker results
- auth and request flow still look healthy

Preferred fix:
- do not rely on one long `MediaRecorder.start(timeslice)` session for standalone chunk uploads
- rotate the recorder per chunk instead:
  - start recorder
  - record one chunk window
  - stop recorder
  - upload that blob
  - start a new recorder for the next chunk

Guardrail:
- treat browser microphone pseudo-streaming as a file-container problem first, not a Scribe-language-model problem

## 10. Live Mode WebSocket handshake fails

Likely causes:
- missing `live-asr` subprotocol
- missing, expired, or invalid Zoom AI Services JWT
- credentials are not provisioned for AI Services
- account concurrency limit reached

Check the upstream HTTP status before treating it as a generic socket failure:
- `401`/`403`: verify Build credentials and JWT generation
- `404`: verify AI Services provisioning and the exact `/v2/aiservices/scribe/live` endpoint
- `429`: enforce concurrency limits and retry with backoff

## 11. Live Mode connects but no transcript arrives

Check:
- `session.update` was sent after the socket opened
- `audio.format` is exactly `pcm16`
- audio is binary PCM16 little-endian, 16 kHz, mono
- frames are approximately 100 ms rather than Base64 or JSON-wrapped audio
- the session has not hit the 30-second no-audio idle timeout
- speech start/stop events and all server `error` events are logged

## 12. Browser Live Mode authentication fails

Cause:
- browser WebSocket clients cannot attach the required `Authorization` header, or credentials
  were incorrectly placed in client-side code

Fix:
- connect the browser to an authenticated backend WebSocket relay
- generate the AI Services JWT on that backend
- let the backend open the authenticated Zoom socket and preserve text/binary frame types

## 13. Final words are missing when stopping Live Mode

Likely cause:
- the client closed the WebSocket immediately after the last audio frame

Fix:
1. stop sending audio
2. send `{ "type": "session.close" }`
3. continue reading final `transcription.completed` events
4. wait for `session.closed`
5. close the socket
