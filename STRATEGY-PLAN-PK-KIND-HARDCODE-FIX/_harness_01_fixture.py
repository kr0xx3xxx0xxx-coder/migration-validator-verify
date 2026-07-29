# -*- coding: utf-8 -*-
"""STRATEGY-PLAN-PK-KIND-HARDCODE-FIX 실측용 Oracle 픽스처 생성.

PK 구조 3종(숫자 단일 / 문자 단일 / 복합)을 asis(원본)·tobe(목적지)에 동일 구조로 만든다.
검증 목적은 '3단계 실행계획 카드의 PK 구조 표시'이므로 건수는 소량(300행)이면 충분하다.
"""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
import oracledb  # noqa: E402


def _preset(f, nm):
    return [x for x in json.load(open(f, encoding="utf-8")) if x["name"] == nm][0]


def _conn(p):
    return oracledb.connect(user=p["user"], password=p["password"],
                            dsn="%s:%s/%s" % (p["host"], p["port"], p["dbname"]))


DDL = {
    # 숫자 단일 PK
    "T_SPKFIX_NUM": """
        CREATE TABLE {t} (
            ID       NUMBER(10)    NOT NULL,
            DEPT_CD  VARCHAR2(4)   NOT NULL,
            AMT      NUMBER(12,2),
            CONSTRAINT PK_{t} PRIMARY KEY (ID)
        )""",
    # 문자 단일 PK
    "T_SPKFIX_TXT": """
        CREATE TABLE {t} (
            CODE     VARCHAR2(20)  NOT NULL,
            DEPT_CD  VARCHAR2(4)   NOT NULL,
            AMT      NUMBER(12,2),
            CONSTRAINT PK_{t} PRIMARY KEY (CODE)
        )""",
    # 복합 PK
    "T_SPKFIX_CMP": """
        CREATE TABLE {t} (
            CO_CD    VARCHAR2(4)   NOT NULL,
            SEQ      NUMBER(8)     NOT NULL,
            DEPT_CD  VARCHAR2(4)   NOT NULL,
            AMT      NUMBER(12,2),
            CONSTRAINT PK_{t} PRIMARY KEY (CO_CD, SEQ)
        )""",
}
INS = {
    "T_SPKFIX_NUM": "INSERT INTO {t} SELECT LEVEL, 'D'||LPAD(MOD(LEVEL,5),3,'0'), LEVEL*10 "
                    "FROM DUAL CONNECT BY LEVEL <= 300",
    "T_SPKFIX_TXT": "INSERT INTO {t} SELECT 'C'||LPAD(LEVEL,8,'0'), 'D'||LPAD(MOD(LEVEL,5),3,'0'), LEVEL*10 "
                    "FROM DUAL CONNECT BY LEVEL <= 300",
    "T_SPKFIX_CMP": "INSERT INTO {t} SELECT 'CO'||LPAD(MOD(LEVEL,3),2,'0'), LEVEL, "
                    "'D'||LPAD(MOD(LEVEL,5),3,'0'), LEVEL*10 FROM DUAL CONNECT BY LEVEL <= 300",
}


def build(conn, suffix):
    cur = conn.cursor()
    for base, ddl in DDL.items():
        t = base + suffix
        try:
            cur.execute("DROP TABLE %s PURGE" % t)
        except Exception:  # noqa: BLE001
            pass
        cur.execute(ddl.format(t=t))
        cur.execute(INS[base].format(t=t))
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM %s" % t)
        print("  %-22s rows=%s" % (t, cur.fetchone()[0]))
    # PK 구조 확인
    cur.execute(
        "SELECT c.table_name, c.constraint_type, cc.column_name, cc.position "
        "FROM user_constraints c JOIN user_cons_columns cc ON c.constraint_name=cc.constraint_name "
        "WHERE c.constraint_type='P' AND c.table_name LIKE 'T_SPKFIX%' ORDER BY 1,4")
    for r in cur.fetchall():
        print("  PK", r)


if __name__ == "__main__":
    src = _preset("db_presets_src.json", "Oracle_asis")
    tgt = _preset("db_presets_tgt.json", "Oracle_tobe")
    print("[asis 1523] 원본 테이블 생성")
    c = _conn(src); build(c, "_SRC"); c.close()
    print("[tobe 1524] 목적지 테이블 생성")
    c = _conn(tgt); build(c, "_TGT"); c.close()
    print("완료")
