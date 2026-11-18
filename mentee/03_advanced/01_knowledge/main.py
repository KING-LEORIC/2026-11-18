"""Day23 실습 01 · 검색 대상과 ID (심화, mentee).

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
# 파일 경로 관리 기능 사용
# - Path : 운영체제 독립적인 경로 처리
from pathlib import Path
# 공용 모듈 경로 추가
# - common 디렉터리 라이브러리 사용 가능
sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'common'))
# 실습 데이터 로드 기능 사용
# - load_knowledge : 지식 데이터 조회
from day23kit.data import load_knowledge
# 결과 저장 기능 사용
# - save_result : JSON 결과 파일 저장
from day23kit.io import save_result

# 지식 데이터 가공 기능 사용
# - select_original : 원본 데이터 선별
# - make_passage_input : Passage 생성
# - make_mapping : ID 매핑 생성
from app.knowledge import select_original, make_passage_input, make_mapping
# 데이터 검증 기능 사용
# - reject_duplicate_ids : 중복 ID 제거
# - reject_missing_fields : 필수값 검증
# - audit_versions : 버전 정보 점검
from app.validation import reject_duplicate_ids, reject_missing_fields, audit_versions

"""검색 대상 데이터 선정 및 ID 관리 실습을 수행하는 메인 모듈"""

# 실습 실행 함수
# - 실습 데이터 가공
# - 검증 결과 생성
# - 결과 데이터 반환
def run(mode,level,args):
    # 지식 데이터 로드
    rows=load_knowledge()
    # 원본 데이터 선별
    # - 검색 대상이 되는 데이터 추출
    selected=select_original(rows)
    # Passage 입력 생성
    # - 검색 모델 입력 예시 생성
    passage=make_passage_input(selected[1])
    # ID 매핑 생성
    # - level 1 : 원본 데이터 기준
    # - level 2 이상 : 전체 데이터 기준
    mapping=make_mapping(selected if level==1 else rows)
    # 결과 데이터 구성
    # - 실습 정보 및 매핑 결과 저장
    result=dict(exercise=1,level=level,source_mode='local_snapshot',
                selected_ids=[r['id'] for r in selected],example_passage=passage,
                total_mapped=len(mapping),mapping=mapping)
    # 심화 검증 수행
    # - 중복 ID 제거 결과 확인
    # - 필수값 누락 여부 확인
    if level>=2:
        result['unique_ids']=len(reject_duplicate_ids(rows))
        result['all_fields_valid']=reject_missing_fields(rows)
    # 버전 관리 검증 수행
    # - 버전 변경 이력 점검
    if level>=3:
        result['versions']=audit_versions(rows)
    return result

# 프로그램 진입 함수
# - 실행 옵션 처리
# - 실습 결과 저장
# - 결과 출력
def main():
    # 명령행 인자 파서 생성
    # - 프로그램 설명 등록
    parser=argparse.ArgumentParser(description='Day23 실습 01 · 검색 대상과 ID')
    # 실행 모드 옵션 등록
    # - fixture : 모의 데이터 사용
    # - live : 실제 E5 및 DB 사용
    parser.add_argument('--mode',choices=['fixture','live'],default='fixture',
        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')
    # 사용자 입력 파싱
    args=parser.parse_args()
    # 실습 실행
    # - level 3 기준 수행
    result=run(args.mode,3,args)
    # 결과 파일 저장
    # - exercise_01.json 생성
    path=save_result(Path(__file__).resolve().parent,'exercise_01.json',result)
    import json
    # 결과 콘솔 출력
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
    # 저장 위치 출력
    print('결과 저장:',path)

if __name__=='__main__':
    main()

"""
지식 데이터에서 검색 대상이 되는 원본 데이터를 선별하고, 검색에 사용할 Passage 및 ID 매핑 정보를 생성하도록 구현하였다.
또한 데이터 품질 검증과 버전 점검을 수행하여 검색 시스템에서 활용 가능한 데이터 상태를 확인할 수 있도록 구성하였다.
"""
