from flask import Blueprint, render_template, request,session
from .database import *

views = Blueprint("views",__name__)

@views.route("/")
def viewsPage():
    return render_template("/main/main.html")

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

    return render_template("/main/list.html",books=result)
    
@views.route("/detail/")
def detailPage():
    return render_template('/main/detail.html')



@views.route("/form/demo/",methods=["GET","POST"])
def formPage():
    if request.method == "POST":
        print(request.form.get('text'))
    
    return render_template('/main/formTemplate.html')

@views.route("/libraries/")
def librariesPage():
    libraries = db_libraries()
    print(libraries)
    return render_template('/main/libraries.html',libraries=libraries)


@views.route("books/library/<library>")
def booksInLibrary(library):
    # get books for library
    aaaaa = db_books_in_lib(library)
    print(aaaaa)
    books = db_books()
    
    result = []
    for i in range(0,len(books),5):
        end = i+5 if (i+5) < len(books) else len(books)
        tmp = []
        for book in books[i:end]:
            book['rating_path'] = '/static/img/rating/' + str(round(book['rating'])*10)+'percent.png'
            tmp.append(book)
        result.append(tmp)

    return render_template("/main/list.html",books=result,library=library)

@views.route("/detail/<bookid>")
def bookDetail(bookid):
    book = db_book_by_id(bookid)[0]
    book['rating_path'] = '/static/img/rating/' + str(round(book['rating'])*10)+'percent.png'
    
    print(book)
    return render_template('/main/detail.html',book=book)

# {'title_id': 15,
# 'release_date': datetime.date(2021, 2, 1),
# 'ISBN': '9788088243519',
# 'rating': 8.2,
# 'description': 'Franku Cottonovi, požitkáři, jenž vyčerpal veškeré možnosti zábavy v této realitě, se podařilo odhalit tajemství Lemarchandovy kostky, bájného hlavolamu, který otevírá dveře k absolutním rozkoším jiných sfér. Stanul na prahu a vyčkával příchodu svých průvodců, cenobitů, příslušníků tajného řádu těch, kdo rozkoš také hledali, našli a už také pochopili, že s vypjatou smyslností je neodmyslitelně spjata i její věčná souputnice: trýznivá bolest. Hrůzná, nesnesitelná kombinace však Franka přivede za hranici života, zpoza níž mu může pomoci pouze Julia, žena, která kdysi podlehla kouzlu jeho osobnosti. Při boji za Frankovu záchranu dojde ke střetu zástupců pekelného světa blahé agonie s obyčejnými smrtelníky, ovládanými chtíčem, žárlivostí i láskou.',
# 'path_to_picture': '/static/img/hellraiser.jpg',
# 'name': 'Hellraiser'}

#static/img/libraries/lib7.jpg
#static/img/libraries/lib7.jpg