# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime , timedelta
# from django.utils.datetime_safe import new_datetime , timedelta
from jalali_date import date2jalali , datetime2jalali
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
import models
from django.core.paginator import Paginator
from django.urls import reverse 

def index(request):
    categorys = models.Category.objects.all()
    context = {'cats' : categorys}
    return render(request,"lib/index.html" , context)

def category(request , pk):
    category = models.Category.objects.get(pk=pk)
    books = category.book_set.all()
    paginator = Paginator(books, 10)
    if request.method == 'GET' and 'page' in request.GET:
        page = request.GET['page']
        if page is not None and page != '':
            current_page = page
    else:
        current_page = 1
    books = paginator.page(current_page)
    findex = books.start_index()
    for book in books:
        book.index = findex
        findex = findex + 1 
    context = {'cat' : category , 'paginator' : paginator , 'books' : books , 'currentpage' : current_page}
    return render(request,"lib/cats.html" , context)

def books(request , pk):
    
    book = models.Book.objects.get(pk=pk)
    if book.status!= "available":
        difftime = book.backDate - timezone.now()  
        print(datetime2jalali(book.backDate))
        if ( difftime.days < 0):
            book.status = "available"
            book.backDate = timezone.now()
            book.save()
            book = models.Book.objects.get(pk=pk)
    context = {'book' : book ,}
    return render(request,"lib/book.html" , context)


def reserveaction(request):
    bookpk = request.POST['book']
    book = models.Book.objects.get(pk=bookpk)
    if book:
        if book.status != "available":
            resp = "book is not available"
            err = 0 
        else:
            book.backDate = timezone.now() + timedelta(minutes = 5)
            book.status = "reserved"
            book.save()
    book = models.Book.objects.get(pk=bookpk)
    return HttpResponse(book.status)