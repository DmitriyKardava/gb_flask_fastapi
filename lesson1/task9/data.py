categories = [
    {"id": 1, "name": 'Одежда'},
    {"id": 2, "name": "Обувь"},
    {"id": 3, "name": "Куртки"},
]

products = [
    {"id": 1, "name": "товар 1", "category_id": 1},
    {"id": 2, "name": "товар 2", "category_id": 2},
    {"id": 3, "name": "товар 3", "category_id": 3},
    {"id": 4, "name": "товар 4", "category_id": 1},
]

def get_category(id):
    return next(filter(lambda c: c.get('id') == id, categories), None)

def get_category_products(id):
    return filter(lambda c: c.get('category_id') == id, products)
    
def get_product(id):
    return next(filter(lambda p: p.get('id') == id, products), None)