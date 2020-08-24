from Byte import app
from flask import render_template, request, url_for, redirect


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.htm")

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
    app.run(app, debug=True)
