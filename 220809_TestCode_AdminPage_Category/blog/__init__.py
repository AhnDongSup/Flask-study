# import click
# from flask.cli import with_appcontext
# from sqlalchemy.exc import IntegrityError

from flask import Flask, abort
from os import path
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .models import DB_NAME, db, get_user_model, get_post_model, get_category_model

from werkzeug.security import generate_password_hash
from wtforms import PasswordField, StringField
from wtforms.validators import InputRequired


# app을 만들어주는 함수를 지정해 주자.
def create_app():
    app = Flask(__name__)  # Flask app 만들기
    app.config['SECRET_KEY'] = "IFP"

    # DB 설정하기
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # DB 관련 추가할 설정
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # flask-admin
    app.config['FLASK_ADMIN_SWATCH'] = 'Darkly'
    admin = Admin(app, name='blog',
                  template_mode='bootstrap3')

    # flask-admin에 model 추가
    class MyUserView(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated and current_user.is_staff == True:
                return True
            else:
                return abort(403)

        class CustomPasswordField(StringField):
            def populate_obj(self, obj, name):
                setattr(obj, name, generate_password_hash(self.data))

        form_extra_fields = {
            'password': CustomPasswordField('Password', validators=[InputRequired()])
        }
        form_excluded_columns = {
            'posts', 'created_at'
        }

    class MyPostView(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated and current_user.is_staff == True:
                return True
            else:
                return abort(403)

        form_excluded_columns = {
            'created_at', 'comments'
        }

    class MyCategoryView(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated and current_user.is_staff == True:
                return True
            else:
                return abort(403)

        form_excluded_columns = {
            'category'
        }

    class MyCommentView(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated and current_user.is_staff == True:
                return True
            else:
                return abort(403)

    admin.add_view(MyUserView(get_user_model(), db.session))  # get_user_model 로 유저 클래스를 가져옴
    admin.add_view(MyPostView(get_post_model(), db.session))
    admin.add_view(MyCategoryView(get_category_model(), db.session))
    db.init_app(app)

    from .views import views
    # blueprint 등록, '/' 를 기본으로 한다.
    app.register_blueprint(views, url_prefix="/")

    from .auth import auth
    # blueprint 등록, '/auth' 를 기본으로 한다.
    app.register_blueprint(auth, url_prefix="/auth")

    # DB 생성하는 함수 호출하기
    from .models import User
    create_database(app)

    login_manager = LoginManager()  # LoginManager() 객체를 만들어 준다.
    login_manager.login_view = "auth.login"  # 만약 로그인이 필요한 곳에 로그인하지 않은 유저가 접근할 경우, 로그인 페이지로 리다리엑트 되도록 해 준다.
    login_manager.init_app(app)

    # 받은 id로부터, DB에 있는 유저 테이블의 정보에 접근하도록 해 줌.
    # login manager는, 유저 테이블의 정보에 접근해, 저장된 세션을 바탕으로 로그인되어 있다면 로그인 페이지로 안 가도 되게끔 해 줌.
    @login_manager.user_loader
    def load_user_by_id(id):
        return User.query.get(int(id))


    # Custom Command Line
    # import click
    # from flask.cli import with_appcontext
    # @click.command(name="create_superuser")
    # @with_appcontext
    # def create_superuser():

    #     # 정보 입력받기
    #     username = input("Enter username : ")
    #     email = input("Enter email : ")
    #     password = input("Enter password : ")
    #     is_staff = True

    #     try:
    #         superuser = get_user_model()(
    #             username = username,
    #             email = email,
    #             password = generate_password_hash(password),
    #             is_staff = is_staff
    #         )
    #         db.session.add(superuser)
    #         db.session.commit()
    #     except IntegrityError:
    #         print('\033[31m' + "Error : username or email already exists.")
    #     print(f"User created! : {email}")

    # app.cli.add_command(create_superuser)

    return app



# DB 추가
def create_database(app):
    if not path.exists("blog/" + DB_NAME):  # DB 경로가 존재하지 않는다면,
        db.create_all(app=app)  # DB를 하나 만들어낸다.