from django.shortcuts import render
from django.contrib.auth import logout as contribLogout, login as contribLogin
from django.contrib.auth import authenticate
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
import datetime, time, pytz
import json

from .models import Resa
from django.contrib.auth.models import User

def _(s):
    """
    translate function; defaults to identity
    """
    return s

def resa4date(date):
    """
    gets reservations for a given date
    @param date the date to query
    @return a list of reservations as tuples: (begin, duration, username)
    begin and duration are in minutes
    """
    result=[]
    if date:
        m,d,y = date.split("/")
        today=datetime.datetime(int(y), int(m), int(d), tzinfo=pytz.utc)
        tomorrow=today+datetime.timedelta(days=1)
        resa=Resa.objects.filter(beg__gte=today).filter(beg__lt=tomorrow)
        for r in resa:
            begin, duration, user = (r.beg-today).total_seconds()/60, (r.end-r.beg).total_seconds()/60, r.user.username
            result.append((begin, duration, user))
    return result

def timeslots (minutes=15):
    """
    Creates a list of timeslots ranging from "00:00" to "23:59"
    @param minutes the duration of a timeslot
    @return a list of timeslots as strings with the format "hh:mm"
    """
    result=[]
    t=0
    h=0
    m=0
    while t < 24*60:
        result.append("<span class='timeslot' title='{h:02d}:{m:02d}... free'>{h:02d}:{m:02d}<input name='t{t:d}' type='checkbox'/></span>".format(m=m, h=h, t=t))
        t+=minutes
        m+=minutes
        if m >= 60:
            h+=1
            m=0
    return result

def index(request):
    context={
        "timeslots": timeslots(15),
        "resa": json.dumps(resa4date(request.session.get("date",""))),
        "logoutURL": '%s?next=%s' % (settings.LOGOUT_URL, request.path),
        "loginURL": '%s?next=%s' % (settings.LOGIN_URL, request.path),
        }
    response = render(request,  'srv/index.html', context)
    response['Cache-Control'] = 'no-cache, no-store'
    return response

def logout(request):
    """
    implements a logout page for the application "srv"
    """
    contribLogout(request)
    return render(request,"srv/logout.html", {"next": request.GET.get("next","/")})

def login(request):
    """
    implements a login page for the application "srv"
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            contribLogin(request, user)
            msg="Welcome {}".format(user.username)
        else:
            msg="Sorry, the account {} is disabled".format(user.username)
    else:
        msg="Sorry, please try to login again, or check your accreditation"
    return render(request,"srv/login.html", {
        "next": request.GET.get("next","/"),
        "msg" : msg,
    })

def reservationsByDate(request):
    """
    gets reservations valid for some date
    @param request gives the wanted date in "wantedDate"
    @return reservations as a JSON string
    """
    date=request.GET.get('wantedDate','')
    request.session["date"]=date
    return JsonResponse({'resa': resa4date(date), 'date': date})

def makeResa(request):
    """
    makes reservations when possible
    @param request provides GET parameters like wantedDate, name,
    password, timeslots
    @return a report after inserting data into the database,
    in JSON string format    
    """
    ok=True
    msg=""
    date=request.GET.get('wantedDate','')
    minutes=[]
    if date:
        request.session["date"]=date
        m,d,y = date.split("/")
        today=datetime.datetime(int(y), int(m), int(d), tzinfo=pytz.utc)
        minutes=[int(ts[1:]) for ts in request.GET.get("timeslots").split(",")]
    else:
        ok=False
        msg+=_(" undefined date;")
    name=request.GET.get('name','')
    if name:
        request.session["name"]=name
    else:
        ok=False
        msg+=_(" undefined name;")
    user=User.objects.filter(username=name)
    if not user:
        ok=False
        msg+=_(" non-existing user: {};").format(name)
    else:
        user=user[0]
    if ok:
        # create reservations!
        for beg in minutes:
            t_beg=today+datetime.timedelta(seconds=beg*60)
            t_end=t_beg+datetime.timedelta(seconds=15*60)
            r=Resa(user=user, beg=t_beg, end=t_end)
            r.save()
    resa=resa4date(date)
    return JsonResponse({'ok': ok, 'msg': msg, 'minutes': minutes,
                         "name": name, 'resa': resa,})
