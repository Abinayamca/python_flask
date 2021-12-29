from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import (StringField, TextField, BooleanField, TimeField, DateTimeField,
                     PasswordField, SubmitField, SelectField, TextAreaField, validators, DateField, IntegerField)

class dailyreport(FlaskForm):
    date1=DateField('date1',validators=[DataRequired()])
    submit=SubmitField('Check')

class monthlyreport(FlaskForm):
    start_date=DateField('start_date',validators=[DataRequired()])
    end_date=DateField('end_date',validators=[DataRequired()])
    submit=SubmitField('Generate')

class employeereport(FlaskForm):
    empid=IntegerField('empid',validators=[DataRequired()])
    submit=SubmitField('Next')

class nextreport(FlaskForm):
    item=IntegerField('item',validators=[DataRequired()])
    quantity=IntegerField('quantity',validators=[DataRequired()])
    submit=SubmitField('Next')

class finalreport(FlaskForm):
    submit=SubmitField('Order')

class addremovereport(FlaskForm):
    id=IntegerField('id',validators=[DataRequired()])
    name=StringField('name',validators=[DataRequired()])
    email=StringField('email',validators=[DataRequired()])
    address=StringField('address',validators=[DataRequired()])
    date_of_joining=DateField('date_of_joining',validators=[DataRequired()])
    experience=SelectField('experience',choices=[('Fresher','Fresher'),('1-2 yrs','1-2 yrs'),('2-4 yrs','2-4 yrs'),('Above 5 yrs','Above 5 yrs')],validators=[DataRequired()])
    submit = SubmitField('Add')

class removereport(FlaskForm):
    id1=IntegerField('id1',validators=[DataRequired()])
    submit1=SubmitField('Remove')

class addfoodreport(FlaskForm):
    food_id=IntegerField('food_id',validators=[DataRequired()])
    food_name=StringField('food_name',validators=[DataRequired()])
    food_type=SelectField('food_type',choices=[('Veg','Veg'),('Non-veg','Non-veg')],validators=[DataRequired()])
    rate=IntegerField('rate',validators=[DataRequired()])
    subsidy=IntegerField('subsidy',validators=[DataRequired()])
    submit = SubmitField('Add')

class loginreport(FlaskForm):
    username=StringField('username',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired()])
    role = IntegerField('role', validators=[DataRequired()])
    submit=SubmitField('Login')