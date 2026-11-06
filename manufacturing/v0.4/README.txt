3-Phase Synth FeatherWing v0.4 manufacturing preparation

STATUS: Fabrication files prepared; ASSEMBLY/PURCHASING ON HOLD.
This is not approval to manufacture or order components.
Nominal outline: 51.0 x 58.5 mm; 2 copper layers; 1.6 mm board.
Confirm FR-4, copper weight, finish, quantity and panelization before an order.

Bare-board archive: Tph_Synth_Featherwing-v0.4-fabrication.zip
Contains fresh Gerbers and separate PTH/NPTH drills only (plus job file if emitted).
Drill maps and checks remain outside the upload archive.
Do not use the historical Tph_Synth_Featherwing\gerbers or bom folders.

assembly\assembly-bom-REVIEW-ONLY.csv is NOT an approved purchasing BOM.
C12's legacy MPN is the wrong package; C1-C3 need lifecycle review; R10 needs mechanical review.
All remaining legacy MPNs require datasheet and live stock/packaging verification.
MS1 is the external host; no adapter PCB is fitted to this PCB at MS1.
Mating 12-pin/16-pin headers are not selected in the schematic BOM.
JP1/JP2, test pads and the OSHW logo are PCB features, not purchased components.

positions-smt.csv covers SMT only; THT parts are listed in release-status.json.
Gerbers/drills/positions use absolute CAD origin, millimetres; bottom X is not negated.
Back assembly SVG is mirrored for viewing only. Confirm machine rotations and polarity.
Unvalidated hardware: power rails, host I2C/firmware, DAC and analog/current outputs.
See release-status.json for blockers and manifest.json for source/output SHA-256 hashes.
