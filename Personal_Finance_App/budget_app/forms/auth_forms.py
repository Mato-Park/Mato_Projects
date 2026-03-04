from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models.user import User

class LoginForm(FlaskForm):
    """로그인 폼"""
    email = StringField('이메일', validators = [
        DataRequired(message = '이메일을 입력해주세요.'),
        Email(message = '올바른 이메일 형식이 아닙니다.')
    ])
    password = PasswordField('비밀번호', validators = [
        DataRequired(message = '비밀번호를 입력해주세요.')
    ])
    remember_me = BooleanField('로그인 상태 유지')
    submit = SubmitField('로그인')

class SignupForm(FlaskForm):
    """회원가입 폼"""
    username = StringField('사용자 이름', validators = [
        DataRequired(message = '사용자 이름을 입력해주세요.'),
        Length(min = 2, max = 50, message = '2-50자 사이로 입력해주세요.')
    ])
    email = StringField('이메일', validators = [
        DataRequired(message = '이메일을 입력해주세요.'),
        Email(message = '올바른 이메일 형식이 아닙니다.')
    ])
    password = PasswordField('비밀번호', validators = [
        DataRequired(message = '비밀번호를 입력해주세요.'),
        Length(min = 6, message = '비밀번호는 최소 6자 이상이어야 합니다.')
    ])
    password2 = PasswordField('비밀번호 확인', validators = [
        DataRequired(message = '비밀번호 확인을 입력해주세요.'),
        EqualTo('password', message = '비밀번호가 일치하지 않습니다.')
    ])
    submit = SubmitField('가입하기')

    # 커스텀 유효성 검사: 중복 사용자 이름 확인
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('이미 사용 중인 사용자 이름입니다.')
        
    # 커스텀 유효성 검사: 중복 이메일 확인
    def validation_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('이미 가입된 이메일입니다.')
