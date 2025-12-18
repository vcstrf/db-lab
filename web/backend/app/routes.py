from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session, contains_eager
from sqlalchemy import or_, and_, func
from app.database import Product, Offer, Attribute, get_db

router = APIRouter()

@router.get("/search/")
async def search(search_query: str, db: Session = Depends(get_db)):
    
    query = db.query(Product).join(Attribute).options(
        contains_eager(Product.attribute)
    )

    if search_query:
        search_query = search_query.strip().lower()
        
        if search_query:
            words = search_query.split()
            conditions = []
            
            for word in words:
                if len(word) >= 1:
                    word_pattern = f"%{word}%"
                    word_conditions = [
                        Product.name.ilike(word_pattern),
                        Product.brand.ilike(word_pattern),
                        Product.type.ilike(word_pattern),
                        Attribute.design.ilike(word_pattern)
                    ]

                    conditions.append(or_(*word_conditions))

            if conditions:
                query = query.filter(and_(*conditions))

            query = query.order_by(
                func.nullif(Product.name.ilike(search_query), True),
                func.nullif(Product.name.ilike(f"{search_query}%"), True),
                func.nullif(and_(*[Product.name.ilike(f"%{word}%") for word in words]), True),
                func.nullif(and_(or_(*[Product.brand.ilike(f"%{word}%") for word in words]), or_(*[Attribute.design.ilike(f"%{word}%") for word in words])), True),
                func.nullif(or_(*[Product.brand.ilike(f"%{word}%") for word in words]), True),
                func.nullif(or_(*[Attribute.design.ilike(f"%{word}%") for word in words]), True),
                func.nullif(or_(*[Product.name.ilike(f"%{word}%") for word in words]), True),
                Product.name
            )
    
    results = query.all()

    return [{
        "id": r.product_id,
        "name": r.name,
        "brand": r.brand,
        "type": r.type,
        "design": r.attribute.design,
        "img_url": r.img_url
    } for r in results]

@router.get("/product/offers/id")
def get_offers(product_id: int, db: Session = Depends(get_db)):
    query = db.query(Offer)

    if product_id:
        query = query.filter(Offer.product_id == product_id)

    results = query.all()
    
    return [{
        "id": r.offer_id,
        "name": r.name,
        "shop": r.website_name,
        "price": r.price,
        "url": r.url
        } for r in results
    ] 

@router.get("/product/attributes/id")
def get_attributes(product_id: int, db: Session = Depends(get_db)):
    query = db.query(Attribute).join(Product).options(
        contains_eager(Attribute.product)
    )

    if product_id:
        query = query.filter(Attribute.product_id == product_id)

        results = query.all()
    
    return [{
        "id": r.attribute_id,
        "type": r.product.type,
        "country": r.country,
        "design": r.design,
        "body_material": r.body_material,
        "neck_material": r.neck_material,
        "number_of_strings": r.number_of_strings,
        "pickups": r.pickups,
        "number_of_frets": r.number_of_frets
        } for r in results
    ] 
