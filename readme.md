# Aurora (Project new dawn)

This project was done by Gokul Naidu Vuppalapati and was named Aurora which means Dawn in Latin.<br /><br />

The whole project was done in under 20hrs, out of which the flask part took the least(~2-3hrs) and designing the website took the most <br/><br/>

Aurora, a web app completely built using Python, Flask, SQLalchemy, HTML, CSS, Javascript, Docker and Telegram API to display the feed dashboard(same for all users) in a very intractable and user friendly manner similar to a notice board where all the team can collaborate and share ideas directly via the web app or just send a message to the telegram channel and it'll be automatically added to the dash.r <br /><br />

New things learnt during process:
- used illustrator for the first time and used to extract vertor images to create layers in HTML
- Using telegram API for data collection from channels

### **Development hardware and software: Macbook Pro 2015, Python Version = 3.9.1, Coding environment= VS code; Vector Image source: freepik.com and was created by katemangostar**
### All the images are uploaded onto my own google drive and added to the websited
## Home Screen Inspiration

The first inspiration for the Home UI was inspired from apple macbook air product page and hence I chose to use vector images for the effect which were sliced using Illustrator

## Dashboard Inspiration

The inspiration is from google keep UI, which has all the elements arranged in a neat boxes.

# How get started

1. First navigate to the directory
2. Open the terminal (recommended in VSCode)
3. `docker image build -t docker-flask-test .` to build the image
4. `docker run -ti -p 5000:5000 docker-flask-test` to run the the image in interactive mode as the telegram api requires phone number and OTP
   _Note:Make sure you are subscribed to the channel before requesting and also the code only gets messages from the channel in the format => `heading - content`. And also the API hash and id is temporary and can be easily replaced with your own api and id(at line 135 and 136 in app.py file)_
5. Later open your broswer and go to address `http://localhost:5000/` to go to home page
6. Either `scroll down on home page to access reveal login` or click on login button on the top bar

# Guide: to Register user

1. Click on Register button on top bar or Create account button in the login page
2. Make sure the username is unique and more than 5 character along with the password being at least 8 characters
3. Upon successfull registration you will be taken to the login page to login
4. Else you will be shown the errors in the same register page and fix the issue accordingly and later click on register

# Guide: to Login

1. Click on Login button on top bar or `scroll down on the home page to reveal the button under aurora text`
2. Make sure you **enter a valid username (at least 5 char) and password(at least 8 chars) and also the username was already registered**, if any of these aren't correct the error will be flashed on login page, which have to be rectified and later **click on Login**.
3. Upon successfull login, you will be taken to top 10 dashboard welcoming with your username and interactive feed

# Guide: to see top 10 feeds

1. Click on `Top10` button on top bar
2. This will display all the first feeds saved to the database and whose `status='new'` or `status='read'`

# Guide: to see all feeds that are not trash

1. Click on `All` button on top bar
2. This will display all feed in the database and whose `status='new'` or `status='read'`

# Guide: to see all read feeds

1. Click on `Read` button on top bar
2. This will display all feed in the database and whose `status='read'`

# Guide: to see the feed that are in trash

1. Click on `Trash` button on top
2. This will display all feed in the database and whose `status='trash'`

# Guide: to add new feed

## Method 1: Directly from text

1. go to the text input in the top bar and type in the feed in format => `heading - content`
2. Once you have type press enter and the feed will be loaded into the database, it's very simple

## Method 2: From Telegram channel

1. go to the text input in the top bar and type in the channel name and hit enter
   Note: make sure the channel name has no `-` in it's name
2. Next a prompt will be seen in the terminal window to enter phone number and later following you OTP(recieved on your telegram app)
3. Upon successful validation all the messages in in format => `heading - content` that haven't been loaded will be loaded on to the database

# Quick guide

1. White card feed => `status = new`
2. Green card feed => `status = read`
3. Red card feed => `status = trash`

# Guide: to change feed status

- Just hover over any white feed card in the `All` or `Top10` pages and you'll be displayed with two buttons `Read` and `Trash`
- Click on `Read` to change to read status which is instantly seen with the card **changing color from white to greenish hue**
- Click on `Trash` and the feed will be removed from all the `All`, `Top10`,`Read` pages and will be only visible in the `Trash` page
- When the feed is in read status it can only be moved to `Trash`(only trash button will be available)
- When the feed is in trash status it is only visible in `Trash` page. The feed card have a reddish hue and when you hover over you have two options `Restore` and `Remove`.
- `Restore` - Restores the feed from trash and changes the feed back to read status making it visible in all the other pages
- `Remove` - Permanently deletes the feed from both the page and the database

# Guide: to Logout

- Just click on the `Logout` button on the top bar and you will be redirected to the `Login Page`

#### fix for issues:
 rarely occurs but just in case: if you ever have issue where it says userdict["user"] not found or exist just go back and login to restore website

#### Future ideas:
1. Get variours formats from telegram like documents and pictures
2. add most viewed read page showcasing decreasing order of highest read count feed and also with changing from darker to lighter hues of green
3. Better Telegram API integration
