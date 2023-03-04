from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, redirect, url_for
import datetime

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


client = MongoClient('mongodb://localhost:27017/')
db = client['Magazin']  # replace with your database name
collection = db['Produse']  # replace with your collection name


@app.route('/chart', methods=['GET', 'POST'])
def get_chart():
    return render_template('chart.html')


@app.route('/get_chart_data')
def get_chart_data():
    Pret = []
    Stoc = []
    Nume = []
    for i in collection.find({}, {"_id": 0}):
        Nume.append(i["Nume"])
        Pret.append(i["Pret"])
        Stoc.append(i["Stoc"])

    return jsonify(Pret=Pret, Stoc=Stoc, Nume=Nume)


# @app.route('/updateChart', methods=['GET', 'POST'])
# def get_update_chart():
#     new_data_set_1 = [50, 10, 60, 20, 60]
#     new_data_set_2 = [110, 60, 10, 70, 40]
#     return render_template('chart.html', data_set_1=new_data_set_1, data_set_2=new_data_set_2)


@app.route('/employees', methods=['GET'])
def get_products():
    products = []
    header_list = []
    for i in collection.find({}, {"_id": 0}):
        for j in i.keys():
            if j not in header_list:
                header_list.append(j)
    for i in collection.find().sort('Nume'):
        days = (datetime.datetime.now() - i["Last Updated"]).days
        if days > 365:
            i["Last Updated"] = f"{round(days / 365, 1)} Years Ago"
        elif days == 0:
            i["Last Updated"] = "Today"
        else:
            i["Last Updated"] = f"{round(days, 0)} Days Ago"
        products.append(i)
    return render_template('employees.html', products=products, header_list=header_list, getattr=getattr)


@app.route('/employees_dep', methods=['GET', 'POST'])
def get_employees_dep():
    # if request.method == "POST":
    #     dep = request.form.get("dep")
    #     return view(dep)
    return render_template('choice.html',categorii=lista_categorii())

def lista_categorii():
    lista_categorii = []
    for i in collection.find():
        if i["Categorie"] not in lista_categorii:
            lista_categorii.append(i["Categorie"])
    return lista_categorii

@app.route('/employees_dep/view', methods=['GET', 'POST'])
def view():
    dep = request.args.get('categorie')
    products = []
    header_list = []
    for i in collection.find({"Categorie": dep}, {"_id": 0}):
        for j in i.keys():
            if j not in header_list:
                header_list.append(j)
    for i in collection.find({"Categorie": dep}).sort('Nume'):
        days = (datetime.datetime.now() - i["Last Updated"]).days
        if days > 365:
            i["Last Updated"] = f"{round(days / 365, 1)} Years Ago"
        elif days == 0:
            i["Last Updated"] = "Today"
        else:
            i["Last Updated"] = f"{round(days, 0)} Days Ago"
        products.append(i)
    return render_template('employees.html', products=products, header_list=header_list, getattr=getattr)


if __name__ == '__main__':
    app.run(debug=True)
