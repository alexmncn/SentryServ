"""App views."""
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

blueprint = Blueprint('ini', __name__)


@login_manager.user_loader
def load_user(user_id):
    # Load user by ID.
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET'])
def home():
    # Home page.
    return render_template('index.html')

@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    # Login the user.
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            
            # Save ips temporaly
            #check = funciones.save_users_ips(current_user.username)
            # Send notification
            #message = f"{username} ha iniciado sesión en la web."
            #send_notis.send_noti(message, current_user.username)
            
            flash('Has iniciado sesión', 'success')
            return redirect(url_for("home"))
        else:
            flash('Credenciales incorrectas.\nPor favor, inténtalo de nuevo.', 'error')

    return render_template('login.html', form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    # Logout.
    logout_user()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    # Register new user.
    form = RegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if a user with the same username existing_user
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash ('El nombre de usuario ya está en uso.\nPor favor, elige otro.', 'danger')
            return redirect(url_for('register'))

        # Creates the new user instance and set password
        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('¡Te has registrado correctamente! Ahora puedes iniciar sesión.', 'success')
        
        # Send notifitacion
        message = f"{username} se ha registrado en la web."
        send_notis.send_noti(message, username)

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

