#!/usr/bin/python3

import cherrypy
from jinja2 import Environment, FileSystemLoader
import os.path
from utils import Button

env = Environment(loader=FileSystemLoader('templates'))

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

def javascriptInit(key, val):
    """
    outputs javascript code to assign a variable
    @return an HTML SCRIPT element, as a string
    """
    return """
<script type="text/javascript">
    {k}="{v}";
</script>
""".format(k=key, v=val)
class Root:
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        # contents for the video tab
        video="""\
    <a href="https://hello.firefox.com/lXFmP8Gfxj0" target="_new">Open "hello" tab.</a>
    <p>A new tab will be created, you can drag it to make a new window and adapt its size</p>
"""
        # contents for the action tab
        actionButtons=[
            Button(name = "Un",   html =  "2+2", action = "action1"),
            Button(name = "Deux", html =  "3+3", action = "action2"),
            Button(name = "Tris", html =  "4+4", action = "action3"),
        ]
        sessionData=str(cherrypy.session.items())
        return tmpl.render(
            video=video,
            buttons=actionButtons,
            sessionData=sessionData, # for debug purpose
            timeslots=timeslots(minutes=15),
            resa=javascriptInit("document.resa",""),
            name=cherrypy.session.get("name",""),
            email=cherrypy.session.get("email",""),
            password=cherrypy.session.get("password",""),
            date=cherrypy.session.get("date",""),
        )
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def reservationsByDate(self, **kw):
        """
        function called back when the date is being changed
        this will return data about known reservations for
        the given date.
        @param **kw a dictionary with the key "wantedDate"
        @param a dictionary about reservation made for the wanted date
        """
        cherrypy.session["date"]=kw.get("wantedDate","")
        return kw # to be changed!
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def makeResa(self, **kw):
        """
        function called back when reservations are being submitted
        @param **k a dictionary with keys name, email, password, wantedDate
        and some more data about checked boxes to ask for reservations
        """
        cherrypy.session["name"]=kw.get("name","")
        cherrypy.session["email"]=kw.get("email","")
        cherrypy.session["password"]=kw.get("password","")
        cherrypy.session["date"]=kw.get("wantedDate","")
        return kw # to be changed!
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def action1(self):
        return "ici on fait l'opération 2+2=4"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def action2(self):
        return "ici on fait l'opération 3+3=6"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def action3(self):
        return "ici on fait l'opération 4+4=8"

if __name__ == '__main__':
    wdir = os.path.dirname(os.path.abspath(__file__))
    # Set up site-wide config first so we get a log if errors occur.
    cherrypy.config.update({'environment': 'production',
                            'log.error_file': 'site.log',
                            'log.screen': True})

    conf = {
        'global': {
            'tools.sessions.on': True,
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(wdir, 'static'),
            'tools.staticdir.content_types': {'html': 'text/html',}
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(wdir, 'css'),
            'tools.staticdir.content_types': {'css': 'text/css',}
        },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(wdir, 'js'),
            'tools.staticdir.content_types': {'js': 'text/javascript',}
        },
    }
    cherrypy.quickstart(Root(), '/', config=conf)
   
