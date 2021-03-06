from Bytes import app , db
from Bytes.forms import RegistrationForm , LoginForm , UpdateUserForm ,NoOfPeople
from Bytes.models import User , Time , Train
from picture_handler import add_profile_pic
from flask import render_template, request, url_for, redirect , flash , abort
from flask_login import current_user, login_required, login_user , logout_user
import datetime
from sqlalchemy import asc , desc
import stripe


public_key = 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'

stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"


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
    x = datetime.datetime.now()
    week = {'Monday' : 1,'Tuesday' : 2,'Wednesday' : 3,'Thursday' : 4,'Friday' : 5,'Saturday' : 6,'Sunday' : 7}
    for t in time:
        if week[t.start.strftime('%A')] == week[x.strftime('%A')]:
            t.seats = 100
            db.session.commit()
        if t.start.strftime('%A') == day:
            m.append(t)

    return render_template('sched.htm' , m = m , x = x , week = week)

@app.route('/letsbookyayyyyyyyy/<timeid>/<ppl>' , methods = ['GET','POST'])
@login_required
def book(timeid,ppl):
    time = Time.query.get_or_404(timeid)
    time.seats = time.seats - int(ppl)
    current_user.timing.append(time)
    db.session.commit()
    return redirect(url_for('ticket' , people = ppl , timeid = timeid , time = time))

@app.route('/noofppl/<timeid>' , methods = ['GET' , 'POST'])
@login_required
def ppl(timeid):
    form = NoOfPeople()
    time = Time.query.get(timeid)
    if form.validate_on_submit():
        people = form.people.data
        if people > time.seats:
            abort(403)
        return redirect(url_for('book_ticket', people=people, timeid = timeid))
    return render_template('ppl.htm' , form = form)


################ STRIPE ########################

@app.route('/book-ticket/<people>/<timeid>' , methods = ['GET' , 'POST'])
@login_required
def book_ticket(people, timeid):
    time = Time.query.get_or_404(timeid)
    print(timeid)
    price = time.price *int(people)
    print(price)
    print(people)
    return render_template('reciept.html', public_key=public_key, people=people, time=time, timeid = timeid , price  =price)


@app.route('/payment/<people>/<timeid>', methods=['POST'])
@login_required
def payment(people, timeid):
    print(timeid)
    # CUSTOMER INFORMATION
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])

    # CHARGE/PAYMENT INFORMATION
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=1999,
        currency='usd',
        description='Booking'
    )

    return redirect(url_for('book' , ppl = people , timeid = timeid))


@app.route('/<time>/<timeid>/<people>/ticket' , methods = ['GET' , 'POST'])
@login_required
def ticket(time,timeid,people):
    t = Time.query.get(timeid)
    if current_user not in t.users:
        abort(403)
    return render_template('ticket.htm' , people = people , t = t)
##############################################

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
