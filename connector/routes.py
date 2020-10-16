import secrets
import os
from PIL import Image
from flask import  render_template, url_for, redirect, flash, request
from connector import app,db,bcrypt
from connector.forms import RegistrationForm,LoginForm,PackageForm,UpdateAccountForm,TravellerDetailsForm,MoreDetailsForm,ItineraryForm,ItinerariFieldList,ReviewForm
from connector.models import User,Packages,TravellerDetails,MoreDetails,Itinerary,Reviews
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def travel():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('Travelapp.html')


@app.route("/signup", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(firstname=form.firstname.data , lastname=form.lastname.data , username=form.username.data , phnumber=form.phnumber.data ,
                 email=form.email.data ,password=hashed_password )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home')) 
        else:
            flash("Login unsuccessful. Please check email and password","danger")
    return render_template('sign in.html' , form=form)

@app.route('/home')
@login_required
def home():
    image_file= url_for('static', filename='profile_pics/' + current_user.image_file)
    rcategories = TravellerDetails.query.filter_by(user_id=current_user.id).all()
    categories = []
    for rcategory in  rcategories:
        if rcategory.travel_package.category not in categories:
            categories.append(rcategory.travel_package.category)
    rpackages=[]
    for category in categories:
        packages=Packages.query.filter_by(category=category).all()
        rpackages.append(packages[-1])
        if len(packages)>1:
            rpackages.append(packages[-2])

    return render_template('home_page.html',image_file=image_file,rpackages=rpackages)

def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def save_package_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/package-images', picture_fn)
    form_picture.save(picture_path)

    return picture_fn


@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_profile_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.phnumber = form.phnumber.data
        current_user.email = form.email.data
        db.session.commit()
        flash(" Your Account has been updated successfully","success")
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.phnumber.data = current_user.phnumber
        form.email.data = current_user.email
    image_file= url_for('static', filename='profile_pics/' + current_user.image_file)
    past_history = TravellerDetails.query.filter_by(user_id=current_user.id).all()
    return render_template('account.html',title='Account', image_file=image_file, form=form, past_history=past_history)

@app.route('/admin', methods=['GET','POST'])
@login_required
def admin():
    image_file= url_for('static', filename='profile_pics/' + current_user.image_file)
    if current_user.email != "admin@gmail.com" and current_user.password != 'admin':
        flash("You dont have admin privileges!", 'danger')
        return redirect(url_for('home'))
    else:
        form = PackageForm()
        if form.validate_on_submit():
            if form.image_file.data:
                picture_file = save_package_picture(form.image_file.data)
                packages=Packages(title=form.title.data, cost=form.cost.data, duration=form.duration.data,
                info1=form.info1.data, info2=form.info2.data, info3=form.info3.data, info4=form.info4.data, info5=form.info5.data
                , category=form.category.data, image_file=picture_file)
            else:
                packages=Packages(title=form.title.data, cost=form.cost.data, duration=form.duration.data,
                info1=form.info1.data, info2=form.info2.data, info3=form.info3.data, info4=form.info4.data, info5=form.info5.data
                , category=form.category.data)
            db.session.add(packages)
            db.session.commit()
            return redirect(url_for('more_details',package_id=packages.id))
    return render_template('admin-page.html', form=form ,image_file=image_file)


@app.route('/admin/<package_id>/more-details', methods=['GET','POST'])
@login_required
def more_details(package_id):
    if current_user.email != "admin@gmail.com" and current_user.password != 'admin':
        flash("You dont have admin privileges!", 'danger')
        return redirect(url_for('home'))
    else:
        form =  MoreDetailsForm()
       
        if form.validate_on_submit():
            if form.image_file1.data and form.image_file2.data and form.image_file3.data and form.image_file4.data:
                picture_file1 = save_package_picture(form.image_file1.data)
                picture_file2 = save_package_picture(form.image_file2.data)
                picture_file3 = save_package_picture(form.image_file3.data)
                picture_file4 = save_package_picture(form.image_file4.data)
                
                moredetails = MoreDetails( package_id=package_id,highlight1= form.highlight1.data,highlight2= form.highlight2.data, 
                                        highlight3= form.highlight3.data, highlight4= form.highlight4.data, facility1 = form.facility1.data, 
                                        facility2 =form.facility2.data, facility3 =form.facility3.data, facility4 = form.facility4.data, 
                                        facility5 =form.facility5.data, facility6 =form.facility6.data, hotel_location1 = form.hotel_location1.data, hotel_location2 = form.hotel_location2.data, hotel_location3 = form.hotel_location3.data, hotel_name1 = form.hotel_name1.data, hotel_name2 = form.hotel_name2.data, hotel_name3 = form.hotel_name3.data, hotel_stay1 = form.hotel_stay1.data, hotel_stay2 = form.hotel_stay2.data,  hotel_stay3 = form.hotel_stay3.data, hotel_rating_1 = form.hotel_rating_1.data, hotel_rating_2 = form.hotel_rating_2.data, hotel_rating_3 = form.hotel_rating_3.data, overview = form.overview.data, image_file1=picture_file1, image_file2=picture_file2, image_file3=picture_file3, image_file4=picture_file4 )
            elif form.image_file1.data and form.image_file2.data and form.image_file3.data:
                picture_file1 = save_package_picture(form.image_file1.data)
                picture_file2 = save_package_picture(form.image_file2.data)
                picture_file3 = save_package_picture(form.image_file3.data)
                moredetails = MoreDetails( package_id=package_id,highlight1= form.highlight1.data,highlight2= form.highlight2.data, 
                                        highlight3= form.highlight3.data, highlight4= form.highlight4.data, facility1 = form.facility1.data, 
                                        facility2 =form.facility2.data, facility3 =form.facility3.data, facility4 = form.facility4.data, 
                                        facility5 =form.facility5.data, facility6 =form.facility6.data, hotel_location1 = form.hotel_location1.data, hotel_location2 = form.hotel_location2.data, hotel_location3 = form.hotel_location3.data, hotel_name1 = form.hotel_name1.data, hotel_name2 = form.hotel_name2.data, hotel_name3 = form.hotel_name3.data, hotel_stay1 = form.hotel_stay1.data, hotel_stay2 = form.hotel_stay2.data,  hotel_stay3 = form.hotel_stay3.data, hotel_rating_1 = form.hotel_rating_1.data, hotel_rating_2 = form.hotel_rating_2.data, hotel_rating_3 = form.hotel_rating_3.data, overview = form.overview.data, image_file1=picture_file1, image_file2=picture_file2, image_file3=picture_file3)     
            db.session.add(moredetails)
            db.session.commit()
            return redirect(url_for("itinerary",package_id=package_id ))
    return render_template('more_details_form.html', form=form)

@app.route('/admin/<package_id>/more-details/itinerary', methods=['GET','POST'])
@login_required
def itinerary(package_id):
    if current_user.email != "admin@gmail.com" and current_user.password != 'admin':
        flash("You dont have admin privileges!", 'danger')
        return redirect(url_for('home'))
    else:
        form = ItinerariFieldList()
        if request.method == "POST":
            total_days=form.totaldays.data
            for i in range(1,total_days+1):
                new_itinerary = Itinerary(more_details_id=package_id , day_number=request.form["itineraries-"+str(i)+"-day_number"] , day_details=request.form["itineraries-"+str(i)+"-day_details"])
                db.session.add(new_itinerary)
                db.session.commit()
            flash("your package has been added successfully!", 'success')    
            return redirect(url_for("home"))    
    return render_template("itinerary.html", form=form)


@app.route('/<package_id>/traveller-details', methods=['GET','POST'])
@login_required
def traveller_details(package_id):
    image_file= url_for('static', filename='profile_pics/' + current_user.image_file)
    package = Packages.query.filter_by(id = package_id).first()
    form = TravellerDetailsForm()
    if form.validate_on_submit():
        travellerdetails=TravellerDetails(user_id=current_user.id , name=form.name.data , DOT=form.DOT.data ,
         total_travellers=form.total_travellers.data ,email=form.email.data ,phnumber=form.phnumber.data, package_id=package_id )
        db.session.add(travellerdetails)
        db.session.commit()
        flash(f'Bon Voyage for your travel!', 'success')
        return redirect(url_for('home'))
    return render_template('traveller-details.html', form=form, package=package,image_file=image_file)



@app.route('/home/adventure')
@login_required
def adventure():
    image_file= url_for('static', filename='profile_pics/' + current_user.image_file)
    packages=Packages.query.filter_by(category='Adventure')
    ratings = []
    reviews = Reviews.query.all()
    for review in reviews:
        if review.package.category=='Adventure':
            id= review.package_id
            rating=0
            count=0
            id_list=[]
            for review in reviews:
                if review.package_id==id :
                    rating+= review.rating
                    count+=1
            if count>0:
                avg_rating=int(abs(rating/count))
            r={}
            r['id']=id
            r['rating']=avg_rating
            if r not in ratings:
                ratings.append(r)
    print(ratings)
    return render_template('categories/adventure.html', title='Adventure', heading='Adventure', packages=packages, image_file=image_file,ratings=ratings)

@app.route('/home/religious')
@login_required
def religious():
    image_file= url_for('static', filename='profile_pics/' + current_user.image_file)
    packages=Packages.query.filter_by(category='Religious')
    ratings = []
    reviews = Reviews.query.all()
    for review in reviews:
        if review.package.category=='Religious':
            id= review.package_id
            rating=0
            count=0
            id_list=[]
            for review in reviews:
                if review.package_id==id :
                    rating+= review.rating
                    count+=1
            if count>0:
                avg_rating=int(abs(rating/count))
            r={}
            r['id']=id
            r['rating']=avg_rating
            if r not in ratings:
                ratings.append(r)
    return render_template('categories/religious.html', title='Religious', heading='Religious',  packages=packages,image_file=image_file,ratings=ratings)

@app.route('/home/historical')
@login_required
def historical():
    image_file= url_for('static', filename='profile_pics/' + current_user.image_file)
    packages=Packages.query.filter_by(category='Historical')
    ratings = []
    reviews = Reviews.query.all()
    for review in reviews:
        if review.package.category=='Historical':
            id= review.package_id
            rating=0
            count=0
            id_list=[]
            for review in reviews:
                if review.package_id==id :
                    rating+= review.rating
                    count+=1
            if count>0:
                avg_rating=int(abs(rating/count))
            r={}
            r['id']=id
            r['rating']=avg_rating
            if r not in ratings:
                ratings.append(r)
    return render_template('categories/historical.html', title='Historical', heading='Historical', packages=packages,image_file=image_file,ratings=ratings)

@app.route('/home/environmental')
@login_required
def environmental():
    image_file= url_for('static', filename='profile_pics/' + current_user.image_file)
    packages=Packages.query.filter_by(category='Environmental')
    ratings = []
    reviews = Reviews.query.all()
    for review in reviews:
        if review.package.category=='Environmental':
            id= review.package_id
            rating=0
            count=0
            id_list=[]
            for review in reviews:
                if review.package_id==id :
                    rating+= review.rating
                    count+=1
            if count>0:
                avg_rating=int(abs(rating/count))
            r={}
            r['id']=id
            r['rating']=avg_rating
            if r not in ratings:
                ratings.append(r)
    return render_template('categories/environmental.html', title='Environmental', heading='Environmental', packages=packages,image_file=image_file,ratings=ratings)


@app.route('/home/<category>/<package_id>', methods=['GET','POST'])
@login_required
def packagedetails(package_id,category):
    form = ReviewForm()
    details_page= MoreDetails.query.filter_by(package_id=package_id).first()
    itinerary_details = Itinerary.query.filter_by(more_details_id = package_id).all()
    reviews = Reviews.query.filter_by(package_id =package_id).all()
    if request.method == "POST":
        rating = request.form["rating"]
    if form.validate_on_submit():
        review=Reviews(package_id =package_id ,user_id=current_user.id,rating =rating,review=form.review.data )
        db.session.add(review)
        db.session.commit()
        flash(f'Your Review added.Thank you very much for your support :)', 'success')
        return redirect(url_for('packagedetails',package_id=package_id,category=category))

    return render_template('packages/layout.html' ,package_id=package_id, details_page=details_page, itinerary_details = itinerary_details, title="More Details",form = form,reviews=reviews)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('travel'))









