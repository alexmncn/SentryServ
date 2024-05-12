"""Web view routes."""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from app.services.user import user_has_role
from app.forms import CredentialsForm
from app.services.pushover_notifications import send_noti

views_bp = Blueprint('views', __name__)


@views_bp.route('/private-panel')
@login_required
def private_panel():
    message = f"{current_user.username} ha accedido a Panel de Control."
    send_noti(message, current_user.username)

    return render_template('private-panel.html')

@views_bp.route('/statistics')
@login_required
def estadisticas():
    #enviamos notificación
    message = f"{current_user.username} ha accedido a Estadisticas."
    send_noti(message, current_user.username)

    return render_template('statistics.html')

@views_bp.route('/user/manage-credentials', methods=['GET', 'POST'])
@login_required
def manage_credentials():
    message = f"{current_user.username} ha accedido a Gestionar Credenciales"
    send_noti(message, current_user.username)

    form = CredentialsForm()

    if form.validate_on_submit():
        new_credential = Credentials(
            user_id = current_user.id,
            site = form.site.data,
            user = form.user.data,
            email = form.email.data,
            password = form.password.data,
            description = form.description.data
        )
        
        db.session.add(new_credential)
        db.session.commit()

        flash('La nueva credencial se ha guardado correctamente', 'error')

        return redirect(url_for(views.manage_credentials))

    return render_template('manage-credentials.html', form=form)
