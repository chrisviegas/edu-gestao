from sqlalchemy import Table, Column, BigInteger, Integer, ForeignKey
from src.config.db_config import db

roles_users = Table(
    "roles_users",
    db.metadata,
    Column("user_id", BigInteger, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)
