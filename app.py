from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

from extensions import db, login_manager
from models import User, Application ,   Job
#from models import Job

app = Flask(__name__)

# App configuration
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()

# User loader (ONLY ONE, VERY IMPORTANT)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']

        user = User(name=name, email=email, password=password, role=role)

        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. Please login.')
            return redirect(url_for('login'))

        except IntegrityError:
            db.session.rollback()
            flash('Email already registered. Please login.')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))

        flash('Invalid credentials')

    return render_template('login.html')


@app.route('/student')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        return "Unauthorized Access", 403

    return render_template('student_dashboard.html')

@app.route('/student/jobs')
@login_required
def student_jobs():
    if current_user.role != 'student':
        return "Unauthorized Access", 403
    
    jobs = Job.query.all()
    return render_template('student_jobs.html', jobs=jobs)

@app.route('/student/application')
@login_required
def student_applications():
    if current_user.role != 'student':
        return "Unauthorized Access", 403
    
    applications = Application.query.filter_by(user_id = current_user.id).all()
    jobs = {j.id: j for j in Job.query.all()}

    return render_template(
        'student_applications.html',
        applications = applications,
        jobs = jobs
    )

@app.route('/student/apply/<int:job_id>')
@login_required
def apply_job(job_id):
    if current_user.role != 'student':
        return "Unauthorized Access", 403
    
    existing = Application.query.filter_by(
        user_id=current_user.id,
        job_id=job_id
    ).first()

    if existing:
        flash('You have already applied for this job')
        return redirect(url_for('student_jobs'))
    
    applicaton = Application(
        user_id = current_user.id,
        job_id = job_id
    )

    db.session.add(applicaton)
    db.session.commit()

    flash('Application submitted successfully')
    return redirect(url_for('student_jobs'))

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return "Unauthorized Access", 403

    return render_template('admin_dashboard.html')

@app.route('/admin/jobs', methods=['GET', 'POST'])
@login_required
def admin_jobs():
    if current_user.role != 'admin':
        return "Unauthorized Access", 403
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        job = Job(title=title, description=description)
        db.session.add(job)
        db.session.commit()

        flash('Job added successfully')

    jobs = Job.query.all()
    return render_template('admin_jobs.html', jobs=jobs)

@app.route('/admin/applications')
@login_required
def admin_application():
    if current_user.role != 'admin':
        return "Unauthorized Access", 403
    
    applications = Application.query.all()
    users = {u.id: u for u in User.query.all()}
    jobs = {j.id: j for j in Job.query.all()}

    return render_template(
        'admin_applications.html',
        applications = applications,
        users = users,
        jobs = jobs
    )

@app.route('/admin/application/<int:app_id>/<status>')
@login_required
def update_application_status(app_id, status):
    if current_user.role != 'admin':
        return "Unauthorized Access", 403
    
    application = Application.query.get_or_404(app_id)
    application.status = status
    db.session.commit()

    flash(f'Application {status}')
    return redirect(url_for('admin_application'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

 
# --------------- END -------------------

if __name__ == '__main__':
    app.run(debug=True)
