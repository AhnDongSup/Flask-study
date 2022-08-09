from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

# init 으로부터 옮김
db = SQLAlchemy()
DB_NAME = "blog.db"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)    #유일키
    email = db.Column(db.String(150), unique=True)  #유일한 값 즉, 중복이 없도록    
    username = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    create_at = db.Column(db.DateTime(timezone=True), default=func.now()) # 생성일자,기본적으로 현재로 저장
    is_staff = db.Column(db.Boolean, default = False) # 스태프 권한이 있는 유저인지 아닌지를 판별하는 불리언 필드



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) # id : 유일 키, integer
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now()) # 생성일자, 기본적으로 현재가 저장되도록 함
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False) # 외래 키, user 테이블의 id 참조할 것임
    user = db.relationship('User', backref = db.backref('posts', cascade='delete'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'), nullable=False) # 외래 키, category 테이블의 id 참조할 것임
    category = db.relationship('Category', backref=db.backref('category', cascade='delete'))
    # comments = db.relationship("Comment", backref="post", passwive_deletes=True)
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True) # 유일 key
    name = db.Column(db.String(150), unique=True)
    
    def __repr__(self):
        return f'<{self.__class__.__name__}(name={self.name})>'
    
    
def get_user_model():
    return User

# Post 클래스를 반환하는 함수 정의
def get_post_model():
    return Post

# Category 클래스를 반환하는 함수 정의
def get_category_model():
    return Category