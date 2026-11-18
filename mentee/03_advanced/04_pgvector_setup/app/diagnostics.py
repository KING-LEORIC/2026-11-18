# Day23 / 실습 04 / 심화 diagnostics / mentee



# BEGIN D23-04-A04
# 확장 설치 상태 판별 함수
# - pgvector 제공 여부 확인
# - pgvector 설치 여부 확인
# - 설치 버전 정보 반환
def check_extension_row(row):
    """
    TODO D23-04-A04 · check_extension_row
        fetchone()으로 읽은 (name, default_version, installed_version) 행을 판정하세요.
        None이면 unavailable, installed_version이 None이면 available_not_installed,
        설치됐으면 installed 및 version을 반환합니다.
    """
    # TODO D23-04-A04: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 확장 정보 없음
    # - PostgreSQL 서버에 pgvector 제공 안 됨
    if row is None: return {'state' : 'unavailable', 'version' : None}
    # 확장 상태 반환
    # - installed : 설치 완료
    # - available_not_installed : 설치 가능하지만 미설치
    # - version : 설치된 버전 정보
    return {'state' : 'installed' if row[2] else 'available_not_installed', 'version' : row[2]}
    # raise NotImplementedError("D23-04-A04: 직접 구현하세요")
# END D23-04-A04

# BEGIN D23-04-A05
# pgvector 설치 오류 분류 함수
# - 설치 실패 위치 확인
# - 환경 문제 진단
# - 민감 정보 저장 방지
def classify_install_error(message):
    """
    TODO D23-04-A05 · classify_install_error
        대표 오류를 실패 위치(compile, server_files, db_permission,
        db_extension, python_env, other)로 분류하세요.
        키나 비밀번호가 들어 있는 예외 원문은 저장하지 않습니다.
    """
    # TODO D23-04-A05: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 오류 메시지 표준화
    # - 대소문자 구분 제거
    msg = message.lower()
    # 컴파일 단계 오류
    # - 빌드 도구 누락
    # - PostgreSQL 헤더 파일 누락
    if 'nmake' in msg or 'postgres.h' in msg: return 'compile'
    # 서버 파일 배치 오류
    # - vector.control 파일 누락
    if 'vector.control' in msg: return 'server_files'
    # 데이터베이스 권한 오류
    # - Superuser 권한 부족
    # - 서버 파일 접근 권한 부족
    if 'permission denied' in msg or 'must be superuser' in msg: return 'db_permission'
    # 확장 활성화 오류
    # - CREATE EXTENSION 이전 상태
    if 'type "vector" does not exist' in msg: return 'db_extension'
    # Python 환경 오류
    # - 라이브러리 미설치
    if 'no module named' in msg: return 'python_env'
    # 기타 오류
    return 'other'
    # raise NotImplementedError("D23-04-A05: 직접 구현하세요")
# END D23-04-A05

# BEGIN D23-04-A06
# 설치 절차 점검 함수
# - 필수 설치 단계 확인
# - 누락 단계 반환
# - 환경 구성 상태 점검
def audit_install_steps(steps):
    """
    TODO D23-04-A06 · audit_install_steps
        빌드 도구·PGROOT·서버 파일·DB 활성화·Python 등록 5단계를 판정하세요.
        입력: {단계명: bool}. 누락된 단계를 리스트로 반환합니다.
        HTML의 순서를 유지하고 미확인을 성공 처리하지 마세요.
    """
    # TODO D23-04-A06: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 설치 점검 순서
    # - build_tools : 컴파일 도구 준비
    # - pgroot : PostgreSQL 설치 경로 설정
    # - server_files : pgvector 서버 파일 복사
    # - db_extension : CREATE EXTENSION 수행
    # - python_adapter : Python 연동 라이브러리 설치
    order = ['build_tools', 'pgroot', 'server_files', 'db_extension', 'python_adapter']
    # 누락 단계 반환
    # - False 또는 미확인 단계 포함
    return [name for name in order if steps.get(name) is not True]
    # raise NotImplementedError("D23-04-A06: 직접 구현하세요")
# END D23-04-A06

"""
pgvector 설치 상태를 점검하기 위해 구현하였다.
확장 제공 여부와 설치 상태를 확인하고, 설치 과정에서 발생하는 오류를 단계별로 분류하여 문제 원인을 빠르게 파악할 수 있도록 구성하였다.
또한 필수 설치 절차를 점검하여 PostgreSQL과 Python 연동 환경이 정상적으로 준비되었는지 확인할 수 있도록 구현하였다.
"""
