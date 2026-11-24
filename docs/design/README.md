# Detailed design references

These are the original full Phase 1 AD documents; **read only role-relevant sections**. See [role-based reading guide](../README.md) and [new decisions](../team/DECISIONS.md) for selected Express ↔ private Python AI HTTP architecture.

- [AD-01 Component Architecture](COMPONENT_ARCHITECTURE.md)
- [AD-02 Data Model](DATA_MODEL.md)
- [AD-03 Full Phase 1 API Contract](API_CONTRACT.md)
- [AD-04 Implementation Plan](IMPLEMENTATION_PLAN.md)

Earlier AD-03/04 assume a predefined Question Bank. That historical plan is not silently equivalent to the new content-grounded Python AI flow; review current [HTTP](../contracts/HTTP_API.md) and [private Python wire](../backend/ai/PYTHON_HTTP_PROTOCOL.md) contracts before integration.
