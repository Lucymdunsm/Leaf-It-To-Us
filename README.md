# Leaf It To Us
Web app for tea enthusiasts powered by the Django framework.

## Setup

### Requirements

This project requires at least `Python 3.4.x`. 

### Installing
First clone the repository. This will create a directory called `Leaf-It-To-Us`.
```bash
$ git clone https://github.com/CameronNicolson/Leaf-It-To-Us.git
```
Move into the newly created directory 
```bash
$ cd Leaf-It-To-Us
```
Create a new virtual environment if needed. Then, install all the required packages.
```bash
$ pip install -r requirements.txt
```
Apply database migrations.
```bash
$ python manage.py migrate
```
Load sample data to the database
```bash
$ python populate_script.py
```
## Authors

* **Akvile Kurilaite** (https://github.com/kukuakvile)
* **Cameron Nicolson** (https://github.com/cameronnicolson)
* **Lucy Dunsmuir** (https://github.com/lucymdunsm)
* **Matej Vucak** (https://github.com/mvvucak)
* **Victoria Green** (https://github.com/vitawood)

See also the list of [contributors](https://github.com/cameronnicolson/Leaf-It-To-Us/contributors) who participated in this project.