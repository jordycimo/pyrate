from flask import Flask, render_template, request, url_for, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "7E1cDNMEiFAKFHLG2wGTa2r0oHlGN16uze2Z8_UmnG_mZA"
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)


class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250), unique=True, nullable=False)
	password = db.Column(db.String(250), nullable=False)


db.init_app(app)


with app.app_context():
	db.create_all()


@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)


#@app.route('/register', methods=["GET", "POST"])
#def register():
#	if request.method == "POST":
#		user = Users(username=request.form.get("username"),
#					password=request.form.get("password"))
#		db.session.add(user)
#		db.session.commit()
#		return redirect(url_for("login"))
#	return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		user = Users.query.filter_by(
			username=request.form.get("username")).first()
		if user.password == request.form.get("password"):
			login_user(user)
			return redirect(url_for("home"))
	return render_template("login.html")


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))


@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def home(req_path):
    BASE_DIR = '/home/js/password/static/'
    abs_path = os.path.join(BASE_DIR, req_path)
    if not os.path.exists(abs_path):
        return abort(404)

    if os.path.isfile(abs_path):
        return send_file(abs_path)

    files = sorted(os.listdir(abs_path))

    return render_template("home.html", files=files)


if __name__ == "__main__":
	app.run()
