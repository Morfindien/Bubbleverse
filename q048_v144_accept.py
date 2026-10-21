import datetime
from q048_v144_contract import *
raw=load(ROOT/'Q048_V144_RAW_V1.json'); val=load(ROOT/'Q048_V144_VALIDATION_V1.json')
if val.get('status')!='PASS': raise SystemExit('validator not PASS')
out={'schema':'bubbleverse.q048.v144.provisional_acceptance.v1','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PROVISIONAL_NOT_CURRENT','raw_sha256':sha(ROOT/'Q048_V144_RAW_V1.json'),'validation_sha256':sha(ROOT/'Q048_V144_VALIDATION_V1.json'),'task_id':raw['task_id'],'task_fingerprint':raw['task_fingerprint'],'candidate_actual':raw['candidate_actual'],'candidate_endpoint':raw['candidate_endpoint'],'theorem_consumptions_candidate':1,'v142_proof_status_before':'ACCEPTED_UNCONSUMED','current_remains':{'count':124,'frontier':840}}
dump(ROOT/'Q048_V144_PROVISIONAL_ACCEPTANCE_V1.json',out)
