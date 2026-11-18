# Day23 / 실습 02 / 심화 validation / mentee
# 수치 연산 라이브러리 사용
# - numpy : 벡터 검증 및 수학 연산 수행
import numpy as np


# BEGIN D23-02-A06
# 벡터 입력 검증 함수
# - 벡터 연산 전 사전 검증 수행
# - 잘못된 입력 차단
def validate_pair(a,b):
    """
    TODO D23-02-A06 · validate_pair
        배열 1차원·shape 일치·유한값·영벡터 여부를 검증하세요.
        각각 dimension_mismatch, nonfinite, zero_vector ValueError로 구분합니다.
        양쪽 입력이 올바르면 True.
    """
    # TODO D23-02-A06: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 차원 및 Shape 검증
    # - 1차원 벡터만 허용
    # - 두 벡터 Shape 일치 필요
    if a.ndim != 1 or b.ndim != 1 or a.shape != b.shape: raise ValueError('dimension_mismatch')
    # 유한값 검증
    # - NaN 금지
    # - Infinity 금지
    if not np.isfinite(a).all() or not np.isfinite(b).all(): raise ValueError('nonfinite')
    # 영벡터 검증
    # - 길이가 0인 벡터 금지
    # - 코사인 유사도 계산 불가
    if np.linalg.norm(a) <= 1e-12 or np.linalg.norm(b) <= 1e-12: raise ValueError('zero_vector')
    # 검증 성공
    return True
    # raise NotImplementedError("D23-02-A06: 직접 구현하세요")
# END D23-02-A06

"""
벡터 연산 수행 전 입력 데이터의 유효성을 검증하도록 구현하였다.
차원 불일치, 비정상 수치(NaN·Infinity), 영벡터를 사전에 차단하여 내적, 코사인 유사도, 거리 계산 과정에서 발생할 수 있는 오류를 방지한다.
이를 통해 안정적인 벡터 검색 및 유사도 계산이 가능하도록 구성하였다.
"""
