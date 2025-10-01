import json
import requests

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

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    products = data.get("products", [])

    result = []
    for product in products:
        price = product.get("sizes", [{}])[0].get("price", {}).get("product", 0) / 100

        item = {
            "id": product.get("id"),
            "name": product.get("name"),
            "brand": product.get("brand"),
            "rating": product.get("rating", 0),
            "reviews_count": product.get("feedbacks", 0),
            "price": price,
            "stock": product.get("totalQuantity", 0)
        }
        result.append(item)

    return result

def main():
    query = "термопаста"
    page = 1
    all_products = []
    seen_ids = set()

    while True:
        print(f"Обработка страницы {page}...")
        products = fetch_wb_products(query=query, page=page, spp=100)

        if not products:
            break

        for p in products:
            if p["id"] not in seen_ids:
                seen_ids.add(p["id"])
                all_products.append(p)

        page += 1

    with open("wb_thermopasta.json", "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
