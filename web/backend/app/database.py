from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@database:3306/guitardb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    __allow_unmapped__ = True

    product_id = Column(String(40), primary_key=True, index=True)
    name = Column(String(250))
    brand = Column(String(50))
    type = Column(String(50))
    description = Column(Text)
    img_url = Column(Text)

    attribute = relationship("Attribute", back_populates="product", uselist=False)
    offers = relationship("Offer", back_populates="product", uselist=False)

class Attribute(Base):
    __tablename__ = "attributes"
    __allow_unmapped__ = True

    attribute_id = Column(Integer, primary_key=True, index=True)
    article = Column(String(50))
    country = Column(String(50))
    design = Column(String(100))
    body_material = Column(String(100))
    neck_material = Column(String(100))
    number_of_strings = Column(Integer)
    pickups = Column(String(100))
    number_of_frets = Column(Integer)

    product_id = Column(Integer, ForeignKey('products.product_id', onupdate='CASCADE', ondelete='SET NULL'), nullable=True)
    product = relationship("Product", back_populates="attribute", uselist=False)

class Offer(Base):
    __tablename__ = "offers"
    __allow_unmapped__ = True

    offer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250))
    website_name = Column(String(50))
    price = Column(Integer)
    url = Column(Text)

    product_id = Column(Integer, ForeignKey('products.product_id', onupdate='CASCADE', ondelete='SET NULL'), nullable=True)
    product = relationship("Product", back_populates="offers", uselist=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()