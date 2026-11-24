# Public API — Frontend ↔ Express

Read [HTTP_API.md](HTTP_API.md) for the **proposed** browser-facing REST API covering US-01/02/03/05/06. Backend A/B/C own different route groups but share one Express server and one error/session convention.

**Do not use this contract for Express ↔ Python.** The private Python service protocol is [backend/ai/PYTHON_HTTP_PROTOCOL.md](../backend/ai/PYTHON_HTTP_PROTOCOL.md); React never calls it. General documentation index: [docs/README.md](../README.md).
