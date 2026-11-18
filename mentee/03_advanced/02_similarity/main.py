"""Day23 실습 02 · Vector·Similarity·Distance (심화, mentee).

실행: python main.py --mode fixture
실제 E5/DB: python main.py --mode live  (필요한 선행 설치 후)
수강생 TODO: 6개 / 상세 요구사항은 각 함수의 주석 및 README.md.
fixture는 모의 시연이지 모델·PostgreSQL 실측 결과가 아닙니다.
"""
# 명령행 인자 처리 기능 사용
# - ArgumentParser : CLI 옵션 정의 및 파싱
import argparse
# 파이썬 실행 환경 제어 기능 사용
# - sys.path : 모듈 검색 경로 추가
import sys
# 파일 경로 처리 기능 사용
# - Path : 운영체제 독립적인 경로 관리
from pathlib import Path
# 공용 모듈 경로 추가
# - common 디렉터리 라이브러리 사용 가능
sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'common'))
# 수치 연산 라이브러리 사용
# - numpy : 벡터 및 행렬 연산 수행
import numpy as np
# 벡터 거리 계산 기능 사용
# - cosine_distance : 코사인 거리 계산
from day23kit.mathops import cosine_distance
# 결과 저장 기능 사용
# - save_result : JSON 결과 파일 저장
from day23kit.io import save_result

# 벡터 연산 기능 사용
# - dot : 내적 계산
# - cosine : 코사인 유사도 계산
# - l2 : 유클리드 거리 계산
# - normalize : 벡터 정규화
# - rank_dot_vs_cosine : 내적과 코사인 유사도 비교
from app.math_ops import dot, cosine, l2, normalize, rank_dot_vs_cosine
# 벡터 입력 검증 기능 사용
# - validate_pair : 벡터 유효성 검사
from app.validation import validate_pair

"""벡터 유사도 및 거리 계산 결과를 검증하는 실습 모듈"""

# 실습 실행 함수
# - 벡터 연산 수행
# - 유사도 및 거리 계산
# - 검증 결과 생성
def run(mode,level,args):
    # 예제 벡터 생성
    # - q : 질의(Query) 벡터
    # - a : 비교 대상 벡터
    # - u : 기준 벡터
    # - v : 크기가 큰 비교 벡터
    q=np.array([1.,0.]);a=np.array([.8,.6]);u=np.array([1.,0.]);v=np.array([10.,10.])
    # 기본 계산 결과 생성
    # - dot : 내적
    # - cosine : 코사인 유사도
    # - l2 : 유클리드 거리
    # - cosine_distance : 코사인 거리
    result=dict(exercise=2,level=level,source_mode='local_math',
                dot=round(dot(q,a),6),cosine=round(cosine(q,a),6),l2=round(l2(q,a),6),
                cosine_distance=round(1-cosine(q,a),6))
    # 정규화 및 순위 비교 수행
    # - normalize : 벡터 크기 영향 제거
    # - ranking : 내적 순위와 코사인 순위 비교
    if level>=2:
        result['normalized_v']=normalize(v).round(6).tolist()
        result['rankings']=rank_dot_vs_cosine(q,{'U':u,'V':v})
    # 입력값 검증 수행
    # - 정상 벡터 검증
    # - 오류 입력 검증
    if level>=3:
        result['validated']=validate_pair(q,a)
        # 오류 사례 저장
        # - 차원 불일치
        # - NaN 포함
        # - 영벡터
        errors={}
        for label,x,y in [('dimension_mismatch',q,np.array([1.,0.,2.])),
                           ('nonfinite',q,np.array([np.nan,1.])),
                           ('zero_vector',q,np.array([0.,0.]))]:
            try:validate_pair(x,y)
            except ValueError as e:errors[label]=str(e)
        result['invalid_inputs']=errors
    return result

# 프로그램 진입 함수
# - 실행 옵션 처리
# - 실습 수행
# - 결과 저장 및 출력
def main():
    # 명령행 인자 파서 생성
    # - 프로그램 설명 등록
    parser=argparse.ArgumentParser(description='Day23 실습 02 · Vector·Similarity·Distance')
    # 실행 모드 옵션 등록
    # - fixture : 모의 실습 환경
    # - live : 실제 E5 및 DB 환경
    parser.add_argument('--mode',choices=['fixture','live'],default='fixture',
        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')
    # 사용자 입력 파싱
    args=parser.parse_args()
    # 실습 실행
    # - level 3 기준 수행
    result=run(args.mode,3,args)
    # 결과 파일 저장
    # - exercise_02.json 생성
    path=save_result(Path(__file__).resolve().parent,'exercise_02.json',result)
    import json
    # 결과 출력
    # - JSON 형식으로 출력
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
    # 저장 경로 출력
    print('결과 저장:',path)

# 프로그램 시작점
# - 직접 실행 시 main() 호출
if __name__=='__main__':
    main()

"""
벡터 검색에서 사용하는 핵심 수학 개념을 검증하도록 구현하였다.
내적(Dot Product), 코사인 유사도(Cosine Similarity), 유클리드 거리(L2 Distance)를 비교하여 벡터 간 유사성을 측정하고,
정규화를 통해 벡터 크기의 영향을 제거하는 과정을 학습하도록 구성하였다.
또한 차원 불일치, NaN, 영벡터 등의 비정상 입력을 검증하여 안정적인 벡터 연산이 가능하도록 구현하였다.
"""