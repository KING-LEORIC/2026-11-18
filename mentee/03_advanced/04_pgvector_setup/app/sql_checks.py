# Day23 / 실습 04 / 심화 sql_checks / mentee
# 벡터 거리 계산 기능 사용
# - cosine_distance : 코사인 거리 계산 개념 참고
from day23kit.mathops import cosine_distance

"""PostgreSQL 및 pgvector 상태 확인용 SQL을 생성하는 모듈"""

# BEGIN D23-04-A01
# PostgreSQL 서버 정보 조회 SQL 생성 함수
# - 서버 버전 조회
# - 현재 데이터베이스 조회
def sql_server_info():
    """
    TODO D23-04-A01 · sql_server_info
        pgAdmin에서 실행할 서버 버전·현재 DB 조회 SQL을 작성하세요.
        반드시 SELECT version()과 current_database()를 포함하세요.
        DB 변경이나 DROP/CREATE DATABASE는 하지 않습니다.
    """
    # TODO D23-04-A01: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 서버 정보 조회 SQL
    # - version() : PostgreSQL 버전 정보
    # - current_database() : 현재 접속 DB
    # - current_user : 현재 로그인 사용자
    return 'SELECT version(); SELECT current_database(), current_user;'
    # raise NotImplementedError("D23-04-A01: 직접 구현하세요")
# END D23-04-A01

# BEGIN D23-04-A02
# pgvector 확장 상태 조회 SQL 생성 함수
# - 확장 제공 여부 확인
# - 설치 여부 확인
def sql_extension_state():
    """
    TODO D23-04-A02 · sql_extension_state
        vector 확장의 제공 여부와 설치 여부를 확인하는 SQL 문자열을 작성하세요.
        pg_available_extensions, installed_version, WHERE name='vector' 사용.
    """
    # TODO D23-04-A02: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 확장 상태 조회 SQL
    # - default_version : 제공 버전
    # - installed_version : 설치 버전
    # - name='vector' : pgvector 확장만 조회
    return "SELECT name, default_version, installed_version FROM pg_available_extensions WHERE name = 'vector';"
    # raise NotImplementedError("D23-04-A02: 직접 구현하세요")
# END D23-04-A02

# BEGIN D23-04-A03
# 벡터 거리 연산 테스트 SQL 생성 함수
# - pgvector 정상 동작 여부 확인
# - 코사인 거리 계산 테스트
def sql_distance_probe():
    """
    TODO D23-04-A03 · sql_distance_probe
        SQL에서 3차원 벡터 [1,0,0]과 [0,1,0]의 Cosine distance를 계산하세요.
        문자열 반환. CAST는 ::vector, 연산자는 <=>를 사용합니다.
        예상값 1.0이며 384차원 E5 출력이 아닙니다.
    """
    # TODO D23-04-A03: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 벡터 거리 계산 SQL
    # - ::vector : pgvector 타입 변환
    # - <=> : Cosine Distance 연산자
    # - 직교 벡터이므로 결과는 1.0
    return "SELECT '[1, 0, 0]'::vector <=> '[0, 1, 0]'::vector AS cosine_distance;"
    # raise NotImplementedError("D23-04-A03: 직접 구현하세요")
# END D23-04-A03

"""
PostgreSQL 서버 상태와 pgvector 확장 상태를 점검하기 위한 SQL 생성 기능을 구현하였다.
서버 버전, 데이터베이스 정보, 확장 설치 여부를 확인할 수 있도록 구성하였으며,
pgvector의 벡터 거리 연산이 정상적으로 동작하는지 검증할 수 있도록 테스트 SQL을 제공한다.
"""