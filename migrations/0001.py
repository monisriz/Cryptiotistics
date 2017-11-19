import sys
import models
import peewee
from playhouse.migrate import migrate, PostgresqlMigrator

def forward():
    models.DB.create_tables([models.User, models.Currency, models.Market, models.UserCurrency])


if __name__ == '__main__':
    forward()
