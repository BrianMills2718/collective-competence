# NetLogo bubble-sort visual calibration

This is a small, off-the-shelf visualization spike for the validated Python
bubble-sort experiment. It is deliberately isolated from Experiment 001 and is
not a migration of the scientific reference implementation.

## Open it

Install [NetLogo 7](https://www.netlogo.org/), then open
`netlogo-bubble.nlogox`. NetLogo automatically loads the adjacent
`netlogo-bubble.nls` source file.

The interface provides:

- Setup, Step, and Go controls
- reproducible model and intervention seeds
- index or shuffled explicit activation
- a block-swap perturbation
- moveable and immovable cell freezing
- a live boundary-length plot and outcome monitors
- persistent cell IDs, values, position, and freeze status
- one-click flat CSV trajectory export

Cell color encodes value; its label shows the value and persistent identity.
Yellow backing marks a moveable freeze and red marks an immovable freeze.

## Batch calibration

The model contains four BehaviorSpace experiments:

- `calibration-baseline`
- `calibration-block-swap`
- `calibration-freeze-moveable`
- `calibration-freeze-immovable`

For example:

```bash
netlogo-headless.sh \
  --model src/spikes/netlogo_bubble/netlogo-bubble.nlogox \
  --experiment calibration-block-swap \
  --table block-swap.csv
```

BehaviorSpace records each tick as CSV-compatible tabular output. The Export
button writes the in-model trajectory log to
`netlogo-bubble-trajectory.csv` in NetLogo's current directory. Each flat row
contains the tick, event, seeds/order, representations, counters, and 12 fields
each for value, identity, and freeze mode.

## Semantics and limits

Each active cell chooses one side with a fair coin, then swaps left if smaller
or right if larger. Every persistent identity is offered one activation per
tick. Moveable frozen cells never initiate an action but can be carried by a
neighbor; immovable frozen cells additionally block swaps.

The model uses NetLogo's random-number generator, so it tests mechanism and
outcome parity rather than byte-identical paths with Python. The Python model
remains authoritative for completed experiments.

Validated headlessly with NetLogo 7.0.4. Across the embedded calibration:

- all 18 baseline runs sorted and became quiescent;
- all 6 post-sort block swaps increased boundary length from 0 to 2, then
  recovered fully;
- matched moveable freezes ended at boundary length 1;
- matched immovable freezes ended at boundary length 2 or 3.

These are calibration observations, not claims of regulation or agency.
