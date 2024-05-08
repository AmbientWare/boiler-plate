from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime, UTC


from .session import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class BaseTable(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))


class User(BaseTable):
    __tablename__ = "user"

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
    credentials = relationship("Credential", back_populates="user")


class Credential(BaseTable):
    __tablename__ = "credential"

    name = Column(String, index=True, nullable=False)
    credentialName = Column(String, index=True, nullable=False)
    encrypted_data = Column(String, nullable=True)
    # foreign keys
    user_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=True)

    user = relationship("User", back_populates="credentials")


class Token(BaseTable):
    __tablename__ = "api_key"

    user_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    hashed_token = Column(String, nullable=False)

    user = relationship("User", back_populates="tokens")


class Subscription(BaseTable):
    __tablename__ = "subscription"

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


class Team(BaseTable):
    __tablename__ = "team"

    creator_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)

    creator = relationship("User", back_populates="created_teams")
    members = relationship("TeamMember", back_populates="team")


class TeamMember(BaseTable):
    __tablename__ = "team_member"

    team_id = Column(Integer, ForeignKey("team.id"), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)

    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="memberships")
