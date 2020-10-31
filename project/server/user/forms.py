# project/server/user/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, InputRequired, Optional


class LoginForm(FlaskForm):
    username = StringField("User Name", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField(
        "User Name",
        validators=[
            DataRequired()
        ]
    )
    
    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(message=None),
            Length(min=6, max=40),
        ],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )


class RemoveUser(FlaskForm):
    username = StringField("User Name", [DataRequired()])


class RemoveRecord(FlaskForm):
    strat_no = IntegerField("SA Strat No", [DataRequired()])


class StratForm(FlaskForm):
    unit_name = StringField("Unit Name", [InputRequired()])
    ASUD_No = IntegerField("ASUD No", [Optional()])
    ASUD_definition_card = BooleanField("ASUD definition card exists")
    strat_no = IntegerField("SA Strat Unit No", [InputRequired()])
    map_symbol = StringField("Map Symbol", [Length(max=8)])
    province = StringField('Province', [Length(max=60)])
    domain = StringField('Domain/Sub-province', [Length(max=60)])
    unit_description = TextAreaField("Stratigraphic Unit Description", [Length(max=500)])
    unit_summary = TextAreaField("Stratigraphic Unit Summary", [Length(max=2000)])
    type_locality = TextAreaField("Type Locality", [Length(max=300)])
    unit_definition = TextAreaField("Unit Definition", [Length(max=6000)])
    unit_correlation = TextAreaField("Unit Correlations", [Length(max=2000)])
    unit_distribution = TextAreaField("Unit Distribution", [Length(max=2000)])
    unit_thickness = TextAreaField("Unit Thickness", [Length(max=2000)])
    unit_lithology = TextAreaField("Unit Lithology", [Length(max=8000)])
    unit_deposition_env = TextAreaField("Unit Depositional Environment", [Length(max=4000)])
    unit_contact_relations = TextAreaField("Unit Contact Relationships", [Length(max=4000)])
    unit_geochronology = TextAreaField("Unit Geochronology", [Length(max=4000)])
    unit_geochemistry = TextAreaField("Unit Geochemistry", [Length(max=4000)])
    unit_geophysical_expression = TextAreaField("Unit Geophysical Expression", [Length(max=4000)])
    references = TextAreaField("References", [Length(max=6000)])


class SearchForm(FlaskForm):
    select = SelectField("Search for a Stratigraphic Unit", choices=[
                ('unit_name','Unit Name'), ('strat_no','SA Strat No'),
                ('map_symbol','Map Symbol')
            ])
    search = StringField('')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', [DataRequired(), Email()])
    


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', [DataRequired()])
    password2 = PasswordField('Repeat Password', [DataRequired(), EqualTo('password')])
    