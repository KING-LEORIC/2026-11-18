# Day23 / 실습 07 / 심화 reference / mentee



# BEGIN D23-07-A01
# 평가 케이스북 생성 함수
# - 강의 질문 3종과 각 질문별 확인할 지식 ID(정답/근거 ID) 목록 구성
# - 자동 생성된 정답이 아닌 사람이 평가할 고정 기준 샘플임을 정의
def make_casebook():
    """
    TODO D23-07-A01 · make_casebook
        강의의 질문 3종과 확인할 지식 ID를 구성하세요.
        server(102), retention(101: 보관 기간 없음), error(103/108).
        자동 생성한 정답이 아니라 사람이 평가할 고정 기준 샘플임을 표시합니다.
    """
    # TODO D23-07-A01: 위 입력·출력 계약에 맞게 직접 구현합니다.
    
    # 평가 케이스북 목록 반환
    # - server, retention, error 케이스별 질문 및 레퍼런스 ID 매핑
    return [
        {'case_id' : 'server', 'question' : '서버는 어디에서 실행하나요?', 'reference_ids' : [102]},
        {'case_id' : 'retention', 'question' : '실습 파일은 몇 년 동안 보관하나요?', 'reference_ids' : []},
        {'case_id' : 'error', 'question' : '오류를 질문할 때 무엇을 적어야 하나요?', 'reference_ids' : [103, 108]},
        ]
    # raise NotImplementedError("D23-07-A01: 직접 구현하세요")
# END D23-07-A01

# BEGIN D23-07-A02
# 훈련 레퍼런스 관련성 수동 판정 함수
# - 교안 원문 근거를 바탕으로 케이스별 문서 ID의 관련성 수준 판정
# - 관련, 부분 관련, 무관 상태로 분류하여 교육용 기준 제공
def judge_training_reference(case_id,doc_id):
    """
    TODO D23-07-A02 · judge_training_reference
        교안에 미리 주어진 원문 근거로 관련/부분 관련/무관을 수동 기준표로 판정하세요.
        server:102 관련,106 부분 관련. retention:101 부분 관련(기간 없음).
        error:103,108 관련. 그 밖에는 무관.
        *이 표는 사람이 만든 교육용 기준이며 모델 검색 평가점수가 아닙니다.*
    """
    # TODO D23-07-A02: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 수동 기준표 골드 데이터 정의
    # - 케이스별 문서 ID에 대응하는 정성평가 판정 결과 매핑
    gold = {'server' : {102 : '관련', 106 : '부분 관련'}, 'retention' : {101 : '부분 관련'}, 'error' : {103 : '관련', 108 : '관련'}}
    # 케이스 존재 여부 검증
    # - 정의되지 않은 케이스 ID 입력 시 ValueError 발생
    if case_id not in gold: raise ValueError('unknown_case')
    # 해당 문서 ID의 판정 결과 반환
    # - 등록된 기준이 없는 경우 기본값 '무관' 반환
    return gold[case_id].get(doc_id, '무관')
    # raise NotImplementedError("D23-07-A02: 직접 구현하세요")
# END D23-07-A02

"""
강의 질문을 기반으로 사람이 검토할 수 있는 정성평가 고정 기준 샘플(케이스북)을 정의하고, 
원문 근거에 따른 수동 관련성 판정 로직을 구현하여 교육용 검색 평가의 신뢰성과 기준을 제공하도록 설계하였다.
"""