import os
from flask import Flask, render_template, request, url_for, redirect, flash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Tables
class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    oportunity = db.Column(db.Boolean, default=True)


class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    color = db.Column(db.String(80), unique=False, nullable=False)
    model = db.Column(db.String(80), unique=False, nullable=False)
    owner = db.relationship('Person', backref=db.backref('cars', lazy=True))
    owner_id = db.Column(db.Integer, db.ForeignKey(
        'persons.id'), nullable=False, autoincrement=True)


# Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


# Routes
@app.route('/')
@login_required
def dashboard():
    get_persons = Person.query.all()
    get_cars = Car.query.all()
    return render_template('dashboard.html', get_persons=get_persons, get_cars=get_cars)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# CRUD Functions


@app.route('/add_person', methods=['GET', 'POST'])
@login_required
def add_person():
    if request.method == 'POST':
        name = request.form['owner_name']
        new_person = Person(name=name)
        db.session.add(new_person)
        db.session.commit()
        return redirect(url_for('dashboard'))


@app.route('/add_car', methods=['GET', 'POST'])
@login_required
def add_car():
    if request.method == 'POST':
        name = request.form['car_name']
        color = request.form['car_color']
        model = request.form['car_model']
        owner_id = request.form['car_owner']

        quantity = Car.query.filter_by(owner_id=owner_id).count()
        if quantity == 3:
            flash('This person already have 3 cars.')
            return redirect(url_for('dashboard'))

        update_oportunity = Person.query.filter_by(name=owner_id).first()
        update_oportunity.oportunity = False
        db.session.commit()
        new_car = Car(name=name, color=color,
                      model=model, owner_id=owner_id)
        db.session.add(new_car)
        db.session.commit()
        return redirect(url_for('dashboard'))


@app.route('/delete/<int:person_id>')
@login_required
def delete_person(person_id):
    person = Person.query.filter_by(id=person_id).first()
    cars_person = Car.query.filter_by(owner_id=person.name).all()

    if cars_person != []:
        for car in cars_person:
            db.session.delete(car)
            db.session.commit()

    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/delete_car/<int:car_id>')
@login_required
def delete_car(car_id):
    car = Car.query.filter_by(id=car_id).first()
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/update_owner/<int:person_id>', methods=['GET', 'POST'])
@login_required
def update_person(person_id):
    person = Person.query.filter_by(id=person_id).first()
    car = Car.query.filter_by(owner_id=person.name).first()
    if request.method == 'POST':
        person.name = request.form['owner_name']
        car.owner_id = person.name
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('update_owner.html', person=person, car=car)


@app.route('/update_car/<int:car_id>', methods=['GET', 'POST'])
@login_required
def update_car(car_id):
    car = Car.query.filter_by(id=car_id).first()
    persons = Person.query.all()
    if request.method == 'POST':
        car.name = request.form['car_name']
        car.color = request.form['car_color']
        car.model = request.form['car_model']
        car.owner_id = request.form['car_owner']
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('update_car.html', car=car, persons=persons)


if __name__ == "__main__":
    app.run(debug=True)
