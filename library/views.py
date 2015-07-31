# Create your views here.
from django.shortcuts import render_to_response,RequestContext
from django.http import HttpResponse
from books.models import *
from users.models import *
import datetime
import pdb
import json
import string
import time
import math
import random

def home(request):
    return render_to_response('home.html')

def getBooks(request):
    type = request.POST['type']
    if type=="first":
        data_list = []
        books = Books.objects.order_by('id')[0:10]
        for i in range(0,len(books)):
            data = {}
            data['id'] = books[i].id
            data['name'] = books[i].name
            data['image_url'] = books[i].image_url
            data_list.append(data)
        return HttpResponse(json.dumps(data_list))
    bookTypeId = string.atoi(type)
    data_list = []
    books = Books.objects.filter(type_id=bookTypeId)
    for i in range(0,len(books)):
        data = {}
        data['id'] = books[i].id
        data['name'] = books[i].name
        data['image_url'] = books[i].image_url
        data_list.append(data)
    return  HttpResponse(json.dumps(data_list))

def getBorrow(request):
    data_list = []
    borrow_type = string.atoi(request.POST['borrow_type'])
    user_id = string.atoi(request.POST['user_id'])
    state = 0
    books_id = 0
    if borrow_type==1:
        state = 2
    if borrow_type==2:
        state = 3
    if borrow_type==3:
        state = 1
    borrows = Borrow.objects.filter(state = state,user_id = user_id)
    for i in range(0,len(borrows)):
        data = {}
        data['borrow_id'] = borrows[i].id
        books_id = borrows[i].books_id
        data['borrow_date'] = borrows[i].borrow_date.strftime("%Y-%m-%d")
        data['return_date'] = borrows[i].also_date.strftime("%Y-%m-%d")
        isbn = borrows[i].isbn
        try:
            books = Books.objects.get(id = books_id)
            data['book_name'] = books.name
        except Book.DoesNotExist:
            data['book_name'] = "null"
        data_list.append(data)
    return HttpResponse(json.dumps(data_list))

def getStudents(request):
    data_list = []
    user_id = string.atoi(request.POST['user_id'])
    class_id = 0
    try:
        teacher = User.objects.get(id = user_id,type=1)
        class_id = teacher.class_id
    except User.DoesNotExist:
        class_id = 0
    try:
        ourClass = Class.objects.get(id = class_id)
        data_list.append({"class_name":ourClass.name})
    except Class.DoesNotExist:
        data_list.append({"class_name":"null"})
    students = User.objects.filter(type = 0,class_id = class_id)
    for i in range(0,len(students)):
        data = {}
        data['student_id'] = students[i].id
        data['student_name'] = students[i].name
        data['student_borrow'] = students[i].borrow_total
        data['student_borrow_history'] = students[i].history_borrow_total
        data_list.append(data)
    return HttpResponse(json.dumps(data_list))

def searchBooks(request):
    text = request.POST['text']
    data_list = []
    books = Books.objects.filter(name__contains=text)
    for i in range(0,len(books)):
        data = {}
        data['id'] = books[i].id
        data['name'] = books[i].name
        data['image_url'] = books[i].image_url
        data_list.append(data)
    books1 = Books.objects.filter(author__contains=text)
    for i in range(0,len(books1)):
        data1 = {}
        data1['id'] = books1[i].id
        data1['name'] = books1[i].name
        data1['image_url'] = books1[i].image_url
        data_list.append(data1)
    return  HttpResponse(json.dumps(data_list))

def getOneBook(request):
    id = string.atoi(request.POST['id'])
    data_list = []
    try:
        book = Books.objects.get(id=id)
        data = {}
        data['id'] = book.id
        data['name'] = book.name
        data['author'] = book.author
        data['description'] = book.description
        data['version'] = book.version
        data['image_url'] = book.image_url
        data['total'] = book.total
        data['stock'] = book.stock
        data['address'] = book.address
        try:
            priceType = PriceType.objects.get(id=book.price_type_id)
            data['pay'] = priceType.duration
        except PriceType.DoesNotExist:
            data['pay'] = 0
        data_list.append(data)
    except Books.DoesNotExist:
        data_list.append({})
    return  HttpResponse(json.dumps(data_list))

def addclass(request):
    classname = request.POST['classname']
    startyear = request.POST['startyear']
    startmonth = request.POST['startmonth']
    endyear = request.POST['endyear']
    endmonth = request.POST['endmonth']
    start_date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(startyear+"-"+startmonth+"-1 00:00:00","%Y-%m-%d %H:%M:%S")))
    end_date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(endyear+"-"+endmonth+"-1 00:00:00","%Y-%m-%d %H:%M:%S")))
    newClass = Class(name=classname,start_date=start_date,end_date=end_date)
    newClass.save()
    return HttpResponse(json.dumps([{'state':'OK'}]))

def adduser(request):
    username = request.POST['username']
    account = request.POST['account']
    password = request.POST['password']
    type = string.atoi(request.POST['type'])
    userclass = string.atoi(request.POST['userclass'])
    user = User(name=username,account=account,password=password,class_id=userclass,type=type,borrow_total=0,history_borrow_total=0)
    user.save()
    return HttpResponse(json.dumps([{'state':'OK'}]))

def addpay(request):
    date = request.POST['date']
    t=datetime.datetime.fromtimestamp(time.mktime(time.strptime(date,"%Y-%m-%d %H:%M:%S")))
    payname = request.POST['payname']
    paynumber = string.atoi(request.POST['paynumber'])
    priceType = PriceType(price_type=0,price=payname,duration=paynumber,update= t,state=0)
    priceType.save()
    return HttpResponse(json.dumps([{'state':'OK'}]))

def commentOneBook(request):
    date = request.POST['date']
    comment_date=datetime.datetime.fromtimestamp(time.mktime(time.strptime(date,"%Y-%m-%d %H:%M:%S")))
    text = request.POST['commentText']
    username = request.POST['username']
    books_id = string.atoi(request.POST['bookId'])
    comment = Comment(text=text,books_id=books_id,user_name=username,comment_date= comment_date,type=0)
    comment.save()
    return HttpResponse(json.dumps([{'state':'OK'}]))

def startBorrowBook(request):
    book_id = string.atoi(request.POST['bookId'])
    try:
        books = Books.objects.get(id=book_id)
        if books.stock==0:
            return HttpResponse(json.dumps([{"type":1}]))
    except Books.DoesNotExist:
        return HttpResponse(json.dumps([{"type":2}]))
    i = 1
    while i>0:
        text = string.join(random.sample(['0','1','2','3','4','5','6','7','8','9','z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 7)).replace(' ','')
        borrows = Borrow.objects.filter(security_code=text)
        i = len(borrows)
    date = request.POST['date']
    t=datetime.datetime.fromtimestamp(time.mktime(time.strptime(date,"%Y-%m-%d %H:%M:%S")))
    t1=datetime.datetime.fromtimestamp(time.mktime(time.strptime("2100-12-12 12:59:59","%Y-%m-%d %H:%M:%S")))
    user_id = string.atoi(request.POST['userId'])
    borrow = Borrow(books_id=book_id,isbn="null",user_id=user_id,borrow_date= t,also_date=t1,security_code=text,state=1,payment=0)
    borrow.save()
    return HttpResponse(json.dumps([{'code':text,"type":0}]))

def borrowBookSearch(request):
    data_list = []
    books_id = 0
    user_id = 0
    security_code = request.POST['random']
    isbn = request.POST['isbn']
    try:
        borrow = Borrow.objects.get(security_code = security_code,state=1)
        data = {}
        data["borrow_id"] = borrow.id
        books_id = borrow.books_id
        user_id = borrow.user_id
        data_list.append(data)
    except Borrow.DoesNotExist:
        return HttpResponse(json.dumps([{"type":1}]))
    try:
        book = Book.objects.get(isbn=isbn,books_id=books_id,state=0)
        data = {}
        data["book_name"] = book.name
        data["book_author"] = book.author
        data["book_description"] = book.description
        data["book_price"] = book.price
        data["isbn"] = book.isbn
        data_list.append(data)
    except Book.DoesNotExist:
        return HttpResponse(json.dumps([{"type":2}]))
    try:
        user = User.objects.get(id=user_id)
        data = {}
        data["user_name"] = user.name
        data["user_account"] = user.account
        data_list.append(data)
    except User.DoesNotExist:
        return HttpResponse(json.dumps([{"type":4}]))
    try:
        books = Books.objects.get(id=books_id)
        data = {}
        data["books_image"] = books.image_url
        data_list.append(data)
        if books.stock==0:
            return HttpResponse(json.dumps([{"type":3}]))
    except Books.DoesNotExist:
        return HttpResponse(json.dumps([{"type":3}]))
    data_list.insert(0,{"type":0})
    return HttpResponse(json.dumps(data_list))

def submitBorrow(request):
    result = 0
    type = request.POST['type']
    user_id = 0
    books_id = 0
    isbn = request.POST['isbn']
    borrow_id = request.POST['borrow_id']
    if type=="1":
        borrow = Borrow.objects.get(id=borrow_id)
        borrow.state = 9
        borrow.isbn = isbn
        borrow.save()
    else:
        borrow = Borrow.objects.get(id=borrow_id)
        borrow.state = 2
        borrow.isbn = isbn
        borrow.save()
        user_id = borrow.user_id
        books_id = borrow.books_id
        isbn = borrow.isbn
        try:
            user = User.objects.get(id=user_id)
            user.borrow_total = user.borrow_total+1
            user.save()
        except User.DoesNotExist:
            result = 1
        try:
            book = Book.objects.get(isbn= isbn)
            book.state = 1
            book.save()
        except Book.DoesNotExist:
            result = 2
        try:
            books = Books.objects.get(id = books_id)
            books.stock = books.stock-1
            books.save()
        except Books.DoesNotExist:
            result = 3
    return HttpResponse(json.dumps({"result":result}))

def returnBook(request):
    data_list = []
    books_id = 0
    user_id = 0
    price_type_id = 0
    price = 0
    isbn = request.POST['isbn']
    try:
        borrow = Borrow.objects.get(isbn = isbn,state=2)
        data = {}
        data["borrow_startDate"] = borrow.borrow_date.strftime("%Y-%m-%d")
        books_id = borrow.books_id
        user_id = borrow.user_id
        data_list.append(data)
    except Borrow.DoesNotExist:
        return HttpResponse(json.dumps([{"type":1}]))
    try:
        book = Book.objects.get(isbn=isbn,books_id=books_id,state=1)
        data = {}
        data["book_name"] = book.name
        data["book_author"] = book.author
        data["book_description"] = book.description
        data["book_price"] = book.price
        data["isbn"] = book.isbn
        data_list.append(data)
    except Book.DoesNotExist:
        return HttpResponse(json.dumps([{"type":2}]))
    try:
        user = User.objects.get(id=user_id)
        data = {}
        data["user_name"] = user.name
        data["user_account"] = user.account
        data_list.append(data)
    except User.DoesNotExist:
        return HttpResponse(json.dumps([{"type":4}]))
    try:
        books = Books.objects.get(id=books_id)
        data = {}
        data["books_image"] = books.image_url
        price_type_id = books.price_type_id
        data_list.append(data)
    except Books.DoesNotExist:
        return HttpResponse(json.dumps([{"type":3}]))
    try:
        price_type = PriceType.objects.get(id=price_type_id)
        price = price_type.duration
    except PriceType.DoesNotExist:
        return HttpResponse(json.dumps([{"type":3}]))
    data1 = {}
    data1['type'] = 0
    data1['price'] = price
    data_list.insert(0,data1)
    return HttpResponse(json.dumps(data_list))

def downBook(request):
    data = {}
    isbn = request.POST["isbn"]
    try:
        book = Book.objects.get(isbn=isbn,state=0)
        books_id = book.books_id
        book.delete()
        try:
            books = Books.objects.get(id=books_id)
            books.total = books.total-1
            books.stock = books.stock-1
            books.save()
            data['type'] = 0
        except Books.DoesNotExist:
            data['type'] = 2
    except Book.DoesNotExist:
        data['type'] = 1
    return HttpResponse(json.dumps(data))

def showclass(request):
    data_list = []
    class_list = Class.objects.all()
    for i in range(0,len(class_list)):
        data = {}
        data['id'] = class_list[i].id
        data['name'] = class_list[i].name
        data['startdate'] = class_list[i].start_date.strftime("%Y-%m-%d")
        data['enddate'] = class_list[i].end_date.strftime("%Y-%m-%d")
        data_list.append(data)
    return HttpResponse(json.dumps(data_list))

def submitReturn(request):
    isbn = request.POST["isbn"]
    books_id = 0
    try:
        borrow =  Borrow.objects.get(isbn = isbn,state=2)
        borrow.state = 3
        borrow.save()
        try:
            book = Book.objects.get(isbn = isbn)
            book.state = 0
            book.save()
            books_id = book.books_id
        except Book.DoesNotExist:
            books_id = 0
        try:
            books = Books.objects.get(id = books_id)
            books.stock = books.stock+1
            books.save()
        except Books.DoesNotExist:
            books_id = 0
    except Borrow.DoesNotExist:
        books_id = 0
    return HttpResponse("hello word")

def showuser(request):
    data_list = []
    user_list = User.objects.all()
    for i in range(0,len(user_list)):
        data = {}
        data['id'] = user_list[i].id
        data['name'] = user_list[i].name
        try:
            userclass = Class.objects.get(id=user_list[i].class_id)
            data['class'] = userclass.name
        except Class.DoesNotExist:
            data['class'] = "NULL"
        data['account'] = user_list[i].account
        data['password'] = user_list[i].password
        data['type'] = user_list[i].type
        data['borrow_total'] = user_list[i].borrow_total
        data['history_borrow_total'] = user_list[i].history_borrow_total
        data_list.append(data)
    return HttpResponse(json.dumps(data_list))

def showpay(request):
    data_list = []
    pay_list = PriceType.objects.all()
    for i in range(0,len(pay_list)):
        data = {}
        data['id'] = pay_list[i].id
        data['name'] = pay_list[i].price
        data['duration'] = pay_list[i].duration
        data['update'] = pay_list[i].update.strftime("%Y-%m-%d")
        data_list.append(data)
    return HttpResponse(json.dumps(data_list))

def showComment(request):
    books_id = string.atoi(request.POST['bookId'])
    data_list = []
    comments = Comment.objects.filter(books_id=books_id)
    for i in range(0,len(comments)):
        data = {}
        data['username'] = comments[i].user_name
        data['text'] = comments[i].text
        data_list.append(data)
    return HttpResponse(json.dumps(data_list))

def bookupdate(request):
    books_id = 0
    bookName = request.POST['bookName']
    author = request.POST['author']
    image = request.POST['image']
    version = request.POST['version']
    isbn = request.POST['isbn']
    typeId = string.atoi(request.POST['typeId'])
    address = request.POST['address']
    pay = request.POST['pay']
    price = request.POST['price']
    description = request.POST['description']
    try:
        books = Books.objects.get(name=bookName)
        books.total = books.total+1
        books_id = books.id
        books.save()
    except Books.DoesNotExist:
        books1 = Books(name=bookName,author=author,description=description,version=version,image_url=image,total=1,stock=1,price_type_id=pay,type_id=typeId,address=address)
        books1.save()
        bookss = Books.objects.get(name=bookName)
        books_id = bookss.id
    book = Book(books_id = books_id,name = bookName,author=author,description=description,isbn=isbn,state=0,price=price)
    book.save()
    return HttpResponse(json.dumps([{'state':'OK'}]))

def login(request):
    data_list = []
    data = {}
    account = request.POST['account']
    password = request.POST['password']
    try:
        user = User.objects.get(account=account,password=password)
        data['id'] = user.id
        data['account'] = user.account
        data['type'] = user.type
        data['name'] = user.name
        data['password'] = user.password
        data_list.append(data)
        return HttpResponse(json.dumps(data_list))
    except User.DoesNotExist:
        data['type'] = 11
        data_list.append(data)
        return HttpResponse(json.dumps(data_list))

def student(request):
    id = string.atoi(request.GET["id"])
    account = request.GET["account"]
    try:
        user = User.objects.get(account=account,id=id)
        name = user.name
        return render_to_response('studenthome.html',{'id':id,'account':account,'name':name})
    except User.DoesNotExist:
        return render_to_response('home.html')

def teacher(request):
    id = string.atoi(request.GET["id"])
    account = request.GET["account"]
    try:
        user = User.objects.get(account=account,id=id)
        name = user.name
        return render_to_response('teacherhome.html',{'id':id,'account':account,'name':name})
    except User.DoesNotExist:
        return render_to_response('home.html')

def manage(request):
    id = string.atoi(request.GET["id"])
    account = request.GET["account"]
    try:
        user = User.objects.get(account=account,id=id)
        name = user.name
        return render_to_response('managehome.html',{'id':id,'account':account,'name':name})
    except User.DoesNotExist:
        return render_to_response('home.html')

def changePassword(request):
    id = string.atoi(request.POST["user_id"])
    password = request.POST['new_password']
    try:
        user = User.objects.get(id=id)
        user.password = password
        user.save()
        return HttpResponse(json.dumps({"type":0}))
    except User.DoesNotExist:
        return HttpResponse(json.dumps({"type":1}))