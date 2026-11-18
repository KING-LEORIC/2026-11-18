"""Day23 실습 04 · 서버 확장과 Python 연결 (심화, mentee).

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
# PostgreSQL 연결 기능 사용
# - connect_db : DB 연결 생성
from day23kit.db import connect_db
# 결과 저장 기능 사용
# - save_result : JSON 결과 파일 저장
from day23kit.io import save_result

# SQL 점검 기능 사용
# - sql_server_info : PostgreSQL 서버 정보 조회 SQL
# - sql_extension_state : 확장(extension) 상태 확인 SQL
# - sql_distance_probe : 벡터 거리 연산 확인 SQL
from app.sql_checks import sql_server_info, sql_extension_state, sql_distance_probe
# 설치 진단 기능 사용
# - check_extension_row : 확장 정보 정리
# - classify_install_error : 설치 오류 분류
# - audit_install_steps : 설치 절차 점검
from app.diagnostics import check_extension_row, classify_install_error, audit_install_steps

"""pgvector 확장 상태와 PostgreSQL 연동 상태를 점검하는 실습 모듈"""


# 실습 실행 함수
# - SQL 점검문 생성
# - 확장 상태 진단
# - PostgreSQL 연결 확인
def run(mode,level,args):
    # SQL 점검문 생성
    # - server : PostgreSQL 서버 정보 조회
    # - extension : pgvector 설치 상태 조회
    # - distance : 벡터 거리 연산 확인
    sqls={'server':sql_server_info(),'extension':sql_extension_state(),'distance':sql_distance_probe()}
    # 기본 결과 생성
    # - fixture : 실제 DB 연결 수행 안 함
    # - live : pgvector 환경 점검 수행
    result=dict(exercise=4,level=level,source_mode='not_run' if mode=='fixture' else 'pgvector_live',
                sql_for_pgadmin=sqls,db_check='not_run')
    # 확장 상태 및 오류 진단 수행
    # - 예시 데이터 기준 동작 확인
    if level>=2:
        result['illustrated_extension_state']=check_extension_row(('vector','0.8.7',None))
        result['example_error_stage']=classify_install_error('postgres.h not found')
    # 설치 절차 점검 수행
    # - 누락된 단계 확인
    if level>=3:
        result['manual_pending']=audit_install_steps({})
    # 실제 PostgreSQL 연결 수행
    # - fixture 모드에서는 실행하지 않음
    if mode=='live':
        # live만 실제 DB 연결. Windows 빌드 및 CREATE EXTENSION은 사전 수동 절차.
        # live만 실제 DB 연결
        # - Windows 빌드 및 CREATE EXTENSION은 사전 수동 절차
        with connect_db(Path(__file__).with_name('.env')) as conn:
            # PostgreSQL 버전 조회
            ver=conn.execute('SELECT version()').fetchone()[0]
            # 현재 데이터베이스명 조회
            dbname=conn.execute('SELECT current_database()').fetchone()[0]
            # pgvector 확장 상태 조회
            ext=conn.execute("SELECT name, default_version, installed_version FROM pg_available_extensions WHERE name='vector'").fetchone()
            # DB 점검 결과 생성
            # - 서버 버전
            # - 데이터베이스명
            # - 확장 상태
            result['db_check']={'server_version':ver,'database':dbname,'extension':check_extension_row(ext)} if level>=2 else {'server_version':ver,'database':dbname,'extension_provided':ext is not None}
            # pgvector 활성화 상태 확인
            # - installed_version 존재 시 거리 연산 수행
            if ext is not None and ext[2]:
                # 벡터 거리 연산 테스트
                # - pgvector 동작 여부 확인
                result['db_check']['distance_probe']=float(conn.execute(sql_distance_probe()).fetchone()[0])
            else:
                # 확장이 활성화되지 않은 경우
                # - 거리 연산 수행 불가
                result['db_check']['distance_probe']='not_run_extension_not_activated'
    return result

# 프로그램 진입 함수
# - 실행 옵션 처리
# - 실습 수행
# - 결과 저장 및 출력
def main():
    # 명령행 인자 파서 생성
    # - 프로그램 설명 등록
    parser=argparse.ArgumentParser(description='Day23 실습 04 · 서버 확장과 Python 연결')
    # 실행 모드 옵션 등록
    # - fixture : 모의 점검 환경
    # - live : 실제 PostgreSQL 환경
    parser.add_argument('--mode',choices=['fixture','live'],default='fixture',
        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')
    # 사용자 입력 파싱
    args=parser.parse_args()
    # 실습 실행
    # - level 3 기준 수행
    result=run(args.mode,3,args)
    # 결과 파일 저장
    # - exercise_04.json 생성
    path=save_result(Path(__file__).resolve().parent,'exercise_04.json',result)
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
PostgreSQL의 pgvector 확장 설치 상태와 Python 연동 상태를 점검하도록 구현하였다.
SQL 점검문을 생성하여 서버 정보, 확장 상태, 벡터 거리 연산 가능 여부를 PostgreSQL 연결을 통해 pgvector 활성화 여부를 검증할 수 있도록 구성하였다.
또한 설치 오류 분류 및 설치 절차 점검 기능을 통해 pgvector 환경 구축 과정을 진단할 수 있도록 구현하였다.
"""

# Extension(확장) : PostgreSQL 기본 기능에 추가 기능을 제공하는 모듈
# pgvector : 벡터 저장 및 유사도 검색 기능 제공
# distance_probe : 벡터 거리 계산이 실제로 동작하는지 시험하는 검증용 쿼리
# live 모드 : 실제 PostgreSQL 서버 연결
# fixture 모드 : 모의 데이터 기반 테스트