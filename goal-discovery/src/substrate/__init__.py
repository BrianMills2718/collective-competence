"""Shared specimen substrate.

One loop, one state, one measurement, one result shape. What differs between
specimens is expressed as policies, alongside five explicit dials, each derived
from a reproduced experimental failure rather than guessed.

Two of the five select behaviour and three record it. `absorbing_failure` and
`symmetry_channel` are read by the shared loop; `outcome_independence`,
`divisible` and `heterogeneity` are read by no code, because the property each
names is implemented inside a specimen's own policies and the dial only declares
it. That is asserted, not assumed, by `tests/test_substrate.py`'s
`test_only_two_dials_are_load_bearing`, which fails if a dial is ever wired in.
Read the three as documentation of what a specimen is, not as a mechanism that
makes it so:

  outcome_independence  Q1-006/Q1-007 -- congestion coupling put a floor under
                        matched-random and blocked completion-condition clause 2
  divisible             C1-002 -- a level signal coordinates a divisible stock
                        and cannot allocate an indivisible slot
  heterogeneity         C2-001 -- achievable coordination is bounded by the
                        number of distinct local values the environment supplies
  symmetry_channel      C1-002 + C2-001 -- a shared scalar is common-mode by
                        construction and can gate but never stagger
  absorbing_failure     Q1-003 + Q1-004 -- collapse produces uniform death,
                        which inverts share-of-variance statistics

Scope: hosts the live specimens only. sorting, bowl and mesa_bubble are
deliberately not ported -- their lanes are stopped and porting would risk
archived findings for no live benefit. See the bounded design's non-goals.
"""

from .contract import Dials, RunOutcome, Specimen, run

__all__ = ["Dials", "RunOutcome", "Specimen", "run"]
