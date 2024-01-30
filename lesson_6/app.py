"""
Необходимо создать базу данных для интернет-магазина.
База данных должна состоять из трёх таблиц: товары, заказы и пользователи.

Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц (6 моделей).
Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API (итого 15 маршрутов).
* Чтение всех
* Чтение одного
* Запись
* Изменение
* Удаление
"""

from datetime import datetime
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field
from models import database, users, products, orders
import bcrypt


# Создание хэша пароля при регистрации
def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')


app = FastAPI()


# Модели pydantic для получения новых данных и возврата существующих в БД
class UserCreate(BaseModel):
    first_name: str = Field(max_length=32)
    last_name: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(min_length=8, max_length=128)


class User(UserCreate):
    id: int


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    order_date: datetime = datetime.now()
    close_order: bool


class Order(OrderCreate):
    id: int


class ProductCreate(BaseModel):
    name: str = Field(max_length=32)
    description: str
    price: float = Field(ge=0)


class Product(ProductCreate):
    id: int


# ===========================================================================================================
# CRUD операции для каждой из таблиц

# GET /users
@app.get("/users/", response_model=List[User])
async def get_users():
    query = users.select()
    return await database.fetch_all(query)


# GET /users/{id}
@app.get("/users/{id}", response_model=User)
async def get_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


# POST /users/
@app.post("/users/", response_model=UserCreate)
async def create_user(user: UserCreate):
    query = users.insert().values(first_name=user.first_name,
                                  last_name=user.last_name,
                                  email=user.email,
                                  password=hash_password(user.password))
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


# UPDATE /users/{user_id}
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserCreate):
    new_user.password = hash_password(new_user.password)
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}
# --------------------------------------------------------------------------------------------------


# GET /products
@app.get("/products", response_model=List[Product])
async def get_products():
    query = products.select()
    return await database.fetch_all(query)


# GET /products/{id}
@app.get("/products/{id}", response_model=Product)
async def get_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)


# POST /products/
@app.post("/products/", response_model=Product)
async def create_product(product: ProductCreate):
    query = products.insert().values(name=product.name,
                                     description=product.description,
                                     price=product.price)
    last_record_id = await database.execute(query)
    return {**product.dict(), "id": last_record_id}


# UPDATE /products/{product_id}
@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductCreate):
    query = products.update().where(products.c.id == product_id).values(**new_product.dict())
    await database.execute(query)
    return {**new_product.dict(), "id": product_id}


# DELETE /products/{product_id}
@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {'message': 'Product deleted'}
# --------------------------------------------------------------------------------------------------


# GET /orders
@app.get("/orders", response_model=List[Order])
async def get_orders():
    query = orders.select()
    return await database.fetch_all(query)


# GET /orders/{id}
@app.get("/orders/{id}", response_model=Order)
async def get_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


# POST /orders/
@app.post("/orders/", response_model=Order)
async def create_order(order: OrderCreate):
    query = orders.insert().values(user_id=order.user_id,
                                   product_id=order.product_id,
                                   order_date=order.order_date,
                                   close_order=order.close_order)
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}


# UPDATE /orders/{order_id}
@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderCreate):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "id": order_id}


# DELETE /orders/{order_id}
@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}
