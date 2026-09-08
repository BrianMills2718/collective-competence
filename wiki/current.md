---
doc-role: current-working-status
authority: working-priority-summary
lifecycle: active
sources:
  - questions.md
  - findings.md
  - ../experiments/11-learned-composition-memory/README.md
---
# Current work

[Wiki home](index.md) · [Questions](questions.md) · [Findings](findings.md) · [Laboratory](laboratory.md)

This is the only hot page that owns **current priority and next action**.

## Where we are

The regeneration sequence now separates positional cues, amount/size, wound identity, intrinsic composition, generative plasticity, reporter integrity, and desired-state memory.

Experiment 11 removes hard-coded A/B target counts from repair. An extracellular trace learns healthy endogenous A/B signal levels from pre-damage history and the same controller then restores healthy compositions `A^6 B^18`, `A^8 B^16`, and `A^10 B^14`. With persistent memory and fate plasticity it repairs all **12/12** declared partial/extinction challenges; decaying memory produces a finite repair horizon. Without plasticity, complete lineage extinction remains unrepaired in **0/6** declared cases.

The remaining reporter problem has now been analyzed rather than simulated again. With observed wound state `W`, current self-produced signal `S`, and learned healthy setpoint `M`, a diagnostic birth can distinguish complete lineage extinction with a healthy reporter from reporter failure: a healthy reporter begins producing signal after the new cell appears; a broken reporter does not.

But once reporter failure is established, **current compartment amount is not identifiable from that channel**. Every reporter-failed wounded abundance produces `S=0`; further births also leave `S=0`. Different initial amounts therefore generate the same observation history while requiring different remaining birth counts. A controller using only `{W, S, M, its own birth history}` cannot guarantee exact repair across those states.

So the missing information is no longer “is the reporter broken?” It is an independent estimate of **current amount or lost amount**.

## Next action

**Compare candidate sources of amount information by the failures they can and cannot resolve—on paper first, then experimentally only where needed.**

Two useful baselines are already clear:

1. **Historical wound-loss counter.** If every lost A cell is perfectly recorded at damage time, then one-shot repair is trivial: add exactly that many A cells. This is sufficient for the declared end-amputation challenge but simply moves the measurement into the wound sensor.
2. **Independent current-abundance measurement.** A second observable of current A amount can close the loop even after the primary chemical reporter fails, but it only counts as redundancy if its source and failure mode are genuinely independent.

The next constructed challenge should be one where these two approaches diverge. Good candidates include unobserved cell loss after the initial wound, pre-existing composition error, internal deletion that does not pass through the counted boundary event, or ongoing loss during repair. An exact wound counter should fail there while a trustworthy current-state measurement can still succeed.

Before implementation, answer:

1. Which finite set of hidden A abundances must the new channel distinguish after primary-reporter failure?
2. What is the minimum information capacity over that declared challenge set? For `K` exact-deficit classes requiring different actions, a noiseless discrete side channel needs at least `ceil(log2 K)` distinguishable states; “one analog scalar” is not a minimality claim without precision/range.
3. What physical/source mechanism could measure current A abundance without sharing A secretion's failure mode?
4. What intervention will fail the proposed secondary channel while leaving the primary channel intact, and vice versa?
5. What joint failure remains impossible even with both channels?

Do **not** add a second chemical reporter merely because it is easy to code. The next positive mechanism should buy a demonstrably new observational distinction.

## Working rules

- Optimize for **different phenomena learned per unit effort**.
- Prefer minimal, inspectable biological analogues over realism for its own sake.
- Construction and mechanism first; discovery analysis second.
- Keep desired-state memory separate from current-state measurement.
- Keep pattern, size, location, composition, reporter integrity, fault diagnosis, memory, plasticity, and exact microstate distinct.
- Treat translations or other symmetries as equivalent unless the experiment explicitly supplies a reason not to.
- State which information is external, tissue-generated, inherited, local, shared, historical, persistent, or supplied by oracle.
- Do not call duplicated channels redundant unless their failure modes are independently challenged.
- Do not simulate a claim whose decisive content is already derivable on paper; use analytic identifiability arguments first.
- Add apparatus only when a concrete experiment requires it.
- Negative results, corrections, and information/feasibility boundaries count as progress.

## Secondary follow-ups

The learned-memory retention sweep can later be extended with noise or delayed repair if a concrete memory-lifetime question requires it. The current front is stricter: determine what *new* current-state information is needed after the primary reporter is known to be broken, and design the challenge before the mechanism.
