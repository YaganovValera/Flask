"""
Таблица пользователей должна содержать следующие поля:
    id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
Таблица заказов должна содержать следующие поля:
    id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.
Таблица товаров должна содержать следующие поля:
    id (PRIMARY KEY), название, описание и цена."""

from datetime import datetime

import databases
import sqlalchemy

# Creating a database
DATABASE_URL = "sqlite:///mydatabase.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Table about users
users = sqlalchemy.Table(
    "users", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer(), primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(32), nullable=False),
    sqlalchemy.Column("last_name", sqlalchemy.String(32), nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String(128), nullable=False, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String(128), nullable=False),
)

# Table about orders
orders = sqlalchemy.Table(
    "orders", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer(), primary_key=True),
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column('product_id', sqlalchemy.ForeignKey("products.id")),
    sqlalchemy.Column("order_date", sqlalchemy.DateTime(), default=datetime.now),
    sqlalchemy.Column("close_order", sqlalchemy.BOOLEAN(), default=False),
)

# Table about products
products = sqlalchemy.Table(
    "products", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer(), primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.Text()),
    sqlalchemy.Column("price", sqlalchemy.Numeric(), nullable=False)
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)
