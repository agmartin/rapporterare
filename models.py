from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Text,
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    ig_username = Column(Text, unique=True)
    ig_num_followers = Column(BigInteger)

    ig_user_posts = relationship("UserPostsCleaned", back_populates="ig_user")


class UserPosts(Base):
    __tablename__ = "user_posts"

    person_id = Column(BigInteger, primary_key=True)
    taken_at = Column(DateTime)
    caption_text = Column(Text)
    caption_tags = Column(Text)
    like_count = Column(BigInteger)
    comment_count = Column(BigInteger)


class UserPostsCleaned(Base):
    __tablename__ = "user_posts_cleaned"

    post_id = Column(BigInteger, primary_key=True)
    person_id = Column(
        ForeignKey(User.id),
        nullable=False,
        unique=False,
    )
    month_name = Column(Text)
    year = Column(Integer)
    taken_at = Column(DateTime)
    caption_text = Column(Text)
    caption_tags = Column(Text)
    like_count = Column(Integer)
    comment_count = Column(Integer)

    ig_user = relationship("User", back_populates="ig_user_posts")
