import sqlite3
import json
import glob
from flask import Flask, request, Response, redirect, url_for
from flask import render_template
import csv
import sys
import os
import pandas as pd
import tablib
import os
from IPython.display import HTML
from pretty_html_table import build_table
import numpy as np
from os import path

app = Flask(__name__)
script_dir = path.dirname(path.abspath(__file__))

#Global Variable to read the CSV
global_d1 = pd.read_csv('netflix_titles.csv')

#Displays the Options at the start
@app.route('/')
def starting_route():
    return render_template('login.html');

#Views the Data based on the columns people want to see
@app.route('/view_data', methods=['GET', 'POST'])
def index():
    global global_d1
    if request.method == 'POST':
        x = (request.form.getlist('mycheckbox'))
        if (x[0] == "all"):
            new = global_d1
        else :
            new = global_d1.filter(x, axis=1)
        return new.to_html()
    return render_template('entry.html')


#Downloads the CSV as the file "netflix_data.csv"
@app.route('/download_as_csv', methods=['GET', 'POST'])
def getCSV():
    csv = global_d1.to_csv(index=False)
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=netflix_data.csv"})

#Ask the user which column they want to edit
@app.route('/column_selection', methods = ['GET', 'POST'])
def column_checker():
    return render_template('index.html')


list_items = []
global_column_name = ""
global_row = 0
@app.route('/row_selection', methods = ['GET', 'POST'])
def row_checker():
    global global_column_name
    global global_row
    global global_d1
    z = (request.form.getlist('mycheckbox'))
    list_items.append(z)
    if (request.method == 'POST'):
        num = request.form.get("int_num")
        list_items.append(num)

    print(list_items)
    if (len(list_items) % 4 == 0):
        if (len(list_items) == 4):
            index = 0;
        else:
            index = len(list_items) / 2
        global_row = (int(list_items[len(list_items) - 1]))
        global_column_name = list_items[index][0]
        dataFrame_one = global_d1[global_column_name]
        list_items.clear()
        print(dataFrame_one[global_row])
        return redirect(url_for('editor'))
    return render_template('page.html')

@app.route('/editing_page', methods = ['GET', 'POST'])
def editor(columns = global_column_name, row = global_row):
    global global_d1
    print(list_items)
    if (request.method == 'POST'):
        num = request.form.get("int_num")
        global_d1[global_column_name][global_row] = num
        return redirect(url_for('index'))
    return render_template('editing.html')

if __name__ == "__main__":
    app.run(debug=True)
