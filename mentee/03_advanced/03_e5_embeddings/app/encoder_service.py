# Day23 / 실습 03 / 심화 encoder_service / mentee
# 수치 연산 라이브러리 사용
# - numpy : 벡터 배열 처리
import numpy as np
# E5 모델 정보 사용
# - E5_MODEL_ID : E5 모델 식별자
from day23kit.data import E5_MODEL_ID
# 임베딩 검증 기능 사용
# - get_model_revision : 모델 리비전 조회
# - validate_vectors : 벡터 형상 및 유효성 검증
from day23kit.embedding import get_model_revision, validate_vectors


# BEGIN D23-03-A03
# 문서 및 질문 임베딩 생성 함수
# - Passage 임베딩 생성
# - Query 임베딩 생성
# - 동일 Encoder 사용
def encode_both(encoder,passages,queries):
    """
    TODO D23-03-A03 · encode_both
        같은 Encoder에 문서와 질문을 나누어 encode하세요.
        반드시 normalize_embeddings=True, convert_to_numpy=True를 전달합니다.
        결과: (doc_vectors, query_vectors). 기본필수의 모의 모드와
        --mode live의 E5 실측을 구분하여 같은 API를 사용합니다.
    """
    # TODO D23-03-A03: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 문서 임베딩 생성
    # - normalize_embeddings=True : 정규화 수행
    # - convert_to_numpy=True : NumPy 배열 반환
    # - batch_size=8 : 배치 단위 처리
    docs = encoder.encode(passages, normalize_embeddings = True, convert_to_numpy = True, batch_size = 8)
    # 질문 임베딩 생성
    # - normalize_embeddings=True : 정규화 수행
    # - convert_to_numpy=True : NumPy 배열 반환
    queries_vec = encoder.encode(queries, normalize_embeddings = True, convert_to_numpy = True)
    # 벡터 타입 통일
    # - float32 배열로 변환
    return np.asarray(docs, dtype = np.float32), np.asarray(queries_vec, dtype = np.float32)
    # raise NotImplementedError("D23-03-A03: 직접 구현하세요")
# END D23-03-A03

# BEGIN D23-03-A04
# 원문과 벡터 정렬 검증 함수
# - ID와 벡터 행 순서 확인
# - 검색 결과 추적 보장
def verify_alignment(rows,vectors):
    """
    TODO D23-03-A04 · verify_alignment
        지식 행 수와 벡터 행 수가 같은지 확인하고 [(ID,행번호),...]를 반환하세요.
        ID가 중복되어 있거나 행 수가 다르면 ValueError.
        예: 지식 102는 vectors[1]과 짝입니다.
    """
    # TODO D23-03-A04: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 전체 ID 추출
    ids = [r['id'] for r in rows]
    # 정렬 상태 검증
    # - ID 중복 금지
    # - 데이터 수와 벡터 수 일치 필요
    if len(ids) != len(set(ids)) or len(rows) != len(vectors): raise ValueError('id_vector_alignment')
    # ID-벡터 행번호 매핑 생성
    # - 원문과 벡터 연결 정보 유지
    return [(r['id'], i) for i, r in enumerate(rows)]
    # raise NotImplementedError("D23-03-A04: 직접 구현하세요")
# END D23-03-A04

# BEGIN D23-03-A05
# 벡터 형상 검증 함수
# - 문서 벡터 형태 검증
# - 질문 벡터 형태 검증
def check_shapes_vectors(docs,queries,doc_count):
    """
    TODO D23-03-A05 · check_shapes_vectors
        문서 벡터 shape=(doc_count,384), 질문 shape=(1,384)를 검사하세요.
        두 배열 모두 유한하고 길이가 1인지 검증합니다.
        정상일 때 True, 오류일 때 ValueError.
    """
    # TODO D23-03-A05: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 문서 벡터 검증
    # - shape=(doc_count,384)
    validate_vectors(docs, doc_count)
    # 질문 벡터 검증
    # - shape=(1,384)
    validate_vectors(queries, 1)
    # 검증 성공
    return True
    # raise NotImplementedError("D23-03-A05: 직접 구현하세요")
# END D23-03-A05

# BEGIN D23-03-A06
# 모델 정보 기록 함수
# - 사용 모델 정보 저장
# - 임베딩 생성 계약 추적
def make_model_stamp(encoder,mode):
    """
    TODO D23-03-A06 · make_model_stamp
        모델 ID·revision·접두어·차원·정규화를 JSON 직렬화 가능한 dict로 기록하세요.
        모의 벡터이면 model_id에 SIMULATED를 분명히 표시합니다.
        실제 revision을 알 수 없으면 'unverified'로 두며 임의 해시를 만들지 않습니다.
    """
    # TODO D23-03-A06: 위 입력·출력 계약에 맞게 직접 구현합니다.

    # 모델 ID 결정
    # - live : 실제 E5 모델 사용
    # - fixture : 모의 모델 사용
    model_id = E5_MODEL_ID if mode == 'live' else encoder.model_id
    # 모델 메타데이터 생성
    # - model_id : 모델 식별자
    # - revision : 모델 버전 정보
    # - dimension : 임베딩 차원 수
    # - query_prefix : Query 접두어
    # - document_prefix : Passage 접두어
    # - normalize_embeddings : 정규화 여부
    return {'model_id' : model_id, 'revision' : get_model_revision(encoder),
            'dimension' : 384, 'query_prefix' : 'query: ',
            'document_prefix' : 'passage: ', 'normalize_embeddings' : True,
            'source_mode' : 'e5_live' if mode == 'live' else 'simulated'}
    # raise NotImplementedError("D23-03-A06: 직접 구현하세요")
# END D23-03-A06

"""
E5 Encoder를 사용하여 문서와 질문 임베딩을 생성하도록 구현하였다.
또한 원문 데이터와 벡터의 정렬 상태를 검증하고, 벡터 형상(shape)과 모델 정보를 기록하여
임베딩 생성 과정을 추적할 수 있도록 구성하였다.
Embedding 생성 이후에도 원문 ID, 모델 버전, 입력 형식을 확인할 수 있도록 구현하였다.
"""