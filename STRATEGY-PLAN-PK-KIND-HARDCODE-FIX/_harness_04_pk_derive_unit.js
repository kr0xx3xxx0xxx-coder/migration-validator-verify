/* _mvDerivePkProfile 분기 단위 검증 — 특히 '확인 불가 → 보수적 HOLD' 폴백. */
const fs = require('fs');
const path = process.argv[2];
const src = fs.readFileSync(path, 'utf8');
global.window = undefined;                     /* 브라우저 아님 — window 가드 확인 */
eval(src);                                     /* 함수 정의 로드 */

const CASES = [
  ['근거 없음(빈 응답)',                 {},                                                          'NONE',           false],
  ['목적지 물리 PK: 숫자 단일',           {target_pk_evidence:{available:true,pk_columns:['ID'],key_column_count:1,types:{ID:'NUMERIC'}}}, 'SINGLE_NUMERIC', true],
  ['목적지 물리 PK: 문자 단일',           {target_pk_evidence:{available:true,pk_columns:['CODE'],key_column_count:1,types:{CODE:'VARCHAR'}}}, 'SINGLE_TEXT',  true],
  ['목적지 물리 PK: 날짜 단일',           {target_pk_evidence:{available:true,pk_columns:['D'],key_column_count:1,types:{D:'DATE'}}}, 'SINGLE_DATE',   true],
  ['목적지 물리 PK: 복합(2컬럼)',         {target_pk_evidence:{available:true,pk_columns:['A','B'],key_column_count:2,types:{A:'VARCHAR',B:'NUMERIC'}}}, 'COMPOSITE',  true],
  ['목적지 물리 PK: 복합(kcc만 2)',       {target_pk_evidence:{available:true,pk_columns:['A'],key_column_count:2,types:{A:'VARCHAR'}}}, 'COMPOSITE',    true],
  ['목적지 물리 PK: PK 없음 확정',        {target_pk_evidence:{available:true,pk_columns:[],key_column_count:0,types:{}}}, 'NONE',                     false],
  ['목적지 물리 PK: 타입 미상 → 보수적',  {target_pk_evidence:{available:true,pk_columns:['X'],key_column_count:1,types:{}}}, 'NONE',                 false],
  ['조회 실패(available=false) → 보수적', {target_pk_evidence:{available:false,reason:'KEY_METADATA_UNAVAILABLE'}}, 'NONE',                          false],
  ['chunk_key 증거 TRUSTED(폴백2)',       {target_pk_evidence:{available:false},chunk_key_evidence_snapshot:{verdict:'TRUSTED_PHYSICAL_PK'}}, 'SINGLE_NUMERIC', true],
  ['DDL 메타 복합(폴백3)',                {analyze_result:{has_meta:true,validated:[{tgt_col:'A',is_pk:true,tgt_type:'VARCHAR2'},{tgt_col:'B',is_pk:true,tgt_type:'NUMBER'}]}}, 'COMPOSITE', true],
  ['DDL 메타 문자 단일(폴백3)',           {analyze_result:{has_meta:true,validated:[{tgt_col:'C',is_pk:true,tgt_type:'VARCHAR2(20)'}]}}, 'SINGLE_TEXT',      true],
  ['메타 자체 없음 → 보수적',             {analyze_result:{has_meta:false}},                           'NONE',           false],
];

let fail = 0;
for (const [name, ad, expKind, expHas] of CASES) {
  const r = _mvDerivePkProfile(ad);
  const ok = (r.pk_kind === expKind && r.has_pk === expHas);
  if (!ok) fail++;
  console.log((ok ? '  PASS  ' : '  FAIL  ') + name.padEnd(34) +
              ' → kind=' + r.pk_kind + ' has_pk=' + r.has_pk + ' evidence=' + r.pk_evidence +
              (ok ? '' : '   (기대 ' + expKind + '/' + expHas + ')'));
}
console.log(fail === 0 ? ('\n전체 ' + CASES.length + '건 통과') : ('\n실패 ' + fail + '건'));
process.exit(fail === 0 ? 0 : 1);
