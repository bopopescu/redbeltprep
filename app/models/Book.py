from system.core.model import Model
from flask import session

class Book(Model):
    def __init__(self):
        super(Book, self).__init__()

    def books_page_get(self):
        user_id = session['id']
        books_query = "SELECT reviews.id, reviews.book_id, reviews.content AS review_content, reviews.posted_by, reviews.created_at, reviews.rating, users.alias, authors.author_name , books.title FROM reviews LEFT JOIN books ON books.id = reviews.book_id LEFT JOIN authors ON authors.id = books.author_id LEFT JOIN users ON reviews.posted_by = users.id ORDER BY created_at DESC LIMIT 3"
        books_return = self.db.query_db(books_query)
        user_query = "SELECT name, alias, id FROM users WHERE id = %s"
        user_data = [user_id]
        user_return = self.db.query_db(user_query, user_data)
        print "retrieved successfully"
        return  books_return, user_return

    def other_reviews_get(self):
        reviews_query = "SELECT books.title, reviews.book_id, reviews.posted_by, users.alias FROM reviews LEFT JOIN books ON reviews.book_id = books.id JOIN users ON reviews.posted_by = users.id"
        reviews_return = self.db.query_db(reviews_query)
        return reviews_return

    def authors_get(self):
        authors_query = "SELECT id, author_name FROM authors ORDER BY id DESC"
        authors_return = self.db.query_db(authors_query)
        return authors_return

    def book_check(self, data, authorfromlist):
        if authorfromlist:
            book_insert_query = "INSERT INTO books (title, author_id) VALUES (%s, %s)"
            book_insert_data = [data['title'], data['author_id']]
            book_insert_return = self.db.query_db(book_insert_query, book_insert_data)
            return {"status": True, "book": book_insert_return}
        else:
            author_insert_query = "INSERT INTO authors (author_name) VALUES (%s)"
            author_insert_data = [data['author_name']]
            author_insert_return = self.db.query_db(author_insert_query, author_insert_data)
            book_insert_query = "INSERT INTO books (title, author_id) VALUES (%s, %s)"
            book_insert_data = [data['title'], data['author_id']]
            book_insert_return = self.db.query_db(book_insert_query, book_insert_data)
            return {"status": True, "author": author_insert_return, "book": book_insert_return}

    def new_book_get(self):
        newest_book_query = "SELECT books.id FROM books ORDER BY books.id DESC LIMIT 1"
        newest_book = self.db.query_db(newest_book_query)[0]
        print "newest book", newest_book
        return newest_book

    def add_review(self, data):
        review_insert_query = "INSERT INTO reviews (book_id, content, posted_by, rating, created_at) VALUES (%s, %s, %s, %s, NOW())"
        review_insert_data = [data['book_id'], data['review_content'], data['posted_by'], data['rating']]
        review_return = self.db.query_db(review_insert_query, review_insert_data)
        print review_return
        return review_return

    def reviews_by_book(self, info):
        reviews_query = "SELECT books.title, books.id AS book_id, books.author_id, authors.author_name, reviews.rating, reviews.posted_by, users.alias, users.id, reviews.content, reviews.created_at FROM books JOIN authors ON books.author_id = authors.id JOIN reviews ON reviews.book_id = books.id JOIN users ON reviews.posted_by = users.id WHERE books.id = %s"
        reviews_data = [info]
        reviews_return = self.db.query_db(reviews_query, reviews_data)
        return reviews_return

    def new_review(self, info):
        new_query = "INSERT INTO reviews (book_id, content, posted_by, rating, created_at) VALUES (%s, %s, %s, %s, NOW())"
        new_data = [info['book_id'], info['content'], info['posted_by'], info['rating']]
        new_return = self.db.query_db(new_query, new_data)
        return new_return
