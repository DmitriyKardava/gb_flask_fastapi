from datetime import date

from pydantic import BaseModel, Field
import databases
import sqlalchemy

DATABASE_URL = "sqlite:///shop.db"
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table("users",
                         metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("name", sqlalchemy.String(32)),
                         sqlalchemy.Column("surname", sqlalchemy.String(32)),
                         sqlalchemy.Column("email", sqlalchemy.String(32)),
                         sqlalchemy.Column("password", sqlalchemy.String(32)),
                         )

items = sqlalchemy.Table("items",
                         metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("title", sqlalchemy.String(32)),
                         sqlalchemy.Column("description", sqlalchemy.String(200)),
                         sqlalchemy.Column("price", sqlalchemy.Numeric(scale=2)),
                         )

statuses = sqlalchemy.Table("statuses",
                            metadata,
                            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column("title", sqlalchemy.String(32)),
                            )

orders = sqlalchemy.Table("orders",
                          metadata,
                          sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column("user_id", sqlalchemy.Integer,
                                            sqlalchemy.ForeignKey("users.id"), nullable=False),
                          sqlalchemy.Column("item_id", sqlalchemy.Integer,
                                            sqlalchemy.ForeignKey("items.id"), nullable=False),
                          sqlalchemy.Column("order_date", sqlalchemy.Date),
                          sqlalchemy.Column("status_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("statuses.id"))
                          )

metadata.create_all(engine)


class Item(BaseModel):
    id: int = Field(default=None, alias='item_id')
    title: str = Field(max_length=32)
    description: str = Field(max_length=200)
    price: float


class ItemIn(BaseModel):
    title: str = Field(max_length=32)
    description: str = Field(max_length=200)
    price: float


class User(BaseModel):
    id: int = Field(default=None, alias='user_id')
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: str = Field(max_length=32)
    password: str = Field(max_length=32)


class UserIn(BaseModel):
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: str = Field(max_length=32)
    password: str = Field(max_length=32)


class OrderStatus(BaseModel):
    id: int = Field(default=None, alias='status_id')
    title: str = Field(max_length=32)


class Order(BaseModel):
    id: int = Field(default=None, alias='order_id')
    user_id: int = Field()
    item_id: int = Field()
    order_date: date
    status_id: int = Field()

    class Config:
        arbitrary_types_allowed = True


class OrderIn(BaseModel):
    user_id: int = Field()
    item_id: int = Field()
    order_date: date
    status_id: int = Field()
