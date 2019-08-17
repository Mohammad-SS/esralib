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
    if logedin(request):
        user = models.User.objects.get(pk=request.session['user'])
    else:
        user = None
    title = "کتابخانه موسسه اسراء"
    categorys = models.Category.objects.all()
    context = {'cats' : categorys , "title" : title , "user" : user}
    return render(request,"lib/index.html" , context)

# This View renders the categorys page . 
def category(request , pk):
    if logedin(request):
        user = models.User.objects.get(pk=request.session['user'])
    else:
        user = None
    category = models.Category.objects.get(pk=pk)
    title = "کتابخانه موسسه اسراء"
    title = title + " | " + category.name
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
    context = {'cat' : category , 'paginator' : paginator , 'books' : books , 'currentpage' : current_page , 'title' : title , "user" : user}
    return render(request,"lib/cats.html" , context)

def books(request , pk):
    if logedin(request):
        user = models.User.objects.get(pk=request.session['user'])
    else:
        user = None
    title = "کتابخانه موسسه اسراء"
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
    title = title + " | " + book.name
    context = {'book' : book , "title" : title , "user" : user}
    return render(request,"lib/book.html" , context)

# This view response only ajax calls from inside of this site . because we should take care of CSRF attacks for more security .
def reserveaction(request):
    bookpk = request.POST['book']
    userpk = request.POST['user']
    book = models.Book.objects.get(pk=bookpk)
    if book:
        # if two requests comes in one time ...
        if book.status != "available":
            resp = "book is not available"
        else:
            book.backDate = timezone.now() + timedelta(minutes = 5)
            book.status = "reserved"
            book.save()

            user = models.User.objects.get(pk=userpk)
            barrow = models.Barrow(user=user , book=book , startDate = timezone.now() , endDate= book.backDate )
            barrow.save()
    book = models.Book.objects.get(pk=bookpk)
    return HttpResponse(book.status)

# this view renders login page . 
def login(request):
    if logedin(request):
        return HttpResponseRedirect(reverse('index'))
    else:
        HttpResponseRedirect(reverse('login'))
    if request.method == 'GET' and 'err' in request.GET:
        # we should is there any get request for pages ?
        if request.GET['err'] is not None and request.GET['err'] != '':
            # if there is , current page is that 
            err = request.GET['err']
    else:
        # if there is not , we are absoloutly in first page !
        err = ''
    context = { 'err' : err}
    return render(request,"lib/login.html" , context)

# this page makes logout . i didnt link anywhere to this , so i must do it manually
def logout(request):
    request.session.flush()
    return HttpResponse("happened")

# view to do login . this page just log you in to website using data that you send from login view
# errors : 
# 1 = User not found
# 2 = Username is not found
# 3 = Password is not correct
def dologin(request):
    # checking is this request sent by POST Method ?
    err = 1
    if request.method == 'POST' and 'username' in request.POST and 'pass' in request.POST:
        # if yes , is user name sent ?
        if request.POST['username'] is not None and request.POST['username'] != '':
            username = request.POST['username']
        else:
            # if not , go back to login page with error 2
            err = 2 
        # same as username cheking
        if request.POST['pass'] is not None and request.POST['pass'] != '':
            password = request.POST['pass']
        else:
            err = 3
        # if we have any error , we will break everything here
        if err :
            return HttpResponseRedirect(reverse('login')+ "?err=" + str(err))
        # if we have no error , so we can check database
        else:
            # lets take user from database
            user = models.User.objects.filter(identityNumber=username , password=password)        
            # is this user exist !? how many ?!
            if user.count() != 1:
                err = 1
                # if err = 1 , so user does not exist 
                return HttpResponseRedirect(reverse('login')+ "?err=" + str(err))
            else:
                # we have no error , every thing is perfect !
                err = 0
                user = user[0]
                request.session['user'] = user.pk
                return HttpResponseRedirect(reverse('login'))

    

# this view will insert dummy books to database , so we can debug better !
def dummybooks(request):
    a = 0
    category = models.Category.objects.get(pk=4)
    # while a<30:
        # book = models.Book(name='کتاب های دسته چهارم' , category=category , documentNumber='123456' , idNumber='54321' , author='سید محمد باقر عظیمی' , publisher='نشر اسراء' , publishdate='پارسال' , info='شماره کتاب :' + str((a+1)*163) )
        # book.save()
        # a = a+1
    # return HttpResponse(request.session['username'])
    # return HttpResponse(a)

# this function will check if the user is loged in or not
# args : request (req object)
# return : True of False (boolean)
def logedin(request):
    if "user" in request.session:
        if request.session['user'] is not None and request.session['user'] != "" :
            return True
        else:
            return False
    else:
        return False
