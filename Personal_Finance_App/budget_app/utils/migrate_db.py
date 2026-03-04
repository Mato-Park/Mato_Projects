"""
데이터베이스 마이그레이션 스크립트
Phase 1-4의 데이터를 Phase 5 (멀티 유저)로 마이그레이션
"""

from app import create_app
from utils.db import db
from models import User, Transaction, Category, PaymentMethod

def migrate_to_multiuser():
    """
    기존 단일 사용자 데이터를 멀티 유저 시스템으로 마이그레이션
    """

    app = create_app('development')

    with app.app_context():
        print("🔄 마이그레이션 시작...")

        # 1. 기존 사용자 확인
        existing_user = User.query.filter_by(user_id = 1).first()

        if existing_user:
            print(f"✅ 기존 사용자 발견: {existing_user.username} (ID: {existing_user.user_id})")

            # 비밀번호가 암호화되지 않은 경우 (temporary)
            if existing_user.password_hash == 'temporary':
                print("⚠️  비밀번호가 암호화되지 않았습니다.")

                new_password = input("새 비밀번호를 입력하세요 (최소 6자): ")

                if len(new_password) < 6:
                    print("❌ 비밀번호는 최소 6자 이상이어야 합니다.")
                    return
                
                existing_user.set_password(new_password)
                db.session.commit()
                print("✅ 비밀번호가 암호화되어 저장되었습니다.")
            else:
                print("✅ 비밀번호가 이미 암호화되어 있습니다.")
        
            # 2. 기존 데이터 개수 확인
            transaction_count = Transaction.query.filter_by(user_id = 1).count()
            category_count = Category.query.filter_by(user_id = 1).count()
            payment_method_count = PaymentMethod.query.filter_by(user_id = 1).count()

            print(f"\n📊 기존 데이터:")
            print(f"  - 거래 내역: {transaction_count}건")
            print(f"  - 카테고리: {category_count}개")
            print(f"  - 결제 수단: {payment_method_count}개")
            
            print("\n✅ 마이그레이션 완료!")
            print(f"   이메일: {existing_user.email}")
            print(f"   사용자명: {existing_user.username}")
            print("   이제 이 계정으로 로그인할 수 있습니다.")

        else:
            print("❌ 기존 사용자(user_id=1)를 찾을 수 없습니다.")
            print("   새로운 계정을 만들어야 합니다.")

            # 사용자 생성 옵션
            create_new = input("\n새 사용자를 생성하시겠습니까? (y/n): ")

            if create_new.lower() == 'y':
                username = input("사용자 이름: ")
                email = input("이메일: ")
                password = input("비밀번호 (최소 6자): ")

                if len(password) < 6:
                    print("❌ 비밀번호는 최소 6자 이상이어야 합니다.")
                    return
                
                # create new user
                new_user = User(
                    username = username,
                    email=email
                )
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.flush()

                # make default cartegory
                for cat_data in Category.get_default_categorires():
                    category = Category(**cat_data, user_id = new_user.user_id)
                    db.session.add(category)

                # make default payment method
                for pm_data in PaymentMethod.get_default_payment_method():
                    payment_method = PaymentMethod(**pm_data, user_id = new_user.user_id)
                    db.session.add(payment_method)
                
                db.session.commit()

                print(f"\n✅ 새 사용자가 생성되었습니다!")
                print(f"   이메일: {email}")
                print(f"   사용자명: {username}")
                print("   이제 이 계정으로 로그인할 수 있습니다.")

def check_database_status():
    app = create_app('development')

    with app.app_context():
        print("\n📊 데이터베이스 상태:")
        print("=" * 50)

        # the number of users
        user_count = User.query.count()
        print(f"사용자: {user_count}명")

        if user_count > 0:
            users = User.query.all()
            for user in users:
                print(f"  - {user.username} ({user.email})")

                # each user's data
                t_count = Transaction.query.filter_by(user_id = user.user_id).count()
                c_count = Category.query.filter_by(user_id = user.user_id).count()
                p_count = PaymentMethod.query.filter_by(user_id = user.user_id).count()

                print(f"    거래: {t_count}건, 카테고리: {c_count}개, 결제수단: {p_count}개")

        print("=" * 50)

if __name__ == "__main__":
    print("🔧 박마토의 가계부 - 데이터베이스 마이그레이션")
    print("=" * 50)
    
    while True:
        print("\n메뉴:")
        print("1. 데이터베이스 상태 확인")
        print("2. 마이그레이션 실행")
        print("3. 종료")

        choice = input("\n선택 (1-3): ")

        if choice == '1':
            check_database_status()
        elif choice == '2':
            migrate_to_multiuser()
        elif choice == '3':
            print("👋 종료합니다.")
            break
        else:
            print("❌ 잘못된 선택입니다.")