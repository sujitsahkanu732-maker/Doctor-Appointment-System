"""
Doctor Appointment System - Main Application File
Flask web application for managing doctor appointments
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

# Initialize Flask application
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doctor_appointment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class User(db.Model):
    """User Model - Stores patient and doctor information"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))
    user_type = db.Column(db.String(20), nullable=False)  # 'patient' or 'doctor'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    # If user is a patient, they can have many appointments
    appointments_as_patient = db.relationship('Appointment', 
                                             foreign_keys='Appointment.patient_id',
                                             backref='patient', 
                                             lazy=True,
                                             cascade='all, delete-orphan')
    
    # If user is a doctor, they have doctor profile
    doctor_profile = db.relationship('Doctor', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class Doctor(db.Model):
    """Doctor Model - Stores doctor-specific information"""
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(200), nullable=False)
    experience = db.Column(db.Integer)  # Years of experience
    consultation_fee = db.Column(db.Float, nullable=False)
    available_days = db.Column(db.String(100))  # e.g., "Mon,Tue,Wed,Thu,Fri"
    available_time = db.Column(db.String(50))  # e.g., "9:00 AM - 5:00 PM"
    
    # Relationship with appointments
    appointments = db.relationship('Appointment', 
                                  foreign_keys='Appointment.doctor_id',
                                  backref='doctor', 
                                  lazy=True)
    
    def __repr__(self):
        return f'<Doctor {self.specialization}>'


class Appointment(db.Model):
    """Appointment Model - Stores appointment information"""
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Confirmed, Completed, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Appointment {self.id} - {self.status}>'


# ==================== HELPER FUNCTIONS ====================

def login_required(f):
    """Decorator to check if user is logged in"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    """Get current logged-in user"""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        user_type = request.form.get('user_type')
        
        # Validation
        if not all([username, email, password, full_name, user_type]):
            flash('All fields are required!', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long!', 'danger')
            return redirect(url_for('register'))
        
        # Check if user already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            flash('Username or email already exists!', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            full_name=full_name,
            phone=phone,
            user_type=user_type
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            
            # If registering as doctor, create doctor profile
            if user_type == 'doctor':
                specialization = request.form.get('specialization')
                qualification = request.form.get('qualification')
                experience = request.form.get('experience', 0)
                consultation_fee = request.form.get('consultation_fee', 0)
                available_days = request.form.get('available_days', 'Mon,Tue,Wed,Thu,Fri')
                available_time = request.form.get('available_time', '9:00 AM - 5:00 PM')
                
                doctor_profile = Doctor(
                    user_id=new_user.id,
                    specialization=specialization,
                    qualification=qualification,
                    experience=int(experience),
                    consultation_fee=float(consultation_fee),
                    available_days=available_days,
                    available_time=available_time
                )
                db.session.add(doctor_profile)
                db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')
            return redirect(url_for('register'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please provide both username and password!', 'danger')
            return redirect(url_for('login'))
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            # Create session
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_type'] = user.user_type
            
            flash(f'Welcome back, {user.full_name}!', 'success')
            
            # Redirect based on user type
            if user.user_type == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            else:
                return redirect(url_for('patient_dashboard'))
        else:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


@app.route('/patient/dashboard')
@login_required
def patient_dashboard():
    """Patient dashboard"""
    user = get_current_user()
    
    if user.user_type != 'patient':
        flash('Access denied!', 'danger')
        return redirect(url_for('index'))
    
    # Get patient's appointments
    appointments = Appointment.query.filter_by(patient_id=user.id).order_by(
        Appointment.appointment_date.desc()
    ).all()
    
    return render_template('patient_dashboard.html', user=user, appointments=appointments)


@app.route('/doctor/dashboard')
@login_required
def doctor_dashboard():
    """Doctor dashboard"""
    user = get_current_user()
    
    if user.user_type != 'doctor':
        flash('Access denied!', 'danger')
        return redirect(url_for('index'))
    
    # Get doctor's appointments
    doctor_profile = Doctor.query.filter_by(user_id=user.id).first()
    appointments = Appointment.query.filter_by(doctor_id=doctor_profile.id).order_by(
        Appointment.appointment_date.desc()
    ).all()
    
    return render_template('doctor_dashboard.html', user=user, doctor=doctor_profile, appointments=appointments)


@app.route('/doctors')
@login_required
def view_doctors():
    """View all available doctors"""
    doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors)


@app.route('/book-appointment/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def book_appointment(doctor_id):
    """Book an appointment with a doctor"""
    user = get_current_user()
    
    if user.user_type != 'patient':
        flash('Only patients can book appointments!', 'danger')
        return redirect(url_for('index'))
    
    doctor = Doctor.query.get_or_404(doctor_id)
    
    if request.method == 'POST':
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        reason = request.form.get('reason')
        
        if not all([appointment_date, appointment_time, reason]):
            flash('All fields are required!', 'danger')
            return redirect(url_for('book_appointment', doctor_id=doctor_id))
        
        # Create appointment
        new_appointment = Appointment(
            patient_id=user.id,
            doctor_id=doctor_id,
            appointment_date=datetime.strptime(appointment_date, '%Y-%m-%d').date(),
            appointment_time=appointment_time,
            reason=reason,
            status='Pending'
        )
        
        try:
            db.session.add(new_appointment)
            db.session.commit()
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('patient_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to book appointment: {str(e)}', 'danger')
    
    return render_template('book_appointment.html', doctor=doctor)


@app.route('/appointment/cancel/<int:appointment_id>')
@login_required
def cancel_appointment(appointment_id):
    """Cancel an appointment"""
    appointment = Appointment.query.get_or_404(appointment_id)
    user = get_current_user()
    
    # Check if user has permission
    if user.user_type == 'patient' and appointment.patient_id != user.id:
        flash('You cannot cancel this appointment!', 'danger')
        return redirect(url_for('patient_dashboard'))
    
    try:
        appointment.status = 'Cancelled'
        db.session.commit()
        flash('Appointment cancelled successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to cancel appointment: {str(e)}', 'danger')
    
    if user.user_type == 'patient':
        return redirect(url_for('patient_dashboard'))
    else:
        return redirect(url_for('doctor_dashboard'))


@app.route('/appointment/update/<int:appointment_id>/<status>')
@login_required
def update_appointment_status(appointment_id, status):
    """Update appointment status (for doctors)"""
    user = get_current_user()
    
    if user.user_type != 'doctor':
        flash('Only doctors can update appointment status!', 'danger')
        return redirect(url_for('index'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    doctor_profile = Doctor.query.filter_by(user_id=user.id).first()
    
    if appointment.doctor_id != doctor_profile.id:
        flash('You cannot update this appointment!', 'danger')
        return redirect(url_for('doctor_dashboard'))
    
    if status in ['Confirmed', 'Completed', 'Cancelled']:
        try:
            appointment.status = status
            db.session.commit()
            flash(f'Appointment status updated to {status}!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to update status: {str(e)}', 'danger')
    
    return redirect(url_for('doctor_dashboard'))


@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    user = get_current_user()
    doctor_profile = None
    
    if user.user_type == 'doctor':
        doctor_profile = Doctor.query.filter_by(user_id=user.id).first()
    
    return render_template('profile.html', user=user, doctor=doctor_profile)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    user = get_current_user()
    
    if request.method == 'POST':
        user.full_name = request.form.get('full_name', user.full_name)
        user.email = request.form.get('email', user.email)
        user.phone = request.form.get('phone', user.phone)
        
        # If doctor, update doctor profile
        if user.user_type == 'doctor':
            doctor_profile = Doctor.query.filter_by(user_id=user.id).first()
            if doctor_profile:
                doctor_profile.specialization = request.form.get('specialization', doctor_profile.specialization)
                doctor_profile.qualification = request.form.get('qualification', doctor_profile.qualification)
                doctor_profile.experience = int(request.form.get('experience', doctor_profile.experience))
                doctor_profile.consultation_fee = float(request.form.get('consultation_fee', doctor_profile.consultation_fee))
        
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to update profile: {str(e)}', 'danger')
    
    doctor_profile = None
    if user.user_type == 'doctor':
        doctor_profile = Doctor.query.filter_by(user_id=user.id).first()
    
    return render_template('edit_profile.html', user=user, doctor=doctor_profile)


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500


# ==================== DATABASE INITIALIZATION ====================

def init_db():
    """Initialize database with sample data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if data already exists
        if User.query.count() == 0:
            # Create sample doctors
            doctors_data = [
                {
                    'username': 'dr_sharma',
                    'email': 'sharma@hospital.com',
                    'password': generate_password_hash('doctor123'),
                    'full_name': 'Dr. Rajesh Sharma',
                    'phone': '9841234567',
                    'user_type': 'doctor',
                    'specialization': 'Cardiologist',
                    'qualification': 'MBBS, MD (Cardiology)',
                    'experience': 10,
                    'consultation_fee': 1500.0
                },
                {
                    'username': 'dr_patel',
                    'email': 'patel@hospital.com',
                    'password': generate_password_hash('doctor123'),
                    'full_name': 'Dr. Priya Patel',
                    'phone': '9841234568',
                    'user_type': 'doctor',
                    'specialization': 'Pediatrician',
                    'qualification': 'MBBS, MD (Pediatrics)',
                    'experience': 8,
                    'consultation_fee': 1200.0
                },
                {
                    'username': 'dr_kumar',
                    'email': 'kumar@hospital.com',
                    'password': generate_password_hash('doctor123'),
                    'full_name': 'Dr. Amit Kumar',
                    'phone': '9841234569',
                    'user_type': 'doctor',
                    'specialization': 'Orthopedic',
                    'qualification': 'MBBS, MS (Orthopedics)',
                    'experience': 12,
                    'consultation_fee': 2000.0
                }
            ]
            
            for doc_data in doctors_data:
                user = User(
                    username=doc_data['username'],
                    email=doc_data['email'],
                    password=doc_data['password'],
                    full_name=doc_data['full_name'],
                    phone=doc_data['phone'],
                    user_type=doc_data['user_type']
                )
                db.session.add(user)
                db.session.flush()
                
                doctor = Doctor(
                    user_id=user.id,
                    specialization=doc_data['specialization'],
                    qualification=doc_data['qualification'],
                    experience=doc_data['experience'],
                    consultation_fee=doc_data['consultation_fee'],
                    available_days='Mon,Tue,Wed,Thu,Fri',
                    available_time='9:00 AM - 5:00 PM'
                )
                db.session.add(doctor)
            
            # Create sample patient
            patient = User(
                username='patient1',
                email='patient1@email.com',
                password=generate_password_hash('patient123'),
                full_name='John Doe',
                phone='9841234570',
                user_type='patient'
            )
            db.session.add(patient)
            
            db.session.commit()
            print("Database initialized with sample data!")


# ==================== MAIN ====================

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)