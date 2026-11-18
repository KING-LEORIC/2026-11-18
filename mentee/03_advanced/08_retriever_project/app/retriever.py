# Day23 / 실습 08 / 심화 retriever / mentee
# 모의 검색 기능 사용
# - fixture_search : 오프라인 벡터 검색 시뮬레이션
from day23kit.fixtures import fixture_search
# 임베딩 생성 및 질의 벡터 변환 기능 사용
# - get_encoder : 인코더 객체 생성
# - encode_question : 사용자 질문 임베딩 생성
from day23kit.embedding import get_encoder, encode_question
# 데이터베이스 연결 및 정확도 Top-K 검색, 데이터 준비 확인 기능 사용
# - connect_db : PostgreSQL 데이터베이스 연결 관리
# - exact_topk : 코사인 거리 기반 Exact Top-K 검색 수행
# - check_data_ready : 검색 대상 데이터 적재 상태 확인
from day23kit.db import connect_db, exact_topk, check_data_ready

"""AI Agent 아키텍처에서 질의에 부합하는 후보 문서를 검색하고, 데이터 구조 정제 및 실행 메타데이터 리포트를 생성하는 Retriever 모듈"""
# 후보 문서 검색 수행 함수
# - 모드에 따라 Fixture 모의 검색 또는 Live 환경의 E5 임베딩 및 pgvector Exact 검색 분기 처리
# - DB 연결 실패 시 예외를 상위로 그대로 전달하여 에러 상태 보존
# BEGIN D23-08-A02
def retrieve_candidates(question,mode,k,category,env_file):
    """
    TODO D23-08-A02 · retrieve_candidates
        fixture면 교육용 fixture_search, live면 E5 query Embedding → pgvector Exact SQL을 사용하세요.
        실제 live는 exercise05에서 9개 자료를 먼저 저장해야 합니다.
        DB 연결 실패를 빈 결과 []로 바꾸지 말고 예외를 전달하세요.
    """
    # TODO D23-08-A02: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # Fixture 모드 분기 처리
    # - 오프라인 모의 검색 함수 호출 결과 반환
    if mode == 'fixture': return fixture_search(question, k, category)
    # Live 모드 처리 (E5 임베딩 및 pgvector 활용)
    # - Live 인코더 생성 및 질문 임베딩 벡터 생성
    encoder = get_encoder('live')
    qvec = encode_question(encoder, question)
    # 데이터베이스 연결 및 검색 수행
    # - 환경 설정 파일 기반 연결 및 데이터 준비 상태 확인 후 Exact Top-K 검색 실행
    with connect_db(env_file) as conn:
        check_data_ready(conn)
        return exact_topk(conn, qvec, k, category)
    # raise NotImplementedError("D23-08-A02: 직접 구현하세요")
# END D23-08-A02

# BEGIN D23-08-A03
# 후보 문서 데이터 포맷팅 함수
# - 검색된 후보들의 고유 ID, 제목, 본문, 카테고리, 소스 버전, 거리를 일관된 딕셔너리 구조로 매핑
# - 원문 내용 요약이나 임의 변조 방지 및 거리 값의 수치 정밀도(소수점 6자리) 유지
def format_candidates(hits):
    """
    TODO D23-08-A03 · format_candidates
        후보의 id/title/content/category/source_version/distance를 반환하세요.
        검색된 원문을 요약·변조하지 않고, distance는 숫자 그대로 둡니다.
        답변 상태(answered)를 자동으로 부여하지 마세요.
    """
    # TODO D23-08-A03: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 검색된 후보 목록 순회 및 필수 필드 추출/포맷팅 수행
    return [{'id' : h['id'], 'title' : h['title'], 'content' : h['content'], 'category' : h['category'],
             'source_version' : h['source_version'], 'distance' : round(float(h['distance']), 6)} for h in hits]
    # raise NotImplementedError("D23-08-A03: 직접 구현하세요")
# END D23-08-A03

# BEGIN D23-08-A05
# 실행 리포트 생성 함수
# - 검색 결과 존재 여부에 따른 run_status(candidates/empty) 판정
# - 소스 모드 매핑, 소요 시간 기록, 검색된 문서 ID 목록 및 근거 승인 필드(human_evidence_ok=None) 구성
def make_run_report(question,hits,mode,elapsed_ms):
    """
    TODO D23-08-A05 · make_run_report
        run_status=candidates 또는 empty를 구분하세요.
        source_mode=(fixture:simulated, live:pgvector_exact), elapsed_ms,
        retrieved_ids, human_evidence_ok=None을 기록합니다.
        검색된 것만으로 답변 정확도·근거 승인 True를 만들지 마세요.
    """
    # TODO D23-08-A05: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 실행 리포트 딕셔너리 구성 및 반환
    return {'run_status' : 'candidates' if hits else 'empty',
            'source_mode' : 'simulated' if mode == 'fixture' else 'pgvector_exact',
            'retrieved_ids' : [h['id'] for h in hits],
            'elapsed_ms' : round(elapsed_ms,3),
            'human_evidence_ok' : None}
    # raise NotImplementedError("D23-08-A05: 직접 구현하세요")
# END D23-08-A05

"""
검색 엔진과 직접 상호작용하여 후보 문서를 유연하게 조회하고, 에러 상황을 안전하게 예외 전파 구조로 처리하도록 구현하였다.
또한 검색된 원문의 형태를 변조 없이 보존하여 포맷팅하고, 실행 소요 시간과 상태 메타데이터를 포함한 리포트를 체계적으로 생성함으로써 
AI Agent 환경에서 신뢰할 수 있는 Context 파이프라인의 기반을 완성하였다.
"""