---
name: code-with-restraint
description: Implement or refactor production code with happy-path-first orchestration, type-driven boundaries, deep modules, and evidence-backed complexity. Use for feature work, bug fixes, architecture changes, and simplification.
---

# Code with restraint

Make the normal use case the easiest code to read. Make every added concept pay rent by hiding real mechanics, enforcing an invariant, or isolating proven change.

When a design choice is contested, terminology is unclear, or a change needs deeper architectural reasoning, read [the design sources](references/design-sources.md). Use the core workflow alone for routine implementation.

## 1. Establish context

- Read the repository instructions and nearby conventions.
- Trace the current callsites, data flow, tests, and user-facing boundary.
- Find the existing behavior and its source of truth before adding another path.
- Separate observed constraints from imagined requirements.

Finish when the current flow, intended outcome, ownership, and verification path are concrete.

## 2. Choose the smallest honest design

- Extend an existing abstraction when it makes the behavior clearer.
- Start with a direct use-case implementation when the problem is small.
- Extract an interface, service, repository, helper, or value object when it owns an invariant, hides substantial mechanics, supports real implementations, removes stable repetition, or isolates a proven change boundary.
- Count total cost across files, call hops, types, configuration, tests, and concepts.
- Preserve security, authorization, data-integrity, concurrency, and compatibility behavior required by evidence or an existing contract.

Patterns are vocabulary for designs that emerged, not a checklist. Finish when every added concept has a concrete job larger than its cost.

## 3. Shape the happy path

- Make the top-level method read as the use case.
- Reject invalid input and broken invariants with early guards.
- Keep simple related code together. Push protocol, process, storage, and platform mechanics behind narrow, intention-revealing interfaces.
- Give mutable state and its invariants one owner.
- Keep domain decisions separate from IO when that separation removes complexity.
- Let failures reach the existing user-facing boundary unless recovery is product behavior.

Aim for orchestration with this shape:

```ts
const version = Version.parse(input)

await server.stop()
await cli.install(version)
await cli.requireVersion(version)
await server.start()
```

Finish when a reviewer can follow the normal flow top-down without reconstructing low-level mechanics.

## 4. Turn boundaries into trusted values

- Parse external, persisted, IPC, network, and configuration input once at the boundary.
- Represent legal states with precise types, tagged unions, schemas, value objects, and required parameters.
- Derive types from the source of truth instead of maintaining parallel declarations.
- Pass trusted values inward. Use assertions for conditions callers must already guarantee.
- Return the value that answers the caller's actual question.

Finish when invalid data fails at its first owned boundary and internal code no longer repeats the same validation.

## 5. Verify stable behavior

- Test the use-case boundary and observable result, order, or failure.
- Reproduce bugs before fixing them when practical, then keep the smallest test that protects the contract.
- Run focused checks proportional to the change and its risk.
- Review the final diff for pass-through layers, speculative branches, stale compatibility code, and helpers that hide no complexity.
- Update affected documentation and remove temporary artifacts.

Finish when the requested behavior works, focused verification passes, and another simplification would damage clarity, correctness, or a real boundary.
