from jeux import Fonctionalite
from plateforme import Options
from prettytable import PrettyTable

class Programme:
    def __init__(self):
        pass
    
    def menu(self): #definir la fonction menu
    # Création du cadre pour le titre avec PrettyTable
        table = PrettyTable()
        table.field_names = ["/" * 40]  # Bordure supérieure
        table.add_row(["MENU JEUXVIDEO GAME"])
        table.add_row(["/" * 40])  # Bordure inférieure
    
    # pour l'encadrement du menu sans import
    #     @staticmethod
    # def titre(str):
    #     longueur = len(str)+2
    #     retour = "+"
    #     retour += "-"*longueur
    #     retour += "+\n"
    #     retour += "|"
    #     retour += " "+str+" "
    #     retour += "|\n"
    #     retour += "+"
    #     retour += "-"*longueur
    #     retour += "+"
    #     return retour

    # print(Menu.titre("Bienvenue dans mon test !"))

        print(table)  # Afficher le cadre

        while True:
            try:
                choix = int(input("Quel choix souhaitez-vous faire ? \n1. Ajouter un jeu \n2. Modifier un jeu \n3. Supprimer un jeu \n4. Afficher la liste des jeux \n5. Afficher la plateformes des jeux \n6. Associer un jeu à une plateforme \n7. Supprimer une association d'un jeu à une plateforme : "))
                if choix <= 0 or choix > 7:
                    print("Le choix est incorrect. Veuillez saisir une des 5 options proposées") 
                f = Fonctionalite()   
                o = Options()          
                if choix == 1:
                    f.ajouter_jeux()
                    print("")   
                if choix == 2:
                    f.modifier_jeux()                  
                if choix == 3:
                    f.supprimer_jeux()
                if choix == 4:
                    f.afficher_jeux()
                if choix == 5: 
                    o.afficher_plateforme()
                if choix == 6:
                    o.associer_plateforme()
                if choix == 7:
                    o.delete_asso_plateforme()
                    
            except ValueError:
                print("Saisie invalide. Veuillez reessayer")    
                
                
programme = Programme()
programme.menu()