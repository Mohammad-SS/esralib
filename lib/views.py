# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime , timedelta
from jalali_date import date2jalali , datetime2jalali
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
import models
from django.core.paginator import Paginator
from django.urls import reverse 

# This View renders main screen . it should be completed when links and statistics get ready
def index(request):
    categorys = models.Category.objects.all()
    context = {'cats' : categorys}
    return render(request,"lib/index.html" , context)

# This View renders the categorys page . 
def category(request , pk):
    category = models.Category.objects.get(pk=pk)
    books = category.book_set.all()
    # Paginator part books in sections with 10 book .
    paginator = Paginator(books, 10)
    if request.method == 'GET' and 'page' in request.GET:
        page = request.GET['page']
        # we should is there any get request for pages ?
        if page is not None and page != '':
            # if there is , current page is that 
            current_page = page
    else:
        # if there is not , we are absoloutly in first page !
        current_page = 1
    books = paginator.page(current_page)
    # it returns the first index of this page
    findex = books.start_index()
    for book in books:
        book.index = findex
        findex = findex + 1 
    context = {'cat' : category , 'paginator' : paginator , 'books' : books , 'currentpage' : current_page}
    return render(request,"lib/cats.html" , context)

def books(request , pk):
    book = models.Book.objects.get(pk=pk)
    if book.status == "reserved":
        # if book is is reserve status , we must see when this book will come back . if this time is passe , so this book is available
        difftime = book.backDate - timezone.now()  
        # when the time is passed , diff time will be negative in days and passed seconds , in seconds 
        if ( difftime.days < 0):
            book.status = "available"
            book.backDate = timezone.now()
            book.save()
            book = models.Book.objects.get(pk=pk)
    context = {'book' : book }
    return render(request,"lib/book.html" , context)

# This view response only ajax calls from inside of this site . because we should take care of CSRF attacks for more security .
def reserveaction(request):
    bookpk = request.POST['book']
    book = models.Book.objects.get(pk=bookpk)
    if book:
        # if two requests comes in one time ...
        if book.status != "available":
            resp = "book is not available"
        else:
            book.backDate = timezone.now() + timedelta(minutes = 5)
            book.status = "reserved"
            book.save()
    book = models.Book.objects.get(pk=bookpk)
    return HttpResponse(book.status)

# this view renders login page . iam going to make this page better and better , so things i should be aware of :
# 1- i must define a form , that sends logins data to back end ( and ofcours a view that should be named action_login ) 
# and if this data was valid , i should do something like it : section['userpk'] = user.pk .
# 2- i must edit all others view , and check if section['userpk'] is empty , so go to login page ! 
# 3- i should define some more tables , user table , barrows table (i dont know is barrow good or not :D ) 
# 4- and i dont know which is better for now ? ajax call or form requests . i should think a lot ! 
def login(request):
    pass

# this view will insert dummy books to database , so we can debug better !
def dummybooks(request):
    a = 0
    category = models.Category.objects.get(pk=4)
    while a<30:
        book = models.Book(name='کتاب های دسته چهارم' , category=category , documentNumber='123456' , idNumber='54321' , author='سید محمد باقر عظیمی' , publisher='نشر اسراء' , publishdate='پارسال' , info='شماره کتاب :' + str((a+1)*163) )
        book.save()
        a = a+1
    return HttpResponse(a)