# Experiment 005 — deterministic adaptation across episodes

**Pre-registered after the 004 batch passed and before any 005 batch is
generated.**

## Question

Does experience in earlier episodes change a controller parameter so later
episodes preserve the same target better, and does that advantage disappear
when the policy is frozen or episode memory is reset?

This calibrates deterministic adaptation. It is not open-ended learning,
planning, or autonomous goal discovery.

## System

The scalar plant retains target and ambient `20`, relaxation `.05`, and bounded
proportional feedback. Each 50-tick episode resets temperature to 20 while
preserving the controller gain only in the adaptive arm. A sustained signed load
is present throughout each episode. Actuator effectiveness multiplies the
command and is never supplied to the controller.

All arms start at gain `.05`. After an episode the adaptive arm updates:

```text
gain' = min(.80, gain + .08 * mean_absolute_episode_error)
```

The frozen arm never updates. The reset-between-episodes arm computes the same
update but resets gain to `.05` before the next episode. There are five episodes
and 250 ticks per run. Late episode error is the mean absolute target error over
episode steps 40–49.

## Held-out matrix

Actuator effectiveness is `.42, .63, .87, 1.08`; sustained load is `-.34, +.28`.
All eight environments run in adaptive, frozen, and reset-between arms: 24
deterministic runs. No case may be removed.

## Frozen decisions

- **A1 — within-run improvement:** adaptive episode-5 late error is at most
  50% of its episode-1 error in every environment.
- **A2 — frozen-policy contrast:** adaptive episode-5 error is at most 50% of
  matched frozen episode-5 error in every environment.
- **A3 — memory null:** reset-between and frozen late errors agree within
  `1e-9` in every episode and environment.
- **A4 — policy change:** the adaptive gain strictly increases after every
  episode unless it has reached `.80`; its final gain exceeds `.05`. Frozen and
  reset-between episode-start gains remain `.05`.
- **A5 — common baseline:** adaptive, frozen, and reset-between episode-1 late
  errors agree within `1e-9` in every environment.
- **A6 — reproducibility:** two fresh 005 batches have byte-identical scientific
  table rows after volatile NetLogo headers are removed.

005 passes only if A1–A6 pass.

## Interpretation limit

Passing shows history-dependent parameter adaptation that generalizes across
the declared plant family. The update rule and target are supplied; it does not
show the system discovered its own learning rule or goal.
