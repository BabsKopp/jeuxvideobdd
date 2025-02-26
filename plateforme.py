import mysql.connector
from mysql.connector import errorcode
from prettytable import PrettyTable
from datetime import datetime


class Options: 
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
        
        
        
    def afficher_plateforme(self):           
    #Afficher la liste des jeux
        try: 
            if self.connexion.is_connected():
                
                
                cursor = self.connexion.cursor(prepared=True)
                query = ("SELECT Jeux_Id, Jeux_Titre, Plateforme_Nom FROM jeux JOIN jeuxplateforme USING (Jeux_Id) JOIN plateforme USING (Plateforme_Id)"
                        )
                             
                cursor.execute(query)
                resultatcursor = cursor.fetchall()
            
                # Vérifier si la table contient des données
                if resultatcursor:
                    # Créer un objet PrettyTable
                    table = PrettyTable()
                    
                    # Ajouter des colonnes
                    table.field_names = ["Id", "Titre", "Plateforme"]
                    
                    # Remplir le tableau
                    for (Jeux_Id, Jeux_Titre, Plateforme_nom) in resultatcursor:
                        table.add_row([Jeux_Id, Jeux_Titre, Plateforme_nom ])
                    
                    # aligner la colonne Titre à gauche    
                    table.align["Titre"] = "l"
                    table.align["Genre"] = "l"

                    # Afficher le tableau
                    print(table)
                    
                    
                    cursor.close()
                    
                else:
                    print("Aucun jeu trouvé dans la base de données.")
            
                
                
                
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
                print("La connexion MYSQL est fermée")

    def associer_plateforme(self):
        try: 
            if self.connexion.is_connected():
                self.connexion.start_transaction() 
                add = input("Souhaites-tu associer un jeu à une plateforme? (O/N) : ") 
                
                if add.upper() == "O": #Si oui, on affiche la liste des jeux 
                    self.afficher_plateforme()
                    cursor = self.connexion.cursor(prepared=True)
                    id_jeu = int(input("Quel est l'ID du jeux que tu souhaites associer : ")) #demande à l'utilisateur l'id du jeu à associer
                    # Vérification de l'existance du jeu
                    cursor.execute("SELECT * FROM jeux WHERE Jeux_Id = %s", (id_jeu,))
                    jeu_existe = cursor.fetchone()
                    if not jeu_existe:
                        print("Ce jeu n'existe pas. Veuillez saisir un ID valide.")
                    else:
                        id_plat = int(input("Quel est l'ID de la plateforme que tu souhaites associer au jeu choisi (1. PC, 2. PS4, 3. ONE, 4. SWITCH): ")) #demande à l'utilisateur l'id de la plateforme à associer au jeu choisi
                        # Vérification de l'existance de la plateforme
                        cursor.execute("SELECT * FROM plateforme WHERE Plateforme_Id = %s", (id_plat,))
                        plateforme_existe = cursor.fetchone()
                        if not plateforme_existe:
                            print("Cette plateforme n'existe pas. Veuillez saisir un ID valide.")
                        else:
                            # Vérifie si l'association existe déjà
                            cursor.execute("SELECT * FROM jeuxplateforme WHERE Jeux_Id = %s AND Plateforme_Id = %s", (id_jeu, id_plat))
                            association_existe = cursor.fetchone()
                            if association_existe:
                                print("Cette association existe déjà !")
                            else:    
                            # Insérer l'association
                                cursor.execute("INSERT INTO jeuxplateforme (Jeux_Id, Plateforme_Id) VALUES (%s, %s)", (id_jeu, id_plat))
                                # self.connexion.commit()
                                print("L'association a été créée avec succès !")
                    self.connexion.commit()        
                else: 
                    print("Aucune modification souhaitée")           

                cursor.close()
                self.connexion.close()
                                
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
                print("La connexion MYSQL est fermée")
                
    def delete_asso_plateforme(self):
        try: 
            if self.connexion.is_connected():
                self.connexion.start_transaction() 
                add = input("Souhaites-tu supprimer une association d'un jeu à une plateforme? (O/N) : ") 
                
                if add.upper() == "O": #Si oui, on affiche la liste des jeux 
                    self.afficher_plateforme()
                    cursor = self.connexion.cursor(prepared=True)
                    id_jeu = int(input("Quel est l'ID du jeux que tu souhaites supprimer : ")) #demande à l'utilisateur l'id du jeu à associer
                    # Vérification de l'existance du jeu
                    cursor.execute("SELECT * FROM jeux WHERE Jeux_Id = %s", (id_jeu,))
                    jeu_existe = cursor.fetchone()
                    if not jeu_existe:
                        print("Ce jeu n'existe pas. Veuillez saisir un ID valide.")
                    else:
                        id_plat = int(input("Quel est l'ID de la plateforme que tu souhaites supprimer au jeu choisi (1. PC, 2. PS4, 3. ONE, 4. SWITCH): ")) #demande à l'utilisateur l'id de la plateforme associé au jeu choisi
                        # Vérification de l'existance de la plateforme
                        cursor.execute("SELECT * FROM plateforme WHERE Plateforme_Id = %s", (id_plat,))
                        plateforme_existe = cursor.fetchone()
                        if not plateforme_existe:
                            print("Cette plateforme n'existe pas. Veuillez saisir un ID valide.")
                        else:
                            # Vérifie si l'association existe déjà
                            cursor.execute("SELECT * FROM jeuxplateforme WHERE Jeux_Id = %s AND Plateforme_Id = %s", (id_jeu, id_plat))
                            association_existe = cursor.fetchone()
                            if not association_existe:
                                print("Cette association n'est pas éxistante !")
                            else:    
                            # Supprimer l'association
                                cursor.execute("DELETE FROM jeuxplateforme WHERE Jeux_Id = %s AND Plateforme_Id = %s", (id_jeu, id_plat))
                                print("L'association a été supprimé avec succès !")
                                
                    self.connexion.commit()        
                else: 
                    print("Aucune modification souhaitée")           

                cursor.close()
                self.connexion.close()
                                
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
                print("La connexion MYSQL est fermée")