"""Day23 실습 07 · 검색 결과 정성평가 (심화, mentee).

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
# - Path : 운영체제 독립적인 경로 처리
from pathlib import Path
# 공용 모듈 경로 추가
# - common 디렉터리 라이브러리 사용 가능
sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'common'))
# 모의 검색 기능 사용
# - fixture_search : Vector Search 시뮬레이션
from day23kit.fixtures import fixture_search
# 임베딩 기능 사용
# - get_encoder : Encoder 생성
# - encode_question : 질문 임베딩 생성
from day23kit.embedding import get_encoder, encode_question
# PostgreSQL 및 pgvector 기능 사용
# - connect_db : DB 연결
# - exact_topk : Top-K 검색 수행
# - check_data_ready : 데이터 준비 상태 확인
from day23kit.db import connect_db, exact_topk, check_data_ready
# 결과 저장 기능 사용
# - save_result : JSON 결과 파일 저장
from day23kit.io import save_result

# 정성평가 케이스 및 레퍼런스 판단 기능 사용
# - make_casebook : 평가 케이스북 생성
# - judge_training_reference : 훈련 레퍼런스 판정
from app.reference import make_casebook, judge_training_reference
# 정성평가 리뷰 및 상태 분류 기능 사용
# - make_review_row : 리뷰 행 데이터 생성
# - classify_search_state : 검색 상태 분류
# - review_filter_effect : 필터 효과 검토
# - check_evaluation_integrity : 평가 무결성 검증
from app.review import make_review_row, classify_search_state, review_filter_effect, check_evaluation_integrity

"""검색 결과에 대한 정성평가 및 케이스 기반 리뷰 데이터를 생성하고 검색 상태와 필터 효과를 분석하는 실습 모듈"""

# 실습 실행 함수
# - 평가 케이스 조회
# - 모의 또는 실제 검색 수행 (Fixture / Live)
# - 검색 상태 분류 및 리뷰 행 생성
# - 필터 효과 및 무결성 검증 수행
def run(mode,level,args):
    # 평가 케이스북 조회
    cases=make_casebook()
    reviews=[]; search_state=[]
    # 각 케이스별 검색 및 리뷰 데이터 생성 루프
    for case in cases:
        # 검색 자체는 fixture의 수학 예시 또는 실제 E5/pgvector.
        if mode=='fixture':hits=fixture_search(case['question'],k=3)
        else:
            # 라이브 모드 캐시 및 연결 초기화
            if '_live_cache' not in locals():
                encoder=get_encoder('live')
                conn=connect_db(Path(__file__).with_name('.env'))
                check_data_ready(conn)
                _live_cache=True
            # 질문 임베딩 생성 및 Top-K 검색 수행
            qvec=encode_question(encoder,case['question'])
            hits=exact_topk(conn,qvec,3)
        # 검색 상태 기록
        # - 레벨 2 이상인 경우 상세 상태 분류, 미만인 경우 기본 상태 기록
        search_state.append({'case_id':case['case_id'],'state':classify_search_state(hits) if level>=2 else ('candidates' if hits else 'empty')})
        # 검색 결과별 리뷰 행 생성 및 버전 정보 할당
        for hit in hits:
            row=make_review_row(case,hit)
            row['source_version']=hit['source_version']
            reviews.append(row)
    # 기본 결과 생성
    # - 실습 정보 저장
    # - 리뷰 행 및 검색 상태 기록
    result=dict(exercise=7,level=level,source_mode='simulated' if mode=='fixture' else 'pgvector_exact',
                review_rows=reviews,search_states=search_state,
                human_evidence_ok=None)
    # 레벨 2 이상 추가 분석 수행
    # - 필터 효과 검토 및 빈 결과 에러 처리 검증
    if level>=2:
        if mode=='live':
            qvec=encode_question(encoder,'서버는 어디에서 실행하나요?')
            baseline=[h['id'] for h in exact_topk(conn,qvec,k=3)]
            filtered=[h['id'] for h in exact_topk(conn,qvec,k=3,category='development')]
        else:
            baseline=[h['id'] for h in fixture_search('서버는 어디에서 실행하나요?',k=3)]
            filtered=[h['id'] for h in fixture_search('서버는 어디에서 실행하나요?',k=3,category='development')]
        result['filter_effect']=review_filter_effect(baseline,filtered)
        result['empty_is_not_error']=classify_search_state([])=='empty' and classify_search_state([],error='DB 연결 오류')=='error'
    # 레벨 3 추가 검증 수행
    # - 평가 무결성 검증 결과 저장
    if level>=3:result['evaluation_integrity']=check_evaluation_integrity(reviews)
    # 데이터베이스 연결 종료 (Live 모드인 경우)
    if mode=='live':conn.close()
    # 실습 결과 반환
    # - 리뷰 및 상태 데이터 포함
    return result

# 프로그램 진입 함수
# - 실행 옵션 처리
# - 실습 실행
# - 결과 출력 및 파일 저장
def main():
    # 명령행 인자 파서 생성
    # - 프로그램 설명 등록
    parser=argparse.ArgumentParser(description='Day23 실습 07 · 검색 결과 정성평가')
    # 실행 모드 옵션 등록
    # - fixture : 모의 검색 환경
    # - live : 실제 pgvector 환경
    parser.add_argument('--mode',choices=['fixture','live'],default='fixture',
        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')
    # 사용자 입력 파싱
    args=parser.parse_args()
    # 실습 실행
    # - Level 3 기준 수행
    result=run(args.mode,3,args)
    # 결과 파일 저장
    # - exercise_07.json 생성
    path=save_result(Path(__file__).resolve().parent,'exercise_07.json',result)
    import json
    # 결과 출력
    # - JSON 형태 출력
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
    # 저장 위치 출력
    print('결과 저장:',path)

# 프로그램 시작점
# - 직접 실행 시 main() 호출
if __name__=='__main__':
    main()


"""
검색 결과에 대한 정성평가 케이스를 바탕으로 리뷰 데이터를 체계적으로 생성하고, 검색 상태의 분류 및 필터 적용 전후의 효과를 비교 검증하도록 구현하였다.
Fixture 및 Live 환경 모두에서 유연하게 동작하도록 설계하여 모의 시연과 실제 pgvector 검색 결과를 모두 지원하며, 
평가 데이터의 무결성 검증 기능을 포함하여 검색 품질 검토 프로세스의 신뢰성을 확보하였다.
"""