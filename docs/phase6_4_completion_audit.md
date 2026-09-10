# Phase 6.4 — Main/UI Bridge Completion Audit

## Status

Phase 6.4 is complete.

Latest implementation commit:

246b0b8 Phase 6.4: enforce main UI bridge boundary

## Verification

The production execution path is:

User Interface / Voice
→ main.py
→ ai.decision.decide()
→ core.controlled_router
→ core.execution_service
→ core.tool_executor
→ Policy / Confirmation
→ Authorized Tool

## Main/UI Boundary

main.py:

- does not import ToolExecutor
- does not construct ToolExecutor
- does not call tool.run()
- does not directly execute plugins
- obtains the authoritative ExecutionService
- obtains the explicit tool registry
- delegates decisions to ai.decision.decide()
- handles human confirmation at the UI boundary
- uses ExecutionService.execute_approved() for approved actions

## Executor Ownership

The only production ToolExecutor import and construction are inside:

core/execution_service.py

ExecutionService owns the authoritative runtime ToolExecutor.

High-level production components do not directly construct ToolExecutor instances.

## LLM / Brain Isolation

The local Ollama/Qwen provider:

- accepts conversational input
- returns conversational text
- has no ToolExecutor access
- has no ToolRegistry access
- has no direct tool execution capability
- cannot approve its own actions

The Brain likewise has no direct execution authority.

## Policy and Confirmation

The execution boundary enforces:

- READ_ONLY → allow
- STATE_CHANGING → confirmation required
- DESTRUCTIVE → deny
- unknown/unsupported capability → fail closed

Approved state-changing actions are executed through the authorized ExecutionService path.

## Legacy Router

core/router.py remains present for regression compatibility.

No active production path uses the legacy router.

The controlled router is the production execution path.

## Dynamic Plugin Loaders

core/plugin_loader.py and core/plugin_manager.py remain in the repository.

Their continued existence is not treated as a Phase 6.4 boundary failure.

They require a separate reachability/dependency audit before any removal or redesign.

## Compatibility Seam

ai/decision.py and core/controlled_router.py retain an executor-injection compatibility seam:

ExecutionService(executor=executor)

This is not currently an active Qwen/Brain/UI bypass.

It remains a future hardening candidate and must not be removed without corresponding test analysis.

## Test Evidence

Phase 6.4 dedicated boundary tests:

23 passed

Full regression baseline:

319 passed
1 skipped
0 failed

The skipped test is platform-dependent battery API coverage.

## Conclusion

Phase 6.4 successfully establishes the Main/UI execution boundary.

The critical security invariant remains intact:

Qwen/Brain/UI must not receive a direct execution path to ToolExecutor.

No production execution bypass was identified by the Phase 6.4 audit.

Further hardening should be handled as a separately scoped phase.
