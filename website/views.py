from flask import Blueprint, render_template, request,session
from .database import *
import random

views = Blueprint("views",__name__)
genres = db_genres()
@views.route("/")
def viewsPage():
    top = db_top_books()
    
    randomlist = random.sample(range(0, 9), 5)
    books = [top[i] for i in randomlist]
    for book in books:
        book['rating_path'] = '/static/img/rating/' + str(round(book['rating'])*10)+'percent.png'
        #book['authors'] = db_book_authors(book['title_id'])

    
    return render_template("/main/main.html",books=books,genres=genres)

@views.route("/list/")
def listPage():
    book_list = [{'Name' : 'HP1', 'Author': 'J.K.Rowling'},{'Name' : 'HP1', 'Author': 'J.K.Rowling'}]
    books = db_books()
    
    result = []
    for i in range(0,len(books),5):
        end = i+5 if (i+5) < len(books) else len(books)
        tmp = []
        for book in books[i:end]:
            book['rating_path'] = '/static/img/rating/' + str(round(book['rating'])*10)+'percent.png'
            tmp.append(book)
        result.append(tmp)

    return render_template("/main/list.html",books=result,genres=genres)
    
@views.route("/detail/")
def detailPage():
    return render_template('/main/detail.html',genres=genres)



@views.route("/libraries/")
def librariesPage():
    libraries = db_libraries()
    print(libraries)
    return render_template('/main/libraries.html',libraries=libraries,genres=genres)


@views.route("/books/genre/<genreid>")
def booksByGenre(genreid):
    books = db_books_with_genre(genreid)
    genre = db_genre_info(genreid)[0]
    result = []
    for i in range(0,len(books),5):
        end = i+5 if (i+5) < len(books) else len(books)
        tmp = []
        for book in books[i:end]:
            book['rating_path'] = '/static/img/rating/' + str(round(book['rating'])*10)+'percent.png'
            tmp.append(book)
        result.append(tmp)
    return render_template('/main/list.html',books=result,genres=genres,active=genre)
    

@views.route("books/library/<library>")
def booksInLibrary(library):
    
    books = db_books_in_lib(library)
    library = db_library_info(library)[0]['name']
    print(library)
    result = []
    for i in range(0,len(books),5):
        end = i+5 if (i+5) < len(books) else len(books)
        tmp = []
        for book in books[i:end]:
            book['rating_path'] = '/static/img/rating/' + str(round(book['rating'])*10)+'percent.png'
            tmp.append(book)
        result.append(tmp)

    return render_template("/main/list.html",books=result,library=library,genres=genres,library_name=library)

@views.route("/detail/<bookid>")
def bookDetail(bookid):
    book = db_book_by_id(bookid)[0]
    book['rating_path'] = '/static/img/rating/' + str(round(book['rating'])*10)+'percent.png'
    
    print(book)
    return render_template('/main/detail.html',book=book,genres=genres)

# {'title_id': 15,
# 'release_date': datetime.date(2021, 2, 1),
# 'ISBN': '9788088243519',
# 'rating': 8.2,
# 'description': 'Franku Cottonovi, požitkáři, jenž vyčerpal veškeré možnosti zábavy v této realitě, se podařilo odhalit tajemství Lemarchandovy kostky, bájného hlavolamu, který otevírá dveře k absolutním rozkoším jiných sfér. Stanul na prahu a vyčkával příchodu svých průvodců, cenobitů, příslušníků tajného řádu těch, kdo rozkoš také hledali, našli a už také pochopili, že s vypjatou smyslností je neodmyslitelně spjata i její věčná souputnice: trýznivá bolest. Hrůzná, nesnesitelná kombinace však Franka přivede za hranici života, zpoza níž mu může pomoci pouze Julia, žena, která kdysi podlehla kouzlu jeho osobnosti. Při boji za Frankovu záchranu dojde ke střetu zástupců pekelného světa blahé agonie s obyčejnými smrtelníky, ovládanými chtíčem, žárlivostí i láskou.',
# 'path_to_picture': '/static/img/hellraiser.jpg',
# 'name': 'Hellraiser'}

#static/img/libraries/lib7.jpg
#static/img/libraries/lib7.jpg