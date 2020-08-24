from Bytes import app , db
from Bytes.forms import RegistrationForm , LoginForm
from Bytes.models import User
from picture_handler import add_profile_pic
from flask import render_template, request, url_for, redirect
from flask_login import current_user, login_required, login_user , logout_user

@app.route('/', methods=['GET', 'POST'])
def index():
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
