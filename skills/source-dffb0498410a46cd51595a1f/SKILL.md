---
name: build-zoom-bot
description: Build a Zoom meeting bot, recorder, or real-time media workflow. Use when joining meetings programmatically, processing live media or transcripts, or combining Meeting SDK, RTMS, and backend services.
---

# /build-zoom-bot

Use this skill for automation that joins meetings, captures media, or reacts to live session data.

## Covers

- Bot architecture
- Meeting join strategy
- Real-time media and transcript handling
- Backend orchestration
- Storage, post-processing, and event flow design

## Workflow

1. Clarify whether the bot needs to join, observe, transcribe, summarize, or act.
2. Select the Marketplace app model for Meeting SDK, Meeting/Webinar RTMS, or Contact Center Voice RTMS before implementation.
3. Route to Meeting SDK and RTMS as the core implementation path.
4. Add REST API for meeting/resource management and Webhooks for asynchronous events when needed.
5. Call out environment and lifecycle constraints early.

## Primary References

- [meeting-sdk](../meeting-sdk/SKILL.md)
- [setup-zoom-marketplace-app](../setup-zoom-marketplace-app/SKILL.md)
- [rtms](../rtms/SKILL.md)
- [scribe](../scribe/SKILL.md)
- [rest-api](../rest-api/SKILL.md)
- [webhooks](../webhooks/SKILL.md)

## Common Mistakes

- Treating batch transcription and live media as the same workflow
- Designing the bot before defining join authority and auth model
- Forgetting post-meeting storage and retry behavior
