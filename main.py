from flask import Blueprint, render_template
from flask_login import login_required, current_user
from config import create_app, db
import commands

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/patient')
@login_required
def patient():
    return render_template('patient.html', name=current_user.name)


app = create_app()

commands.init_app(app)

if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True)
