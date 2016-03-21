
from system.core.controller import *

class Books(Controller):
    def __init__(self, action):
        super(Books, self).__init__(action)

        self.load_model('Book')
        self.load_model('Book')


    def books(self):
        print "books page loaded"
        data = self.models['Book'].books_page_get()
        bookdata = data[0]
        userdata = data[1]
        print bookdata, userdata
        otherreviews = self.models['Book'].other_reviews_get()
        return self.load_view('/books.html', bookdata=bookdata, userdata=userdata, reviews=otherreviews)

    def add(self):
        print "new review page"
        authors = self.models['Book'].authors_get()
        print "authors:", authors
        return self.load_view('add.html', authors=authors)

    def create(self):
        print "creating new review"
        authorid = request.form['author_list']
        print "author id from list = ", authorid
        print request.form
        if authorid == "none":
            authors = self.models['Book'].authors_get()
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
        bookcheck = self.models['Book'].book_check(review_info, authorfromlist)
        newbook = self.models['Book'].new_book_get()
        review_info['book_id'] = newbook['id']
        print "review info:" ,review_info
        review = self.models['Book'].add_review(review_info)
        print review
        return redirect('/books')

    def new_review(self, id):
        print "new review creation page"
        review_info_new = {
        "book_id" : request.form['book_id'],
        "author_id" : request.form['author_list'],
        "content" : request.form['review_content'],
        "rating" : request.form['rating'],
        "posted_by" : session['id']
        }
        print "did it break yet?"
        review_response = self.models['Book'].new_review(review_info_new)
        print "review response",review_response
        return redirect('/books')

    def book_page(self, id):
        reviewsbybook = self.models['Book'].reviews_by_book(id)
        print reviewsbybook[0]
        return self.load_view('/book_page.html', reviews=reviewsbybook)
