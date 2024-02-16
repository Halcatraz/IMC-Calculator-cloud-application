import firebase_admin
from firebase_admin import db,credentials

# authentification à firebase grâce à la clé privée
cred = credentials.Certificate("cloud-application-calcul-imc-firebase-adminsdk-puimg-4fd9d30848.json")
# connection avec la database
firebase_admin.initialize_app(cred, {"databaseURL": "https://cloud-application-calcul-imc-default-rtdb.firebaseio.com/"})

# fonction pour stocker les data dans la base de données de Firebase
def pushData(name, weight, size, IMC):
    # peut etre faire un seul push avec un dictionnaire
    # créer le node name et ajoute au node le nom, le poids, la taille et l'IMC de la personne
    db.reference(name).update({"name":name})
    db.reference(name).update({"weight":weight})
    db.reference(name).update({"size":size})
    db.reference(name).update({"IMC":IMC})

# fonction pour récupérer les data de la database
def getData(name):
    # vérification que le nom cherché existe dans la base de donnée
    # sinon renvoie un message d'erreur
    ref = db.reference("/")
    checkData = ref.get()
    if name is not None and name in checkData :
        # la méthode get() renvoie un dictionnaire contenant toutes les données sur l'individu
        data = db.reference(name).get()
        # verifier que le IMC existe dans la base de données
        # sinon renvoyer message d'erreur
        # normalement pas possible donc pas de soucis
        IMC = data.get("IMC")
        if IMC is not None:
            print("L'IMC de " + name + " est de", IMC)
        else:
            print("Un problème s'est produit, il n'y a pas d'IMC associé au nom fournit")
    else:
        print("Erreur le nom fournit n'est pas dans la base de donnée. Réessayer avec un autre nom")

# fonction pour calculer l'IMC
def calculIMC(weight, size):
    return weight / (size ** 2)

# fonction main
def main():
    print("Calcul de l'IMC avec stockage des informations dans une real time database sur Firebase")
    print("----------------------------------------------------------------------------------------")

    while True:
        print("\nMenu")
        print("1. Calculer un IMC")
        print("2. Trouver un IMC")
        print("3. Quitter")

        select = input("\nQue voulez-vous faire ? ")

        if select == "1":
            name = input("Entrer le nom : ")
            weight = int(input("Entrer le poids (en kg) : "))
            size = float(input("Entrer le taille (en m) : "))
            IMC = calculIMC(weight=weight, size=size)
            print("L'IMC de " + name + " est de", IMC)
            pushData(name=name, weight=weight, size=size, IMC=IMC)

        elif select == "2":
            name = input("Entrer le nom : ")
            getData(name=name)

        else:
            print("Quitter")
            break
