from flask_wtf import FlaskForm,Form
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField ,SubmitField, SelectField, BooleanField, RadioField, IntegerField, TextField, FileField,TextAreaField, FieldList, FormField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError,InputRequired, Regexp
from connector.models import User,Packages,TravellerDetails,MoreDetails,Reviews
from connector import app,bcrypt




class RegistrationForm(FlaskForm):
	firstname = StringField('Firstname',validators=[DataRequired(),Length(min=3, max=20)])
	lastname = StringField('Lastname',validators=[DataRequired(),Length(min=3, max=20)])
	username = StringField('Username',validators=[DataRequired(),Length(min=3, max=20)])
	phnumber = IntegerField('Contact number',validators=[DataRequired(message='Field is required and should consist digits only.')])
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	submit  = SubmitField('Sign Up')

	def validate_username(self, username):
		user=User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken.Please try other username.')

	def validate_email(self, email):
		user=User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken.Please try other email.')

	def validate_phnumber(self, phnumber):
		user=User.query.filter_by(phnumber=phnumber.data).first()
		if user:
			raise ValidationError('Contact number is taken.Please choose different number.')

usertemp=''
	
class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	remember=BooleanField('Remember Me')
	submit = SubmitField('Login')

	def validate_email(self, email):
		user=User.query.filter_by(email=email.data).first()
		global usertemp
		usertemp=user
		if not user:
			raise ValidationError('Email id does not exist. Sign up if not done.')

	def validate_password(self, password):
		if usertemp and not bcrypt.check_password_hash(usertemp.password, password.data):
			raise ValidationError('That password is incorrect. Please try again.')


class UpdateAccountForm(FlaskForm):
    phnumber = IntegerField('Phone Number',validators=[DataRequired(message='Field is required and should consist digits only.')])
    email=StringField('Email',validators=[DataRequired(),Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit=SubmitField('Update')

    def validate_phnumber(self,phnumber):
        if phnumber.data != current_user.phnumber:
            user=User.query.filter_by(phnumber=phnumber.data).first()
            if user:
                raise ValidationError("This Phone Number already exists")

    def validate_email(self,email):
        if email.data != current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("This Email already exists")


class PackageForm(FlaskForm):
	category = SelectField('Department',choices=[('Adventure', 'Adventure'), ('Historical', 'Historical'), 
							('Religious', 'Religious'),('Environmental','Environmental')],validators=[DataRequired()])
	title = StringField('Heading',validators=[DataRequired()])
	duration = StringField('Duration',validators=[DataRequired()])
	cost = StringField('Cost',validators=[DataRequired()])
	info1 = TextField('Highlight-1',validators=[DataRequired()])
	info2 = TextField('Highlight-2',validators=[DataRequired()])
	info3 = TextField('Highlight-3',validators=[DataRequired()])
	info4 = TextField('Highlight-4')
	info5 = TextField('Highlight-5')
	image_file = FileField('Image',validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
	submit  = SubmitField('Create Package')

	def validate_title(self, title):
		package=Packages.query.filter_by(title=title.data).first()
		if package:
			raise ValidationError('Heading already exists. Kindly choose another Heading .')


class TravellerDetailsForm(FlaskForm):
	name = StringField('Traveller Name',validators=[DataRequired(),Length(min=3, max=50)])
	DOT = DateField('Date of Travel', validators=[DataRequired()])
	total_travellers = IntegerField('No. of Travellers', validators=[DataRequired(message='Field is required and should consist digits only.')])
	email = StringField('Email',validators=[DataRequired(),Email()])
	phnumber = IntegerField('Contact number',validators=[DataRequired(message='Field is required and should consist digits only.')])
	submit  = SubmitField('Travel')


class MoreDetailsForm(FlaskForm):
	highlight1 = TextField('Highlight-1',validators=[DataRequired()])
	highlight2 = TextField('Highlight-2',validators=[DataRequired()])
	highlight3 = TextField('Highlight-3',validators=[DataRequired()])
	highlight4 = TextField('Highlight-4')
	facility1 = BooleanField('Breakfast')
	facility2 = BooleanField('Dinner')
	facility3 = BooleanField('Hotel')
	facility4 = BooleanField('Travel')
	facility5 = BooleanField('Sightseeing')
	facility6 = BooleanField('Guide')
	hotel_location1 = TextField('Hotel Location 1')
	hotel_name1 = TextField('Hotel Name 1')
	hotel_stay1 = TextField('Hotel Stay 1')
	hotel_location2 = TextField('Hotel Location 2')
	hotel_name2 = TextField('Hotel Name 2')
	hotel_stay2 = TextField('Hotel Stay 2')
	hotel_location3 = TextField('Hotel Location 3')
	hotel_name3 = TextField('Hotel Name 3')
	hotel_stay3 = TextField('Hotel Stay 3')
	overview = TextAreaField('Overview')
	hotel_rating_1 = IntegerField('Ratings for Hotel 1 (in stars. Max rating = 5 stars amd Min rating=0)')
	hotel_rating_2 = IntegerField('Ratings for Hotel 2(in stars. Max rating = 5 stars amd Min rating=0)')
	hotel_rating_3 = IntegerField('Ratings for Hotel 3(in stars. Max rating = 5 stars amd Min rating=0)')
	image_file1 = FileField('Image',validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
	image_file2 = FileField('Image',validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
	image_file3 = FileField('Image',validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
	image_file4 = FileField('Image',validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
	submit  = SubmitField('Add Itinerary')


class ItineraryForm(FlaskForm):
	day_number = IntegerField('Day Number',validators=[DataRequired(message='Field is required and should consist digits only.')])
	day_details = TextAreaField('Day Details', validators=[DataRequired()])
	

class ItinerariFieldList(FlaskForm):
	totaldays = IntegerField('Total Days')
	itineraries = FieldList(FormField(ItineraryForm))
	submit  = SubmitField('Add Package')

class ReviewForm(FlaskForm):
	review = TextAreaField('Review',render_kw={"placeholder": "Write the review of your wonderful experience for this tour."})
	submit  = SubmitField('Post Review')









	