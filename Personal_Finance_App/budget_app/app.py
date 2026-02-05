from flask import Flask
from config import config
from utils.db import db, init_db

def create_app(config_name = 'development'):
    """
    Flask 애플리케이션 팩토리
    """

    app = Flask(__name__)

    # 설정 로드
    app.config.from_object(config[config_name])

    # 데이터베이스 초기화
    db.init_app(app)

    # 블루프린트 등록
    from routes import main_bp, transaction_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(transaction_bp)

    # 첫 실행 시, 데이터베이스 및 기본 데이터 생성
    with app.app_context():
        from models import User, Category, PaymentMethod, Transaction

        # 테이블 생성
        db.create_all()

        # 기본 사용자 생성(Phase 1)
        if User.query.count() == 0:
            default_user = User(
                username = '박마토',
                email = 'dark1432@naver.com',
                password_hash = 'temporary'  # Phase 5에서 암호화 적용
            )
            db.session.add(default_user)
            db.session.commit()
            print("✅ 기본 사용자 생성 완료!")

        # 기본 카테고리 생성
        if Category.query.count() == 0:
            for cat_data in Category.get_default_categorires():
                category = Category(**cat_data, user_id = 1)
                db.session.add(category)
            db.session.commit()
            print("✅ 기본 카테고리 생성 완료!")

        # 기본 결제수단 생성
        if PaymentMethod.query.count() == 0:
            for pm_data in PaymentMethod.get_default_payment_method():
                payment_method = PaymentMethod(**pm_data, user_id = 1)
                db.session.add(payment_method)
            db.session.commit()
            print("✅ 기본 결제수단 생성 완료!")
    
    # 기본 라우트 (테스트용)
    # @app.route('/')
    # def index():
    #     return """
    #     <h1>🎉 박마토의 가계부 만들기</h1>
    #     <p>환경 설정이 완료되었습니다!</p>
    #     <ul>
    #         <li>Flask 애플리케이션 실행 중 ✅</li>
    #         <li>데이터베이스 연결 완료 ✅</li>
    #         <li>기본 데이터 생성 완료 ✅</li>
    #     </ul>
    #     <p><strong>다음 단계:</strong> Phase 2 - CRUD 기능 구현</p>
    #     """
    
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug = True, host = '0.0.0.0', port = 5001)