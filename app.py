from Bytes import app , db
from Bytes.forms import RegistrationForm , LoginForm , UpdateUserForm
from Bytes.models import User , Time , Train
from picture_handler import add_profile_pic
from flask import render_template, request, url_for, redirect , flash
from flask_login import current_user, login_required, login_user , logout_user
import datetime
from sqlalchemy import asc , desc
@app.route('/', methods=['GET', 'POST'])
def index():
    time = Time.query.get(5)
    time.start = datetime.datetime(2020, 8, 26, 16, 50)
    time.end = datetime.datetime(2020, 8, 25, 17, 30)
    time = Time.query.get(6)
    time.start = datetime.datetime(2020, 8, 26, 17, 35)
    time.end = datetime.datetime(2020, 8, 25, 18, 5)
    time = Time.query.get(7)
    time.start = datetime.datetime(2020, 8, 26, 18, 10)
    time.end = datetime.datetime(2020, 8, 25, 18, 45)
    time = Time.query.get(4)
    db.session.delete(time)
    db.session.commit()
    return render_template("index.htm")

@app.route('/register' , methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(name = form.name.data,
                    username = form.username.data,
                    email = form.email.data ,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        if form.picture.data is not None:
            id = user.id
            pic = add_profile_pic(form.picture.data,id)
            user.profile_image = pic
            db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.htm', form = form)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/login' , methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    error = ''
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data) :

            login_user(user)
            flash('Log in Success!')

            next = request.args.get('next')
            if next == None or not next[0] =='/':
                next = url_for('index')
            return redirect(next)
        elif user is not None and user.check_password(form.password.data) == False:
            error = 'Wrong Password'
        elif user is None:
            error = 'No such login Pls create one'

    return render_template('login.htm', form=form, error = error)

@app.route('/account',methods = ['GET','POST'])
@login_required
def account():
    pic = current_user.profile_image
    form = UpdateUserForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data


        if form.picture.data is not None:
            id = current_user.id
            pic = add_profile_pic(form.picture.data,id)
            current_user.profile_image = pic

        flash('User Account Created')
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename= current_user.profile_image)
    return render_template('account.htm', profile_image=profile_image, form=form, pic = pic)

@app.route('/sched/<day>' , methods = ['GET' , 'POST' ])
@login_required
def sched(day):
    time = Time.query.order_by(Time.start.asc())
    m = []
    for t in time:
        print(t.start.strftime('%A'))
        if t.start.strftime('%A') == day:
            m.append(t)

    return render_template('sched.htm' , m = m)


###########################################


@app.errorhandler(404)
def page_not_found(e):
    return render_template('Error/404.html'), 404


@app.errorhandler(403)
def action_forbidden(e):
    return render_template('Error/403.html'), 403


@app.errorhandler(410)
def page_deleted(e):
    return render_template('Error/410.html'), 410


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('Error/500.html'), 500

##############################################


if __name__ == '__main__':
    app.run(debug=True)
