from datetime import datetime, timezone
from utils.db import db

class User(db.Model):
    """
    사용자 모델 (추후 활성화)
    """

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.now(timezone.utc), nullable = False)

    # 관계 설정
    """
    Claude는 relationship의 옵션을 backref로 제시했지만,
    back_populates로 바꿈

    back_ref의 경우, 관계를 한쪽에만 정의
    back_populates의 경우, 양쪽 모두에서 정의함

    back_populatesa는 양뱡향 관계를 정의해야해서 code를 더 치는 단점이 있지만
    가독성과 명시성에서 back_populates가 더 우수함 + 오류 가능성 감소

    relationship 참조: https://databoom.tistory.com/entry/FastAPI-SQLAlchemy-%EC%83%81%EC%84%B8-ForeignKey-relationship-6-5
    """
    transactions = db.relationship('Transaction', back_populates = 'user', lazy = 'select', cascade = 'all, delete-orphan')  # select - lazy loading, 객체에 처음 접근할 때, SELECT 쿼리 실행
    categories = db.relationship('Category', back_populates = 'user', lazy = 'select', cascade = 'all, delete-orphan')
    payment_methods = db.relationship('PaymentMethod', back_populates = 'user', lazy = 'select', cascade = 'all, delete-orphan')

    def __repr__(self):  # 객체의 "공식적인" 문자열 표현을 계산하기 위해 사용되는 메서드
        return f"<User {self.username}>"
    
    def to_dict(self):
        """
        dictionary로 변환 (JSON 응답용)
        """
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }