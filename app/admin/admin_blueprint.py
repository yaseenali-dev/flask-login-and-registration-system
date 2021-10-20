from flask import Blueprint, render_template
from flask_login import login_required
from ..decorators import admin_required

admin_blueprint = Blueprint('admin_blueprint', __name__)

@admin_blueprint.get('/admin')
@login_required
@admin_required
def admin():
    return render_template('admin/admin.html')
