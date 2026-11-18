# Day23 / 실습 06 / 심화 plan_review / mentee

"""PostgreSQL 실행 계획 텍스트 분석, 연산자 호환성 검증, Top-K 일치율 산출 및 ANN 필터링 진단 기능을 수행하는 실습 모듈"""

# BEGIN D23-06-A03
# 실행 계획 스캔 방식 판정 함수
# - EXPLAIN 결과 텍스트를 분석하여 Index Scan, Seq Scan 여부 확인
def read_scan_type(plan_lines):
    """PostgreSQL EXPLAIN 텍스트 라인들을 분석하여 스캔 방식을 판정합니다.

    Args:
        plan_lines (list[str]): EXPLAIN 결과의 텍스트 라인 리스트

    Returns:
        str: 스캔 방식 판정 결과 ('index', 'seq', 또는 'unknown')
    """
    """
    TODO D23-06-A03 · read_scan_type
        PostgreSQL EXPLAIN 텍스트에서 Index Scan / Seq Scan / 기타를 구분하세요.
        계획이 없으면 unknown, index가 있으면 index, seq면 seq로 반환합니다.
        작은 9건 테이블에서 Seq Scan은 오류가 아닙니다.
    """
    # TODO D23-06-A03: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 실행 계획 라인들을 하나의 문자열로 결합
    # - 검색 편의를 위한 공백 기준 병합
    s = ' '.join(plan_lines)
    # Index Scan 포함 여부 검사
    # - 인덱스 활용 시 'index' 반환
    if 'Index Scan' in s: return 'index'
    # Seq Scan 포함 여부 검사
    # - 순차 스캔 시 'seq' 반환
    if 'Seq Scan' in s: return 'seq'
    # 판정 불가 시 기본값 반환
    # - 'unknown' 상태 반환
    return 'unknown'
    # raise NotImplementedError("D23-06-A03: 직접 구현하세요")
# END D23-06-A03

# BEGIN D23-06-A04
# 연산자 호환성 검증 함수
# - SQL 내 코사인 거리 연산자(<=>)와 벡터 연산자 클래스 일치 여부 확인
def check_operator_compatibility(sql,operator_class):
    """SQL 내 사용된 거리 연산자와 지정된 연산자 클래스의 호환성을 검증합니다.

    Args:
        sql (str): 실행할 SQL 쿼리 문자열
        operator_class (str): 벡터 연산자 클래스명 (예: 'vector_cosine_ops')

    Returns:
        bool: 검증 성공 시 True 반환

    Raises:
        ValueError: 코사인 연산자(<=>)를 사용했으나 'vector_cosine_ops'가 아닐 경우
    """
    """
    TODO D23-06-A04 · check_operator_compatibility
        SQL이 cosine <=> 를 사용하면 vector_cosine_ops가 맞는지 검사하세요.
        불일치 시 ValueError, 정상 시 True.
        L2 / negative inner product와 혼동하지 않습니다.
    """
    # TODO D23-06-A04: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 코사인 거리 연산자 사용 여부 및 연산자 클래스 일치 검사
    # - <=> 사용 시 vector_cosine_ops 필수 지정 요구
    if '<=>' in sql and operator_class != 'vector_cosine_ops': raise ValueError('operator_class_mismatch')
    # 검증 통과 시 True 반환
    return True
    # raise NotImplementedError("D23-06-A04: 직접 구현하세요")
# END D23-06-A04

# BEGIN D23-06-A05
# Top-K 검색 결과 일치율 계산 함수
# - Exact Top-K 결과와 ANN Top-K 결과 간의 ID 집합 일치 비율 산출
def compare_topk(exact_ids,ann_ids):
    """Exact Top-K 결과 ID 집합과 ANN Top-K 결과 ID 집합의 일치율을 계산합니다.

    Args:
        exact_ids (list): 정확한 검색(Exact) 결과 ID 리스트
        ann_ids (list): 근사 검색(ANN) 결과 ID 리스트

    Returns:
        float | None: 일치율 (겹치는 ID 수 / exact_ids 수). exact_ids가 비어있으면 None 반환.
    """
    """
    TODO D23-06-A05 · compare_topk
        Exact Top-k와 ANN Top-k의 ID 집합 일치율을 계산하세요.
        겹치는 ID 수 / exact_ids 수. 빈 exact_ids는 None.
        인덱스 속도나 모델 품질을 만들어 내면 안 됩니다.
    """
    # TODO D23-06-A05: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 기준 데이터(exact_ids) 존재 여부 검사
    # - 빈 목록인 경우 계산 불가로 None 반환
    if not exact_ids: return None
    # 교집합 개수 산출 및 일치율 계산
    # - 겹치는 ID 수 / 기준 전체 ID 수
    return len(set(exact_ids) & set(ann_ids)) / len(set(exact_ids))
    # raise NotImplementedError("D23-06-A05: 직접 구현하세요")
# END D23-06-A05

# BEGIN D23-06-A06

# 필터링된 ANN 검색 결과 부족 판정 함수
# - 메타데이터 필터 및 ANN 검색 결합 시 결과 부족 여부 진단
def filtered_ann_warning(k,returned,exact_count):
    """메타데이터 필터가 포함된 ANN 검색에서 결과 반환 개수의 부족 여부를 진단합니다.

    Args:
        k (int): 요청된 Top-K 개수
        returned (int): 실제로 반환된 결과 개수
        exact_count (int): 조건에 부합하는 전체 원문의 총 개수

    Returns:
        str: 진단 결과 메시지 ('review_ann_filter' 또는 'no_shortfall_observed')
    """
    """
    TODO D23-06-A06 · filtered_ann_warning
        ANN + Metadata 필터에서 반환 개수가 부족한지 판정하세요.
        기대 최대 개수=min(k,exact_count). 반환이 부족하면 검토 메시지를 반환하세요.
        이는 성능 측정이 아니라 후보 누락 가능성을 알려주는 진단입니다.
    """
    # TODO D23-06-A06: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 기대되는 최대 결과 개수 계산
    # - 요청된 k와 실제 전체 일치 항목 수 중 최솟값 선정
    expected = min(k, exact_count)
    # 반환된 개수와 기대 개수 비교
    # - 반환된 결과가 기대치보다 적을 경우 경고 메시지 반환
    return 'review_ann_filter' if returned < expected else 'no_shortfall_observed'
    # raise NotImplementedError("D23-06-A06: 직접 구현하세요")
# END D23-06-A06

"""
PostgreSQL의 실행 계획 텍스트를 분석하여 인덱스 스캔(Index Scan) 및 순차 스캔(Seq Scan) 여부를 판정하고, 
SQL 내 벡터 연산자와 연산자 클래스의 호환성을 엄밀하게 검증할 수 있도록 구현하였다.
또한 Exact Top-K와 근사 검색(ANN) 결과 간의 일치율을 정량적으로 산출하고, 
메타데이터 필터링 결합 시 발생할 수 있는 후보 누락 가능성을 진단하는 기능을 추가하여 검색 안정성과 신뢰성을 확보하였다.
"""