# Design sources

Use this reference to investigate a design principle, settle an architectural tradeoff, or recover the vocabulary and provenance behind the core workflow. The operating instructions remain in [`SKILL.md`](../SKILL.md).

This skill distills Hona's [`code-like-luke` gist](https://gist.github.com/Hona/53142c07c9decb735392f132ace34003) into a shorter execution path.

## Vocabulary

| Design goal | Useful vocabulary |
| --- | --- |
| Keep main methods readable | Composed Method, intention-revealing interface, use-case orchestration |
| Coordinate well-named operations | Application Service, Use Case Interactor, Transaction Script |
| Hide substantial mechanics | Information hiding, deep modules, complexity pulled downward |
| Separate decisions from process and network work | Functional Core and Imperative Shell, Ports and Adapters |
| Organize around user behavior | Vertical Slice Architecture, use-case-driven architecture, Screaming Architecture |
| Encode invariants in types | Type-driven design, illegal states unrepresentable |
| Convert boundary input into trusted values | Parse, Don't Validate, smart constructors, refinement types |
| Enforce caller and object guarantees | Design by Contract, preconditions, postconditions, invariants |
| Keep the valid path flat | Guard clauses, fail-fast design |
| Avoid imagined requirements | YAGNI, evolutionary design, avoid speculative generality |
| Extract reuse after evidence | Rule of Three, semantic compression, AHA programming |
| Make helpers hide more than they expose | Deep modules, locality of behavior |
| Give state and behavior one owner | Encapsulation, Tell, Don't Ask, Information Expert |

## Start here

Read only as far as the current design question requires.

1. John Ousterhout, [A Philosophy of Software Design](https://stanford.edu/~ouster/cgi-bin/aposd.php), for deep modules and complexity management.
2. John Ousterhout and Robert Martin, [Ousterhout versus Clean Code](https://github.com/johnousterhout/aposd-vs-clean-code), for competing views on method size, decomposition, and abstraction.
3. Alexis King, [Parse, Don't Validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/), for trusted boundary values.
4. Scott Wlaschin, [Making Illegal States Unrepresentable](https://fsharpforfunandprofit.com/posts/designing-with-types-making-illegal-states-unrepresentable/), for type-driven invariants.
5. Gary Bernhardt, [Functional Core, Imperative Shell](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell), for separating decisions from effects.
6. Martin Fowler, [YAGNI](https://martinfowler.com/bliki/Yagni.html), for the full cost of speculative capability.
7. Casey Muratori, [Semantic Compression](https://caseymuratori.com/blog_0015), for extracting reuse after concrete examples.
8. Jimmy Bogard, [Vertical Slice Architecture](https://www.jimmybogard.com/vertical-slice-architecture/), for use-case-specific structure.
9. Alistair Cockburn, [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/), for explicit application boundaries.
10. Carson Gross, [Locality of Behaviour](https://htmx.org/essays/locality-of-behaviour/), for judging the navigation cost of abstraction.

## Focused sources

- Gary Bernhardt, [Boundaries](https://www.destroyallsoftware.com/talks/boundaries), for value-oriented cores and effectful boundaries.
- Scott Wlaschin, [Domain Modeling Made Functional](https://pragprog.com/titles/swdddf/domain-modeling-made-functional/), for domain modeling with types.
- Bertrand Meyer and Eiffel, [Design by Contract and Assertions](https://www.eiffel.org/doc/solutions/Design_by_Contract_and_Assertions), for executable contracts and invariants.
- Martin Fowler, [Replace Nested Conditional with Guard Clauses](https://refactoring.com/catalog/replaceNestedConditionalWithGuardClauses.html), for flat control flow.
- Robert Martin, [Screaming Architecture](https://blog.cleancoder.com/uncle-bob/2011/09/30/Screaming-Architecture.html), for structures that reveal use cases rather than frameworks.
- Martin Fowler, [Transaction Script](https://martinfowler.com/eaaCatalog/transactionScript.html), for direct orchestration when the domain is simple.
- Carson Gross, [The Grug Brained Developer](https://grugbrain.dev/), for delaying abstractions until stable cut points appear.
- Martin Fowler, [Tell, Don't Ask](https://martinfowler.com/bliki/TellDontAsk.html), for balanced behavior ownership.
- Sandi Metz, [The Wrong Abstraction](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction), for preferring removable duplication to rigid reuse.
- Kent C. Dodds, [AHA Programming](https://kentcdodds.com/blog/aha-programming), for waiting until a shared shape is evident.
- Dan Abramov, [Goodbye, Clean Code](https://overreacted.io/goodbye-clean-code/), for preserving changeability when requirements diverge.
- Martin Fowler, [Beck Design Rules](https://martinfowler.com/bliki/BeckDesignRules.html), for minimizing classes and methods after correctness and clarity.
- Joel Spolsky, [Don't Let Architecture Astronauts Scare You](https://www.joelonsoftware.com/2001/04/21/dont-let-architecture-astronauts-scare-you/), for keeping abstractions tied to user problems.
