
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        self.load_model('User')


    def index(self):
        return self.load_view('index.html')

    def register(self):
        print "registration submitted"
        register_info = {
        "name" : request.form['name'],
        "alias" : request.form['alias'],
        "email" : request.form['email'],
        "password" : request.form['password'],
        "confirm_pw" : request.form['confirm_pw']
        }
        newuser = self.models['User'].register_user(register_info)
        print newuser
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

    def books(self):
        print "books page loaded"
        data = self.models['User'].books_page_get()
        bookdata = data[0]
        userdata = data[1]
        print bookdata, userdata
        return self.load_view('/books.html', bookdata=bookdata, userdata=userdata)

    def add(self):
        print "new review page"
        authors = self.models['User'].authors_get()
        print "authors:", authors
        return self.load_view('add.html', authors=authors)

    def create(self):
        print "creating new review"
        authorid = request.form['author_list']
        print "author id from list = ", authorid
        print request.form
        if authorid == "none":
            authors = self.models['User'].authors_get()
            authorid = (authors[0]['id'] + 1)
            print "author id set to", authorid
            authorfromlist = False
        else:
            authorid = request.form['author_list']
            print "author is from list"
            authorfromlist = True
        review_info = {
        "title" : request.form['book_title'],
        "review_content" : request.form['review_content'],
        "rating" : request.form['rating'],
        "author_id" : authorid,
        "posted_by" : session['id'],
        "author_name" : request.form['author_name']
        }
        print "review info return", review_info
        bookcheck = self.models['User'].book_check(review_info, authorfromlist)
        newbook = self.models['User'].new_book_get()
        review_info['book_id'] = newbook['id']
        print "review info:" ,review_info
        review = self.models['User'].add_review(review_info)
        print review
        return redirect('/books')
