# Day23 / 실습 07 / 심화 review / mentee
# 지식 데이터 조회 기능 사용
# - load_knowledge : 전체 지식 데이터 로드
from day23kit.data import load_knowledge

# 교안 레퍼런스 판정 기능 사용
# - judge_training_reference : 수동 관련성 판정 함수 임포트
from .reference import judge_training_reference

"""검색 결과 행 생성, 검색 상태 및 예외 분류, 메타데이터 필터 전후 효과 분석, 그리고 평가 데이터 무결성 검증 기능을 수행하는 모듈"""

# BEGIN D23-07-A03
# 리뷰 행 생성 함수
# - 질문 ID, 검색된 ID, 본문, 거리, 교재 기준 라벨을 조합하여 단일 리뷰 데이터 생성
# - human_reviewed 플래그를 False로 설정하여 수동 검토 대기 상태 표시
def make_review_row(case,hit):
    """
    TODO D23-07-A03 · make_review_row
        질문 ID·검색된 ID·본문·거리·교재 기준 라벨을 한 행으로 만드세요.
        distance는 정답 확률로 표현하지 않습니다.
        human_reviewed는 False로 두어 실제 수강생의 근거 검토 전임을 표시합니다.
    """
    # TODO D23-07-A03: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 리뷰 행 딕셔너리 반환
    # - 검색된 결과의 핵심 메타데이터 및 교재 기준 라벨 포함
    return dict(case_id = case['case_id'], query = case['question'],
                retrieved_id = hit['id'], content = hit['content'],
                distance = round(hit['distance'], 6),
                teaching_reference = judge_training_reference(case['case_id'], hit['id']),
                human_reviewed = False)
    # raise NotImplementedError("D23-07-A03: 직접 구현하세요")
# END D23-07-A03

# BEGIN D23-07-A04
# 검색 상태 분류 함수
# - 데이터베이스 예외 발생 여부, 빈 결과 목록 여부에 따라 상태 문자열 반환
# - 결과 없음과 DB 장애 상황을 엄격히 분리하여 처리
def classify_search_state(rows,error=None):
    """
    TODO D23-07-A04 · classify_search_state
        데이터베이스 예외(error)는 error, 정상 조회 결과 []는 empty,
        후보가 있으면 candidates를 반환하세요. 결과 없음과 DB 장애를 섞지 마세요.
    """
    # TODO D23-07-A04: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 데이터베이스 예외 존재 여부 검사
    # - 에러 발생 시 'error' 상태 반환
    if error is not None: return 'error'
    # 검색 결과 존재 여부에 따른 상태 분기
    # - 결과가 있으면 'candidates', 없으면 'empty' 반환
    return 'candidates' if rows else 'empty'
    # raise NotImplementedError("D23-07-A04: 직접 구현하세요")
# END D23-07-A04

# BEGIN D23-07-A05
# 필터 적용 효과 분석 함수
# - 필터 적용 전후의 ID 목록을 비교하여 제거된 ID와 추가된 ID 목록 산출
def review_filter_effect(before,after):
    """
    TODO D23-07-A05 · review_filter_effect
        필터 전후 ID 목록을 비교해 빠진 ID와 추가된 ID를 반환하세요.
        출력 {'removed': [...], 'added': [...]} 정렬된 목록.
        필터 때문에 k보다 적게 반환될 수 있습니다.
    """
    # TODO D23-07-A05: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 제거된 ID 및 추가된 ID 목록 계산
    # - 집합 연산을 통해 차집합을 구한 뒤 정렬된 리스트로 변환
    return {'removed' : sorted(set(before) - set(after)), 'added' : sorted(set(after) - set(before))}
    # raise NotImplementedError("D23-07-A05: 직접 구현하세요")
# END D23-07-A05

# BEGIN D23-07-A06
# 평가 데이터 무결성 검증 함수
# - 동일 케이스 내 중복된 retrieved_id 검사, 유효한 ID 범위 확인, 원문 버전 일치 여부 검증
def check_evaluation_integrity(rows):
    """
    TODO D23-07-A06 · check_evaluation_integrity
        같은 case_id의 retrieved_id가 중복되면 ValueError.
        지식 101~109에 없는 ID나 원문 버전 불일치도 구분하세요.
        정상일 때 true. 주의: 이 검사는 사람의 관련성 평가를 대체하지 않습니다.
    """
    # TODO D23-07-A06: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 전체 지식 데이터 스냅샷 조회
    # - ID를 키로 하는 지식 데이터 딕셔너리 생성
    snapshot={r['id']:r for r in load_knowledge()}
    seen = set()
    # 리뷰 행 순회 및 무결성 검사 루프
    for row in rows:
        key = (row['case_id'], row['retrieved_id'])
        # 중복된 결과 검사
        # - 동일한 케이스에서 동일한 ID가 중복 검색된 경우 에러 발생
        if key in seen: raise ValueError('duplicate_result')
        seen.add(key)
        # 유효한 지식 ID 존재 여부 검사
        # - 스냅샷에 존재하지 않는 ID인 경우 에러 발생
        if row['retrieved_id'] not in snapshot: raise ValueError('unknown_id')
        # 원문 버전 일치 여부 검사
        # - 검색된 소스 버전과 현재 지식 데이터의 버전이 다른 경우 에러 발생
        if row.get('source_version') != snapshot[row['retrieved_id']]['source_version']:
            raise ValueError('stale_source_version')
    # 모든 검증 통과 시 True 반환
    return True
    # raise NotImplementedError("D23-07-A06: 직접 구현하세요")
# END D23-07-A06

"""
검색 결과 리뷰 행을 일관된 포맷으로 생성하고, 데이터베이스 장애 상황과 빈 검색 결과를 명확하게 구분하여 상태를 분류하도록 구현하였다.
또한 메타데이터 필터 전후의 변화를 정밀하게 추적하는 비교 로직과, 중복 결과·알 수 없는 ID·버전 불일치 등을 철저히 검증하는 무결성 검사 함수를 추가하여 정성평가 데이터의 신뢰성을 높였다.
"""