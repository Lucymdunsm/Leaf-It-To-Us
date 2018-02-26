# Leaf It To Us
Web app for tea enthusiasts powered by the Django framework

## Setup
First clone the repo 
```bash
$ git clone https://github.com/CameronNicolson/Leaf-It-To-Us.git
```

Move into the working directory 
```bash
$ cd Leaf-It-To-Us
```
Install all the required packages 
```bash
$ sudo pip install -r requirements.txt
```
Apply database migrations
```bash
$ python manage.py migrate
```
Load sample data to the database
```bash
$ python populate_script.py
```