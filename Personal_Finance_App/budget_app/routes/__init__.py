from routes.main import main_bp
from routes.transaction import transaction_bp

__all__ = ['main_bp', 'transaction_bp']

"""
라우트(route) : 데이터 패킷이 출발지 -> 목적지 가지의 경로를 의미함, 어디로, 어느 경로로, 누구에게
라우터(router) : 네트워크에서 데이터 패킷이 목적지까지 올바르게 도달할 수 있도록 경로를 설정하고 관리하는 장치
라우팅(routing) : 데이터 패킷이 출발지에서 목적지까지 올바른 경로 중 최적의 경로를 선택하는 과정이나 알고리즘 그 자체

용어 정의
URL: 사용자가 접속하는 웹 주소
Route: URL과 해당 URL에 대한 요청을 처리하는 함수 간의 매핑 규칙
Blueprint: 플라스크에서 라우트와 관련된 기능들을 모듈화하여 관리하는 단위
함수: 특정 작업을 수행하는 코드 블록
"""