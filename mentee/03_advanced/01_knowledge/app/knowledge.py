# Day23 / 실습 01 / 심화 knowledge / mentee



# BEGIN D23-01-A01
# 원본 지식 선택 함수
# - 기존 학습 데이터(101, 102, 103)만 선별
# - ID 오름차순 정렬
# - 원본 데이터 수정 방지
def select_original(rows):
    """
    TODO D23-01-A01 · select_original
        기존 수업에서 사용한 101·102·103만 ID 오름차순으로 선택합니다.
        입력: 전체 지식 목록(list[dict]). 출력: 원래 지식 3개를 담은 list.
        원본 딕셔너리의 id/title/content를 수정하지 마세요.
        개념: 원문 ID 고정·검색할 자료의 범위.
    """
    # TODO D23-01-A01: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 원본 지식 선별
    # - ID가 101, 102, 103인 데이터만 선택
    # - dict(r) : 원본 객체 복사
    # - key=lambda r:r['id'] : ID 오름차순 정렬
    return sorted((dict(r) for r in rows if r['id'] in (101, 102, 103)), key = lambda r : r['id'])
    # raise NotImplementedError("D23-01-A01: 직접 구현하세요")
# END D23-01-A01

# BEGIN D23-01-A02
# Passage 입력 생성 함수
# - E5 문서 검색 모델 입력 형식 생성
# - "passage: 제목 본문" 형식 사용
# - 제목과 본문 사이 공백 1개 사용
def make_passage_input(row):
    """
    TODO D23-01-A02 · make_passage_input
        E5 문서 입력 텍스트를 "passage: 제목 본문" 형식으로 만드세요.
        입력: 지식 한 행. 출력: 문자열. 제목과 본문을 공백 하나로 구분하세요.
        개념: FAQ 질문과 달리 지식 본문을 검색 대상으로 사용합니다.
    """
    # TODO D23-01-A02: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # E5 Passage 생성
    # - passage: : 문서 검색용 접두어
    # - title : 문서 제목
    # - content : 문서 본문
    return 'passage: ' + row['title'] + ' ' + row['content']
    # raise NotImplementedError("D23-01-A02: 직접 구현하세요")
# END D23-01-A02

# BEGIN D23-01-A03
# 지식-벡터 추적 정보 생성 함수
# - 원문 데이터 보존
# - 검색 대상 정보 기록
# - 버전 정보 추적
def make_mapping(rows):
    """
    TODO D23-01-A03 · make_mapping
        각 지식의 id/title/content/category/source_version 및 passage_input을 기록하세요.
        입력: 선택된 지식 목록. 출력: 딕셔너리 목록.
        개념: 벡터를 생성하기 전에도 원문·ID·버전을 추적해야 합니다.
    """
    # TODO D23-01-A03: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 매핑 정보 생성
    # - id : 원본 지식 식별자
    # - title : 지식 제목
    # - content : 지식 본문
    # - category : 지식 분류
    # - source_version : 원본 데이터 버전
    # - passage_input : 검색 모델 입력 문자열
    return [dict(id = r['id'], title = r['title'], content = r['content'], category = r['category'],
                 source_version = r['source_version'], passage_input = make_passage_input(r)) for r in rows]
    # raise NotImplementedError("D23-01-A03: 직접 구현하세요")
# END D23-01-A03

"""
검색 시스템에서 사용할 원본 지식을 선별하고, E5 임베딩 모델 입력 형식인 Passage를 생성하도록 구현하였다.
또한 원문 데이터, 식별자(ID), 버전 정보를 함께 매핑하여 벡터 생성 이후에도 검색 결과의 원본 추적이 가능하도록 구성하였다.
"""