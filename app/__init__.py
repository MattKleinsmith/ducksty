from flask import Flask, render_template, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from .models import db, User, Product, Review, ProductImage
from .config import Config
from .user_form import LoginForm


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return "<h1>Homepage</h1>"


@app.route("/products")
def products():
    products = Product.query.all()
    return [product.to_dict() for product in products]


@app.route("/products/<product_id>/reviews")
def reviews_of_product(product_id):
    reviews = Review.query.filter(Review.product_id == product_id).all()
    return [review.to_dict() for review in reviews]


@app.route("/reviews")
def reviews():
    reviews = Review.query.all()
    return [review.to_dict() for review in reviews]


# Integrating Flask-Login
# Create the login manager
login = LoginManager(app)
# By default, when a user attempts to access a login_required view without being logged in,
# Flask-Login will flash a message and redirect them to the log in view.
login.login_view = ".login"


@login.user_loader
# Use load_user function to get User objects from the database
def load_user(id):
    return User.query.get(int(id))


@app.route("/login", methods=["GET", "POST"])
def login():
    # flask_login.current_user
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter(User.email == data["email"]).first()
        if not user or not user.check_password(data["password"]):
            return redirect("login")
        login_user(user)
        return user.to_dict()


@app.route("/logout", methods=["POST"])
def logout():
    # flask_login.current_user.logout()
    logout_user()
    return redirect('/login')
