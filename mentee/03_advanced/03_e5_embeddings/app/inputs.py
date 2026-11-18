# Day23 / 실습 03 / 심화 inputs / mentee
# E5 입력 문자열 생성 기능 사용
# - passage_text : E5 문서 입력 형식 생성
from day23kit.data import passage_text


# BEGIN D23-03-A01
# E5 문서 입력 생성 함수
# - 지식 데이터를 Passage 형식으로 변환
# - 입력 순서 유지
# - 문서 임베딩 대상 생성
def make_passages(rows):
    """
    TODO D23-03-A01 · make_passages
        지식 목록을 E5 문서 입력 문자열 목록으로 변환하세요.
        문서에는 'passage: ' + 제목 + ' ' + 본문을 사용합니다.
        한 행마다 정확히 한 문자열을 만들어 순서를 유지하세요.
    """
    # TODO D23-03-A01: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # Passage 목록 생성
    # - passage: 접두어 추가
    # - 제목과 본문 결합
    # - 입력 데이터 순서 유지
    return [passage_text(row) for row in rows]
    # raise NotImplementedError("D23-03-A01: 직접 구현하세요")
# END D23-03-A01

# BEGIN D23-03-A02
# E5 질문 입력 생성 함수
# - 사용자 질문을 Query 형식으로 변환
# - 질문 임베딩 대상 생성
def make_queries(questions):
    """
    TODO D23-03-A02 · make_queries
        질문 목록 각 요소 앞에 query: 공백을 붙이세요.
        출력: 입력과 동일한 순서의 문자열 리스트.
        빈 질문을 추가해 그럴듯한 벡터를 만들지 마세요.
    """
    # TODO D23-03-A02: 위 입력·출력 계약에 맞게 직접 구현합니다.
    
    # Query 목록 생성
    # - query: 접두어 추가
    # - 질문 순서 유지
    return ['query: ' + q for q in questions]
    # raise NotImplementedError("D23-03-A02: 직접 구현하세요")
# END D23-03-A02

"""
E5 임베딩 모델의 입력 형식을 맞추기 위해 구현하였다.
문서는 passage: 접두어를 사용하고, 질문은 query: 접두어를 사용하여 모델이 입력 유형을 구분할 수 있도록 구성하였다.
"""
