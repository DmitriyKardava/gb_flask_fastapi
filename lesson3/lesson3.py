from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from models import db, User
from forms import RegisterForm
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydata.db'
app.config['SECRET_KEY'] = b"c35973ab51d70d92606019956aebc0bb6d042570ad271307b57a08151675ce59"
csrf = CSRFProtect(app)
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/register/", methods=["GET", "POST"])
def login():
    form = RegisterForm()
    if request.method == "POST" and form.validate():
        if request.form['password'] == request.form['repeat_password']:
            user = User()
            check_user = db.session.query(User).filter_by(email=request.form['email']).one_or_none()
            if not check_user:
                user.name = request.form['name']
                user.surname = request.form['surname']
                user.email = request.form['email']
                user.password = generate_password_hash(request.form['password'])
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("index"))
            else:
                flash('Такой пользователь уже существует')
    return render_template('register.html', form=form)
