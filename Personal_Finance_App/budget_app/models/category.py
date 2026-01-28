from datetime import datetime, timezone
from utils.db import db

class Category(db.Model):
    """
    카테고리 모델
    """

    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False, default = 1)
    name = db.Column(db.String(50), nullable = False)
    category_type = db.Column(db.String(10), nullable = False)  # 'income' or 'expense'
    color = db.Column(db.String(7), default = '#6366f1') # 차트 색상 hex code
    is_active = db.Column(db.Boolean, default = True, nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.now(timezone.utc), nullable = False)

    # 관계 설정
    user = db.relationship('User', back_populates = 'categories', lazy = 'joined')
    transactions = db.relationship('Transaction', back_populates = 'category', lazy = 'select', cascade = 'save-update')

    def __repr__(self):
        return f'<Category - {self.name}'
    
    def to_dict(self):
        return {
            'category_id': self.category_id,
            'user_id': self.user_id,
            'name': self.name,
            'category_type': self.category_type,
            'color': self.color,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }
    
    @staticmethod
    def get_default_categorires():
        """
        기본 카테고리 목록
        """
        return [
            # 자출 카테고리
            {'name': '식비', 'category_type': 'expense', 'color': '#ef4444'},
            {'name': '카페&간식', 'category_type': 'expense', 'color': '#f59e0b'},
            {'name': '편의점&마트&잡화', 'category_type': 'expense', 'color' : '#ec4899'},
            {'name': '교통비', 'category_type': 'expense', 'color': '#8b5cf6'},
            {'name': '술&유흥', 'category_type': 'expense', 'color': '#10b981'},
            {'name': '쇼핑', 'category_type': 'expense', 'color': '#06b6d4'},
            {'name': '취미&문화', 'category_type': 'expense', 'color': "#01011f"},
            {'name': '뷰티&미용', 'category_type': 'expense', 'color': '#14b8a6'},
            {'name': '경조사', 'category_type': 'expense', 'color': '#f97316'},
            {'name': '교육&자기계발', 'category_type': 'expense', 'color': '#64748b'},
            {'name': '주거&통신&생활', 'category_type': 'expense', 'color': '#22c55e'},
            {'name': '보험&세금', 'category_type': 'expense', 'color': "#c0cc16"},
            {'name': '의료&건강', 'category_type': 'expense', 'color': '#a3e635'},
            {'name': '구독', 'category_type': 'expense', 'color': "#4ad2de"},
            {'name': '저축&투자', 'category_type': 'expense', 'color': '#22c55e'},
            {'name': '여행', 'category_type': 'expense', 'color': "#0F118D"},
            {'name': '기타', 'category_type': 'expense', 'color': "#575457"},

            # 수입 카테고리
            {'name': '급여', 'category_type': 'income', 'color': '#ef4444'},
            {'name': '부수입', 'category_type': 'income', 'color': '#f59e0b'},
            {'name': '금융수입', 'category_type': 'income', 'color': '#10b981'},
            {'name': '기타수입', 'category_type': 'income', 'color': "#1b66e6"}
        ]