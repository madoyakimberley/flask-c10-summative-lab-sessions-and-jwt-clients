from app import app
from models import db, User, Note
#As the name a python lib that generates fake data

from faker import Faker


fake = Faker()

with app.app_context():
    db.drop_all()
    db.create_all()

    users = []

    for i in range(3):
        user = User(username=fake.user_name())
        user.set_password("1234")
        db.session.add(user)
        users.append(user)

    db.session.commit()

    for user in users:
        for _ in range(5):
            note = Note(
                title=fake.sentence(),
                content=fake.text(),
                user_id=user.id
            )
            db.session.add(note)

    db.session.commit()

    print("Seeding was successfull >,<")