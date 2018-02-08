#!/usr/bin/env python
import jinja2
import os
from flask import Flask,render_template
from helper.RedisHelper import redisManager

app = Flask(__name__)

@app.route('/')
def helloWork():
    redis_server = redisManager.doGetServer()
    keylist = redis_server.keys('*')
    return render_template('Persion.html')

if __name__ == '__main__':

    app.run(debug=True)
