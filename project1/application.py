# -*- coding: UTF-8 -*-
import os
import requests
from flask import Flask, flash, jsonify, render_template, request, \
    redirect, session, url_for
from jinja2 import Markup
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Blueprint
from flask_paginate import Pagination, get_page_args


app = Flask(__name__, static_folder='static')
mod = Blueprint('/', __name__)


def get_gr(isbn, api='review_counts', success_code=200):
    """Goodreads API data
    return json or None
    """
    urls = {'review_counts': 'https://www.goodreads.com/book/review_counts.json'}
    url = urls[api]
    res = requests.get(
            url, params={'key': 'yFLoMH1lgWCNlYDs1kWA', 'isbns': isbn},
            timeout=10)
    try:
        res = requests.get(
            url, params={'key': 'yFLoMH1lgWCNlYDs1kWA', 'isbns': isbn},
            timeout=10)
    except requests.exceptions.ProxyError:
        res = requests.get(
            url, params={'key': 'yFLoMH1lgWCNlYDs1kWA', 'isbns': isbn},
            proxies={'http': os.getenv('http_proxy'),
                     'https': os.getenv('https_proxy')},
            timeout=10)
    if res.status_code == success_code:
        return res.json()
    else:
        return None


def subset_rec(rec, offset=0, per_page=20):
    return rec[offset: offset + per_page]



# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
sess = db()


@app.teardown_request
def remove_session(ex=None):
    db.remove()


@app.route("/", methods=['GET'])
def home():
    """Home page
    """
    if session.get('act_user') is None:
        return redirect(url_for("sign_in"))
    else:
        return render_template("index.html", act_user=session.get('act_user'))


@app.route("/login", methods=['GET', 'POST'])
def sign_in():
    """Sign in
    """
    if request.method == 'GET':
        if session.get('act_user') is None:
            return render_template(
                "login.html", act_user=session.get("act_user"))
        else:
            return render_template(
                "index.html", act_user=session.get("act_user"))
    elif request.method == 'POST':
        username = request.form.get('username')
        pwd = request.form.get('password')
        mbrinfo = sess.execute(
            """SELECT id, username FROM mbr WHERE username = :username
            AND pwd = :pwd;""",
            {"username": username, "pwd": pwd}).fetchone()
        if mbrinfo is None:
            flash(Markup(
                """<i class='fa fa-2x fa-exclamation-circle'></i>
                User not exist or wrong password."""), 
                'danger')
        else:
            session['act_user'] = {'id': mbrinfo[0], 'username': mbrinfo[1]}
        return home()


@app.route('/logout', methods=['GET'])
def sign_off():
    session.pop('act_user', None)
    flash(Markup(
        """<i class='fa fa-2x fa-check-square-o'></i>
        You have logged out."""), 'success')
    return home()


@app.route("/signup", methods=['GET', 'POST'])
def sign_up():
    """Sign up
    """
    if request.method == 'GET':
        return render_template("register.html", act_user=None)
    elif request.method == 'POST':
        username = request.form.get('username')
        pwd = request.form.get('password')
        repwd = request.form.get('repassword')
        mbrinfo = sess.execute(
            """SELECT id, username FROM mbr WHERE username = :username;""", 
            {"username": username}).fetchone()
        if mbrinfo is not None:
            flash(Markup(
                """<i class='fa fa-2x fa-check-square-o'></i>
                The username has been registered. Please change one."""), 
                'warning')
            return redirect(url_for('sign_up'))
        else:
            if pwd == repwd:
                sess.execute(
                    'INSERT INTO mbr (username, pwd) VALUES (:username, :pwd);',
                    {'username': username, 'pwd': pwd})
                sess.commit()
                flash(Markup(
                    """<i class='fa fa-2x fa-check-square-o'></i>
                    You have successfully created a new account. Now sign in."""), 
                    'success')
                return redirect(url_for("sign_in"))
            else:
                flash(Markup(
                    """<i class='fa fa-2x fa-exclamation-circle'></i>
                    You did not input the same password."""), 'danger')
                return redirect(url_for('sign_up'))


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        books = sess.execute(
            'SELECT id, isbn, title, author, year FROM book;').fetchall()
    elif request.method == 'POST':
        # run the query
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        author = request.form.get('author')
        qry = ["%s LIKE '%%%s%%'" % (x, y) for x, y in
            (('isbn', isbn), ('title', title), ('author', author))
            if y is not None and y != '']
        if len(qry) == 0:
            books = sess.execute(
                'SELECT id, isbn, title, author, year FROM book;').fetchall()
        else:
            books = sess.execute(
                'SELECT id, isbn, title, author, year FROM book WHERE '
                + ' AND '.join(qry) + ';').fetchall()
        # flash(Markup(
        #     """<i class='fa fa-2x fa-info-circle'></i>
        #     A total of %i books found.""" % len(books)), 'info')

    page, _, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    page_books = subset_rec(books, offset=offset, per_page=20)
    pagination = Pagination(page=page, total=len(books), bs_version=3, per_page=20)

    return render_template(
        'index.html', act_user=session.get('act_user'), books=page_books, pagination=pagination)


@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def review(book_id):
    """Book detail
    """
    book = sess.execute(
        """SELECT id, title, author, isbn, year FROM book WHERE
        id = :book_id""", {"book_id": book_id}).fetchone()
    gr_data = get_gr(isbn=book[3])
    if gr_data is not None:
        gr_data = gr_data['books'][0]
    else:
        gr_data = {'work_ratings_count': '', 'average_rating': ''}
    my_reviews = sess.execute(
        """SELECT count(*) FROM review WHERE mbr_id = :mbr_id and
        book_id = :book_id;""",
        {'mbr_id': session.get('act_user')['id'],
         'book_id': book_id}).fetchone()[0]
    if engine.name == 'sqlite':
        reviews_qry = """SELECT review.id, 
            datetime(review.rev_at, 'localtime'),
            mbr.username, review.rating, review.review FROM
            review LEFT JOIN mbr ON review.mbr_id = mbr.id
            WHERE review.book_id = :book_id"""
    elif engine.name == 'postgresql':
        reviews_qry = """SELECT review.id, 
            review.rev_at at time zone 'utc' at time zone 'cst',
            mbr.username, review.rating, review.review FROM
            review LEFT JOIN mbr ON review.mbr_id = mbr.id
            WHERE review.book_id = :book_id"""
    reviews = sess.execute(
        reviews_qry, {"book_id": book_id}).fetchall()
    # methods
    if request.method == 'GET':
        return render_template(
            'book.html', act_user=session.get('act_user'), book=book
            , reviews=reviews, gr_data=gr_data, my_reviews=my_reviews)
    elif request.method == 'POST':
        comment = request.form.get('comment')
        rating = request.form.get('rating')
        if (comment is not None and comment != '') or \
            (rating is not None and rating != ''):
            sess.execute(
                """INSERT INTO review (mbr_id, book_id, rating, review)
                VALUES (:mbr_id, :book_id, :rating, :review);""",
                {'mbr_id': session.get('act_user')['id'],
                 'book_id': book_id, 'rating': rating, 'review': comment})
            sess.commit()
            flash(Markup(
                """<i class='fa fa-2x fa-check-square-o'></i>
                You have successfully submitted the comment."""), 'success')
        else:
            flash(Markup(
                """<i class='fa fa-2x fa-warning'></i>
                You cannot submit empty rating and comments."""), 'warning')
        return redirect(url_for("review", book_id=book_id))


@app.route('/api/book', methods=['GET'])
def api():
    if session.get('act_user') is None:
        return render_template(
            "error.html", act_user=None, err="404 Error",
            err_info="You have not logged in!")
    book_isbn = request.args.get('isbn')
    book = sess.execute(
        """SELECT id, title, author, isbn, year FROM book WHERE
        isbn = :book_isbn""", {"book_isbn": book_isbn}).fetchone()
    if book is None or len(book) == 0:
        return render_template(
            "error.html", act_user=session.get('act_user'),
            err="404 Error", err_info="Book with ISBN = %s not found!" % book_isbn)
    else:
        gr_data = get_gr(isbn=book_isbn)
        if gr_data is not None:
            gr_data = gr_data['books'][0]
        else:
            gr_data = {'work_ratings_count': '', 'average_rating': ''}
        rslt = {'result': True, 'book': 
            {'title': book[1], 'author': book[2], 'year': book[4]
            , 'isbn': book[3], 'review_count': gr_data['work_ratings_count']
            , 'average_score': gr_data['average_rating']}}
        return jsonify(rslt)


if __name__ == "main":
    app.run(debug=True)
