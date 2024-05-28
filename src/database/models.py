import peewee

database = peewee.SqliteDatabase('database.db')


class BaseModel(peewee.Model):
    class Meta:
        database = database


class User(BaseModel):
    fullname = peewee.CharField(unique=True)
    role = peewee.CharField()


class UserAuth(BaseModel):
    user = peewee.ForeignKeyField(User, backref='auth_data')
    login = peewee.CharField(unique=True)
    password = peewee.CharField()


class Vehicle(BaseModel):
    owner_name = peewee.CharField()
    mark = peewee.CharField()
    model = peewee.CharField()
    year = peewee.CharField()


class Service(BaseModel):
    name = peewee.CharField()
    price = peewee.CharField()


class Order(BaseModel):
    vehicle = peewee.ForeignKeyField(Vehicle, backref='vehicles')
    service = peewee.ForeignKeyField(Service, backref='services')
    done = peewee.BooleanField(default=False)


class Report(BaseModel):
    from_user = peewee.ForeignKeyField(User, backref='reports')
    text = peewee.TextField()


class Invoice(BaseModel):
    full_price = peewee.FloatField()
    services = peewee.CharField()


database.create_tables([
    User,
    UserAuth,
    Vehicle,
    Service,
    Order,
    Report,
    Invoice
])
