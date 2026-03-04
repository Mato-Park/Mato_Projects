from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from forms.auth_forms import LoginForm, SignupForm
from models.user import User
from models.category import Category
from models.payment_method import PaymentMethod
from utils.db import db

auth_bp = Blueprint('auth', __name__, url_prefix = '/auth')

@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    """login"""
    # 이미 로그인한 경우 메인으로 리다이렉트
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()

    if form.validate_on_submit():
        # 사용자 찾기
        user = User.query.filter_by(email = form.email.data).first()

        # 비밀번호 확인
        if user and user.check_password(form.password.data):
            login_user(user, remember = form.remember_me.data)
            flash(f'{user.username}님, 환영합니다!', 'success')

            # next 파라미터가 있으면 해당 페이지로, 없으면 메인으로
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.index'))
        else:
            flash('이메일 또는 비밀번호가 올바르지 않습니다.', 'error')
        
    return render_template('auth/login.html', form=form)

@auth_bp.route('/signup', methods = ['GET', 'POST'])
def signup():
    """회원가입"""
    # 이미 로그인한 경우 메인으로 리다이렉트
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = SignupForm()

    if form.validate_on_submit():
        try:
            # 새 사용자 생성
            user = User(
                username = form.username.data,
                email = form.email.data
            )
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.flush() # create user_id

            # 기본 카테고리 생성
            for cat_data in Category.get_default_categorires():
                category = Category(**cat_data, user_id = user.user_id)
                db.session.add(category)
            
            # 기본 결제 수단 생성
            for pm_data in PaymentMethod.get_default_payment_method():
                payment_method = PaymentMethod(**pm_data, user_id = user.user_id)
                db.session.add(payment_method)
            
            db.session.commit()

            flash('회원가입이 완료되었습니다! 로그인해주세요.', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            flash(f'회원가입 중 오류가 발생했습니다.: {str(e)}', 'error')
        
    return render_template('auth/signup.html', form = form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('로그아웃되었습니다.', 'success')
    return redirect(url_for('auth.login'))