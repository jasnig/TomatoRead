from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash
from mongoengine import connect,errors
from model import model
import hashlib


app = Flask(__name__)
app.config.from_object('config')

connect('linkhub')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/u')
def user_list():
    return 'Hi'


@app.route('/u/<blog_id>')
def user_index(blog_id):
    return render_template('user_index.html')


@app.route('/register',methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        user = model.User()
        user.email = request.form['email']
        user.password = request.form['password']

        user.blog_id = hashlib.md5(user.email).hexdigest()
        try:
            user.save()
            flash('Register succeed')
            return redirect(url_for('user_index', blog_id=user.blog_id))
        except errors.NotUniqueError, err:
            error = 'Save error (Email existed) :' + err.message
        except errors.OperationError, err:
            error = 'Save error : ' + err.message

    return render_template('register.html', error=error)


@app.route('/login')
def login():
    return 'login'


@app.route('/logout')
def logout():
    return 'logout'

# AddLink
# ClickLink
# UpdateLink
#

if __name__ == '__main__':
    app.run()

