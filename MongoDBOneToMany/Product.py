from mongoengine import *
from decimal import Decimal
from PriceHistory import PriceHistory
from datetime import datetime


class Product(Document):
    productCode = StringField(db_field='product_code', max_length=15, required=True)
    productName = StringField(db_field='product_name', max_length=70, required=True)
    productDescription = StringField(db_field='product_description', max_length=800, required=True)
    quantityInStock = IntField(db_field='quantity_in_stock', min_value=0, required=True)
    buyPrice = Decimal128Field(db_field='buy_price', min_value=0.01, precision=2, required=True)
    msrp = Decimal128Field(db_field='msrp', min_value=0.01, precision=2, required=True)
    priceHistory = EmbeddedDocumentListField(PriceHistory, db_field='price_history')

    meta = {'collection': 'products',
            'indexes': [
                {'unique': True, 'fields': ['productCode'], 'name': 'products_pk'},
                {'unique': True, 'fields' : ['productName'], 'name': 'products_uk_01'}
            ]}


    def __init__(self, productCode: str, productName: str, productDescription: str, quantityInStock: int, buyPrice: Decimal, msrp: Decimal, *args, **values):
        super().__init__(*args, **values)
        self.productCode = productCode
        self.productName = productName
        self.productDescription = productDescription
        self.quantityInStock = quantityInStock
        self.buyPrice = buyPrice
        self.msrp = msrp


    def change_price(self, new: PriceHistory):
        if not self.priceHistory:
            self.priceHistory = [PriceHistory(self.buyPrice, datetime(1, 1, 1, 1, 1))]
        if self.priceHistory[-1].price == new.price:
            raise ValueError("New price is equivalent to current price.")
        elif new.price < Decimal(0.01):
            raise ValueError("New price below threshold of $0.01.")
        elif self.priceHistory[-1].priceChangeDate >= new.priceChangeDate:
            raise ValueError('New price change must occurr later than the latest status change.')
        elif new.priceChangeDate > datetime.utcnow():
            raise ValueError('The price change cannot occur in the future.')
        self.priceHistory.append(new)
        self.buyPrice = new.price


    def __str__(self):
        return (f"{self.productName} ({self.productCode}) - {self.productDescription}\n"
                f"{self.quantityInStock} in stock.\nPrice: ${self.buyPrice} - MSRP: ${self.msrp}")
