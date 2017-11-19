import datetime
import os
import peewee
from playhouse.db_url import connect
import markdown2


DB = connect(
    os.environ.get(                                         #how to connect the app database to the server
        'DATABASE_URL',
        'postgres://localhost:5432/crypto_database'
    )
)


class BaseModel(peewee.Model):
    """your base model will always stay the same. all the other tables will inhert from this."""
    class Meta:
        database = DB


class User(BaseModel):
    fname = peewee.CharField(max_length=60)
    lname = peewee.CharField(max_length=60)
    email = peewee.CharField(max_length=60)
    picture = peewee.CharField()

    # def __str__(self):
    #     return self.name


class Currency(BaseModel):
    """This will create the currency table with its respective details"""
    coin_pair = peewee.CharField(null=True)
    day_high = peewee.DecimalField(max_digits=20, decimal_places=10, null=True)
    day_low = peewee.DecimalField(max_digits=20, decimal_places=10, null=True)
    volume = peewee.DecimalField(max_digits=20, decimal_places=4, null=True)
    last_price = peewee.DecimalField(max_digits=20, decimal_places=10, null=True)
    base_volume = peewee.DecimalField(max_digits=20, decimal_places=10, null=True)
    bid_price = peewee.DecimalField(max_digits=20, decimal_places=10, null=True)
    ask_price = peewee.DecimalField(max_digits=20, decimal_places=10, null=True)
    open_buy = peewee.DecimalField(max_digits=20, decimal_places=0, null=True)
    open_sell = peewee.DecimalField(max_digits=20, decimal_places=0, null=True)
    prev_day = peewee.DecimalField(max_digits=20, decimal_places=10, null=True)

    # def __str__(self):
    #     return self.coin_name


class Market(BaseModel):
    currency = peewee.ForeignKeyField(Currency, null=True)
    coin_ticker = peewee.CharField(null=True)
    coin_base = peewee.CharField(null=True)
    coin_name = peewee.CharField(null=True)
    coin_pair = peewee.CharField(null=True)
    coin_active = peewee.CharField(null=True)
    coin_created = peewee.DateTimeField(null=True)
    coin_logo = peewee.CharField(null=True)


    # def __str__(self):
    #     return self.coin_ticker


class UserCurrency(BaseModel):
    """This table creates relations between user & currency classes"""
    user = peewee.ForeignKeyField(User, null=True)
    market = peewee.ForeignKeyField(Market, null=True)
    currency = peewee.ForeignKeyField(Currency, null=True)
