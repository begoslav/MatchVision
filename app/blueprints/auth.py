from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

class RegistrationForm(FlaskForm):
    """Registration form"""
    username = StringField('Uživatelské jméno', 
                          validators=[
                              DataRequired(message='Vyplňte uživatelské jméno'),
                              Length(min=3, max=80, message='Uživatelské jméno musí mít 3-80 znaků')
                          ])
    email = StringField('E-mail', 
                       validators=[
                           DataRequired(message='Vyplňte e-mail'),
                           Email(message='Zadejte platný e-mail')
                       ])
    password = PasswordField('Heslo', 
                            validators=[
                                DataRequired(message='Vyplňte heslo'),
                                Length(min=6, message='Heslo musí mít alespoň 6 znaků')
                            ])
    confirm_password = PasswordField('Potvrzení hesla',
                                    validators=[
                                        DataRequired(message='Potvrďte heslo'),
                                        EqualTo('password', message='Hesla se neshodují')
                                    ])
    submit = SubmitField('Zaregistrovat se')
    
    def validate_username(self, username):
        """Check if username already exists"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Toto uživatelské jméno je již obsazeno.')
    
    def validate_email(self, email):
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('E-mail je již zaregistrován.')

class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Uživatelské jméno', validators=[DataRequired(message='Vyplňte uživatelské jméno')])
    password = PasswordField('Heslo', validators=[DataRequired(message='Vyplňte heslo')])
    submit = SubmitField('Přihlásit se')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registrace byla úspěšná! Nyní se můžete přihlásit.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Chyba při registraci. Zkuste to znovu.', 'danger')
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login user"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Špatné uživatelské jméno nebo heslo.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('Byli jste odhlášeni.', 'info')
    return redirect(url_for('main.index'))
