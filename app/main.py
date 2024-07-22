from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from .scraper import Scraper
from .settings import Settings
from .models import Product, get_db, create_db_and_tables
from .notifier import notify

app = FastAPI()

settings = Settings()

STATIC_AUTH_TOKEN = settings.static_auth_token

async def get_token_header(authorization: str = Header(...)):
    if authorization != f"Bearer {STATIC_AUTH_TOKEN}":
        raise HTTPException(status_code=403, detail="Invalid token")

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

@app.get("/scrape/", dependencies=[Depends(get_token_header)])
async def scrape(pages: int = 1, proxy: str = None, db: Session = Depends(get_db)):
    scraper = Scraper(base_url="https://dentalstall.com/shop/", pages=pages, proxy=proxy)
    products = scraper.scrape()

    updated_count = 0
    total_count = 0
    for product_data in products:
        title = product_data.product_title
        price = product_data.product_price
        image_path = product_data.path_to_image
        total_count += 1

        existing_product = db.query(Product).filter(Product.product_title == title).first()
        if existing_product:
            if existing_product.product_price != price:
                existing_product.product_price = price
                existing_product.path_to_image = image_path
                db.add(existing_product)
                db.commit()
                updated_count += 1
        else:
            new_product = Product(
                product_title=title,
                product_price=price,
                path_to_image=image_path
            )
            db.add(new_product)
            db.commit()
            updated_count += 1

    scraper.save_to_json(products)
    notify(f"Scraping completed. {updated_count} products were scraped and updated in DB.")
    return {"status": "success", "updated_count": updated_count, 'total_count': total_count}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)