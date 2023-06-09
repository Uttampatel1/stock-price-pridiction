from flask import render_template, request, Blueprint , make_response
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    if current_user.is_authenticated:
        return render_template('home.html', title="Home", user=current_user)
    return render_template('home.html', title="Home" , user=None)

@main.route('/about')
def about():
    return render_template("about.html",title="About")

@main.route('/announcements')
def announcements():
    return render_template('announcements.html')

@main.route('/toggle-dark-mode')
def toggle_dark_mode():
    response = make_response("Dark mode toggled")
    if request.cookies.get('dark_mode') == 'enabled':
        response.set_cookie('dark_mode', 'disabled')
    else:
        response.set_cookie('dark_mode', 'enabled')
    return response
