"""Day23 실습 06 · Exact·HNSW·EXPLAIN (심화, mentee).

실행: python main.py --mode fixture
실제 E5/DB: python main.py --mode live  (필요한 선행 설치 후)
수강생 TODO: 6개 / 상세 요구사항은 각 함수의 주석 및 README.md.
fixture는 모의 시연이지 모델·PostgreSQL 실측 결과가 아닙니다.
"""
# 명령행 인자 처리 기능 사용
# - ArgumentParser : CLI 옵션 정의 및 파싱
import argparse
# 파이썬 실행 환경 제어 기능 사용
# - sys.path : 모듈 검색 경로 추가
import sys
# 파일 경로 처리 기능 사용
# - Path : 운영체제 독립적인 경로 처리
from pathlib import Path
# 공용 모듈 경로 추가
# - common 디렉터리 라이브러리 사용 가능
sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'common'))
# E5 모델 정보 사용
# - E5_MODEL_ID : 임베딩 모델 식별자
from day23kit.data import E5_MODEL_ID
# 임베딩 기능 사용
# - get_encoder : Encoder 생성
# - encode_question : Query 임베딩 생성
from day23kit.embedding import get_encoder, encode_question
# PostgreSQL 및 pgvector 기능 사용
# - connect_db : DB 연결
# - exact_topk : Exact Search 수행
# - check_data_ready : 검색 데이터 준비 상태 확인
from day23kit.db import connect_db, exact_topk, check_data_ready
# 결과 저장 기능 사용
# - save_result : JSON 결과 파일 저장
from day23kit.io import save_result

# HNSW 및 EXPLAIN SQL 생성 기능 사용
# - create_index_sql : HNSW 인덱스 생성 SQL
# - explain_sql : 실행 계획 조회 SQL
from app.index_sql import create_index_sql, explain_sql
# 실행 계획 분석 기능 사용
# - read_scan_type : Scan 방식 판별
# - check_operator_compatibility : 연산자 호환성 확인
# - compare_topk : 검색 결과 비교
# - filtered_ann_warning : ANN 검색 주의사항 생성
from app.plan_review import read_scan_type, check_operator_compatibility, compare_topk, filtered_ann_warning

"""HNSW 인덱스 생성과 EXPLAIN 실행 계획 분석을 수행하는 실습 모듈"""

# 실습 실행 함수
# - 인덱스 SQL 생성
# - 실행 계획 분석
# - Exact Search와 비교
def run(mode,level,args):
    # HNSW 인덱스 생성 SQL 조회
    sql_index=create_index_sql()
    # 실행 계획 조회 SQL 생성
    sql_plan=explain_sql()
    # 기본 결과 생성
    # - 생성 SQL 저장
    # - 실행 환경 기록
    result=dict(exercise=6,level=level,source_mode='simulated' if mode=='fixture' else 'pgvector_live',
                index_sql=sql_index,explain_sql=sql_plan)
    # Fixture 환경 실행
    # - 실제 PostgreSQL 미사용
    # - 예제 실행 계획 사용
    if mode=='fixture':
        # 예제 실행 계획 생성
        # - Seq Scan 예시
        # - Cosine Distance 정렬 예시
        sample=['Seq Scan on day23_search_docs (cost=...)','Sort Key: (embedding <=> ...)']
        # Scan 방식 판별
        result['scan_type']=read_scan_type(sample)
        # 모의 환경 여부 기록
        result['plan_is_simulated']=True
    else:
        # 실제 Encoder 생성
        encoder=get_encoder('live')
        # 검색 질문 임베딩 생성
        qvec=encode_question(encoder,'서버는 어디에서 실행하나요?')
        # PostgreSQL 연결
        with connect_db(Path(__file__).with_name('.env')) as conn:
            # 검색 데이터 준비 여부 확인
            # - 테이블 존재 여부
            # - 검색 데이터 존재 여부
            check_data_ready(conn)
            # HNSW 인덱스 생성
            # - create-index 옵션 활성화 시 수행
            if getattr(args,'create_index',False):
                # HNSW 인덱스 생성
                conn.execute(sql_index)
                # 통계 정보 갱신
                # - Planner가 최신 정보 사용
                conn.execute('ANALYZE day23_search_docs')
            # EXPLAIN 실행 계획 조회
            plan_lines=[str(r[0]) for r in conn.execute(sql_plan,(E5_MODEL_ID,qvec)).fetchall()]
            # Scan 방식 판별
            result['scan_type']=read_scan_type(plan_lines)
            # 실행 계획 저장
            result['explain_lines']=plan_lines
            if level>=3:
                # Exact 기준선과 인덱스 유도 계획을 같은 질문/데이터/필터에서 실제 비교합니다.
                # SET LOCAL은 수업용 트랜잭션 동안만 적용되며 결과의 우열을 단정하지 않습니다.
                # Exact Search 결과 생성
                # - Index Scan 사용 방지
                # - 정확한 기준선 확보
                conn.execute('SET LOCAL enable_indexscan=off')
                conn.execute('SET LOCAL enable_bitmapscan=off')
                exact_ids=[h['id'] for h in exact_topk(conn,qvec,k=3,category='development')]
                # Index Scan 재허용
                conn.execute('SET LOCAL enable_indexscan=on')
                conn.execute('SET LOCAL enable_bitmapscan=on')
                # Seq Scan 비활성화
                # - 인덱스 사용 유도
                conn.execute('SET LOCAL enable_seqscan=off')
                # 인덱스 사용 시 실행 계획 조회
                indexed_plan=[str(r[0]) for r in conn.execute(sql_plan,(E5_MODEL_ID,qvec)).fetchall()]
                # 인덱스 사용 환경 검색
                indexed_ids=[h['id'] for h in exact_topk(conn,qvec,k=3,category='development')]
                # Seq Scan 복구
                conn.execute('SET LOCAL enable_seqscan=on')
                # HNSW 인덱스 사용 여부 확인
                confirmed_index=(read_scan_type(indexed_plan)=='index')
                # Exact Search와 인덱스 결과 비교
                result['comparison']={
                    'category':'development','k':3,'exact_ids':exact_ids,
                    'forced_plan_ids':indexed_ids,
                    'forced_plan_scan':read_scan_type(indexed_plan),
                    'hnsw_index_observed':confirmed_index,
                    # 결과 중복도 계산
                    # - Exact Search 결과와 ANN 결과 비교
                    'exact_vs_ann_overlap':compare_topk(exact_ids,indexed_ids) if confirmed_index else None,
                    'note':'Index Scan이 관측됐을 때만 ANN 비교라 기록합니다. 9건에서 속도 향상 주장 금지.',
                }
    # 연산자 및 결과 비교 수행
    if level>=2:
        # 연산자 호환성 점검
        # - vector_cosine_ops 사용 여부 확인
        result['operator_compatible']=check_operator_compatibility(sql_plan,'vector_cosine_ops')
        # 결과 중복도 예시 생성
        result['example_overlap']=compare_topk([102,106,107],[102,107,101])
    # ANN 검색 주의사항 생성
    if level>=3:
        # Approximate Search 결과 누락 예시 생성
        result['ann_filtered_example']=filtered_ann_warning(k=3,returned=1,exact_count=4)
    # 실습 결과 반환
    # - 실행 계획 결과 포함
    # - 비교 분석 결과 포함
    return result

# 프로그램 진입 함수
# - 실행 옵션 처리
# - 실습 수행
# - 결과 저장 및 출력
def main():
    # 명령행 인자 파서 생성
    # - 프로그램 설명 등록
    parser=argparse.ArgumentParser(description='Day23 실습 06 · Exact·HNSW·EXPLAIN')
    # 실행 모드 옵션 등록
    # - fixture : 모의 환경
    # - live : 실제 PostgreSQL 환경
    parser.add_argument('--mode',choices=['fixture','live'],default='fixture',
        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')

    # HNSW 인덱스 생성 옵션 등록
    # - live 환경에서만 사용
    parser.add_argument('--create-index',action='store_true',help='live에서만 HNSW 인덱스를 실제 생성')
    # 사용자 입력 파싱
    args=parser.parse_args()
    # 실습 실행
    # - Level 3 기준 수행
    result=run(args.mode,3,args)
    # 결과 파일 저장
    # - exercise_06.json 생성
    path=save_result(Path(__file__).resolve().parent,'exercise_06.json',result)
    import json
    # 결과 출력
    # - JSON 형식 출력
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
    # 저장 경로 출력
    print('결과 저장:',path)

# 프로그램 시작점
# - 직접 실행 시 main() 호출
if __name__=='__main__':
    main()

"""
pgvector의 HNSW 인덱스를 활용한 ANN 검색 구조를 학습하기 위해 구현하였다.
EXPLAIN을 사용하여 PostgreSQL이 실제로 어떤 실행 계획을 선택하는지 확인하고, Seq Scan과 Index Scan의 차이를 분석할 수 있도록 구성하였다.
또한 Exact Search 결과와 인덱스 기반 검색 결과를 비교하여 검색 정확도와 결과 중복도를 확인할 수 있도록 구현하였다.
검색 연산자와 인덱스 설정의 호환성을 검증하고, ANN 검색에서 발생할 수 있는 결과 누락 가능성을 학습할 수 있도록 구성하였다.
"""