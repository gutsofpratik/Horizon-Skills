# Live Mode Node Relay

Use a trusted backend relay because browser WebSocket clients cannot attach the required Zoom
`Authorization` header. The browser sends session JSON and binary PCM16 frames to your relay; the
relay forwards them to Zoom and returns Zoom's events.

## Upstream Connection

```js
import { WebSocket } from 'ws';

const upstream = new WebSocket(
  'wss://api.zoom.us/v2/aiservices/scribe/live',
  ['live-asr'],
  {
    headers: {
      Authorization: `Bearer ${generateZoomAiServicesJwt()}`,
    },
  },
);

upstream.on('open', () => {
  upstream.send(JSON.stringify({
    type: 'session.update',
    language: 'en-US',
    audio: { format: 'pcm16' },
  }));
});

upstream.on('message', (data) => {
  const event = JSON.parse(data.toString());
  if (event.type === 'transcription.completed') {
    persistSegment(event.item_id, event.transcript, {
      startMs: event.audio_start_ms,
      endMs: event.audio_end_ms,
      latencyMs: event.transcription_latency_ms,
    });
  } else if (event.type === 'error') {
    console.error(event.error.code, event.error.message);
    if (event.error.fatal) upstream.close();
  }
});
```

## Audio Contract

- Send raw binary frames only after `session.update`.
- Use PCM16 little-endian, 16 kHz, mono audio.
- Target approximately `1600` samples, or `100 ms`, per frame.
- Keep `session.update` and `session.close` as JSON text frames.
- Do not Base64-encode audio.

For a browser microphone, capture with `getUserMedia`, convert `Float32` samples to signed
16-bit PCM in an `AudioWorklet`, and send each `ArrayBuffer` to your backend WebSocket. The
backend must generate the JWT and own the Zoom connection.

## Relay Lifecycle

1. Authenticate the browser/client to your relay before accepting audio.
2. Open the Zoom socket and buffer only a bounded amount of client data while it connects.
3. Forward text frames as control messages and binary frames as audio without changing their type.
4. Propagate Zoom events to the client and log handshake status, session ID, fatal errors, and close reason.
5. On stop, cease audio, send `{ "type": "session.close" }`, wait for final
   `transcription.completed` events and `session.closed`, then close both sockets.
6. Apply backpressure and per-user session limits; never allow an unbounded pre-open frame queue.

## Limits

- Default maximum session duration: `60 minutes`.
- Default idle timeout: `30 seconds` without audio.
- Concurrent sessions per account: Default `20`, Enterprise `100`, Large Contact Center `1,000`, Custom `5,000+`.

Source: https://developers.zoom.us/docs/ai-services/scribe/live-mode/
