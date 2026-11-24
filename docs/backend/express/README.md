# Backend A — Express / Auth / Course / Deadlines

**Shared transport responsibility:** Configure Express-to-Python private HTTP base URL, internal service key, request timeouts and sanitized errors; do not expose Python paths through Vite or public routes. Use [private Python protocol](../ai/PYTHON_HTTP_PROTOCOL.md) with Backend B. Backend A does not write AI prompts or model logic.

**Read in order:** [Backend coordination](../README.md) → [HTTP API](../../contracts/HTTP_API.md) → [AD-03 `4 Auth](../../API_CONTRACT.md#4-authentication-and-authorization-contract), [`5 Identity/Deadlines](../../API_CONTRACT.md#5-proposed-request-and-response-dto-examples), [`10 Errors](../../API_CONTRACT.md#10-unified-error-contract-proposed) → [AD-04 IMP-01, IMP-06A](../../IMPLEMENTATION_PLAN.md#4-small-future-codex-tasks).

**Own:** Express bootstrap/config; runtime validation, health/proxy, session store, password/authentication, CSRF+Origin/cookie policies, role/Course membership middleware, trusted Teacher/Course provisioning support, Deadline CRUD and Upcoming date logic; shared safe error mapping.

**Do not own:** AI SDK, quiz generation prompts, grading, attempt state, Mongo schema in isolation.

**First delivery:** working config + safe server startup and local proxy; followed by auth/me/assigned Courses with Backend A↔Database tests. Deadlines after that. Choose G-01/02/03/12/13/14 in AD-04 before affected code. 
**Integration handshake:** provide `requireUser` / `requireCourseRole` middleware contract and User/Course DTO to B/C/Frontend. All routes continue to validate ownership. Course timezone is configured per offering; day 0 through +7 Upcoming, +8 future visible unmarked, past hidden from Students.
