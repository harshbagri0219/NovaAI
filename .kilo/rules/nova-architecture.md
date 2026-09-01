# Project NOVA Engineering Rules

## Mission

NOVA is an offline-first personal AI assistant designed primarily for Android.

The system must remain modular, observable, testable, secure, and controllable.

## Core Architecture

The canonical execution flow is:

User
→ Interface
→ Brain
→ Planner
→ Policy Engine
→ Tool Registry
→ Tool
→ Structured Result
→ Brain
→ User

Memory is a separate subsystem.

## Brain

The Brain decides what should happen.

The Brain must NOT directly execute operating-system commands.

## Policy Engine

Every tool action must pass through the policy layer.

Actions must have explicit capability definitions.

High-impact actions require confirmation.

## Tool Layer

Tools provide capabilities.

Examples:

* Android
* Filesystem
* Network information
* Termux
* Kali/NetHunter
* System monitoring
* Documents

Tools must return structured results.

## Kali / NetHunter

Kali and NetHunter are controlled execution environments.

They are tools, not the AI brain.

Security functionality is restricted to authorized defensive, educational, and testing contexts.

## Memory

Do not store unrestricted conversation history as permanent memory.

Do not use one giant JSON file as the primary persistent memory store.

Prefer structured storage such as SQLite.

Memory must have explicit categories and retention policies.

## Offline First

Core functionality must work without internet whenever technically possible.

Network-dependent capabilities must degrade gracefully.

## Android Separation

Android-specific code must not contaminate the core Brain architecture.

The core must remain portable.

## Dependencies

Prefer minimal, well-maintained dependencies.

Do not add dependencies without justification.

## Testing

Every major subsystem requires tests.

Refactoring should not remove existing working behavior without replacement tests.

## Git

Make small logical commits.

Before major refactoring:

```text
git status
```

After successful tests:

```text
git add .
git commit
```

Never silently destroy working functionality.

## AI Agent Behavior

Before large changes:

* Inspect existing code.
* Explain intended changes.
* Identify affected files.
* Preserve working behavior.

Never perform broad rewrites unless explicitly requested.

Never delete files merely because they appear unused without proving they are unused.

## Priority

When requirements conflict, prioritize:

1. Safety
2. Existing working functionality
3. Architecture
4. Testability
5. Maintainability
6. Performance
7. New features
