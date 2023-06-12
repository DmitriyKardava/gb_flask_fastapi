from fastapi import FastAPI, HTTPException
from models import database, users, items, orders, statuses, User, Item, Order, UserIn, ItemIn, OrderIn
import uvicorn
from typing import List

app = FastAPI()


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/user/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(name=user.name,
                                  surname=user.surname,
                                  email=user.email,
                                  password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


@app.get("/items/", response_model=List[Item])
async def read_items():
    query = items.select()
    return await database.fetch_all(query)


@app.get("/items/{item_id}", response_model=Item)
async def read_user(item_id: int):
    query = items.select().where(items.c.id == item_id)
    return await database.fetch_one(query)


@app.post("/items/", response_model=Item)
async def create_item(item: ItemIn):
    query = items.insert().values(title=item.title,
                                  description=item.description,
                                  price=item.price)
    last_record_id = await database.execute(query)
    return {**item.dict(), "id": last_record_id}


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, new_item: ItemIn):
    query = items.update().where(items.c.id == item_id).values(**new_item.dict())
    await database.execute(query)
    return {**new_item.dict(), "id": item_id}


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    query = items.delete().where(items.c.id == item_id)
    await database.execute(query)
    return {'message': 'Item deleted'}


@app.get("/orders/", response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get("/orders/{order_id}", response_model=List[Order])
async def read_user_orders(user_id):
    query = orders.select(orders.c.user_id == user_id)
    return await database.fetch_all(query)


@app.get("/orders/{order_id}", response_model=List[Order])
async def read_item_orders(item_id):
    query = orders.select(orders.c.item_id == item_id)
    return await database.fetch_all(query)


@app.get("/orders/{order_id}", response_model=Order)
async def read_orders(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    check_q = users.select(users.c.id == order.user_id)
    _q = await database.fetch_one(check_q)
    if not _q:
        raise HTTPException(status_code=404, detail=f"user {order.user_id} not found")

    check_q = items.select(items.c.id == order.item_id)
    _q = await database.fetch_one(check_q)
    if not _q:
        raise HTTPException(status_code=404, detail=f"item {order.item_id} not found")

    check_q = statuses.select(statuses.c.id == order.status_id)
    _q = await database.fetch_one(check_q)
    if not _q:
        raise HTTPException(status_code=404, detail=f"status {order.status_id} not found")

    query = orders.insert().values(user_id=order.user_id,
                                   item_id=order.item_id,
                                   order_date=order.order_date,
                                   status_id=order.status_id)
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "id": order_id}


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
