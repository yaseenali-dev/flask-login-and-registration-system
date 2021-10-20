from .models import User
from faker import Faker
from .app import db

def g_user(counter=50):
    f = Faker()
    for _ in range(counter):
        email = f.email()
        name= f.user_name()
        u = User(name=name, email=email, password=email)
        db.session.add(u)
        db.session.commit()
        print(u)
