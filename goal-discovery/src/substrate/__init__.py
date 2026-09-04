"""Shared specimen substrate.

One loop, one state, one measurement, one result shape. What differs between
specimens is expressed as policies selected by five explicit dials, each of
which was derived from a reproduced experimental failure rather than guessed:

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

from .contract import Dials, Specimen, RunOutcome, run

__all__ = ["Dials", "Specimen", "RunOutcome", "run"]
