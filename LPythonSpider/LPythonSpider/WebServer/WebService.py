# -*- coding: utf-8 -*-


from flask import Flask, render_template

app = Flask(__name__, template_folder='templates', static_folder='../static')


@app.route('/')
def index():
    return render_template('spider_run_status.html')


if __name__ == '__main__':
    app.template_folder = "templates"
    app.run(debug=True, port=6088)
