# Day23 / 실습 06 / 심화 index_sql / mentee
# HNSW 인덱스 SQL 정의 기능 사용
# - HNSW_SQL : 기본 제공되는 HNSW 인덱스 생성 쿼리 임포트
from day23kit.db import HNSW_SQL

"""day23_search_docs 테이블의 벡터 검색 성능 최적화를 위한 HNSW 인덱스 생성 SQL과 실행 계획 분석 SQL을 정의하는 실습 모듈"""

# BEGIN D23-06-A01
# HNSW 인덱스 생성 SQL 반환 함수
# - day23_search_docs 테이블의 embedding 컬럼에 대한 Cosine HNSW 인덱스 정의
# - USING hnsw (embedding vector_cosine_ops) 연산자 클래스 활용
def create_index_sql():
    """day23_search_docs.embedding의 Cosine HNSW 인덱스를 정의하는 SQL을 반환합니다.

    Returns:
        str: HNSW 인덱스 생성 SQL 문자열 (`HNSW_SQL`)
    """
    """
    TODO D23-06-A01 · create_index_sql
        day23_search_docs.embedding의 Cosine HNSW 인덱스를 정의하세요.
        USING hnsw (embedding vector_cosine_ops)를 사용합니다.
        인덱스는 선택 항목이며 9건에서 빠른 성능을 보장하지 않습니다.
    """
    # TODO D23-06-A01: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # HNSW 인덱스 생성 SQL 반환
    # - 미리 정의된 HNSW_SQL 상수 반환
    return HNSW_SQL
    # raise NotImplementedError("D23-06-A01: 직접 구현하세요")
# END D23-06-A01

# BEGIN D23-06-A02
# 쿼리 실행 계획 분석 SQL 생성 함수
# - 거리순 검색 성능 및 인덱스 활용 여부 검증용 EXPLAIN 쿼리 작성
# - 바인딩 파라미터 2개 사용
def explain_sql():
    """데이터베이스 검색 쿼리의 실행 계획을 분석하기 위한 EXPLAIN SQL을 반환합니다.

    Returns:
        str: EXPLAIN (ANALYZE, BUFFERS) 포함된 거리순 검색 SQL 템플릿
    """
    """
    TODO D23-06-A02 · explain_sql
        SELECT id FROM day23_search_docs를 거리순으로 검색하는
        EXPLAIN (ANALYZE, BUFFERS) SQL을 작성하세요. 바인딩은 %s 두 개.
        인덱스 사용 여부를 임의로 주장하면 안 됩니다.
    """
    # TODO D23-06-A02: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # EXPLAIN 분석 SQL 반환
    # - ANALYZE 및 BUFFERS 옵션 포함
    # - 코사인 거리(<=>) 기준 정렬 및 상위 3개 제한
    return """EXPLAIN (ANALYZE, BUFFERS)
            SELECT id FROM day23_search_docs
            WHERE embedding_model = %s
            ORDER BY embedding <=> %s ASC LIMIT 3"""
    # raise NotImplementedError("D23-06-A02: 직접 구현하세요")
# END D23-06-A02

"""
day23_search_docs 테이블의 벡터 검색 성능 최적화를 위해 HNSW 코사인 인덱스 생성 SQL을 정의하였다.
또한, PostgreSQL에서 쿼리 실행 시 인덱스 활용 여부를 면밀히 분석할 수 있는 EXPLAIN (ANALYZE, BUFFERS) SQL 템플릿을 구현하였다.
코사인 거리 연산자와 pgvector 환경에서의 쿼리 동작을 검증하기 위한 기반을 충실히 마련하였다.
"""