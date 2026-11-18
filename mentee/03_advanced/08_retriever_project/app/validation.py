# Day23 / 실습 08 / 심화 validation / mentee
# 지식 데이터 조회 및 임베딩 모델 식별자 사용
# - load_knowledge : 기준 지식 스냅샷 로드
# - E5_MODEL_ID : 공식 E5 임베딩 모델 식별자 상수
from day23kit.data import load_knowledge, E5_MODEL_ID

"""AI Agent의 안정적인 파이프라인 구동을 위해 입력값의 정합성을 검사하고, 모델 및 데이터 소스의 버전을 엄격하게 검증하는 보안 및 무결성 모듈"""

# BEGIN D23-08-A01
# 질문 유효성 검증 함수
# - 입력된 질문이 문자열 타입인지 확인하고 앞뒤 공백 제거 수행
# - 빈 문자열이거나 공백만으로 구성된 경우 ValueError 발생
def validate_question(question):
    """
    TODO D23-08-A01 · validate_question
        질문은 1자 이상의 문자열이어야 하며 앞뒤 공백을 제거하세요.
        빈 값/공백만 있는 값이면 ValueError. 반환은 정리된 질문.
        API가 연결되어 있지 않아도 검사 가능한 순수 함수입니다.
    """
    # TODO D23-08-A01: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 타입 및 공백 검사 수행
    # - 문자열이 아니거나 공백을 제거했을 때 길이가 0인 경우 예외 발생
    if not isinstance(question, str) or not question.strip(): raise ValueError('empty_question')
    # 앞뒤 공백이 제거된 정제된 질문 문자열 반환
    return question.strip()
    # raise NotImplementedError("D23-08-A01: 직접 구현하세요")
# END D23-08-A01

# BEGIN D23-08-A04
# 검색 옵션 유효성 검증 함수
# - k 값이 불리언을 제외한 1 이상 9 이하의 정수인지 검사
# - category 값이 허용된 범위(None, course, development, support) 내에 있는지 확인
def validate_options(k,category):
    """
    TODO D23-08-A04 · validate_options
        k는 bool 제외 정수 1~9, category는 None 또는 course/development/support.
        위반하면 ValueError. 정상 출력은 {'k': k,'category': category}.
        입력 검사를 끝내기 전 모델·DB를 호출하지 마세요.
    """
    # TODO D23-08-A04: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # k 파라미터 제약 조건 검사 (불리언 제외 정수 및 범위 1~9 확인)
    if type(k) is not int or not 1 <= k <= 9: raise ValueError('invalid_k')
    # 카테고리 필터 값 유효성 검사
    if category not in (None, 'course', 'development', 'support'): raise ValueError('invalid_category')
    # 검증 완료된 옵션 딕셔너리 반환
    return {'k' : k, 'category' : category}
    # raise NotImplementedError("D23-08-A04: 직접 구현하세요")
# END D23-08-A04

# BEGIN D23-08-A06
# 모델 및 소스 버전 무결성 검증 함수
# - 모드가 Fixture인 경우 'simulated_only' 상태 반환
# - Live 모드인 경우 검색된 결과의 embedding_model이 E5_MODEL_ID와 일치하는지 검사
# - 검색된 문서 ID의 유효성 및 원문 source_version이 현재 스냅샷과 일치하는지 엄격 대조
def check_model_and_versions(hits,mode):
    """
    TODO D23-08-A06 · check_model_and_versions
        live 결과의 embedding_model이 intfloat/multilingual-e5-small인지 확인하세요.
        모든 ID의 source_version이 오늘 고정 스냅샷과 일치하는지 검증하세요.
        fixture는 실제 DB/모델 검증이 아니므로 'simulated_only'로 기록하세요.
    """
    # TODO D23-08-A06: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # Fixture 모드인 경우 검증 생략 후 시뮬레이션 상태 반환
    if mode == 'fixture': return 'simulated_only'
    # 기준 지식 스냅샷 데이터 로드 (ID 기반 딕셔너리 맵핑)
    snapshot = {r['id'] : r for r in load_knowledge()}
    # 검색된 각 후보 문서 순회 및 계약 검증 수행
    for hit in hits:
        # 임베딩 모델 식별자 일치 여부 검사
        if hit.get('embedding_model') != E5_MODEL_ID: raise ValueError('embedding_model_mismatch')
        # 지식 ID 존재 여부 검사
        if hit['id'] not in snapshot: raise ValueError('unexpected_knowledge_id')
        # 소스 버전 일치 여부 검사
        if hit['source_version'] != snapshot[hit['id']]['source_version']:
            raise ValueError('source_version_mismatch')
    # 모든 무결성 검증 통과 시 성공 상태 반환
    return 'live_contract_verified'
    # raise NotImplementedError("D23-08-A06: 직접 구현하세요")
# END D23-08-A06


"""
사용자 입력 질의와 검색 옵션에 대한 철저한 유효성 검사 로직을 구현하여 비정상적인 파라미터 유입을 원천 차단하도록 설계하였다.
또한 Live 환경에서는 실제 사용된 E5 모델의 식별자와 지식 소스의 버전 정합성을 스냅샷 데이터와 실시간으로 대조 검증함으로써, 
시스템 전반의 데이터 신뢰성과 계약 무결성을 완벽하게 보장하도록 구현하였다.
"""