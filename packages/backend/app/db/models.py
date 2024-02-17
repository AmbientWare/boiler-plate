from sqlalchemy import Boolean, Column, Integer, String

from .session import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import JSON


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    role = Column(String, default="user")
    hashed_password = Column(String, nullable=True)
    picture = Column(String, nullable=True)
    is_confirmed = Column(Boolean, default=False, nullable=True)

    tokens = relationship("Token", back_populates="user")
    created_teams = relationship("Team", back_populates="creator")
    memberships = relationship("TeamMember", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")


class Token(Base):
    __tablename__ = "api_key"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    hashed_token = Column(String, nullable=False)

    user = relationship("User", back_populates="tokens")


class Subscription(Base):
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    subscription_email = Column(String, nullable=False)
    customer_id = Column(String, nullable=False)
    subscription_id = Column(String, nullable=False)
    price_id = Column(String, nullable=False)
    status = Column(String, nullable=True, default="active")
    product = Column(String, nullable=True)
    product_price = Column(String, nullable=True)
    billing_period = Column(String, nullable=True)
    product_currency = Column(String, nullable=True)

    user = relationship("User", back_populates="subscriptions")


class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)

    creator = relationship("User", back_populates="created_teams")
    members = relationship("TeamMember", back_populates="team")


class TeamMember(Base):
    __tablename__ = "team_member"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("team.id"), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)

    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="memberships")
