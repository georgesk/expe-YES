from django.shortcuts import render
from django.contrib.auth import logout as contribLogout, login as contribLogin
from django.contrib.auth import authenticate
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
import datetime, time, pytz
import json

from .models import Resa, Comment
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils import translation
from .utils import Button, Range

def resa4date(date,user=None):
    """
    gets reservations for a given date
    @param date the date to query
    @param user the user which is logged: useful to get the timezone
    @return a list of reservations as tuples: (begin, duration, username)
    begin and duration are in minutes
    """
    try:
        tz=pytz.timezone(user.profile.timezone)
    except:
        tz=pytz.utc
    result=[]
    if date:
        m,d,y = date.split("/")
        today=tz.localize(datetime.datetime(int(y), int(m), int(d)))
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
        result.append("<span class='timeslot' title='{h:02d}:{m:02d}{status}'/>{h:02d}:{m:02d}<input name='t{t:d}' type='checkbox' onChange='toggleResa(\"{{user.username}}\",this);'/></span>".format(m=m, h=h, t=t, status=_("... free")))
        t+=minutes
        m+=minutes
        if m >= 60:
            h+=1
            m=0
    return result

def index(request):
    user_language = 'en'
    try:
        user_language = request.user.profile.language
    except:
        pass
    translation.activate(user_language)
    
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    date=request.session.get("date","")
    # contents for the action tab
    actionButtons=[
        Button(name = "LED",
               label =  _("Toggle the LED's light"),
               action = "/srv/action/toggleLED",
               description=_("Lights the LED up or down. It should modify the LDR's resistance.")
        ),
    ]
    actionRanges=[
        Range(
            name="range1",
            action="/srv/action/freqSqr1",
            label=_("Frequency"),
            description=_("Tune the frequency for the buzzer (500 to 10000 Hz). It should have consequences on the frequency and the ammplitude of the microphone's signal."),
            minval="500",
            maxval="10000",
            value="1500",
            step="10",
            )
    ]
    context={
        "timeslots": timeslots(15),
        "date": date,
        "resa": json.dumps(resa4date(date, request.user)),
        "logoutURL": '%s?next=%s' % (settings.LOGOUT_URL, request.path),
        "loginURL": '%s?next=%s' % (settings.LOGIN_URL, request.path),
        "buttons": actionButtons,
        "ranges": actionRanges,
        "comments": Comment.objects.all()
        }
    response = render(request,  'srv/index.html', context)
    response['Cache-Control'] = 'no-cache, no-store'
    return response

def action (request, p):
    """
    service called by action buttons
    @param p given by the urls
    """
    return JsonResponse({_("action call"): p, _("action state"): _("not yet implemented")})

def add_comment(request):
    """
    page featuring a form to add a comment
    """
    if request.method == "POST":
        text=request.POST.get("text","")
        if text.strip():
            comment=Comment(text=text, author=request.user)
            comment.save()
            return redirect('/srv')
    else:
        return render(request, 'srv/comment.html', {})
    
def logout(request):
    """
    implements a logout page for the application "srv"
    """
    contribLogout(request)
    return render(request,"srv/logout.html", {
        "next": request.GET.get("next","/"),
        "msg" : _("Logout"),
    })

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
            msg=_("Welcome {}").format(user.username)
        else:
            msg=_("Sorry, the account {} is disabled").format(user.username)
    else:
        msg=_("Sorry, please try to login again, or check your accreditation")
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
    return JsonResponse({'resa': resa4date(date, request.user), 'date': date, 'name': request.user.username,})

def makeResa(request):
    """
    makes reservations when possible
    @param request provides GET parameters like wantedDate, name,
    password, timeslots
    @return a report after inserting data into the database,
    in JSON string format    
    """
    msg=""
    ok=True
    date=request.GET.get('wantedDate','')
    user=request.user
    try:
        tz=pytz.timezone(user.profile.timezone)
    except:
        tz=pytz.utc
    minutes=[]
    if date:
        request.session["date"]=date
        m,d,y = date.split("/")
        today=tz.localize(datetime.datetime(int(y), int(m), int(d)))
        timeslots=request.GET.get("timeslots")
        minutes=[]
        if (len(timeslots)):
            minutes=[int(ts[1:]) for ts in timeslots.split(",")]
    else:
        ok=False
        msg+=_(" undefined date;")
    name=request.GET.get('name','')
    if not user or not user.is_authenticated():
        ok=False
        msg+=_(" user is not authenticated;")
    if ok:
        # create reservations!
        for beg in minutes:
            t_beg=today+datetime.timedelta(seconds=beg*60)
            t_end=t_beg+datetime.timedelta(seconds=15*60)
            if not Resa.objects.filter(beg=t_beg):
                ## do not overwrite previous reservations !
                r=Resa(user=user, beg=t_beg, end=t_end)
                r.save()
    resa=resa4date(date, request.user)
    return JsonResponse({'ok': ok, 'msg': msg, 'minutes': minutes,
                         "name": user.username, 'resa': resa,})

def toggleResa(request):
    """
    toggles a reservation when possible
    @param request provides GET parameters like wantedDate, name, etc.
    @return a report after inserting data into the database or deleting some,
    in JSON string format    
    """
    msg=""
    ok=True
    date=request.GET.get('wantedDate','')
    user=request.user
    try:
        tz=pytz.timezone(user.profile.timezone)
    except:
        tz=pytz.utc
    minute=request.GET.get("minute","")
    if minute:
        minute=int(minute[1:]) # get rid of leading 't'
    else:
        ok=False
        msg += _(" missing time information;")
    if date:
        request.session["date"]=date
        m,d,y = date.split("/")
        today=tz.localize(datetime.datetime(int(y), int(m), int(d)))
    else:
        ok=False
        msg+=_(" undefined date;")
    name=request.GET.get('name','')
    if not user or not user.is_authenticated():
        ok=False
        msg+=_(" user is not authenticated;")
    checked=request.GET.get("checked","")
    if len(checked)==0:
        ok=False
        msg += _(" error about checked box;")
    else:
        checked=(checked=="true")
    if ok:
        # create or delete reservation!
        t_beg=today+datetime.timedelta(seconds=minute*60)
        t_end=t_beg+datetime.timedelta(seconds=15*60)
        if checked:
            # create the resa
            if not Resa.objects.filter(beg=t_beg):
                ## do not overwrite previous reservations !
                r=Resa(user=user, beg=t_beg, end=t_end)
                r.save()
        else:
            # delete the resa
            Resa.objects.filter(beg=t_beg).delete()
    resa=resa4date(date, request.user)
    return JsonResponse({'ok': ok, 'msg': msg, 'minute': minute,
                         "name": user.username, 'resa': resa,})
