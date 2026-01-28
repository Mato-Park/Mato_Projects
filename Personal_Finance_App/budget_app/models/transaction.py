from datetime import datetime, timezone
from utils.db import db

class Transaction(db.Model):
    """
    거래 내역 모델
    """

    __tablename__ = 'transactions'

    transaction_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False, default = 1)
    date = db.Column(db.Date, nullable = False, default = datetime.now(timezone.utc).date())
    description = db.Column(db.String(255), nullable = False)  # 거래 내용
    transaction_type = db.Column(db.String(10), nullable = False)  # 'income' or 'expense'
    amount = db.Column(db.Integer, nullable = False)  # 거래 금액
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable = False)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.payment_method_id'), nullable = False)
    is_fixed = db.Column(db.Boolean, default = False, nullable = False)  # 고정 지출 여부
    memo = db.Column(db.Text)  # 메모
    created_at = db.Column(db.DateTime, default = datetime.now(timezone.utc), nullable = False)
    updated_at = db.Column(db.DateTime, default = datetime.now(timezone.utc), onupdate = datetime.now(timezone.utc))

    # 관계 설정
    user = db.relationship('User', back_populates = 'transactions', lazy = 'joined')
    category = db.relationship('Category', back_populates = 'transactions', lazy = 'joined')
    payment_method = db.relationship('PaymentMethod', back_populates = 'transactions', lazy = 'joined')


    def __repr__(self):
        return f'<Transaction - {self.description} ({self.transaction_type}): {self.amount}원>'
    
    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'user_id': self.user_id,
            'date': self.date.isoformat(),
            'description': self.description,
            'transaction_type': self.transaction_type,
            'amount': self.amount,
            'category': {
                'category_id': self.category.category_id,
                'name': self.category.name,
                'color': self.category.color
            } if self.category else None,
            'payment_method': {
                'payment_method_id': self.payment_method.payment_method_id,
                'name': self.payment_method.name,
                'payment_type': self.payment_method.payment_method_type
            } if self.payment_method else None,
            'is_fixed': self.is_fixed,
            'memo': self.memo,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @property
    def formatted_amount(self):
        # 금액 포맷팅 (천 단위 콤마 추가)
        return f"{self.amount:,}원"
    
    @property
    def display_type(self):
        return '수입' if self.transaction_type == 'income' else '지출'