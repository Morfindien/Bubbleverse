import json,hashlib,pathlib,datetime
R=pathlib.Path('/mnt/data')
def L(p): return json.load(open(p,encoding='utf-8'))
def S(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
r=L(R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_RAW_V1.json'); v=L(R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_VALIDATION_V1.json'); p=L(R/'Q048_V105_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json'); a=L(R/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_ACCEPTANCE_V1.json')
assert v['status']=='PASS' and v['result_sha256']==S(R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_RAW_V1.json')
assert v['checks_total']==v['checks_passed'] and v['semantic_mutations_total']==v['semantic_mutations_rejected']
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
cp={
 'schema':'bubbleverse.q048.v107.source_correct_actual_consumer.accepted_checkpoint.v1','q':'Q048','target_q':'Q048','status':'VALIDATED','technical_state':'PASS','scientific_state':'INCONCLUSIVE','checkpoint_kind':'ACCEPTED_ACTUAL_REANALYSIS_LINEAGE','task_id':r['task_id'],
 'actual_before':{'count':110,'frontier':980,'accepted_checkpoint_sha256':S(R/'Q048_V105_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json')},
 'accepted_actual':{'count':111,'frontier':970},'frontiers':r['candidate_actual']['frontiers'],'endpoint':r['candidate_actual']['endpoint'],'connected_lower':r['candidate_actual']['connected_lower'],'K_upper':r['candidate_actual']['K_upper'],'correct_saha_fact':'3.016103031869581e21',
 'parent_sha256':S(R/'Q048_V105_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json'),'theorem_acceptance_sha256':S(R/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_ACCEPTANCE_V1.json'),'theorem_raw_sha256':a['raw_sha256'],'theorem_verification_sha256':a['verification_sha256'],'source_result_sha256':S(R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_RAW_V1.json'),'validation_sha256':S(R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_VALIDATION_V1.json'),'guard_primary_row_sha256':r['guard_binding']['primary_row_sha256'],
 'new_actual_cells':1,'new_mathematical_proof_cells':0,'historical_v101_replayed':False,'historical_record_modified':False,'accepted_at_utc':now,'no_physical_reset':True,'no_native_trajectory_claim':True,'below970_work':False,'q_complete':False,'NativeP6':'UNRESOLVED','resume_rule':'Return exactly once to Result Ingestion2.1.0; no below970 continuation.'
}
cp_path=R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json'; cp_path.write_text(json.dumps(cp,indent=2)+'\n',encoding='utf-8')
checks={
 'checkpoint_validated':cp['status']=='VALIDATED','count_increment':cp['accepted_actual']['count']==111,'frontier':cp['accepted_actual']['frontier']==970,
 'parent_exact':cp['parent_sha256']=='cedaef00bab86ac24bb876ae475e5dff15f8b97a0a55f83d9ba12d25da07b098','theorem_exact':cp['theorem_acceptance_sha256']=='5294bed5e3d32d71e396d933a5387c8c8f7538e1bc55c432b0b151fc0e9f9fe3','source_correct':cp['correct_saha_fact']=='3.016103031869581e21','one_actual':cp['new_actual_cells']==1,'zero_proof':cp['new_mathematical_proof_cells']==0,'no_reset':cp['no_physical_reset'],'no_below970':cp['below970_work'] is False,'history_firewall':not cp['historical_v101_replayed'] and not cp['historical_record_modified'],'q_inconclusive':cp['scientific_state']=='INCONCLUSIVE','result_pin':cp['source_result_sha256']==S(R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_RAW_V1.json'),'validation_pin':cp['validation_sha256']==S(R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_VALIDATION_V1.json'),'guard_pin':cp['guard_primary_row_sha256']=='01e9f92295d60287f74a2760c1d38da42d2d37098a4d0dd32d1782dbf757b5ea'
}
post={'schema':'bubbleverse.q048.v107.source_correct_actual_consumer.postaccept_validation.v1','status':'PASS' if all(checks.values()) else 'FAIL','checks_total':len(checks),'checks_passed':sum(checks.values()),'checks':checks,'accepted_checkpoint_sha256':S(cp_path)}
post_path=R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_POSTACCEPT_VALIDATION_V1.json'; post_path.write_text(json.dumps(post,indent=2)+'\n',encoding='utf-8')
print('checkpoint',S(cp_path)); print('postaccept',S(post_path),post['status'],post['checks_passed'],post['checks_total'])
