# Q048 V144 implementation plan

Build a new source-independent contract consumer for840→830. Historical V140 source files remain missing and are not reconstructed. Inputs are V140 accepted checkpoint + preserved validated contract artifacts, V142 accepted proof, row61 guard and prefix capture. Freeze first; run one consumer→validator→provisional→postaccept→publication chain; stop on first failure.
