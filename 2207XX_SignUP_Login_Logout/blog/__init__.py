from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from pprint import pprint

# DB 설정하기
db = SQLAlchemy() # 이 줄 추가!
DB_NAME =  "blog.db" # 이 줄 추가!


# app을 만들어주는 함수를 지정해 주자.
def create_app():
    app = Flask(__name__) # Flask app 만들기
    app.config['SECRET_KEY'] = "IFP"

    # DB 설정하기
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # 이 줄 추가!
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app) # 이 줄 추가!
    
    from .views import views
    app.register_blueprint(views, url_prefix="/blog")
    from .auth import auth
    app.register_blueprint(auth, url_prefix="/auth")

   
    # DB 생성하는 함수 호출하기
    from .models import User
    create_database(app)
    
    login_manager = LoginManager() # LoginManager() 객체를 만들어 준다.
    login_manager.login_view = "auth.login" # 만약 로그인이 필요한 곳에 로그인하지 않은 유저가 접근할 경우, 로그인 페이지로 리다이렉트 되도록 해준다.
     # 받은 id로부터, DB에 있는 유저 테이블의 정보에 접근하도록 해 줌.
    login_manager.init_app(app)
    # login manager는, 유저 테이블의 정보에 접근해, 저장된 세션을 바탕으로 로그인되어 있다면 로그인 페이지로 안 가도 되게끔 해 줌.
    @login_manager.user_loader
    def load_user_by_id(id):
        return User.query.get(int(id))
    
    return app
        
    
# DB 추가
def create_database(app):
    if not path.exists("blog/" + DB_NAME):  # DB 경로가 존재하지 않는다면,
        db.create_all(app=app)  # DB를 하나 만들어낸다.