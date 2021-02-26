# FlaskBlog
FlaskBlog is a simple yet more than a basic blog website built using FLask.

****
## Local installation guide:
**Clone the repository**
```bash
 git clone https://github.com/shubham7743/FlaskBlog.git
```

**Install virtual enviornment**
```bash
python -m pip install --user virtualenv
python -m virtualenv --help
```

**Activate the  virtual enviornment**
```bash
cd blog
Scripts\activate
```

****
## Installing dependencies
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies in blog directory.
```bash
python -m pip install --upgrade pip	// to update pip
pip install flask
pip install Flask-wtf
pip install flask-sqlalchemy
pip install flask-bcrypt
python -m pip install --upgrade pip	// to update pip
python -m pip install --no-use-pep517 bcrypt // if bcrypt show error
pip install flask-login
pip install email_validator
pip install Pillow
pip install flask-mail
pip install flask-serialize
```
****
## Build the Database
**Build the datbase in blog directory. Write the following in terminal**
```bash
 from flaskblog import db
 db.create_all()
 exit()
 ```
 ****
 
## Run the code at your local envn
**Run it as**
```bash
 python run.py
 ```
 
 
