#!/usr/bin/python3

import cherrypy
from jinja2 import Environment, FileSystemLoader
import os.path
from utils import Button

env = Environment(loader=FileSystemLoader('templates'))

class Root:
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render(
            videoIframe="""\
    <a href="https://hello.firefox.com/lXFmP8Gfxj0" target="_new">Open "hello" tab.</a>
            <p>A new tab will be created, you can drag it to make a new window and adapt its size</p>\n""",
            buttons=[
                Button(name = "Un",html =  "2+2", action = "action1"),
                Button(name = "Deux",html =  "3+3", action = "action2"),
                Button(name = "Tris",html =  "4+4", action = "action3"),
            ],
        )
    
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
   
