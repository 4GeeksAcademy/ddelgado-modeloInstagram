from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user")

    posts:Mapped[list["Post"]]= relationship("Post", back_populates="user")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
    
class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    image_url: Mapped[str] = mapped_column(String(300), nullable=False)
    caption: Mapped[str] = mapped_column(String(500), nullable=True)

    user:Mapped["User"]= relationship("User", back_populates="posts")
    

    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image_url": self.image_url,
            "caption": self.caption
            # do not serialize the password, its a security breach
        }
    


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text:Mapped[str] = mapped_column(String(300), nullable=False)
    author: Mapped[str] = mapped_column(String(300), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="comments")

    post:Mapped["Post"]= relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author": self.author,
            "post_id": self.post_id
            # do not serialize the password, its a security breach
        }
