from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_file
from flask_login import login_required, current_user
from config import create_app, db
from werkzeug.utils import secure_filename
from models import Files
from io import BytesIO
import commands
import os

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/patient')
@login_required
def patient():
    return render_template('patient.html', name=current_user.name)


@main.route('/doctor')
@login_required
def doctor():
    return render_template('doctor.html', name=current_user.name)


@main.route('/patient', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    user_id = current_user.id

    if filename != '':
        uploaded_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        new_file = Files(file=filename, user_id=user_id, data=uploaded_file.read())
        db.session.add(new_file)
        db.session.commit()
        flash("File uploaded successfully")
    return render_template('patient.html', filename=filename)


@main.route('/view_reports', methods=['GET'])
def view_report():
    if request.method == 'GET':
        reports = Files.query.all()
        return render_template('viewreports.html', reports=reports)
    return render_template('viewreports.html')


@main.route('/display/<filename>')
def display_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename))


app = create_app()

commands.init_app(app)

if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True)
