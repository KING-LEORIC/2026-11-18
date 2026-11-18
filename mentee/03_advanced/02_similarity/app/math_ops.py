# Day23 / 실습 02 / 심화 math_ops / mentee
# 수치 연산 라이브러리 사용
# - numpy : 벡터 및 행렬 연산 수행
import numpy as np


# BEGIN D23-02-A01
# 벡터 내적 계산 함수
# - 두 벡터의 방향 유사성 계산에 사용
# - 코사인 유사도 계산의 기반
def dot(a,b):
    """
    TODO D23-02-A01 · dot
        같은 위치의 숫자를 곱해 합산하는 내적을 구현하세요.
        예: (1,0)·(0.8,0.6)=0.8. 입력 NumPy 배열 2개, 출력 float.
    """
    # TODO D23-02-A01: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 벡터 내적 계산
    # - 같은 위치 원소끼리 곱한 후 합산
    # - 결과를 float 타입으로 변환
    return float(np.dot(a,b))
    # raise NotImplementedError("D23-02-A01: 직접 구현하세요")
# END D23-02-A01

# BEGIN D23-02-A02
# 코사인 유사도 계산 함수
# - 두 벡터의 방향 유사성 측정
# - 벡터 크기의 영향을 제거
def cosine(a,b):
    """
    TODO D23-02-A02 · cosine
        내적을 두 벡터 길이의 곱으로 나누어 Cosine similarity를 구하세요.
        q=(1,0), A=(0.8,0.6)라면 0.8입니다.
        입력: NumPy 배열 2개. 출력: float. 영벡터는 무조건 거부합니다.
    """
    # TODO D23-02-A02: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 벡터 길이 계산
    # - norm : 벡터 크기(Magnitude)
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    # 영벡터 검증
    # - 길이가 0인 벡터는 코사인 계산 불가
    if na <= 1e-12 or nb <= 1e-12: raise ValueError('zero_vector')
    # 코사인 유사도 계산
    # - 내적 ÷ (벡터A 길이 × 벡터B 길이)
    return dot(a, b) / (na * nb)
    # raise NotImplementedError("D23-02-A02: 직접 구현하세요")
# END D23-02-A02

# BEGIN D23-02-A03
# 유클리드 거리 계산 함수
# - 두 벡터 사이 실제 거리 측정
# - 값이 작을수록 서로 가까움
def l2(a,b):
    """
    TODO D23-02-A03 · l2
        두 벡터의 좌표 차이로 L2 거리를 구하세요. 출력 float.
        q=(1,0), A=(0.8,0.6) → sqrt(0.4) ≈ 0.6325.
    """
    # TODO D23-02-A03: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # L2 거리 계산
    # - 두 벡터 차이의 길이 계산
    return float(np.linalg.norm(a - b))
    # raise NotImplementedError("D23-02-A03: 직접 구현하세요")
# END D23-02-A03

# BEGIN D23-02-A04
# 벡터 정규화 함수
# - 벡터 길이를 1로 변환
# - 방향만 남기고 크기 영향 제거
def normalize(a):
    """
    TODO D23-02-A04 · normalize
        임의 벡터 a를 길이가 1인 단위 벡터로 변환하세요.
        기존 배열을 직접 변경하지 않습니다. 영벡터는 ValueError.
    """
    # TODO D23-02-A04: 위 입력·출력 계약에 맞게 직접 구현합니다.
    # 벡터 길이 계산
    n=float(np.linalg.norm(a))
    # 영벡터 검증
    # - 길이가 0인 벡터는 정규화 불가
    if n <= 1e-12: raise ValueError('zero_vector')
    # 단위 벡터 생성
    # - 원본 벡터를 길이로 나누기
    return a / n
    # raise NotImplementedError("D23-02-A04: 직접 구현하세요")
# END D23-02-A04

# BEGIN D23-02-A05
# 유사도 순위 비교 함수
# - Dot Product 기준 순위 생성
# - Cosine Similarity 기준 순위 생성
def rank_dot_vs_cosine(q,candidates):
    """
    TODO D23-02-A05 · rank_dot_vs_cosine
        후보 {이름:벡터}를 Dot 내림차순과 Cosine 내림차순으로 각각 정렬하세요.
        결과: {'dot':[이름...], 'cosine':[이름...]}.
        크기가 큰 벡터가 Dot 순위를 바꿀 수 있음을 확인합니다.
    """
    # TODO D23-02-A05: 위 입력·출력 계약에 맞게 직접 구현합니다.
    # Dot Product 기준 정렬
    # - 값이 클수록 높은 순위
    d = sorted(candidates, key = lambda n : (-dot(q, candidates[n]), n))
    # Cosine Similarity 기준 정렬
    # - 방향이 유사할수록 높은 순위
    c = sorted(candidates, key = lambda n : (-cosine(q, candidates[n]), n))
    # 순위 결과 반환
    return {'dot':d,'cosine':c}
    # raise NotImplementedError("D23-02-A05: 직접 구현하세요")
# END D23-02-A05

"""
벡터 검색에서 사용하는 핵심 수학 연산을 구현하였다.
내적(Dot Product), 코사인 유사도(Cosine Similarity), 유클리드 거리(L2 Distance)를 통해 벡터 간 관련성을 계산하고,
정규화를 이용하여 벡터 크기의 영향을 제거할 수 있도록 구성하였다.
또한 Dot Product와 Cosine Similarity의 순위 차이를 비교하여 벡터 검색에서 코사인 유사도가 사용되는 이유를 확인할 수 있도록 구현하였다.
"""