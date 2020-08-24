from flask import render_template,request, url_for, redirect
from flask_login import current_user, login_required, login_user , logout_user\



if __name__ == '__main__':
    socketio.run(app,debug=True)
