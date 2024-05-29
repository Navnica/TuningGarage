import peewee
import datetime

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
    license_plate = peewee.CharField()
    mark = peewee.CharField()
    model = peewee.CharField()
    year = peewee.CharField()


class Service(BaseModel):
    name = peewee.CharField()
    price = peewee.CharField()


class Order(BaseModel):
    vehicle = peewee.ForeignKeyField(Vehicle, backref='orders')
    done = peewee.BooleanField(default=False)
    created_date = peewee.DateTimeField(default=datetime.datetime.now().replace(second=0, microsecond=0))


class ServiceOrder(BaseModel):
    order = peewee.ForeignKeyField(Order, backref='service_orders')
    service = peewee.ForeignKeyField(Service, backref='service_orders')


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
    ServiceOrder,
    Report,
    Invoice
])
