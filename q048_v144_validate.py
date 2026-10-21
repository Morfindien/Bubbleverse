import datetime
from q048_v144_contract import *
raw=load(ROOT/'Q048_V144_RAW_V1.json')
checks=validate_raw(raw); controls=run_controls(raw)
status='PASS' if all(checks.values()) and all(c['rejected'] for c in controls) and len(checks)>=35 and len(controls)>=40 else 'FAIL'
out={'schema':'bubbleverse.q048.v144.validation.v1','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':status,'checks':checks,'checks_total':len(checks),'checks_passed':sum(checks.values()),'controls':controls,'semantic_controls_total':len(controls),'semantic_controls_rejected':sum(c['rejected'] for c in controls),'raw_sha256':sha(ROOT/'Q048_V144_RAW_V1.json'),'control_roster_sha256':sha(ROOT/'Q048_V144_CONTROL_ROSTER_V1.json'),'independence':'Independent script reloads parent/proof/guard inputs and re-derives row61 endpoint; no expected endpoint imported as derivation.'}
dump(ROOT/'Q048_V144_VALIDATION_V1.json',out)
if status!='PASS': raise SystemExit(2)
