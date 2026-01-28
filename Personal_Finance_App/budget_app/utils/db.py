from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy 객체 생성
db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    
    with app.app_context():
        # 모든 모델 import (모델 파일 생성 후 주석 해제)
        from models.user import User
        from models.transaction import Transaction
        from models.category import Category
        from models.payment_method import PaymentMethod

        db.create_all()  # 데이터베이스 테이블 생성
        print("✅ 데이터베이스 초기화 완료!")

def reset_db(app):
    """
    데이터베이스 초기화 (모든 데이터 삭제) - 개발 중에만 사용
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("⚠️  데이터베이스 리셋 완료! (모든 데이터 삭제됨)")