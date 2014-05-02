from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from django.contrib.auth.decorators import login_required
from library.library.models import Book,Author,Publisher
import pdb

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

  #  print books
    book_info = [{"title":book.title, "authors":book.authors.all(), "publisher":book.publisher} for book in books]
    return render_to_response("search.html",{'books':book_info},context_instance=RequestContext(request))



