from connector import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    phnumber = db.Column(db.Integer(), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    traveler_details = db.relationship('TravellerDetails', backref='traveller', lazy=True) 
    reviews = db.relationship('Reviews', backref='reviewer', lazy=True)  

    
    def __repr__(self):
        return f"User('{self.firstname}','{self.lastname}','{self.username}','{self.phnumber}', '{self.email}', '{self.image_file}')"


class Packages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),unique=True ,nullable=False)
    cost = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    info1 = db.Column(db.String(100), nullable=False)
    info2 = db.Column(db.String(100), nullable=False)
    info3 = db.Column(db.String(100), nullable=False)
    info4 = db.Column(db.String(100), nullable=True)
    info5 = db.Column(db.String(100), nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='default-package.jpg')
    category = db.Column(db.String(), nullable=False)
    more_details = db.relationship('MoreDetails', backref='details', lazy=True )
    traveller_details = db.relationship('TravellerDetails', backref='travel_package', lazy=True )
    review = db.relationship('Reviews', backref='package', lazy=True )
    

    def __repr__(self):
        return f"User('{self.title}','{self.cost}','{self.duration}', '{self.info1}', '{self.info2} ', '{self.info3}', '{self.info4}','{self.info5}')"


class TravellerDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False,unique=False)
    name = db.Column(db.String(), nullable=False, unique=False)
    DOT = db.Column(db.String(10), nullable=False,unique=False)
    total_travellers = db.Column(db.Integer, nullable=True,unique=False)
    email = db.Column(db.String(50), nullable=False,unique=False)
    phnumber = db.Column(db.Integer, unique=False, nullable=False)
    package_id = db.Column(db.String, db.ForeignKey('packages.id'), nullable=False,unique=False)

    def __repr__(self):
        return f"User('{self.name}','{self.DOT}','{self.total_travellers}','{self.email}', '{self.phnumber}')"


class MoreDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'), nullable=False)
    highlight1 = db.Column(db.String(), nullable=False)
    highlight2 = db.Column(db.String(), nullable=False)
    highlight3 = db.Column(db.String(), nullable=False)
    highlight4 = db.Column(db.String(), nullable=True)
    facility1 = db.Column(db.Boolean, nullable=True)
    facility2 = db.Column(db.Boolean, nullable=True)
    facility3 = db.Column(db.Boolean, nullable=True)
    facility4 = db.Column(db.Boolean, nullable=True)
    facility5 = db.Column(db.Boolean, nullable=True)
    facility6 = db.Column(db.Boolean, nullable=True)
    hotel_location1 = db.Column(db.String(100),nullable=False)
    hotel_location2 = db.Column(db.String(100),nullable=True)
    hotel_location3 = db.Column(db.String(100),nullable=True)
    hotel_name1 = db.Column(db.String(100),nullable=False)
    hotel_name2 = db.Column(db.String(100),nullable=True)
    hotel_name3 = db.Column(db.String(100),nullable=True)
    hotel_stay1 = db.Column(db.String(100),nullable=False)
    hotel_stay2 = db.Column(db.String(100),nullable=True)
    hotel_stay3 = db.Column(db.String(100),nullable=True)
    hotel_rating_1 = db.Column(db.Integer, nullable=False)
    hotel_rating_2 = db.Column(db.Integer, nullable=True)
    hotel_rating_3 = db.Column(db.Integer, nullable=True)
    overview = db.Column(db.String(500),nullable=False)
    day_details = db.relationship('Itinerary', backref='day', lazy=True )
    image_file1 = db.Column(db.String(20), nullable=True, default='default-package.jpg')
    image_file2 = db.Column(db.String(20), nullable=True, default='default-package.jpg')
    image_file3 = db.Column(db.String(20), nullable=True, default='default-package.jpg')
    image_file4 = db.Column(db.String(20), nullable=True, default='default-package.jpg')


class  Itinerary(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    more_details_id = db.Column(db.Integer, db.ForeignKey('more_details.id'), nullable=False, unique=False)
    day_number = db.Column(db.String(20),nullable=False)
    day_details = db.Column(db.String(100),nullable=False)

class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer(), nullable=False)
    