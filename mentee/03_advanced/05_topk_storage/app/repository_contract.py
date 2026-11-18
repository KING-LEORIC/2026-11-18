# Day23 / 실습 05 / 심화 repository_contract / mentee
# E5 문서 입력 생성 기능 사용
# - passage_text : 지식 데이터를 E5 Passage 형식 문자열로 변환
from day23kit.data import passage_text
# PostgreSQL Vector Search SQL 사용
# - TABLE_SQL : 검색 전용 테이블 생성 SQL
# - SQL_TOPK : Top-K 검색 SQL
# - SQL_CATEGORY : 카테고리 필터 검색 SQL
from day23kit.db import TABLE_SQL, SQL_TOPK, SQL_CATEGORY

"""원문 데이터와 벡터 데이터를 저장하기 위한 저장 구조와 Vector Search SQL 계약을 정의하는 모듈"""

# BEGIN D23-05-A01
# 검색 전용 테이블 생성 SQL 반환 함수
# - 원본 knowledge 테이블과 분리
# - Vector Search 전용 저장소 사용
# - pgvector 기반 벡터 저장 지원
def schema_sql():
    """
    TODO D23-05-A01 · schema_sql
        기존 knowledge 테이블을 건드리지 않는 day23_search_docs의 CREATE TABLE SQL을 작성하세요.
        필드: id(PK),title,content,category,source_version,embedding_model,embedding vector(384).
        DROP/TRUNCATE를 사용하지 않습니다.
    """
    # TODO D23-05-A01: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 검색 전용 테이블 생성 SQL 반환
    # - 원문 데이터 저장
    # - 임베딩 벡터 저장
    # - knowledge 테이블과 독립 운영
    return TABLE_SQL
    # raise NotImplementedError("D23-05-A01: 직접 구현하세요")
# END D23-05-A01

# BEGIN D23-05-A02
# 검색용 문서 데이터 생성 함수
# - 원문 데이터 보존
# - Passage 입력 생성
# - Embedding 입력 준비
def prepare_document_rows(rows):
    """
    TODO D23-05-A02 · prepare_document_rows
        지식 101~109의 ID/제목/본문/분류/버전 및 passage 입력을 순서대로 묶으세요.
        반환: [{'id', 'passage_input', ...}, ...]. 같은 ID를 새로 만들지 않습니다.
    """
    # TODO D23-05-A02: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 검색용 문서 데이터 생성
    # - 원본 필드 유지
    # - passage_input 필드 추가
    # - 원본 ID 유지
    return [{**dict(r), 'passage_input' : passage_text(r)} for r in rows]
    # raise NotImplementedError("D23-05-A02: 직접 구현하세요")
# END D23-05-A02

# BEGIN D23-05-A03
# Top-K 검색 SQL 반환 함수
# - Cosine Distance 기반 검색
# - 가까운 벡터 우선 조회
# - 임베딩 모델 혼합 방지
def topk_sql():
    """
    TODO D23-05-A03 · topk_sql
        Cosine distance(<=>) 오름차순, k개 제한 SQL을 작성하세요.
        SELECT에 id,title,content,category,source_version,embedding_model,distance 포함.
        E5 외 다른 공간 혼합을 막도록 embedding_model을 필터합니다.
    """
    # TODO D23-05-A03: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # Top-K 검색 SQL 반환
    # - Cosine Distance(<=>) 기준 정렬
    # - 가장 가까운 벡터부터 조회
    # - Top-K 개수 제한
    # - embedding_model 필터 적용
    return SQL_TOPK
    # raise NotImplementedError("D23-05-A03: 직접 구현하세요")
# END D23-05-A03

# BEGIN D23-05-A04
# 카테고리 필터 검색 SQL 반환 함수
# - Category 조건 검색 지원
# - Top-K 검색 수행
# - SQL Injection 방지
def filtered_sql():
    """
    TODO D23-05-A04 · filtered_sql
        category 필터가 포함된 Top-k SQL을 작성하세요.
        쿼리 벡터와 category, 모델, k는 문자열 합치기가 아닌 %s 바인딩입니다.
    """
    # TODO D23-05-A04: 위 입력·출력 계약에 맞게 직접 구현합니다.
    
    # 카테고리 필터 검색 SQL 반환
    # - category 조건 적용
    # - Cosine Distance 기반 Top-K 검색
    # - %s Parameter Binding 사용
    # - SQL Injection 공격 방지
    # - embedding_model 필터 적용
    return SQL_CATEGORY
    # raise NotImplementedError("D23-05-A04: 직접 구현하세요")
# END D23-05-A04

"""
PostgreSQL과 pgvector를 이용한 검색 저장소 구조를 정의하도록 구현하였다.
원본 지식 데이터는 그대로 유지하고, 검색용 Passage와 Embedding Vector를 별도 테이블에 저장할 수 있도록 구성하였다.
또한 Cosine Distance 기반 Top-K 검색 SQL과 카테고리 조건 검색 SQL을 분리하여 다양한 검색 조건을 처리할 수 있도록 구현하였다.
검색 시 embedding_model을 함께 관리하여 서로 다른 임베딩 모델의 벡터가 혼합되지 않도록 설계하였다.
"""