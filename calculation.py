from flask import Flask, render_template, request, redirect
from cal import make_table, get_result, get_num, reset_table
app = Flask("calculation")


@app.route("/")
def home():
    make_table()
    return render_template("index.html", result_num="")


@app.route("/add", methods=['POST'])
def add_number():
    addednum = request.form['addednum']
    get_num(addednum,'add')
    return redirect("/")

@app.route("/minus", methods=['POST'])
def minus_number():
    addednum = request.form['addednum']
    get_num(addednum,'minus')
    return redirect("/")

@app.route("/multi", methods=['POST'])
def multi_number():
    addednum = request.form['addednum']
    get_num(addednum,'multi')
    return redirect("/")

@app.route("/divide", methods=['POST'])
def divide_number():
    addednum = request.form['addednum']
    get_num(addednum,'divide')
    return redirect("/")

@app.route("/result", methods=['POST'])
def result():
    addednum = request.form['addednum']
    result_num = get_result(addednum)
    return render_template("index.html", result_num=result_num)

@app.route("/reset")
def reset():
    reset_table()
    return render_template("index.html", result_num="")

app.run()
