import pymongo
import re

# connect to the MongoDB server
client = pymongo.MongoClient('mongodb://localhost:27017/')
# access the database
DB = client['Magazin']
# access the collections
Haine_DB = DB['Haine']
Accesorii_DB = DB['Accesorii']
Incaltaminte_DB = DB['Incaltaminte']


class Magazin:
    @classmethod
    def alegere_categorie(cls):
        match input("\n1. Haine"
                    "\n2. Accesorii"
                    "\n3. Incaltaminte"
                    "\n  Alegeti categorie: "):
            case '1':
                return Haine_DB
            case '2':
                return Accesorii_DB
            case '3':
                return Incaltaminte_DB
            case _:
                return Magazin.alegere_categorie()

    @classmethod
    def float_inp(cls):
        try:
            return round(float(input()))
        except ValueError:
            print("Introduceti un numar:")
            return Magazin.float_inp()

    @classmethod
    def int_inp(cls):
        try:
            return int(input())
        except ValueError:
            print("Introduceti un numar:")
            return Magazin.int_inp()

    @classmethod
    def find_all(cls):
        list_db = [Haine_DB, Accesorii_DB, Incaltaminte_DB]
        print("=============================================")
        for j in list_db:
            for i in j.find({}, {"_id": 0}):
                for attr, value in i.items():
                    print(f"{attr}: {value}")
                print(f"=============================================")
        input("Press return to continue...")

    # add produs
    @classmethod
    def add_produs_nou(cls):
        nume = input("Introduceti numele: ")
        print("Introduceti pretul: ")
        pret = Magazin.float_inp()
        print("Introduceti stocul:")
        stoc = Magazin.float_inp()
        match input("Introduceti tipul M/F/U").upper():
            case "M":
                tip = "Barbati"
            case "F":
                tip = "Femei"
            case "U":
                tip = "Unisex"
            case _:
                print("Valoare nerecunoascuta, produs de tip unisex din oficiu")
                tip = "Unisex"
        produs_nou = {
            'Nume': nume,
            'Pret': pret,
            'Stoc': stoc,
            'Tip': tip
        }
        for i in Produs.caracteristici_produs():
            if input(f"Doriti sa adaugati {i} la caracteristicile produsului"
                     "\nY/N: ").upper() == 'Y':
                produs_nou[i] = input(f"Introduceti caracteristicile pentru {i}")
        Magazin.alegere_categorie().insert_one(produs_nou)


class Produs(Magazin):
    def __init__(self, Nume, **kwargs):

        for i in kwargs:
            setattr(self, i, kwargs[i])
        self.Nume = Nume

    # print obj
    def print_attributes(self):
        item = Magazin.alegere_categorie()
        cursor = item.find({'Nume': self.Nume}, {'_id': 0})
        if item.count_documents({'Nume': self.Nume}) <= 1:
            for i in cursor:
                for attr, value in i.items():
                    print(f"{attr}: {value}")
        input("Press return to continue...")

    @classmethod  # pt adaugare caracteristici
    def caracteristici_produs(cls):
        sir_de_procesat = input("Introduceti caracteristicile produsului, separate prin virgula:")
        lista_de_procesat = sir_de_procesat.split(",")
        lista_procesata = [re.sub(r'[^a-zA-Z]', '', string) for string in lista_de_procesat]
        return lista_procesata

    # del produs
    def del_produs(self):
        item = Magazin.alegere_categorie()
        cursor = item.find({'Nume': self.Nume}, {'_id': 0})
        if item.count_documents({'Nume': self.Nume}) <= 1:
            for i in cursor:
                for attr, value in i.items():
                    print(f"{attr}: {value}")
        if input("Doriti sa eliminati produsul ?"
                 "\nAceasta actiune este ireversibila"
                 "\nY/N: ").upper() == "Y":

            item.delete_one({'Nume': self.Nume})
        else:
            print("Schimbare neefectuata")

    # update caracteristici
    def update_caracteristici(self):
        nume = self.__dict__["Nume"]
        item = Magazin.alegere_categorie()
        cursor = item.find({'Nume': self.Nume}, {'_id': 0})
        if item.count_documents({'Nume': nume}) <= 1:
            for i in cursor:
                dict_actual = {}
                for attr, value in i.items():
                    print(f"{attr}: {value}")
                if input(f"Doriti sa actualizati caracteristicile produsului {nume}"
                         "\nY/N: ").upper() == "Y":
                    match input("1. Adaugare caracteristici\n"
                                "2. Stergere caracteristici\n"
                                "   Alegerea dvs: "):
                        case '1':
                            for j in Produs.caracteristici_produs():
                                if input(f"Doriti sa adaugati {j} la caracteristicile produsului"
                                         "\nY/N: ").upper() == 'Y':
                                    var = input(f"Introduceti caracteristicile pentru {j}")
                                    if var.isnumeric():
                                        dict_actual[j] = int(var)
                                    else:
                                        dict_actual[j] = var
                            item.update_one({'Nume': nume}, {"$set": dict_actual})
                        case '2':
                            for j in Produs.caracteristici_produs():
                                if input(f"Doriti sa stergeti {j} de la caracteristicile produsului"
                                         "\nY/N: ").upper() == 'Y':
                                    dict_actual[j] = ""
                            item.update_one({'Nume': nume}, {"$unset": dict_actual})
                        case _:
                            print("Optiune Nerecunoscuta")
                else:
                    print("Schimbare neefectuata")

    # update pret
    def update_pret(self):
        nume = self.__dict__["Nume"]
        item = Magazin.alegere_categorie()
        pret_actual = None
        cursor = item.find({'Nume': nume}, {'_id': 0, 'Pret': 1})
        if item.count_documents({'Nume': nume}) <= 1:
            for i in cursor:
                pret_actual = i["Pret"]
            print(f"Pretul produsului {nume} este: {pret_actual}")
            if input("Doriti sa schimbati pretul ?"
                     "Y/N: ").upper() == "Y":
                print("Introduceti noul pret: ")
                pret_actual = Magazin.float_inp()
                item.update_one({'Nume': nume}, {"$set": {"Pret": pret_actual}})
                print(f"Pretul produsului {nume} este acum: {pret_actual}")
            else:
                print("Schimbare neefectuata")

    # update stoc
    def update_stoc(self):
        nume = self.__dict__["Nume"]
        item = Magazin.alegere_categorie()
        stoc_actual = None
        cursor = item.find({'Nume': nume}, {'_id': 0, 'Stoc': 1})
        if item.count_documents({'Nume': nume}) <= 1:
            for i in cursor:
                stoc_actual = i["Stoc"]
            print(f"Stocul produsului {nume} este: {stoc_actual}")
            if input("Doriti sa schimbati stocul ?"
                     "Y/N: ").upper() == "Y":
                print("Introduceti noul stoc: ")
                stoc_actual = Magazin.int_inp()
                item.update_one({'Nume': nume}, {"$set": {"Stoc": stoc_actual}})
                print(f"Stocul produsului {nume} este acum: {stoc_actual}")
            else:
                print("Schimbare neefectuata")
