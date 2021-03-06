
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        self.load_model('User')
        self.load_model('Book')


    def index(self):
        return self.load_view('users/index.html')

    def register(self):
        print "registration submitted"
        register_info = {
        "name" : request.form['name'],
        "alias" : request.form['alias'],
        "email" : request.form['email'],
        "password" : request.form['password'],
        "confirm_pw" : request.form['confirm_pw']
        }
        creation_validation = self.models['User'].creation_validation(register_info)
        if creation_validation['status'] == True:
            newuser = self.models['User'].register_user(register_info)
            print newuser
            userid = self.models['User'].get_user_id()
            print "userid", userid
            session['id'] = userid[0]['id']
            print "session ID made so:", session['id']
            return redirect('/books')
        else:
            flash(creation_validation['errors'])
            return redirect('/')

    def login(self):
        print "login request submitted"
        login_info = {
        "email" : request.form['email'],
        "password" : request.form['password']
        }
        login = self.models['User'].validate_login(login_info)
        if login['status']:
            print "session id:", session['id']
            return redirect('/books')
        else:
            flash(login['errors'])
            return redirect('/')

    def logout(self):
        session.clear()
        return redirect('/')

    def user_page(self, id):
        userinfo = self.models['User'].get_user_info(id)[0]
        reviews = self.models['Book'].reviews_by_user(id)
        print reviews
        return self.load_view('/users/user_page.html', user=userinfo, reviews=reviews)
