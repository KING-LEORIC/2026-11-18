"""Day23 실습 05 · 원문·벡터 저장과 Top-k (심화, mentee).

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
# 원문 데이터 및 검색 테이블 정보 사용
# - load_knowledge : 지식 데이터 조회
# - E5_MODEL_ID : E5 임베딩 모델 식별자
# - TABLE_NAME : 검색 테이블명
from day23kit.data import load_knowledge, E5_MODEL_ID, TABLE_NAME
# 모의 검색 기능 사용
# - fixture_search : Vector Search 시뮬레이션
from day23kit.fixtures import fixture_search
# 임베딩 기능 사용
# - get_encoder : Encoder 생성
# - encode_passages : 문서 임베딩 생성
# - encode_question : 질문 임베딩 생성
# - validate_vectors : 벡터 유효성 검증
from day23kit.embedding import get_encoder, encode_passages, encode_question, validate_vectors
# PostgreSQL 및 pgvector 기능 사용
# - connect_db : DB 연결
# - ensure_table : 검색 테이블 생성
# - upsert_rows : 원문 및 벡터 저장
# - exact_topk : Top-K 검색 수행
from day23kit.db import connect_db, ensure_table, upsert_rows, exact_topk
# 결과 저장 기능 사용
# - save_result : JSON 결과 파일 저장
from day23kit.io import save_result

# 검색 저장소 계약 기능 사용
# - schema_sql : 테이블 생성 SQL 반환
# - prepare_document_rows : 검색용 문서 데이터 생성
# - topk_sql : Top-K 검색 SQL 반환
# - filtered_sql : 카테고리 필터 검색 SQL 반환
from app.repository_contract import schema_sql, prepare_document_rows, topk_sql, filtered_sql
# 검색 검증 기능 사용
# - check_search_options : 검색 옵션 검증
# - check_id_vector_integrity : 원문-벡터 무결성 검증
from app.validation import check_search_options, check_id_vector_integrity

"""원문 데이터와 임베딩 벡터를 저장하고 Cosine Distance 기반 Top-K 검색을 수행하는 실습 모듈"""

# 실습 실행 함수
# - 원문 데이터 준비
# - 임베딩 생성
# - 검색 수행
# - 결과 생성
def run(mode,level,args):
    # 원문 데이터 조회
    rows=load_knowledge()
    # 검색 테이블 생성 SQL 조회
    sql_schema=schema_sql()
    # 검색용 문서 데이터 생성
    # - Passage 포함
    # - 원문 데이터 유지
    inputs=prepare_document_rows(rows)
    # Top-K 검색 SQL 조회
    sql_query=topk_sql()
    # 검색 질문 생성
    # - 사용자 Query 역할 수행
    question='서버는 어디에서 실행하나요?'
    # 기본 결과 생성
    # - 실습 정보 저장
    # - 검색 환경 기록
    result=dict(exercise=5,level=level,source_mode='simulated' if mode=='fixture' else 'pgvector_exact',
                table=TABLE_NAME,model=E5_MODEL_ID,prepared_count=len(inputs),
                first_passage=inputs[0]['passage_input'],
                sql_schema=sql_schema,sql_topk=sql_query)
    # 검색 Category 결정
    # - Level1 : 전체 검색
    # - Level2 이상 : development 검색
    category=None if level==1 else 'development'
    # 검색 옵션 검증 수행
    # - 필터 SQL 생성
    # - 파라미터 유효성 검사
    if level>=2:
        result['sql_filtered']=filtered_sql()
        result['options']=check_search_options(3,category)
    # Fixture 검색 수행
    # - 실제 DB 없이 검색 결과 시뮬레이션
    if mode=='fixture':
        # 모의 Top-K 검색
        hits=fixture_search(question,3,category=category)
    else:
        # 실사용 Encoder 생성
        encoder=get_encoder('live')
        # 문서 임베딩 생성
        vectors=encode_passages(encoder,rows)
        # 원문-벡터 무결성 검증
        # - Level3에서 추가 검사
        if level>=3:check_id_vector_integrity(rows,vectors)
        # 벡터 기본 검증
        else:validate_vectors(vectors,len(rows))
        # Query 임베딩 생성
        qvec=encode_question(encoder,question)
        # PostgreSQL 연결
        with connect_db(Path(__file__).with_name('.env')) as conn:
            # 검색 테이블 준비
            # - 없으면 생성
            ensure_table(conn)
            # 원문 및 벡터 저장
            # - 동일 ID 데이터 갱신
            upsert_rows(conn,rows,vectors,E5_MODEL_ID)
            # Top-K 검색 수행
            # - Cosine Distance 기준
            # - Category 필터 적용
            hits=exact_topk(conn,qvec,k=3,category=category)
    # 검색 결과 생성
    # - ID
    # - 내용
    # - Distance
    result['hits']=[{'id':h['id'],'content':h['content'],'distance':round(h['distance'],6)} for h in hits]
    # 무결성 추가 검증
    # - Fixture 환경 포함
    if level>=3:
        # 이전 단계의 벡터를 재사용합니다. live에서는 같은 모델을 다시 다운로드/로드하지 않습니다.
        # 이전 단계의 벡터를 재사용합니다.
        # live에서는 같은 모델을 다시 다운로드/로드하지 않습니다.
        if mode=='fixture':
            # Fixture Encoder 생성
            encoder=get_encoder('fixture')
            # Fixture 임베딩 생성
            vectors=encode_passages(encoder,rows)
        # 원문-벡터 무결성 검증 결과 저장
        result['id_vector_integrity']=check_id_vector_integrity(rows,vectors)
    # 실습 결과 반환
    # - 검색 결과 포함
    # - 검증 결과 포함
    return result

# 프로그램 진입 함수
# - 실행 옵션 처리
# - 실습 실행
# - 결과 출력
def main():
    # 명령행 인자 파서 생성
    # - 프로그램 설명 등록
    parser=argparse.ArgumentParser(description='Day23 실습 05 · 원문·벡터 저장과 Top-k')
    # 실행 모드 옵션 등록
    # - fixture : 모의 검색 환경
    # - live : 실제 pgvector 환경
    parser.add_argument('--mode',choices=['fixture','live'],default='fixture',
        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')
    # 사용자 입력 파싱
    args=parser.parse_args()
    # 실습 실행
    # - Level 3 기준 수행
    result=run(args.mode,3,args)
    # 결과 파일 저장
    # - exercise_05.json 생성
    path=save_result(Path(__file__).resolve().parent,'exercise_05.json',result)
    import json
    # 결과 출력
    # - JSON 형태 출력
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
    # 저장 위치 출력
    print('결과 저장:',path)

# 프로그램 시작점
# - 직접 실행 시 main() 호출
if __name__=='__main__':
    main()

"""
원문 데이터와 임베딩 벡터를 PostgreSQL 및 pgvector 기반 저장소에 저장하도록 구현하였다.
문서 Passage를 임베딩하여 검색 가능한 벡터로 변환하고, Cosine Distance 기반 Top-K 검색을 수행할 수 있도록 구성하였다.
또한 검색 옵션 검증, 원문-벡터 무결성 검증, 검색 결과 추적 기능을 추가하여 검색 품질과 데이터 신뢰성을 확보하였다.
실습 환경에서는 Fixture 기반 검색을 제공하고, 실제 환경에서는 E5 임베딩과 pgvector를 활용한 실제 Vector Search를 수행할 수 있도록 구현하였다.
"""