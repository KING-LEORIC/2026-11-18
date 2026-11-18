"""Day23 실습 08 · AI Agent용 Retriever (심화, mentee).

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
# 실행 시간 측정 기능 사용
# - perf_counter : 고정밀 성능 측정
from time import perf_counter
# 결과 저장 기능 사용
# - save_result : JSON 결과 파일 저장
from day23kit.io import save_result

# 입력 검증 및 모델 무결성 검사 기능 사용
# - validate_question : 질문 유효성 검사
# - validate_options : 검색 옵션 검사
# - check_model_and_versions : 모델 및 버전 무결성 검증
from app.validation import validate_question, validate_options, check_model_and_versions
# 검색 후보 조회, 포맷팅 및 실행 리포트 생성 기능 사용
# - retrieve_candidates : 후보 검색 수행
# - format_candidates : 후보 데이터 포맷팅
# - make_run_report : 실행 결과 리포트 작성
from app.retriever import retrieve_candidates, format_candidates, make_run_report

"""AI Agent 환경에서 활용할 수 있는 Retriever 모듈을 구동하고, 검색 후보 조회부터 실행 시간 측정 및 계약 검증까지 수행하는 메인 실습 모듈"""

# 실습 실행 함수
# - 질문 유효성 검증 및 레벨별 옵션 설정
# - 후보 문서 검색 수행 및 실행 소요 시간 측정
# - 검색 결과 포맷팅 및 레벨별 리포트/계약 검증 추가
def run(mode,level,args):
    # 질문 검증 수행
    # - 인자로 전달된 질문 또는 기본 질문 유효성 검사
    question=validate_question(getattr(args,'question','서버는 어디에서 실행하나요?'))
    # 레벨에 따른 검색 개수(k) 및 카테고리 설정
    # - Level 1인 경우 기본값 k=3, 카테고리 None 적용
    k=3 if level==1 else args.k
    category=None if level==1 else args.category
    # 검색 옵션 유효성 검증 수행
    # - 레벨 2 이상인 경우 엄격한 옵션 검증 적용, 미만인 경우 기본 딕셔너리 구성
    if level>=2:options=validate_options(k,category)
    else:options={'k':k,'category':category}
    # 검색 실행 시간 측정 시작
    # - 고정밀 성능 측정 카운터 초기화
    t0=perf_counter()
    # 후보 문서 검색 수행
    # - 질문, 모드, k 개수, 카테고리 필터 및 환경 설정 파일 경로 전달
    hits=retrieve_candidates(question,mode,options['k'],options['category'],Path(__file__).with_name('.env'))
    # 검색 실행 소요 시간 산출 (밀리초 단위 변환)
    elapsed=(perf_counter()-t0)*1000
    # 검색된 후보 결과 포맷팅 수행
    formatted=format_candidates(hits)
    # 기본 실습 결과 딕셔너리 생성
    # - 실습 정보, 소스 모드, 질문, 옵션, 검색 결과 및 다음 단계 안내 포함
    result=dict(exercise=8,level=level,source_mode='simulated' if mode=='fixture' else 'pgvector_exact',question=question,options=options,
                retrieved=formatted,retrieved_count=len(formatted),human_evidence_ok=None,
                next_step='검토 후 Context 후보로 전달; LLM 답변 생성은 Day25 RAG에서 수행')
    # 레벨 2 이상 추가 분석 수행
    # - 실행 결과 리포트 생성 및 추가
    if level>=2:result['run_report']=make_run_report(question,hits,mode,elapsed)
    # 레벨 3 추가 검증 수행
    # - 모델 및 버전 무결성 계약 검증 결과 추가
    if level>=3:result['contract_check']=check_model_and_versions(hits,mode)
    # 최종 결과 딕셔너리 반환
    return result

# 프로그램 진입 함수
# - 명령행 인자 파싱 및 실행 모드 설정
# - 예외 처리를 통한 라이브 모드 에러 로깅 및 결과 파일 저장
# - 콘솔 결과 출력
def main():
    # 명령행 인자 파서 생성
    # - 프로그램 설명 등록
    parser=argparse.ArgumentParser(description='Day23 실습 08 · AI Agent용 Retriever')
    # 실행 모드 옵션 등록
    # - fixture : 모의 검색 환경
    # - live : 실제 pgvector 환경
    parser.add_argument('--mode',choices=['fixture','live'],default='fixture',
        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')

    # 검색 질문 및 옵션 인자 등록
    parser.add_argument('--question',default='서버는 어디에서 실행하나요?',help='검색 질문')
    parser.add_argument('--k',type=int,default=3,help='반환할 최대 검색 후보 (1~9)')
    parser.add_argument('--category',default=None,choices=['course','development','support'],help='Metadata 분류 필터')
    # 사용자 명령행 인자 파싱
    args=parser.parse_args()
    try:
        # 실습 실행
        # - Level 3 기준 수행
        result=run(args.mode,3,args)
    except NotImplementedError:
        # TODO가 미완성이면 교육용 오류를 그대로 보여줍니다.
        raise
    except Exception as exc:
        # live DB/모델 연결 실패는 빈 결과가 아니라 error로 기록합니다.
        # 환경변수·DB 비밀번호가 들어 있을 수 있으므로 오류 이름만 파일에 남깁니다.
        # 라이브 DB 및 모델 연결 실패 시 예외 처리
        # - 라이브 모드인 경우 에러 상태를 별도의 실패 JSON 파일로 저장 후 종료
        if args.mode=='live':
            failure={'exercise':8,'level':3,'source_mode':'pgvector_live',
                     'run_status':'error','error_type':type(exc).__name__,
                     'human_evidence_ok':None}
            save_result(Path(__file__).resolve().parent,'exercise_08.json',failure)
            print('실행 실패:',type(exc).__name__,file=sys.stderr)
            raise SystemExit(1) from None
        raise
    # 성공 결과 파일 저장
    # - exercise_08.json 생성
    path=save_result(Path(__file__).resolve().parent,'exercise_08.json',result)
    import json
    # 결과 출력
    # - JSON 형태 출력 (들여쓰기 및 한글 깨짐 방지 적용)
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
    # 저장 완료 경로 출력
    print('결과 저장:',path)

# 프로그램 시작점
# - 직접 실행 시 main() 호출
if __name__=='__main__':
    main()

"""
AI Agent 아키텍처에서 LLM의 Context 제공을 담당하는 Retriever 모듈의 메인 실행 스크립트이다.
명령행 인자(모드, 질문, k개수, 카테고리)를 유연하게 처리하며, Fixture 모의 환경과 Live pgvector 환경을 모두 지원하도록 설계되었다.
실행 소요 시간 측정, 검색 결과 포맷팅, 레벨별 실행 리포트 생성 및 계약 무결성 검증을 체계적으로 통합하였으며, 
라이브 모드 실행 시 발생할 수 있는 데이터베이스 및 모델 연결 예외를 안전하게 가로채어 에러 상태 리포트로 기록하는 견고한 예외 처리 구조를 완성하였다.
"""