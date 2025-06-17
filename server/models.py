from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

# --------------------
# Customer Model
# --------------------
class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Relationships
    reviews = relationship("Review", back_populates="customer")

    # Association Proxy
    items = association_proxy('reviews', 'item')

    # Serialization Rules
    serialize_rules = ('-reviews.customer',)

    def __repr__(self):
        return f"<Customer {self.id}, {self.name}>"

# --------------------
# Item Model
# --------------------
class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    # Relationships
    reviews = relationship("Review", back_populates="item")

    # Serialization Rules
    serialize_rules = ('-reviews.item',)

    def __repr__(self):
        return f"<Item {self.id}, {self.name}, {self.price}>"

# --------------------
# Review Model
# --------------------
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    comment = Column(String)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    item_id = Column(Integer, ForeignKey('items.id'))

    # Relationships
    customer = relationship("Customer", back_populates="reviews")
    item = relationship("Item", back_populates="reviews")

    # Serialization Rules
    serialize_rules = ('-customer.reviews', '-item.reviews',)

    def __repr__(self):
        return f"<Review {self.id}, Customer {self.customer_id}, Item {self.item_id}>"
