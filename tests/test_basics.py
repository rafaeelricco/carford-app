
from app import app, db, User, Car, Person
from faker import Faker
fake = Faker()


def test_create_app():
    assert app is not None


def test_create_db():
    assert db is not None


def test_register_user():
    with app.app_context():
        user = User(username=fake.user_name(), password=fake.password())
        db.session.add(user)
        db.session.commit()
        assert user.id != 0


def test_login_user():
    with app.app_context():
        user = User.query.first()
        password = user.password
        assert user is not None
        assert password is not None


def test_delete_user():
    with app.app_context():
        user_to_delete = User.query.first().username
        user = User.query.filter_by(username=user_to_delete).first()
        db.session.delete(user)
        db.session.commit()
        assert User.query.filter_by(username=user_to_delete).first() is None

# Car CRUD


def test_add_car():
    with app.app_context():
        car = Car(name=fake.user_name(), color='Amarelo',
                  model='Sedan', owner_id=fake.random_int(min=1, max=100))
        db.session.add(car)
        db.session.commit()
        assert car.id != 0


def test_get_car():
    with app.app_context():
        car = Car.query.first()
        assert car is not None


def test_update_car():
    with app.app_context():
        car_name = Car.query.first().name
        car = Car.query.filter_by(name=car_name).first()
        car.name = fake.user_name()
        db.session.commit()
        assert Car.query.filter_by(name=car_name).first() is None


def test_delete_car():
    with app.app_context():
        car_name = Car.query.first().name
        car = Car.query.filter_by(name=car_name).first()
        db.session.delete(car)
        db.session.commit()
        assert Car.query.filter_by(name=car_name).first() is None

# Person CRUD


def test_add_person():
    with app.app_context():
        person = Person(name=fake.user_name())
        db.session.add(person)
        db.session.commit()
        assert person.id != 0


def test_get_person():
    with app.app_context():
        person = Person.query.first()
        assert person is not None


def test_update_person():
    with app.app_context():
        person_name = Person.query.first().name
        person = Person.query.filter_by(name=person_name).first()
        person.name = fake.user_name()
        db.session.commit()
        assert Person.query.filter_by(name=person_name).first() is None


def test_delete_person():
    with app.app_context():
        person_name = Person.query.first().name
        person = Person.query.filter_by(name=person_name).first()
        db.session.delete(person)
        db.session.commit()
        assert Person.query.filter_by(name=person_name).first() is None
