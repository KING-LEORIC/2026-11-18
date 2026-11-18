# Day23 / 실습 05 / 심화 validation / mentee
# 원문 데이터 검증 기능 사용
# - validate_snapshot : 원문 데이터 무결성 검증
from day23kit.data import validate_snapshot
# 임베딩 벡터 검증 기능 사용
# - validate_vectors : 벡터 개수, 차원, 값 상태 검증
from day23kit.embedding import validate_vectors

"""검색 옵션과 원문-벡터 무결성을 검증하는 모듈"""

# BEGIN D23-05-A05
# 검색 옵션 검증 함수
# - Top-K 검색 개수 검증
# - Category 조건 검증
# - 잘못된 검색 요청 차단
def check_search_options(k,category):
    """
    TODO D23-05-A05 · check_search_options
        k는 bool을 제외한 정수 1~9, category는 None 또는 course/development/support인지 검사하세요.
        잘못된 값은 ValueError. 정상 시 {'k':k,'category':category} 반환.
    """
    # TODO D23-05-A05: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # Top-K 개수 검증
    # - bool 타입 제외
    # - 정수만 허용
    # - 1~9 범위만 허용
    if type(k) is not int or not 1 <= k <= 9: raise ValueError('invalid_k')
    # Category 조건 검증
    # - None 허용
    # - 정의된 Category만 허용
    if category is not None and category not in ('course', 'development', 'support'):
        raise ValueError('invalid_category')
    # 검증 결과 반환
    # - k : 검증 완료된 Top-K 개수
    # - category : 검증 완료된 Category 조건
    return {'k' : k, 'category' : category}
    # raise NotImplementedError("D23-05-A05: 직접 구현하세요")
# END D23-05-A05

# BEGIN D23-05-A06
# 원문-벡터 무결성 검증 함수
# - 원문 데이터 무결성 검증
# - 벡터 데이터 무결성 검증
# - ID 변경 여부 검증
# - 데이터 버전 정보 검증
def check_id_vector_integrity(rows,vectors):
    """
    TODO D23-05-A06 · check_id_vector_integrity
        지식 ID 중복·누락·벡터 행 수/차원/유한값/norm을 검사하세요.
        기존 원문과 행 순서를 유지하며 정상일 때 True를 반환합니다.
        실제 DB 저장 전 검증에 사용합니다.
    """
    # TODO D23-05-A06: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 원문 데이터 검증
    # - ID 중복 확인
    # - 필수 필드 확인
    # - Snapshot 무결성 확인
    validate_snapshot(rows)
    # 임베딩 벡터 검증
    # - 벡터 개수 검증
    # - 벡터 차원 검증
    # - 유한값 및 정규화 상태 검증
    validate_vectors(vectors, len(rows))
    # 원본 ID 집합 검증
    # - 101~109 고정 여부 확인
    # - 원문 데이터 변조 여부 확인
    if sorted(r['id'] for r in rows) != list(range(101, 110)):
        raise ValueError('knowledge_id_set_changed')
    # source_version 검증
    # - 101~103 : knowledge_v1
    # - 104~109 : knowledge_search_v2
    for r in rows:
        # 기대 버전 결정
        expected = 'knowledge_v1' if r['id'] <= 103 else 'knowledge_search_v2'
        # 버전 정보 검증
        # - 원문 버전 계약 준수 여부 확인
        if r['source_version'] != expected: raise ValueError('source_version_mismatch')
    # 무결성 검증 성공
    # - 원문 데이터와 벡터 데이터 모두 정상
    return True
    # raise NotImplementedError("D23-05-A06: 직접 구현하세요")
# END D23-05-A06

"""
Vector Search 저장 전 데이터 품질을 검증하기 위해 구현하였다.
검색 옵션(k, category)이 허용 범위 내에 있는지 확인하고, 잘못된 검색 요청이 수행되지 않도록 구성하였다.
또한 원문 데이터와 임베딩 벡터의 개수, 차원, ID 집합, 버전 정보를 검증하여 검색 결과와 원문 데이터의 연결 관계를 보장하도록 구현하였다.
DB 저장 이후에도 원문과 벡터를 안정적으로 추적할 수 있도록 검색 인덱스의 무결성을 유지하는 역할을 수행한다.
"""