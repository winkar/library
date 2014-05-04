#coding: UTF-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from django.contrib.auth.decorators import login_required
from library.library.models import Book,Author,Publisher,Borrow
import pdb
import datetime


@login_required
def library(request):
    return render_to_response("index.html",context_instance=RequestContext(request))

@login_required
def book_info(request):
    book_name = request.REQUEST.get('book','not_found_book');
    book = Book.objects.filter(title = 'book_name')
    return render_to_response("book_info.html",{'book':book},context_instance=RequestContext(request))

def search_by_title(info):
    return Book.objects.filter(title__contains = info)

def search_by_Author(info):
#    return Author.object.filter(first_name_contains = info)
#    return Author.object.filter(last_name_contains = info)
    return Book.objects.filter(authors__first_name__contains = info)

def search_by_Publisher(info):
#    return Publisher.object.filter(name_contains = info)
    return Book.objects.filter(publisher__name__contains = info)

def borrowed(book):
    borrow = Borrow.objects.filter(book_id = book.id, return_date__isnull = True)
    if borrow:
        return u'已借出'
    return u'在架上'

@login_required
def search(request):
    info = request.REQUEST.get('info')
    byAuthor = request.REQUEST.get('byAuthor')
    byPublisher = request.REQUEST.get('byPublisher')
    byTitle = request.REQUEST.get('byTitle')

#    pdb.set_trace()

    books = []
    if byAuthor=="true":
        books += search_by_Author(info)
    if byPublisher=="true":
        books += search_by_title(info)
    if byTitle=="true":
        books += search_by_Publisher(info)
    books = {}.fromkeys(books).keys()  
  #  print books

    book_info = [{"title":book.title, 
                "authors":book.authors.all(), 
                "publisher":book.publisher,
                "imageurl" : book.image.url,
                "publication_date" :book.publication_date,
                "borrowed" : borrowed(book),
                "id" : book.id,
                } for book in books]
    return render_to_response("search.html",{'books':book_info},context_instance=RequestContext(request))


def inhand(book, user):
    inhand = Borrow.objects.filter(book_id = book.id, return_date__isnull = True, user__id = user.id)
    if inhand:
        return "inhand"
    return None


@login_required
def book_info(request):
    bookId = request.REQUEST.get('bookId')

    book = Book.objects.filter(id = bookId) [0]
    info = {"title":book.title, 
                "authors":book.authors.all(), 
                "publisher":book.publisher,
                "imageurl" : book.image.url,
                "publication_date" :book.publication_date,
                "borrowed" : borrowed(book),
                "inhand" : inhand(book, request.user),
                "id" : book.id,
                } 
    return render_to_response("book_info.html",{'book':info},context_instance=RequestContext(request))

DEBUG =0
@login_required
def borrow(request):
    bookId = request.REQUEST.get("bookId")
    if DEBUG :
        pdb.set_trace()
    book = Book.objects.filter(id = bookId) [0]
    
    if not inhand(book, request.user):
        borrow = Borrow(book = book,
                        user = request.user,
                        borrow_date = datetime.datetime.now().date() 
                        )
        borrow.save() 
    
    info = {"title":book.title, 
                "authors":book.authors.all(), 
                "publisher":book.publisher,
                "imageurl" : book.image.url,
                "publication_date" :book.publication_date,
                "borrowed" : borrowed(book),
                "inhand" : inhand(book, request.user),
                "id" : book.id,
                } 
    return render_to_response("book_info.html",{'book':info},context_instance=RequestContext(request))

@login_required
def return_book(request):
    bookId = request.REQUEST.get("bookId")
    book = Book.objects.filter(id = bookId) [0]
    borrow = Borrow.objects.filter(book_id = book.id, return_date__isnull = True, user__id = request.user.id)
    if len(borrow)>0:
        borrow[0].return_date = datetime.datetime.now().date()
        borrow[0].save() 
        
    info = {"title":book.title, 
                "authors":book.authors.all(), 
                "publisher":book.publisher,
                "imageurl" : book.image.url,
                "publication_date" :book.publication_date,
                "borrowed" : borrowed(book),
                "inhand" : inhand(book, request.user),
                "id" : book.id,
                } 
    return render_to_response("book_info.html",{'book':info},context_instance=RequestContext(request))


@login_required
def query(request):
    bookId = request.REQUEST.get("bookId")
    user = request.user

    borrows = Borrow.objects.filter(user__id = user.id, return_date__isnull = True)
    books = [ borrow.book for borrow in borrows]
    book_info = [{"title":book.title, 
                "authors":book.authors.all(), 
                "publisher":book.publisher,
                "imageurl" : book.image.url,
                "publication_date" :book.publication_date,
                "borrowed" : borrowed(book),
                "id" : book.id,
                } for book in books]
    return render_to_response("query.html",{'books':book_info},context_instance=RequestContext(request))
