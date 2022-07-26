from flask import Flask, render_template, url_for, redirect, request,flash,g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask import request
from telethon import TelegramClient, events, sync
import csv
import datetime
import asyncio

#create a Flask application object 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'techbotgokulnaidu'
db = SQLAlchemy(app)
#create a Encryption instance
bcrypt = Bcrypt(app)
#to store the current active logged in user
userdict={}
#to handle the login and logout
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#User table
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

#Feed table
class Feed(db.Model):
    __tablename__ = 'feed'
    id = db.Column(db.Integer,primary_key= True)
    chat_id = db.Column(db.Integer,unique = True, nullable= True)
    feed_heading = db.Column(db.String(100),nullable= False)
    feed_content = db.Column(db.String(300),nullable= False)
    status = db.Column(db.String(10),nullable= False, default = 'new')


#To route to home/index page
@app.route('/')
def home(): 
    return render_template('index.html')


#To route to login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    #when post method
    if request.method == "POST":
        #getting username and password from html and also setting global value of current logged in user
        name = request.form.get("username")
        userdict["user"]=name
        password = request.form.get("userpass")
        #checking if the conditions are met or a error message is flased onto screen
        if name == '' and password == '':
            flash('Please enter username and password to login')
            return render_template('login_page.html')
        if name == '':
            flash('Please enter username')
            return render_template('login_page.html')
        if password == '':
            flash('Please enter a password')
            return render_template('login_page.html')
        #querying the databse and finding if the user exists else flash error message
        user_present = User.query.filter_by(username=request.form.get("username")).first()
        if user_present:
            #checking if the password entered matches the password(encrypted) in database
            if bcrypt.check_password_hash(user_present.password, request.form.get("userpass")):
                login_user(user_present)
                return redirect(url_for('dash10',username = name))
        else:
            flash("User doesn't exist")
    #rendering login page
    return render_template('login_page.html')

#To route after login or upon click route to view first 10 new or read status posts only
@app.route('/dash10', methods=['GET'])
@login_required
def dash10():  
    data=[]      
    if request.method == "GET":
        #getting only first 10 feeds with read or new status    
        data = Feed.query.filter(or_(Feed.status=='new',Feed.status=='read')).limit(10).all()
    #rendering dash10 html with username and data
    return render_template('dash10.html', data=data,username=userdict["user"])

#similar to dash 10 but all feed with new or read status
@app.route('/dashAll', methods=['GET'])
@login_required
def dashAll():
    data=[]      
    if request.method == "GET":    
        data = Feed.query.filter(or_(Feed.status=='new',Feed.status=='read'))
    return render_template('dashAll.html', data=data,username=userdict["user"])

#To route upon click route to view all read feed
@app.route('/dashRead', methods=['GET'])
@login_required
def dashRead():
    data=[]      
    if request.method == "GET":    
        data = Feed.query.filter_by(status='read')
    return render_template('dashRead.html', data=data,username=userdict["user"])

#To route upon click route to view all trashed feed
@app.route('/dashTrash', methods=['GET'])
@login_required
def dashTrash():
    data=[]      
    if request.method == "GET":    
        data = Feed.query.filter_by(status='trash')
    return render_template('dashTrash.html', data=data,username=userdict["user"])

#To get data from channel or take text from field and make into feed
@app.route('/addtelefeed',methods=['POST'])
@login_required
def pushtelefeed():
    #date = datetime.datetime.today().date()
    value_tele=request.form.get("value")
    value_list = value_tele.split('-')
    #if channel name is sent
    if (len(value_list)==1):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        api_id = 10173805
        api_hash = 'f57fc3e50b0dd38c0d813b58714e3534'
        client = TelegramClient(None, api_id, api_hash,loop = loop)
        client.start()
        chats = client.get_messages(value_list[0],reverse = True,limit = None)
        print(chats)
        client.disconnect()
        # Get message id, message, sender id, reply to message id, and timestamp
        if len(chats):
            for chat in chats:
                message_id=chat.id
                message=chat.message
                time=chat.date
                #cause first entry in any channel is None to avoid that
                if message == None:
                    continue
                feed_entry = message.split("-")
                if (len(feed_entry)==2):
                    feedexist = Feed.query.filter_by(chat_id = message_id).first()
                    #Pushing the feed into the database only if the message id is new and doesn't exist
                    if not feedexist:
                        new_feed  = Feed(chat_id=message_id,feed_heading=feed_entry[0],feed_content = feed_entry[1])
                        db.session.add(new_feed)
                        db.session.commit()
    #if feed is entered into the field in the format heading-content
    elif (len(value_list)==2):
        #pushing data into Feed table in the database
        new_feed = Feed(feed_heading= value_list[0], feed_content=value_list[1])
        db.session.add(new_feed)
        db.session.commit()
    #we rae doinf request.args.get to make sure the page where 
    #the task is tried the feed display will continue in the same page
    return redirect(url_for(request.args.get('type'),username = userdict["user"]))    

#To update from new/trash status to read
@app.route('/updatestatus/<int:feed_id>')
@login_required
def update(feed_id):
    feed = Feed.query.filter_by(id=feed_id).first()
    print(feed)
    feed.status = "read"
    db.session.commit()
    return redirect(url_for(request.args.get('type'),username=userdict["user"]))   

#to update status from read/new to trash
@app.route('/deletefeed/<int:feed_id>')
@login_required
def delete(feed_id):
    feed = Feed.query.filter_by(id=feed_id).first()
    feed.status = "trash"
    db.session.commit()
    return redirect(url_for(request.args.get('type'),username=userdict["user"]))     

#to permanently remove feed from the database
@app.route('/deletepermfeed/<int:feed_id>')
@login_required
def delete_permanent(feed_id):
    feed = Feed.query.filter_by(id=feed_id).first()
    db.session.delete(feed)
    db.session.commit()
    return redirect(url_for(request.args.get('type'),username=userdict["user"]))   

#to logout
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have succefully logged out!!!')
    return redirect(url_for('login'))

#to register
@ app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("userpass")
        if name == '' and password == '':
            flash('Please enter username and password to register')
            return render_template('reg_page.html')
        if name == '':
            flash('Please enter username')
            return render_template('reg_page.html')
        if password == '':
            flash('Please enter a password')
            return render_template('reg_page.html')
        #encrypting password and storing in database
        hashed_password = bcrypt.generate_password_hash(password)
        existing_user_username = User.query.filter_by(username=name).first()
        if existing_user_username:
            flash('That username already exists. Please choose a different one.')
        else:
            #adding new user to database only if he/she isn't in the database
            new_user = User(username=name, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('You have succefully regestered')
            return redirect(url_for('login'))

    return render_template('reg_page.html')

#to start the Flask app and also create database if it isn't present
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True,host='0.0.0.0')
