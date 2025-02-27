import mysql.connector
from mysql.connector import errorcode
from prettytable import PrettyTable
from datetime import datetime

class Utile:
    @staticmethod
    def checkInput(msg, params = ("str", {})):
        # msg : msg a affiché 
        # params : tuple contenant 2 valeurs : 
        # - le type de retour
        # - les options supplémentaires
        
        # Vérification si l'on attend un entier 
        while True:
            donneTemp = input(msg) # Demande une entrée utilisateur avec le message fourni 
            if(params[0] == "int"):
                try:
                    donnee = int(donneTemp)  # Convertit l'entrée en entier
                    break # Sort de la boucle si la conversion réussit
                except:
                    print("Un nb entier est demandé") 
            
            # Vérification si l'on attend un nombre flottant 
            if(params[0] == "float"):
                try:
                    donnee = float(donneTemp) # Convertit l'entrée en float
                    break
                except:
                    print("Un nb décimal est demandé") # Message d'erreur si la conversion échoue
            
            # Vérification si l'on attend un booléen         
            elif(params[0] == "bool"):

                t = ["1", "O", "Y", "T", "YES", "OUI", "TRUE"] # Liste des valeurs considérées comme True
                if donneTemp.upper() in t:  # Si l'entrée correspond à une valeur True
                    donnee = True
                else:
                    donnee = False # Sinon, c'est False
                break
            
            # Vérification si l'on attend une date 
            elif(params[0] == "date"):
                try:
                    donnee = datetime.strptime(donneTemp, params[1]['format']) # Convertit l'entrée en date selon le format fourni
                    break
                except:
                    print("Format manquant ou incorect") # Message d'erreur si la conversion échoue
            
            # Vérification si l'on attend une chaîne de caractères 
            elif(params[0] == "str"):
                donnee = donneTemp # Stocke directement l'entrée utilisateur
                break
        return donnee # Retourne la valeur convertie après validation 
                
# Méthode statique pour tester la fonction `checkInput`       
    @staticmethod
    def start():
        test = Utile.checkInput("une chaine ?") # Test avec une chaîne de caractères
        print(test)
        testf = Utile.checkInput("un float ?", ("float",)) # Test avec un float
        print(testf)
        testD = Utile.checkInput("une date ?", ("date", {"format":"%Y-%m-%d"})) # Test avec une date au format AAAA-MM-JJ
        print(testD)


class Fonctionalite:
    def __init__(self):
        
        # """Détermination de la config de connexion"""
        self.config = {
            'host' : "localhost",
            'database' : "jeuxvideo",
            'user' : "root",
            'password' : "28469",
            'raise_on_warnings' : True
        }
        # """ Ouvre une connexion"""
        self.connexion = mysql.connector.connect(**self.config) 
    
    
    def connecter(self):
        # """ Ouvre une connexion si elle n'est pas active """
        if not self.connexion.is_connected():
            self.connexion = mysql.connector.connect(**self.config)
    
    def ajouter_jeux(self):
        # """ajout de Jeux""" 
        try: 
            if self.connexion.is_connected():
                self.connexion.start_transaction() 
                add = input("Souhaites-tu ajouter un jeu ? (O/N) : ") #demander à l'utilisateur s'il veut modifier un contact
                if add.upper() == "O":
                    cursor = self.connexion.cursor(prepared=True) # Initialisation d'un curseur pour exécuter des requêtes préparées (sécurisé & optimisé)
                    add_jeu = ("INSERT INTO jeux "
                                "(Jeux_Titre, Jeux_Description, Jeux_Prix, Jeux_DateSortie, Jeux_PaysOrigine, Jeux_Connexion, Jeux_Mode, Genre_Id)"
                                "VALUES (%(Jeux_Titre)s, %(Jeux_Description)s, %(Jeux_Prix)s, %(Jeux_DateSortie)s, %(Jeux_PaysOrigine)s, %(Jeux_Connexion)s, %(Jeux_Mode)s, %(Genre_Id)s)"
                                ) #Ajout des critères d'ajout d'un jeu dans les colonnes prédéfinis 
                    
                    data_jeux = {
                        'Jeux_Titre' : Utile.checkInput("Titre du jeu : "),
                        'Jeux_Description' : Utile.checkInput("Description du jeu : "),
                        'Jeux_Prix' : Utile.checkInput("Le prix du jeu (ex: 99,99) : ", ("float",)),
                        'Jeux_DateSortie' : Utile.checkInput("Date de sortie (ex : 2017-11-11) : ", ("date", {"format":"%Y-%m-%d"}),),
                        'Jeux_PaysOrigine' : Utile.checkInput("Pays d'origine : ").upper(),
                        'Jeux_Connexion' : Utile.checkInput("Jeu online (Oui/Non) : "),
                        'Jeux_Mode' : Utile.checkInput("Mode de jeu (Solo, Multi...) : "),
                        'Genre_Id' : Utile.checkInput("Type du jeu (1. MMO, 2. FPS, 3. RPG, 4. Action, 5. Sport, 6. Plateformer, 7. Course, 8. Puzzle, 9. Educatif) :  )", ("int",))
                    }       
                    cursor.execute(add_jeu, data_jeux)
                    print(cursor.rowcount, "Jeu ajouté")
                    self.connexion.commit() 
                    cursor.close()
                else:    
                    print("Pas de modification souhaitée")
                    
                
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Acces à la base de donnée refusé(User ou mdp incorrect)")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("La base de donnée choisit n'existe pas")
            else:    
                print("Erreur sur la BDD", err)
            self.connexion.rollback()
        #Fermeture du curseur & de la connexion à la fin de la requête   
        finally:
            if self.connexion.is_connected():
                self.connexion.close()
                print("La connexion MYSQL est fermée")
        
          
# Requete 2 : modification d'un ou plusieurs elements d'un jeux        
    def modifier_jeux(self):     
        # """Modifier un jeu par l'ID"""
        try: 
            if self.connexion.is_connected():
                self.connexion.start_transaction() 
                update = input("Souhaites-tu modifier un jeu ? (O/N) : ") #demander à l'utilisateur s'il veut modifier un jeu
                Fonctionalite.afficher_jeux
                if update.upper() == "O":
                    cursor = self.connexion.cursor(prepared=True) # Initialisation d'un curseur pour exécuter des requêtes préparées (sécurisé & optimisé)
                    update_jeux = ("UPDATE jeux SET Jeux_Prix = %(Jeux_Prix)s WHERE Jeux_Id = %(Jeux_Id)s ")
                    
                    id = int(input("Quel est l'ID du jeux que tu souhaites modifier : "))
                    cursor.execute("SELECT * FROM jeux WHERE Jeux_Id = %s", (id,)) #Execute la requete SQL
                    jeu_existant = cursor.fetchone()

                    if jeu_existant:
                        print(f"Le jeu {jeu_existant[1]} existe et peut être modifié.")
                        
                        data_jeux = {
                        'Jeux_Id' : id,
                        'Jeux_Titre' : Utile.checkInput("Titre du jeu : "),
                        'Jeux_Description' : Utile.checkInput("Description du jeu : "),
                        'Jeux_Prix' : Utile.checkInput("Le prix du jeu (ex: 99,99) : ", ("float",)),
                        'Jeux_DateSortie' : Utile.checkInput("Date de sortie (ex : 2017-11-11) : ", ("date", {"format":"%Y-%m-%d"}),),
                        'Jeux_PaysOrigine' : Utile.checkInput("Pays d'origine : ").upper(),
                        'Jeux_Connexion' : Utile.checkInput("Jeu online (Oui/Non) : "),
                        'Jeux_Mode' : Utile.checkInput("Mode de jeu (Solo, Multi...) : "),
                        'Genre_Id' : Utile.checkInput("Type du jeu (1. MMO, 2. FPS, 3. RPG, 4. Action, 5. Sport, 6. Plateformer, 7. Course, 8. Puzzle, 9. Educatif) :  )", ("int",))
                    }  
                        
                        cursor.execute(update_jeux, data_jeux)
                        print(cursor.rowcount, "Jeu modifié") # affiche le nombre de ligne modifiée (rowcount)
                        self.connexion.commit()
                        cursor.close()    
                 
                    else:
                        print("Aucun jeu trouvé avec cet ID.")
                            
                    
                else: 
                    print("Aucune modification souhaitée")        
                    
                
            
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Acces à la base de donnée refusé(User ou mdp incorrect)")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("La base de donnée choisit n'existe pas")
            else:    
                print("Erreur sur la BDD", err)
            self.connexion.rollback()
        #Fermeture du curseur & de la connexion à la fin de la requête   
        finally:
            if self.connexion.is_connected():
                
                self.connexion.close()
                print("La connexion MYSQL est fermée")


    # Supprimer un element 
    def supprimer_jeux(self):
        # """Supprimer un jeu par l'ID"""
        try: 
            if self.connexion.is_connected(): # Si la connexion est effectuée
                self.connexion.start_transaction() #lancement de la transaction
                self.afficher_jeux
                delete = input("Souhaites-tu supprimer un jeu ? (O/N) : ") #Demander à l'utilisateur s'il veut modifier un jeu
                if delete.upper() == "O":
                    cursor = self.connexion.cursor(prepared=True) # Initialisation d'un curseur pour exécuter des requêtes préparées (sécurisé & optimisé)
                    delete_jeux = ("DELETE FROM jeux WHERE Jeux_Id = %(Jeux_Id)s ") #definition de la requete SQL avec un element de la colonne Jeux_Id
                                
                    id = int(input("Quel est l'ID du jeux que tu souhaites supprimer : "))
                    data_jeux = {'Jeux_Id' : id,}    
                
                    cursor.execute(delete_jeux, data_jeux) #Execution des deux requetes 
                    print(cursor.rowcount, "Le jeu a été supprimé") #Utilisation de .rowcount pour qu'il compte le nombre de ligne modifié
                    self.connexion.commit() #Execution des requetes de la transaction
                    cursor.close() #fermeture du cursor 
                
                else:  
                    print("Pas de modification souhaitée")
                     
                
                
                
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Acces à la base de donnée refusé(User ou mdp incorrect)")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("La base de donnée choisit n'existe pas")
            else:    
                print("Erreur sur la BDD", err)
            self.connexion.rollback()
        #Fermeture du curseur & de la connexion à la fin de la requête   
        finally:
            if self.connexion.is_connected():
                
                self.connexion.close()
                print("La connexion MYSQL est fermée")


    def afficher_jeux(self):           
    #Afficher la liste des jeux
        try: 
            if self.connexion.is_connected():
                self.connexion.start_transaction() 
                
                cursor = self.connexion.cursor(prepared=True)
                select_jeux = ("select * FROM jeux")
                             
                cursor.execute(select_jeux)
                resultatcursor = cursor.fetchall()
            
                # Vérifier si la table contient des données
                if resultatcursor:
                    # Créer un objet PrettyTable
                    table = PrettyTable()
                    
                    # Ajouter des colonnes
                    table.field_names = ["Id", "Titre", "Prix", "Date de sortie", "Pays d'origine", "Genre"]
                    
                    # Remplir le tableau
                    for (Jeux_Id, Jeux_Titre,Jeux_Description, Jeux_Prix, Jeux_DateSortie, Jeux_PaysOrigine, Jeux_Connexion, Jeux_Mode, Genre_Id) in resultatcursor:
                        table.add_row([Jeux_Id, Jeux_Titre, f"{Jeux_Prix:.2f}€", Jeux_DateSortie.strftime("%d/%m/%Y"), Jeux_PaysOrigine, Genre_Id])
                    
                    # aligner la colonne Titre à gauche    
                    table.align["Titre"] = "l"
                    table.align["Genre"] = "l"

                    # Afficher le tableau
                    print(table)
                else:
                    print("Aucun jeu trouvé dans la base de données.")
            
                self.connexion.commit()
                
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Acces à la base de donnée refusé(User ou mdp incorrect)")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("La base de donnée choisit n'existe pas")
            else:    
                print("Erreur sur la BDD", err)
            self.connexion.rollback()
        #Fermeture du curseur & de la connexion à la fin de la requête   
        finally:
            if self.connexion.is_connected():
                cursor.close()
                self.connexion.close()
                print("La connexion MYSQL est fermée")
                
                
                
 # def verif(self, msg, type):
    #     while True : 
    #         try:
    #             if type == "int":
    #                 donnee = int(input(msg))
    #                 if donnee.isdigit():
    #                     print(f"La saisie est valide", msg)
    #                     break
    #                 else:
    #                     print("Saisie incorrect. Veuillez réessayer")
    #                 break
    #             if type == "float":
    #                 donnee = float(input(msg))
    #                 if donnee.isdigit():
    #                     print(f"La saisie est valide", msg)
    #                     break
    #                 else:
    #                     print("Saisie incorrect. Veuillez réessayer")
                    
    #             if type == "str":
    #                 donnee = input(msg)
    #                 if donnee.is():
    #                     print(f"La saisie est valide", msg)
    #                     break
    #                 else:
    #                     print("Saisie incorrect. Veuillez réessayer")
    #                 break
    #             if type == "bool":
    #                 donnee = bool(input(msg))
    #                 if donnee.is():
    #                     print(f"La saisie est valide", msg)
    #                     break
    #                 else:
    #                     print("Saisie incorrect. Veuillez réessayer")
    #             if type == "date":
    #                 donnee = datetime.strptime(input(msg), "%Y-%m-%d")
    #                 break
                    
    #         except ValueError:
    #             print(f"Erreur : veuillez entrer une valeur valide pour le type {type}.")
    #     return donnee