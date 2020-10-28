# project/server/user/views.py


from flask import render_template, Blueprint, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from project.server import bcrypt, db
from project.server.models import User, Stratigraphy
from project.server.utils import row2dict
from project.server.user.forms import LoginForm, RegisterForm, RemoveUser, StratForm
from project.server.user.tables import IndexTable


user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/admin", methods=["GET"])
@login_required
def admin():
    user_list = db.session.query(User.id, User.username, User.email).order_by(User.id)
    #register_form = RegisterForm(request.form)
    #remove_form = RemoveUser(request.form)
    return render_template("user/admin.html", user_list = user_list, register_form=RegisterForm(), remove_form=RemoveUser())

@user_blueprint.route("/admin/register", methods=["POST"])
@login_required
def register():
    user_list = db.session.query(User.id, User.username, User.email).order_by(User.id)
    register_form = RegisterForm(request.form)
    #remove_form = RemoveUser(request.form)
    if register_form.validate_on_submit():
        User.create(
           username=register_form.username.data,
           email=register_form.email.data,
           password=register_form.password.data
        )
        flash("Successfully registered new user.", "success")
        return redirect(url_for("user.admin"))
    return render_template("user/admin.html", user_list = user_list, register_form=register_form, remove_form=RemoveUser())

@user_blueprint.route("/admin/remove", methods=["POST"])
@login_required
def remove():        
    user_list = db.session.query(User.id, User.username, User.email).order_by(User.id)
    #register_form = RegisterForm(request.form)
    remove_form = RemoveUser(request.form)
    if remove_form.validate_on_submit():
        user = User.query.filter_by(username=remove_form.username.data).first()
        user.delete()
        flash(f"successfully removed {user}.", "success")
        return redirect(url_for("user.admin"))

    return render_template("user/admin.html", user_list = user_list, register_form=RegisterForm(), remove_form=remove_form)


@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(
            user.password, request.form["password"]
        ):
            login_user(user)
            flash("You are logged in. Welcome!", "success")
            return redirect(url_for("user.index"))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template("user/login.html", form=form)
    return render_template("user/login.html", title="Please Login", form=form)


@user_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out. Bye!", "success")
    return redirect(url_for("main.home"))


@user_blueprint.route("/data_entry", methods=["GET", "POST"])
@login_required
def data_entry():
    
    return render_template("user/data_entry.html", entry_form=StratForm())

@user_blueprint.route("/data_entry/new", methods=["GET", "POST"])
@login_required
def new_entry():
    "Enter Strat data into the db"

    entry_form = StratForm(request.form)
    if request.method == "POST" and entry_form.validate_on_submit():
        strat_no = Stratigraphy.query.filter_by(strat_no=entry_form.strat_no.data).first()
        if not strat_no:
            Stratigraphy.create(
                unit_name= entry_form.unit_name.data,
                ASUD_No=entry_form.ASUD_No.data,
                ASUD_definition_card=entry_form.ASUD_definition_card.data,
                strat_no=entry_form.strat_no.data,
                map_symbol=entry_form.map_symbol.data,
                province=entry_form.province.data,
                domain=entry_form.domain.data,
                unit_description=entry_form.unit_description.data,
                unit_summary=entry_form.unit_summary.data,
                type_locality=entry_form.type_locality.data,
                unit_definition=entry_form.unit_definition.data,
                unit_correlation=entry_form.unit_correlation.data,
                unit_distribution=entry_form.unit_distribution.data,
                unit_thickness=entry_form.unit_thickness.data,
                unit_lithology=entry_form.unit_lithology.data,
                unit_deposition_env=entry_form.unit_deposition_env.data,
                unit_contact_relations=entry_form.unit_contact_relations.data,
                unit_geochronology=entry_form.unit_geochronology.data,
                unit_geochemistry=entry_form.unit_geochemistry.data,
                unit_geophysical_expression=entry_form.unit_geophysical_expression.data,
                references=entry_form.references.data,
                compiler_id=current_user.get_id()
            )
            flash("You have successfully entered a new unit description", "success")
            return redirect(url_for("user.index"))
        else:
            flash("That SA Strat No already exists","warning")
            return redirect(url_for("user.data_entry"))
                
    return render_template("user/data_entry.html", entry_form=entry_form)


@user_blueprint.route("/view/<int:id>", methods=["GET", "POST"])
@login_required
def view(id):
    record = Stratigraphy.query.filter_by(id=id).first()
    record_dict = row2dict(record)
    if record:

        return render_template("user/view_record.html", record=record_dict)

    return render_template("user/index.html")


@user_blueprint.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    record = Stratigraphy.query.filter_by(id=id).first()
    form = StratForm(request.form, obj=record)
    if record:
        if request.method == "POST" and form.validate_on_submit():
            form.populate_obj(record)
            Stratigraphy.update(record)
            flash("Record updated", "success")
            return redirect(url_for('user.index'))
        return render_template('user/edit_record.html', entry_form=form)
    else:
        flash("Error loading record #{id}".format(id=id), "warning")
        
    return render_template("user/index.html")


@user_blueprint.route("/index")
@login_required
def index():
    entry_count = db.session.query(Stratigraphy.id).count()
    entry_list = db.session.query(
                Stratigraphy.id, Stratigraphy.unit_name, Stratigraphy.strat_no,
                Stratigraphy.map_symbol).order_by(Stratigraphy.map_symbol)
    table = IndexTable(entry_list)

    return render_template("user/index.html", entry_count=entry_count, table=table)