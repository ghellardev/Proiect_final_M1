from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, redirect, url_for
import datetime

app = Flask(__name__)


@app.route('/')
def home() -> str:
    return render_template('home.html')


client = MongoClient('mongodb://localhost:27017/')
db = client['Magazin']  # replace with your database name
collection = db['Produse']  # replace with your collection name


@app.route('/chart', methods=['GET', 'POST'])
def get_chart() -> str:
    return render_template('chart.html')


@app.route('/get_chart_data')
def get_chart_data():
    pret = []
    stoc = []
    nume = []
    for i in collection.find({}, {"_id": 0}):
        nume.append(i["Nume"])
        pret.append(i["Pret"])
        stoc.append(i["Stoc"])
    print(type(jsonify(Pret=pret, Stoc=stoc, Nume=nume)))
    return jsonify(Pret=pret, Stoc=stoc, Nume=nume)


@app.route('/produse', methods=['GET'])
def get_products() -> str:
    products = lista_products()
    header_list = lista_headers()
    print(type(render_template('produse.html', products=products, header_list=header_list, getattr=getattr)))
    return render_template('produse.html', products=products, header_list=header_list, getattr=getattr)


@app.route('/poduse_cat', methods=['GET', 'POST'])
def produse_cat() -> str:
    return render_template('choice.html', categorii=lista_categorii())


def lista_categorii() -> list[str]:
    lista_categ = []
    for i in collection.find():
        if i["Categorie"] not in lista_categ:
            lista_categ.append(i["Categorie"])
    return lista_categ


def lista_caracteristici() -> list[str]:
    lista_car = []
    for i in collection.find():
        for j in i.keys():
            if j in ["_id", "Nume", "Pret", "Stoc"]:
                continue
            else:
                if j not in lista_car:
                    lista_car.append(j)
    return lista_car


def lista_nume() -> list[str]:
    lista_names = []
    for i in collection.find():
        if i["Nume"] not in lista_names:
            lista_names.append(i["Nume"])
    return lista_names


def lista_products(collection_received=collection.find({}, {"_id": 0}).sort('Nume')) -> list[str]:
    products = []
    for i in collection_received:
        days = (datetime.datetime.now() - i["Last Updated"]).days
        if days > 365:
            i["Last Updated"] = f"{round(days / 365, 1)} Years Ago"
        elif days == 0:
            i["Last Updated"] = "Today"
        else:
            i["Last Updated"] = f"{round(days, 0)} Days Ago"
        products.append(i)
    return products


def lista_headers(collection_received=collection.find({}, {"_id": 0})) -> list[str]:
    header_list = []
    for i in collection_received:
        for j in i.keys():
            if j not in header_list:
                header_list.append(j)
    return header_list


@app.route('/addProdus', methods=['GET', 'POST'])
def addProdus() -> str:
    return render_template('add_produs.html', categorii=lista_categorii())


@app.route('/add_produs', methods=['POST'])
def add_produs():
    # Process the form data and insert the new product into the database
    if request.method == "POST":
        categorie = request.form.get('categorie')
        nume = request.form.get('nume')
        pret = request.form.get('pret')
        stoc = request.form.get('stoc')
        tip = request.form.get('tip')
        produs_nou = {
            'Nume': nume,
            'Pret': float(pret),
            'Stoc': int(stoc),
            'Categorie': categorie,
            'Tip': tip,
            'Last Updated': datetime.datetime.now()
        }
        collection.insert_one(produs_nou)

    # Redirect the user back to the home page
    return redirect(url_for('home'))


@app.route('/produse/add_car', methods=['GET', 'POST'])
def addCar() -> str:
    return render_template('add_car.html', categorii=lista_nume())


@app.route('/produse/add_car/add', methods=['POST'])
def add_car():
    if request.method == "POST":
        car_val = request.form.get('car_val')
        car_name = request.form.get('car_name')
        nume = request.form.get('nume')
        dict_actual = {}
        if car_val.isnumeric():
            dict_actual[car_name] = int(car_val)
        else:
            dict_actual[car_name] = car_val
        collection.update_one({'Nume': nume}, {"$set": dict_actual})
    return redirect(url_for('get_products'))


@app.route('/produse/rem_car', methods=['GET', 'POST'])
def remCar() -> str:
    return render_template('rem_car.html', names=lista_nume(), carname=lista_caracteristici())


@app.route('/produse/rem_car/remove', methods=['POST'])
def rem_car():
    if request.method == "POST":
        car_name = request.form.get('car_name')
        nume = request.form.get('nume')
        collection.update_one({'Nume': nume}, {"$unset": {car_name: ""}})
    return redirect(url_for('get_products'))


@app.route('/produse_cat/view', methods=['GET', 'POST'])
def view() -> str:
    categorie = request.args.get('categorie')
    products = lista_products(collection.find({"Categorie": categorie}, {"_id": 0}).sort('Nume'))
    header_list = lista_headers(collection.find({"Categorie": categorie}, {"_id": 0}))
    return render_template('produse.html', products=products, header_list=header_list, getattr=getattr)


if __name__ == '__main__':
    app.run(debug=True)
