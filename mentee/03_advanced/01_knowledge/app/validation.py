# Day23 / 실습 01 / 심화 validation / mentee



# BEGIN D23-01-A04
# ID 중복 검증 함수
# - 모든 지식의 ID 유효성 검사
# - 중복 ID 검출
# - 검색 결과 추적 오류 방지
def reject_duplicate_ids(rows):
    """
    TODO D23-01-A04 · reject_duplicate_ids
        모든 9개 지식의 ID 중복 여부를 점검하고 중복이면 ValueError를 내세요.
        단순 len만 비교하지 말고 id의 타입이 int(True 제외)인지도 확인합니다.
        출력: 중복이 없으면 실제 ID 집합(set).
    """
    # TODO D23-01-A04: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 전체 ID 추출
    # - 모든 지식의 식별자 수집
    ids = [r.get('id') for r in rows]
    # ID 타입 검증
    # - int 타입만 허용
    # - bool(True, False) 제외
    # - 1 이상의 양의 정수만 허용
    if any(type(x) is not int or x <= 0 for x in ids): raise ValueError('id 타입 오류')
    # ID 중복 검사
    # - 동일 ID 존재 시 검색 결과 추적 불가
    if len(ids) != len(set(ids)): raise ValueError('duplicate_id')
    # 검증된 ID 집합 반환
    return set(ids)
    # raise NotImplementedError("D23-01-A04: 직접 구현하세요")
# END D23-01-A04

# BEGIN D23-01-A05
# 필수 필드 검증 함수
# - 검색에 필요한 핵심 데이터 확인
# - 누락 및 공백 데이터 차단
# - Embedding 품질 보장
def reject_missing_fields(rows):
    """
    TODO D23-01-A05 · reject_missing_fields
        title/content/category/source_version의 누락 또는 공백 문자열을 거부하세요.
        입력: 전체 지식 목록. 정상 출력: True. 잘못된 항목은 ValueError.
        개념: 잘못된 원문은 정상적인 Embedding 입력이 될 수 없습니다.
    """
    # TODO D23-01-A05: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 전체 데이터 순회
    for r in rows:
        # 필수 필드 검증
        # - title : 지식 제목
        # - content : 지식 본문
        # - category : 지식 분류
        # - source_version : 데이터 버전 정보
        for name in ('title', 'content', 'category', 'source_version'):
            # 문자열 여부 및 공백 검사
            # - None 방지
            # - 빈 문자열 방지
            # - 공백만 입력된 값 방지
            if not isinstance(r.get(name), str) or not r[name].strip():
                raise ValueError('missing_or_blank:' + name)
    # 검증 성공
    return True
    # raise NotImplementedError("D23-01-A05: 직접 구현하세요")
# END D23-01-A05

# BEGIN D23-01-A06
# 버전 관리 검증 함수
# - 지식별 버전 계약 확인
# - 데이터 변경 이력 추적
# - 잘못된 버전 데이터 차단
def audit_versions(rows):
    """
    TODO D23-01-A06 · audit_versions
        101~103은 knowledge_v1, 104~109는 knowledge_search_v2인지 검사하세요.
        기존 원문을 덮어쓰지 말고, 오류이면 ValueError를 발생시킵니다.
        반환: {버전: ID 목록} 딕셔너리. 개념: 데이터 갱신 계약·버전 추적.
    """
    # TODO D23-01-A06: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 버전별 ID 저장 구조 생성
    # - knowledge_v1 : 기존 지식 데이터
    # - knowledge_search_v2 : 검색 확장 데이터
    out={'knowledge_v1':[],'knowledge_search_v2':[]}
    # 전체 데이터 순회
    for r in rows:
        # 기대 버전 결정
        # - 101~103 : knowledge_v1
        # - 104~109 : knowledge_search_v2
        expected = 'knowledge_v1' if r['id'] in (101, 102, 103) else 'knowledge_search_v2'
        # 버전 계약 검증
        # - 실제 버전과 기대 버전 비교
        if r['source_version'] != expected: raise ValueError('version_mismatch:' + str(r['id']))
        # 버전별 ID 기록
        out[expected].append(r['id'])
    # 버전별 ID 목록 반환
    return out
    # raise NotImplementedError("D23-01-A06: 직접 구현하세요")
# END D23-01-A06

"""
검색용 지식 데이터의 품질을 검증하기 위해 구현하였다.
ID 중복 여부를 확인하여 검색 결과의 식별 가능성을 보장하고, 필수 필드 검증을 통해 정상적인 Embedding 입력만 사용하도록 구성하였다.
또한 source_version 검사를 수행하여 데이터 변경 계약과 버전 이력을 추적할 수 있도록 구현하였다.
"""