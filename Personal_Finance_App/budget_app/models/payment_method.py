from datetime import datetime, timezone
from utils.db import db

class PaymentMethod(db.Model):
    """
    결제 수단 모델
    """

    __tablename__ = 'payment_methods'

    payment_method_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False, default = 1)
    name = db.Column(db.String(50), nullable = False)
    payment_method_type = db.Column(db.String(20), nullable = False)  # 'cash', 'credit_card', 'debit_card', 'bank_transfer', 'other
    created_at = db.Column(db.DateTime, default = datetime.now(timezone.utc), nullable = False)

    # 관계 설정
    user = db.relationship('User', back_populates = 'payment_methods', lazy = 'joined')
    transactions = db.relationship('Transaction', back_populates = 'payment_method', lazy = 'select', cascade = 'save-update')

    def __repr__(self):
        return f'<PaymentMethod - {self.name} ({self.payment_method_type})>'
    
    def to_dict(self):
        return {
            'payment_method_id': self.payment_method_id,
            'user_id': self.user_id,
            'name': self.name,
            'payment_method_type': self.payment_method_type,
            'created_at': self.created_at.isoformat()
        }
    
    @staticmethod
    def get_default_payment_method():
        """
        기본 결제 수단 목록
        """

        return [
            {'name': '현금', 'payment_method_type': 'cash'},
            {'name': '신용카드', 'payment_method_type': 'credit_card'},
            {'name': '체크카드', 'payment_method_type': 'debit_card'},
            {'name': '계좌이체', 'payment_method_type': 'bank_transfer'},
            {'name': '기타', 'payment_method_type': 'other'}
        ]
