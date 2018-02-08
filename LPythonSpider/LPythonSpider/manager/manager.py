# -*- coding: utf-8 -*-

from flask_script import Manager
from WebServer.WebService import app

manager = Manager(app)

@manager.command
def runserver():
    print 'server is start'

if __name__ == '__main__':
    manager.run()


