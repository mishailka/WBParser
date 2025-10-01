import requests
from sqlalchemy.orm import sessionmaker
from database import engine, Product
SessionLocal = sessionmaker(bind=engine)

def fetch_wb_products(query: str, page: int = 1, spp: int = 100):

    url = "https://search.wb.ru/exactmatch/ru/common/v18/search"
    params = {
        "ab_testing": "false",
        "appType": "1",
        "curr": "rub",
        "dest": "-971647",
        "inheritFilters": "false",
        "lang": "ru",
        "page": page,
        "query": query,
        "resultset": "catalog",
        "sort": "popular",
        "spp": spp,
        "suppressSpellcheck": "false",
        "uclusters": "2"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data.get("products", [])


def save_products_to_db(products):
    db = SessionLocal()
    for item in products:
        # Проверяем, есть ли товар по wb_id
        product = db.query(Product).filter_by(wb_id=item["id"]).first()
        if not product:
            price = item.get("sizes", [{}])[0].get("price", {}).get("product", 0) / 100
            product = Product(
                wb_id=item.get("id"),
                name=item.get("name"),
                brand=item.get("brand"),
                price=float(price),
                rating=float(item.get("rating")) if isinstance(item.get("rating"), (int, float)) else None,
                reviews_count=item.get("feedbacks", 0),
                stock=item.get("totalQuantity", 0)
            )
            db.add(product)
    db.commit()
    db.close()


def main():
    query = "термопаста"
    page = 1
    total_saved = 0

    while True:
        print(f"Обработка страницы {page}...")
        products = fetch_wb_products(query=query, page=page, spp=100)

        if not products:
            break

        save_products_to_db(products)
        total_saved += len(products)
        page += 1
if __name__ == "__main__":
    main()
