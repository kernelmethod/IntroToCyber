import datetime
from flask_login import UserMixin
from ticktock.app import db
from ticktock.config import max_post_len


class User(db.Model, UserMixin):
    __tablename__ = "users"

    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    uid = db.Column(db.Integer, primary_key=True)

    def get_id(self) -> str:
        return str(self.uid)

    def __repr__(self) -> str:
        return f"<User {self.uid}: {self.username!r}>"


class Post(db.Model):
    __tablename__ = "posts"

    post_id: int = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey("users.uid"), nullable=False)
    author = db.relationship("User", backref=db.backref("user", lazy=True))

    content = db.Column(db.String(max_post_len), nullable=False)
    posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def to_json(self):
        return {
            "username": self.author.username,
            "uid": self.author_id,
            "content": self.content,
            "posted": self.posted,
            "post_id": self.post_id,
        }
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
