
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
>Open your browser and the site can be found running at http://127.0.0.1:5000/ 

****
****
**Login Page**
![](https://github.com/shubham7743/FlaskBlog/blob/main/images/1614590392437.png)

**Registration Page**
![](https://github.com/shubham7743/FlaskBlog/blob/main/images/1614590327249.png)

**Upon successful account creation**
![](https://github.com/shubham7743/FlaskBlog/blob/main/images/1614590297394.png)

**Home page for a logged -in user. Here all the posts are displayed.**
![](https://github.com/shubham7743/FlaskBlog/blob/main/images/1614590532424.png)

**Account page for a user**
![](https://github.com/shubham7743/FlaskBlog/blob/main/images/1614590507876.png)

**New post creation for users**
![](https://github.com/shubham7743/FlaskBlog/blob/main/images/1614590466105.png)

**Users can also update or delete posts**
![](https://github.com/shubham7743/FlaskBlog/blob/main/images/1614590600820.png)
