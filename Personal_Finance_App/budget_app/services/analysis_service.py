import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import func
from models import Transaction, Category, PaymentMethod
from utils.db import db

class AnalysisService:
    """ Advanced Data Analysis Service """

    @staticmethod
    def get_transaction_dataframe(start_date = None, end_date = None, transaction_type = None, user_id = None):
        """
        거래 내역을 pandas dataframe으로 변환

        Args:
            start_date: 시작일 (datetime.date)
            end_date: 종료일 (datetime.date)
            transaction_type: 'income' or 'expense'
            user_id: 사용자 ID
        """
        query = db.session.query(
            Transaction.transaction_id,
            Transaction.date,
            Transaction.description,
            Transaction.transaction_type,
            Transaction.amount,
            Transaction.is_fixed,
            Transaction.memo,
            Category.name.label('category_name'),
            Category.color.label('category_color'),
            PaymentMethod.name.label('payment_method_name')
        )

        # 필터 적용
        if user_id:
            query = query.filter(Transaction.user_id)
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        if transaction_type:
            query = query.filter(Transaction.transaction_type == transaction_type)

        query = query.join(Category).join(PaymentMethod)

        # Transform into dataframe
        results = query.all()

        if not results:
            return pd.DataFrame()
        
        df = pd.DataFrame([{
            'transaction_id': r.transaction_id,
            'date': r.date,
            'description': r.description,
            'type': r.transaction_type,
            'amount': r.amount,
            'is_fixed': r.is_fixed,
            'memo': r.memo,
            'category': r.category_name,
            'category_color': r.category_color,
            'payment_method': r.payment_method_name
        } for r in results ])

        # transform date column into datetime
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['weekday'] = df['date'].dt.day_name()
        df['week'] = df['date'].dt.isocalendar().week

        return df
    
    @staticmethod
    def get_mom_comparison(year, month, user_id = None):
        """
        MoM(Month Over Month) 비교 분석
        전월 대비 증감률
        """

        # current month
        current_month_start = datetime(year, month, 1).date()
        if month == 12:
            current_month_end = datetime(year + 1, 1, 1).date() - timedelta(days = 1)
            prev_month_start = datetime(year, 11, 1).date()
            prev_month_end = datetime(year, 12, 1).date() - timedelta(days = 1)
        else:
            current_month_end = datetime(year, month + 1, 1).date() - timedelta(days = 1)
            if month == 1:
                prev_month_start = datetime(year - 1, 12, 1).date()
                prev_month_end = datetime(year, 1, 1).date() - timedelta(days = 1)
            else:
                prev_month_start = datetime(year, month - 1, 1).date()
                prev_month_end = datetime(year, month, 1).date() - timedelta(days = 1)

        # current month data
        query_base = db.session.query(func.sum(Transaction.amount))
        if user_id:
            query_base.filter(Transaction.user_id == user_id)

        current_income = query_base.filter(Transaction.transaction_type == 'income',
                    Transaction.date >= current_month_start,
                    Transaction.date <= current_month_end).scalar() or 0
        
        current_expense = query_base.filter(Transaction.transaction_type == 'expense',
                    Transaction.date >= current_month_start,
                    Transaction.date <= current_month_end).scalar() or 0
        
        current_balance = current_income - current_expense
        
        # prev month data
        prev_income = query_base.filter(Transaction.transaction_type == 'income',
                    Transaction.date >= prev_month_start,
                    Transaction.date <= prev_month_end).scalar() or 0
        
        prev_expense = query_base.filter(Transaction.transaction_type == 'expense',
                    Transaction.date >= prev_month_start,
                    Transaction.date <= prev_month_end).scalar() or 0
        
        prev_balance = prev_income - prev_expense

        # calculate increase rate
        income_change = ((current_income - prev_income) / prev_income * 100) if prev_income > 0 else 0
        expense_change = ((current_expense - prev_expense) / prev_expense * 100) if prev_expense > 0 else 0
        balance_change = ((current_balance - prev_balance) / prev_balance * 100) if prev_balance > 0 else 0

        return {
            'current': {
                'income': current_income,
                'expense': current_expense,
                'balance': current_balance
            },
            'previous': {
                'income': prev_income,
                'expense': prev_expense,
                'balance': prev_balance
            },
            'change': {
                'income': income_change,
                'expense': expense_change,
                'balance': balance_change,
                'income_diff': current_income - prev_income,
                'expense_diff': current_expense - prev_expense
            }
        }
    
    @staticmethod
    def get_yoy_comparison(year, month, user_id = None):
        """
        YoY (Year Over Year) 비교 분석 - 전년 동월 대비 증감률
        """
        # Current Year
        current_start = datetime(year, month, 1).date()
        if month == 12:
            current_end = datetime(year + 1, 1, 1).date() - timedelta(days = 1)
        else:
            current_end = datetime(year, month + 1, 1).date() - timedelta(days = 1)

        # last year
        prev_year_start = datetime(year - 1, month, 1).date()
        if month == 12:
            prev_year_end = datetime(year, 1, 1).date() - timedelta(days = 1)
        else:
            prev_year_end = datetime(year - 1, month + 1, 1).date() - timedelta(days = 1)

        query_base = db.session.query(func.sum(Transaction.amount))
        if user_id:
            query_base.filter(Transaction.user_id == user_id)

        # current year data
        current_income = query_base.filter(Transaction.transaction_type == 'income',
                    Transaction.date >= current_start,
                    Transaction.date <= current_end).scalar() or 0
        
        current_expense = query_base.filter(Transaction.transaction_type == 'expense',
                    Transaction.date >= current_start,
                    Transaction.date <= current_end).scalar() or 0
        
        current_balance = current_income - current_expense
        
        # last year data
        prev_income = query_base.filter(Transaction.transaction_type == 'income',
                    Transaction.date >= prev_year_start,
                    Transaction.date <= prev_year_end).scalar() or 0

        prev_expense = query_base.filter(Transaction.transaction_type == 'expense',
                    Transaction.date >= prev_year_start,
                    Transaction.date <= prev_year_end).scalar() or 0
        
        prev_balance = prev_income - prev_expense

        # calculate increase rate
        income_change = ((current_income - prev_income) / prev_income * 100) if prev_income > 0 else 0
        expense_change = ((current_expense - prev_expense) / prev_expense * 100) if prev_expense > 0 else 0
        balance_change = ((current_balance - prev_balance) / prev_balance * 100) if prev_balance > 0 else 0

        return {
            'current_year': {
                'income': current_income,
                'expense': current_expense,
                'balance': current_balance
            },
            'previous_year': {
                'income': prev_income,
                'expense': prev_expense,
                'balance': prev_balance
            },
            'change': {
                'income': income_change,
                'expense': expense_change,
                'balance': balance_change,
                'income_diff': current_income - prev_income,
                'expense_diff': current_expense - prev_expense
            }
        }
    
    @staticmethod
    def get_custom_period_analysis(start_date, end_date, user_id = None):
        """
        커스텀 기간 분석 (기간 선택?)
        """
        df = AnalysisService.get_transaction_dataframe(start_date = start_date, end_date = end_date, user_id = user_id)
        print(len(df))

        if df.empty:
            return {
                'summary': {
                    'total_income': 0,
                    'total_expense': 0,
                    'balance': 0,
                    'transaction_count': 0,
                    'avg_daily_expense': 0
                },
                'by_category': [],
                'by_payment_method': [],
                'by_weekday': []
            }
        
        # basic statistics
        # income_df = df[df['Type'] == 'income']
        income_df = df.query("type == 'income'")
        expense_df = df.query("type == 'expense'")

        total_income = income_df['amount'].sum()
        total_expense = expense_df['amount'].sum()

        # average daily expense
        days = (end_date - start_date).days + 1
        avg_daily_expense = total_expense / days if days > 0 else 0

        # per category
        category_analysis = expense_df.groupby('category').agg({
            'amount': ['sum', 'count', 'mean']
        }).round(2)

        by_category = [{
            'category': cat,
            'total': row['amount']['sum'],
            'count': int(row['amount']['count']),
            'average': row['amount']['mean']
        } for cat, row in category_analysis.iterrows()]


        # per payment method
        payment_analysis = expense_df.groupby('payment_method')['amount'].sum()
        by_payment_method = [{
            'payment_method': pm,
            'total': amount
        } for pm, amount in payment_analysis.items()]

        # per daily
        weekday_analysis = expense_df.groupby('weekday')['amount'].sum()
        by_weekday = [{
            'weekday': day,
            'total': amount
        } for day, amount in weekday_analysis.items()]

        return {
            'summary': {
                'total_income': int(total_income),
                'total_expense': int(total_expense),
                'balance': int(total_income - total_expense),
                'transaction_count': len(df),
                'avg_daily_expense': round(avg_daily_expense, 2)
            },
            'by_category': sorted(by_category, key = lambda x: x['total'], reverse = True),
            'by_payment_method': sorted(by_payment_method, key = lambda x: x['total'], reverse = True),
            'by_weekday': by_weekday
        }
    
    @staticmethod
    def get_spending_pattern_analysis(year, month, user_id = None):
        """
        expense pattern analysis (daily, weekly, timely)
        """
        start_date = datetime(year, month, 1).date()
        if month == 12:
            end_date = datetime(year + 1, 1, 1).date() - timedelta(days = 1)
        else:
            end_date = datetime(year, month + 1, 1).date() - timedelta(days = 1)

        df = AnalysisService.get_transaction_dataframe(start_date, end_date, 'expense', user_id)

        if df.empty:
            return {
                'by_weekday': [],
                'by_week': [],
                'by_day': []
            }
        
        # daily average expense
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_stats = df.groupby('weekday')['amount'].agg(['sum', 'count', 'mean']).reindex(weekday_order, fill_value = 0)

        by_weekday = [{
            'weekday': day,
            'total': int(row['sum']),
            'count': int(row['count']),
            'average': round(row['mean'], 2)
        } for day, row in weekday_stats.iterrows()]

        # weekly expense
        by_week = df.groupby('week')['amount'].sum().to_dict()
        by_week_list = [{'week': week, 'total': int(amount)} for week, amount in by_week.items()]

        # daily expense
        by_day = df.groupby('day')['amount'].sum().to_dict()
        by_day_list = [{'day': day, 'total': int(amount)} for day, amount in by_day.items()]

        return {
            'by_weekday': by_weekday,
            'by_week': sorted(by_week_list, key = lambda x: x['week']),
            'by_day': sorted(by_day_list, key = lambda x: x['day'])
        }