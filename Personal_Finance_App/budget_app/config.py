import os

# 프로젝트 루트 경로
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    기본 설정
    """

    # Flask 기본 설정
    """
    Flask에서 secret_key는 세션 관리, 쿠키 서명 등 보안 기능을 위해 필수적.
    Flask secret_key는 임의의 문자열(랜덤값)을 할당하여 설정함.
    Flask-Login 와 같은 확장 기능 사용 시 반드시 필요함.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # 데이터베이스 설정
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 페이지 당 항목 수 (페이지네이션)
    ITEMS_PER_PAGE = 20

    # 타임존 설정
    TIMEZONE = 'Asia/Seoul'

    # 디버그 모드 (개발 중에만 True)
    DEBUG = True

class DevelopmentConfig(Config):
    """
    개발 환경 설정
    """
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """
    운영(프로덕션) 환경 설정
    """
    DEBUG = False
    TESTING = False

class TestConfig(Config):
    """
    테스트 환경 설정
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' 
    """
    인메모리 데이터베이스 사용: 디스크 파일 대신 RAM(메모리)에 데이터베이스를 생성하고 작업을 수행하는 SQLite의 특수 연결 문자열
    """

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}