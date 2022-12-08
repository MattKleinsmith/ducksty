from flask import Flask, render_template, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from .models import db, User, Product, Review, ProductImage
from .config import Config
from .user_form import LoginForm
from .routes import api
from .review_form import ReviewForm
from flask import jsonify

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(api.bp)
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return "<h1>Homepage</h1>"


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
    return "login page error"


@app.route("/logout", methods=["POST"])
def logout():
    # flask_login.current_user.logout()
    logout_user()
    return redirect('/login')


@app.route("/api/products/<int:product_id>/reviews", methods=["get", "post"])
def review(product_id):
    product = Product.query.filter(Product.id == product_id).all()
    reviews = Review.query.filter(Review.product_id == product_id).all()
    result = [review.to_dict() for review in reviews]
    jsonify(result)

    form = ReviewForm()
    if form.validate_on_submit():
        new_review = Review(
            user_id= product[0].user_id,
            product_id=product_id,
            rating=form.data["rating"],
            review= form.data["review"]
        )
        db.session.add(new_review)
        db.session.commit()
        return {"review": new_review.to_dict()}, 200, {"Content-Type": "application/json" }

    if form.errors:
        return {"errors": form.errors}, 400, {"Content-Type": "application/json" }

    return {"Reviews": result}

@app.route("/api/reviews/<int:review_id>", methods=["patch"])
def update_review(review_id):
    return

@app.route("/api/reviews/<int:review_id>", methods=["delete"])
def delete_review(review_id):
    review_tobe_deleted = Review.query.get(review_id)
    db.session.delete(review_tobe_deleted)
    db.session.commit()
    return {
        "message": "Successfully deleted",
        "statusCode": 200
        }, 200, {"Content-Type": "application/json" }
