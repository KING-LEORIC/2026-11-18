"""Day23 실습 03 · E5 문장 Embedding (심화, mentee).

실행: python main.py --mode fixture
실제 E5/DB: python main.py --mode live  (필요한 선행 설치 후)
수강생 TODO: 6개 / 상세 요구사항은 각 함수의 주석 및 README.md.
fixture는 모의 시연이지 모델·PostgreSQL 실측 결과가 아닙니다.
"""
# 명령행 인자 처리 기능 사용
# - ArgumentParser : CLI 옵션 정의 및 파
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
# 실습 데이터 및 모델 정보 사용
# - load_knowledge : 지식 데이터 조회
# - E5_MODEL_ID : E5 모델 식별자
from day23kit.data import load_knowledge, E5_MODEL_ID
# 임베딩 모델 로드 기능 사용
# - get_encoder : Encoder 객체 생성
from day23kit.embedding import get_encoder
# 결과 저장 기능 사용
# - save_result : JSON 결과 파일 저장
from day23kit.io import save_result

# E5 입력 데이터 생성 기능 사용
# - make_passages : 문서 입력 생성
# - make_queries : 질문 입력 생성
from app.inputs import make_passages, make_queries
# Encoder 서비스 기능 사용
# - encode_both : 문서 및 질문 임베딩 생성
# - verify_alignment : 원문과 벡터 순서 검증
# - check_shapes_vectors : 벡터 형상 검증
# - make_model_stamp : 모델 계약 정보 생성
from app.encoder_service import encode_both, verify_alignment, check_shapes_vectors, make_model_stamp

"""E5 모델을 사용한 문장 임베딩 생성 및 검증을 수행하는 실습 모듈"""

# 실습 실행 함수
# - Passage 생성
# - Embedding 생성
# - 결과 검증
def run(mode,level,args):
    # 실습 데이터 준비
    # - level 1 : 앞 3개 데이터만 사용
    # - level 2 이상 : 전체 데이터 사용
    rows=load_knowledge()[:3] if level==1 else load_knowledge()
    # Encoder 생성
    # - fixture : 모의 임베딩
    # - live : 실제 E5 모델 사용
    encoder=get_encoder(mode)
    # 문서 입력 생성
    # - E5 문서 검색용 Passage 생성
    passages=make_passages(rows)
    # 질문 입력 생성
    # - E5 질의(Query) 입력 생성
    questions=make_queries(['서버는 어디에서 실행하나요?'])
    # 임베딩 생성
    # - docs : 문서 벡터
    # - queries : 질문 벡터
    docs,queries=encode_both(encoder,passages,questions)
    # 기본 결과 생성
    # - model_id : 사용 모델 식별자
    # - document_shape : 문서 벡터 형상
    # - query_shape : 질문 벡터 형상
    result=dict(exercise=3,level=level,source_mode='e5_live' if mode=='live' else 'simulated',
                model_id=E5_MODEL_ID if mode=='live' else encoder.model_id,
                document_shape=list(docs.shape),query_shape=list(queries.shape),
                example_passage=passages[0],example_query=questions[0])
    # 정렬 및 벡터 검증 수행
    # - 원문과 벡터 순서 일치 여부 확인
    # - 벡터 개수 및 형상 검증
    if level>=2:
        result['alignment']=verify_alignment(rows,docs)
        result['vectors_valid']=check_shapes_vectors(docs,queries,len(rows))
    # 모델 계약 정보 생성
    # - 모델 버전 및 실행 환경 기록
    if level>=3:result['model_contract']=make_model_stamp(encoder,mode)
    return result

# 프로그램 진입 함수
# - 실행 옵션 처리
# - 실습 수행
# - 결과 저장 및 출력
def main():
    # 명령행 인자 파서 생성
    # - 프로그램 설명 등록
    parser=argparse.ArgumentParser(description='Day23 실습 03 · E5 문장 Embedding')
    # 실행 모드 옵션 등록
    # - fixture : 모의 임베딩 환경
    # - live : 실제 E5 모델 환경
    parser.add_argument('--mode',choices=['fixture','live'],default='fixture',
        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')
    # 사용자 입력 파싱
    args=parser.parse_args()
    # 실습 실행
    # - level 3 기준 수행
    result=run(args.mode,3,args)
    # 결과 파일 저장
    # - exercise_03.json 생성
    path=save_result(Path(__file__).resolve().parent,'exercise_03.json',result)
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
E5 임베딩 모델에 입력할 Passage와 Query를 생성하고, 문서 및 질문 벡터를 생성하도록 구현하였다.
또한 원문 데이터와 벡터의 정렬 상태를 검증하고, 벡터 개수 및 형상을 점검하여
검색 시스템에서 사용할 Embedding 데이터의 무결성을 확인할 수 있도록 구성하였다.
"""