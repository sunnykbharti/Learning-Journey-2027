from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import datetime
from models import db, Users, Patient, Doctor

#creating the app and defining th path of db
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin.sqlite'
app.config["SECRET_KEY"] = "supersecretkey"

#initialising database and login manager
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        id = request.form.get("id")
        username = request.form.get("username")
        password = request.form.get("password")

        if Users.query.filter_by(username=username).first():
            return render_template("register.html", error="Username already taken!")

        new_user = Users(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")


@app.route('/login', methods=["GET","POST"])
def login():
    time=datetime.datetime.now()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        if user and user.password==password :
            login_user(user)
            return redirect(url_for("reception"))
        else:
            return render_template("login.html", error = "Invalid username or password!", time=time)
    return render_template('login.html',time=time)

@app.route('/reception', methods=["GET","POST"])
def reception():
    time = datetime.datetime.now()
    return render_template("reception.html",time=time)

@app.route('/logout', methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/admission', methods=["GET","POST"])
def admission():
    if request.method == "POST":
        name = request.form.get("name")
        uhid = request.form.get("uhid")
        aadhar = request.form.get("aadhar")
        city = request.form.get("city")
        state = request.form.get("state")
        mobile = request.form.get("mobile")
        emergency = request.form.get("emergency")
        doctor = request.form.get("doctor")
        department = request.form.get("department")
        docid = request.form.get("docid")
        date = request.form.get("date")

        newp = Patient(name=name, uhid=uhid, aadhar=aadhar, city=city, state=state, mobile=mobile, emergency=emergency, doctor=doctor, department=department, docid=docid, date=date)
        db.session.add(newp)
        db.session.commit()

        return redirect(url_for("reception"))
    return redirect(url_for("reception"))

if __name__=="__main__":
    app.run(debug=True)