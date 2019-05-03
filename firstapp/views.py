from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect
from django.contrib import messages
from .functions import *
import ast

cUser = None
fid = None
fname = None
cid = None
cname = None
# Create your views here.
def home(request):
    return render(request, "firstapp/home.html")


def logout(request):
    cUser = None
    return render(request, "firstapp/home.html")


def login(request):
    global cUser
    users = get_users()
    logged = False
    data = {"user": "sultan", "password": "super", "message": "User name or password is incorrect"}
    uname = request.POST.get("username")
    upass = request.POST.get("userpass")

    for u in users:
        if u[1] == uname:
            if u[2] == upass:
                cUser = {"username": u[1], "userpass": u[2]}
                logged = True
                break

    if not logged:
        return render(request, "firstapp/home.html", context= data)
    return HttpResponsePermanentRedirect("/profile")


def hello(request):
    return HttpResponse("<h2>Hello WORLD!</h2>")


def about(request):
    return HttpResponse("<ul><li>Heulo</li><li>Miello</li><li>Fuckin akello</li></ul>")


def products(request, pr_id = 1):
    category = request.GET.get("cat", "Man")
    if pr_id > 20:
        output = "<h1>Product with id: {}, Category: {}</h1>".format(pr_id, category)
    else:
        output = "<h1>Product with id: -13, Category: {}</h1>".format(category)

    return HttpResponse(output)


def users(request):
    name = request.GET.get("name", "Sultan")
    id = request.GET.get("id", 1)
    output = "<h2>User {} id: {}</h2>".format(name, id)

    return HttpResponse(output)


def contacts(request):
    return HttpResponseRedirect("/about")


def details(request):
    return HttpResponsePermanentRedirect("/")


def logup(request):
    global cUser
    if request.method == "GET":
        return render(request, "firstapp/logup.html")
    else:
        users = get_users()
        uname = request.POST.get("uname")
        upass1 = request.POST.get("pass1")
        upass2 = request.POST.get("pass2")
        data = {"message": ""}
        key = False

        if upass1 == upass2:
            for u in users:
                if u[1] == uname:
                    data['message'] = "There exists user with such name"
                    key = True
                    break

            if not key:
                messages.info(request, 'Now you are one of us!')
                set_user(uname, upass1)
                udata = {"user": uname, "password": upass1}
                return render(request, "firstapp/home.html", context= udata)

        else:
            data['message'] = "Passwords aren't the same, try again"

        return render(request, "firstapp/logup.html", context= data)


def profile(request):
    return render(request, "firstapp/profile.html", context= cUser)


def cinemas(request):
    cins = get_cinemas()
    return render(request, "firstapp/cinemas.html", context= {"cins": cins})


def history(request):
    orders = get_orders(cUser["username"])
    new_orders = []
    for order in orders:
        new_orders.append(ast.literal_eval(order[0]))

    context = {"orders": new_orders}
    return render(request, "firstapp/history.html", context= context)

def films(request, cin="unknown"):
    global cid, cname
    cid = request.GET.get("cid")
    cname = cin
    cid = int(cid)
    films = get_films()
    new_films = []
    x = 3

    for f in range(0, len(films)):
        path = "images/{}.jpg"
        open = False
        close = False
        if f == 0 or f == x:
            open = True
        elif f == 2 or f == (2+x):
            if f != 2:
                x += 3
            close = True
        elif f == len(films):
            close = True
        new_films.append((films[f][0], films[f][1], films[f][2], open, close, path.format(films[f][0])))

    data = { "cinema": cname, "films": new_films}
    return render(request, "firstapp/films.html", context= data)


def myfilm(request):
    global fid, fname
    fid = request.GET.get("id")
    fid = int(fid)
    film_info = get_film_info(fid, cid)
    fname = film_info[1]
    path = "images/{}.jpg".format(fid)
    filmdata = {"film": film_info, "path": path}

    return render(request, "firstapp/myfilm.html", context= filmdata)


def booking(request):
    sid = request.GET.get("sid")
    seats = get_seats(sid)
    new_seats = []
    i = 0
    for s in seats:
        open = False
        close = False
        if i == 0 or i == 5:
            open = True
        if i == 4 or i == 9:
            close = True
        new_seats.append((s[0], s[1], s[2], open, close))
        i += 1

    data = {"seats": new_seats, "filmname": fname}
    return render(request, "firstapp/booking.html", context= data)

def bookseats(request):
    seats = request.POST.getlist("seat-input")
    kids = request.POST.get("kids")
    studs = request.POST.get("students")
    adults = request.POST.get("adults")
    kids = int(kids)
    studs = int(studs)
    adults = int(adults)
    tickets = {
        "kids": kids,
        "students": studs,
        "adults": adults,
        "total": kids + studs + adults
    }
    book_seats(cUser["username"], fid, cinema=(cid, cname), seats= seats, tickets= tickets)

    return render(request, "firstapp/profile.html", context= cUser)


