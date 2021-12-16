# -*- coding: utf-8 -*-
""" 
/***************************************************************************
 physiocap_creer_arbre
                                 A QGIS 3 plugin
 Physiocap3 plugin helps analyse raw data from Physiocap in QGIS 3 and 
 creates a synthesis of Physiocap measures' campaign
 Physiocap3 plugin permet l'analyse les données brutes de Physiocap dans QGIS 3 
 et crée une synthese d'une campagne de mesures Physiocap
 
 Le module physiocap_creer_arbre gère le nommage et création 
 de l'arbre des résultats d'analyse (dans une structure de 
 données semblable à celle créé par PHYSICAP_V8 du CIVC) 

 Les variables et fonctions sont nommées en Francais
 
                             -------------------
        begin                : 2015-12-05
        git sha              : $Format:%H$
        email                : jean@jhemmi.eu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 * Physiocap3 plugin créé par jhemmi.eu et CIVC est issu de :               *
 *- PSPY : PHYSIOCAP SCRIPT PYTHON VERSION 8.0 10/11/2014                  *
 *   CREE PAR LE POLE TECHNIQUE ET ENVIRONNEMENT DU CIVC                   *
 *   MODIFIE PAR LE CIVC ET L'EQUIPE VIGNOBLE DE MOËT & CHANDON            *
 *   AUTEUR : SEBASTIEN DEBUISSON, MODIFIE PAR ANNE BELOT ET MANON MORLET  *
 *   Physiocap3 plugin comme PSPY sont mis à disposition selon les termes   *
 *   de la licence Creative Commons                                        *
 *   CC-BY-NC-SA http://creativecommons.org/licenses/by-nc-sa/4.0/         *
 *- Plugin builder et QGIS 3 API et à ce titre porte aussi la licence GNU    *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *   http://www.gnu.org/licenses/gpl-2.0.html                              *
 *                                                                         *
***************************************************************************/
"""
from .Physiocap_tools import ( physiocap_message_box, physiocap_question_box,\
        physiocap_log, physiocap_error, physiocap_write_in_synthese, \
        physiocap_rename_existing_file, physiocap_rename_create_dir, physiocap_open_file, \
        physiocap_look_for_MID, physiocap_list_MID, physiocap_csv_vers_vecteur, 
        quel_poly_point_INTER, generer_contour_depuis_points, quelle_campagne, assert_campagne
        )
        
from .Physiocap_CIVC import (physiocap_assert_csv, physiocap_ferme_csv, \
        physiocap_fichier_histo, physiocap_tracer_histo, physiocap_filtrer
        )   

from .Physiocap_var_exception import *

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QPixmap
from qgis.core import ( QgsProject, QgsVectorLayer)

import glob
import shutil
import time  
   
# Creation des repertoires source puis resultats puis histo puis shape

class PhysiocapFiltrer( QtWidgets.QDialog):
    """QGIS Pour voir les messages traduits."""

    def __init__(self, parent=None):
        """Class constructor."""
        super( PhysiocapFiltrer, self).__init__()
    def physiocap_creer_donnees_resultats( self, dialogue, laProjectionCRS, laProjectionTXT, 
        EXT_CRS_SHP, EXT_CRS_PRJ,
        details = "NO", histogrammes = "NO", recursif = "NO",  version_3 = "NO"):
        """ Récupération des paramètres saisies et 
        creation de l'arbre "source" "texte" et du fichier "resultats"
        Ce sont les résultats de l'analyse filtration des données brutes"""
                    
        # Récupérer les paramètres saisies
        Repertoire_Donnees_Brutes = dialogue.lineEditDirectoryPhysiocap.text()
        Repertoire_Donnees_Cibles = dialogue.lineEditDirectoryFiltre.text()
        Nom_Session = dialogue.lineEditSession.text()
        Nom_Profil = dialogue.fieldComboProfilPHY.currentText()
        #Format_vecteur =  dialogue.fieldComboFormats.currentText()

        mindiam = int( dialogue.spinBoxMinDiametre.value())
        maxdiam = int( dialogue.spinBoxMaxDiametre.value())
        max_sarments_metre = int( dialogue.spinBoxMaxSarmentsParMetre.value())

        leModeDeTrace = dialogue.fieldComboModeTrace.currentText() 
            
        if version_3 == "YES":
            segment_mini_vitesse = float( dialogue.doubleSpinBoxVitesseMiniSegment.value())
            segment_maxi_vitesse = float( dialogue.doubleSpinBoxVitesseMaxiSegment.value())
            segment_max_pdop = float( dialogue.doubleSpinBoxPdopMaxSegment.value())   
            segment_mini_point = int( dialogue.spinBoxNombreMiniPointsConsecutifs.value())
            segment_max_derive = int( dialogue.spinBoxDeriveMaxSegment.value())
            segment_pas_de_derive = int( dialogue.spinBoxPasDeDerive.value())
        else:
            segment_mini_vitesse = 0.0
            segment_maxi_vitesse = 1000.0
            segment_mini_point = 2
            segment_max_pdop = 0.1
            segment_max_derive = 50
            segment_pas_de_derive = 25

        if details == "YES":
            interrangs = int( dialogue.spinBoxInterrangs.value())
            interceps = int( dialogue.spinBoxInterceps.value())
            hauteur = int( dialogue.spinBoxHauteur.value())
            densite = float( dialogue.doubleSpinBoxDensite.value())
#            leCepage = dialogue.fieldComboCepage.currentText()
#            laTaille = dialogue.fieldComboTaille.currentText()
        else:
            interrangs = 110
            interceps = 100 
            densite = 0.9
            hauteur = 90
            
        # Vérification de l'existance ou création du répertoire session
        chemin_session = os.path.join(Repertoire_Donnees_Cibles, Nom_Session)
        if not (os.path.exists( chemin_session)):
            try:
                os.mkdir( chemin_session)
            except:
                raise physiocap_exception_rep( Nom_Session)
        else:
            # Le répertoire existant est renommé en (+1)
            try: 
                chemin_session = physiocap_rename_create_dir( chemin_session)
            except:
                raise physiocap_exception_rep( chemin_session)
        
        # Stocker dans la fenetre principale le nom de la session courante
        chemin_base_session = os.path.basename( chemin_session)
        dialogue.lineEditDerniereSession.setText( chemin_base_session)
        dialogue.settings= QSettings( PHYSIOCAP_NOM, PHYSIOCAP_NOM_3)
        dialogue.settings.setValue("Physiocap/derniereSession", chemin_base_session) 
        
        physiocap_log( self.tr( "{0} {1} Début du traitement pour la session Physiocap {2}").\
                format( PHYSIOCAP_2_ETOILES , PHYSIOCAP_UNI, chemin_base_session), leModeDeTrace)
        physiocap_log( self.tr( "Paramètres pour filtrer les diamètres min : {0} max : {1}").\
            format( str( mindiam), str( maxdiam)), leModeDeTrace)
                    
        # Progress BAR 2 %
        dialogue.progressBar.setValue( 2)
        
        # Verification de l'existance ou création du répertoire des sources MID et fichier csv
        if version_3 == "YES":
            chemin_sources = os.path.join(chemin_session, REPERTOIRE_SOURCE_V3)
        else:
            chemin_sources = os.path.join(chemin_session, REPERTOIRE_SOURCES)
        if not (os.path.exists( chemin_sources)):
            try:
                os.mkdir( chemin_sources)
            except:
                raise physiocap_exception_rep( REPERTOIRE_SOURCES)
                    
        # Fichier de concaténations CSV des résultats bruts        
        nom_court_csv_concat = Nom_Session + SUFFIXE_BRUT_CSV
        try:
            nom_csv_concat, csv_concat = physiocap_open_file( nom_court_csv_concat, chemin_sources, "w")
        except physiocap_exception_fic:
            raise physiocap_exception_csv( nom_court_csv_concat)
            
        # Création du fichier concaténé
        nom_fichiers_recherches = os.path.join(Repertoire_Donnees_Brutes, RECHERCHE_EXTENSION_MID)
        
        # Assert le nombre de MID > 0
        # le Tri pour retomber dans l'ordre de Physiocap_V8
        if ( recursif == "YES"):
            # On appelle la fonction de recherche récursive
            listeTriee = physiocap_look_for_MID( Repertoire_Donnees_Brutes, "YES", REPERTOIRE_SOURCES)
        else:
            # Non recursif
            listeTriee = sorted(glob.glob( nom_fichiers_recherches))

        if len( listeTriee) == 0:
            raise physiocap_exception_no_mid( REPERTOIRE_SOURCES)
        
        # Verification si plus de 15 MIDs
        if len( listeTriee) >= 15:
            # Beaucoup de MIDs Poser une question si cancel, on stoppe
            uMsg =self.tr( "Plus de 15 fichier MIDs sont à analyser. Temps de traitement > à 1 minute. Voulez-vous continuer ?")
            if len( listeTriee) >= 30:
                # Beaucoup de MIDs Poser une question si cancel, on stoppe
                uMsg =self.tr( "Plus de 30 fichier MIDs sont à analyser. Temps de traitement > à 5 minute. Voulez-vous continuer ?")
            if ( physiocap_question_box( self, uMsg)):
                pass
            else:
                # Arret demandé
                raise physiocap_exception_stop_user( REPERTOIRE_SOURCES) 
            
        for mid in listeTriee:
            try:
                f_mid = open(mid, "r")
                shutil.copyfileobj(  f_mid, csv_concat)
                # et copie des MID
                nom_cible = os.path.join( chemin_sources, os.path.basename(mid))
                if os.path.exists( nom_cible):
                    nouveau_long = physiocap_rename_existing_file( nom_cible)
                    shutil.copyfile( mid, nouveau_long)
                else:  #copie simple
                    shutil.copy( mid, chemin_sources)
            except:
                raise physiocap_exception_mid( mid)
            f_mid.close()
        csv_concat.close()

        # Assert le fichier de données n'est pas vide
        if os.path.getsize( nom_csv_concat ) == 0 :
            uMsg = self.tr( "Le fichier {0} a une taille nulle !").\
                format( nom_court_csv_concat)
            physiocap_message_box( self, uMsg)
            return physiocap_error( self, uMsg)
        
        # Création la première partie du fichier de synthèse
        fichier_resultat_analyse = chemin_base_session + SEPARATEUR_ + FICHIER_RESULTAT
        nom_fichier_synthese, fichier_synthese = physiocap_open_file( fichier_resultat_analyse, chemin_session , "w")
        fichier_synthese.write( "SYNTHESE PHYSIOCAP\nPROFIL{}\n".format( Nom_Profil))
        fichier_synthese.write( "Générée le : ")
        a_time = time.strftime( "%d/%m/%y %H:%M\n",time.localtime())
        fichier_synthese.write( a_time)
        fichier_synthese.write( "Répertoire de base ")
        fichier_synthese.write( chemin_base_session)
        fichier_synthese.write( "\n")
        if (version_3 == "NO"):
            fichier_synthese.write( "Nom des MID \t\t Date et heures\n=>Nb. Valeurs brutes\tVitesse km/h")
        else:
            fichier_synthese.write( "Nom des MID \t Tiny \t Date et heures\n=>Nb. Valeurs brutes\tVitesse km/h")
        if (CENTROIDES == "YES"):
            fichier_synthese.write("\nCentroïdes")
        fichier_synthese.write("\n")
        info_mid = physiocap_list_MID( Repertoire_Donnees_Brutes, listeTriee)
#        physiocap_log( self.tr( "{} Liste MIDs {}").\
#                format( PHYSIOCAP_UNI, info_mid), leModeDeTrace)

        campagne_debut = quelle_campagne( dialogue, info_mid[0])
        campagne = assert_campagne( dialogue, campagne_debut, info_mid[-1])        
        dialogue.lineEditCampagne.setText( campagne)
        
        for all_info in info_mid:
            info = all_info.split(";")
            if (version_3 == "NO"):
                fichier_synthese.write( str(info[0]) + "\t" + str(info[2]) + "->" + str(info[3])+ "\n")
            else:
                fichier_synthese.write( str(info[0]) + "\t" + str(info[1]) + "\t" + str(info[2]) + "->" + str(info[3])+ "\n")
            # une seule décimale pour vitesse
            fichier_synthese.write( "=>\t{0}\t{1:.1f}".format( info[4], float( info[5])))
            if (CENTROIDES == "YES"):
                # Centroides
                fichier_synthese.write( "\n" + str(info[6]) + "--" + str(info[7]))
            fichier_synthese.write("\n")
    ##        nom_mid = ""
    ##        for fichier_mid in listeTriee:
    ##            nom_mid = nom_mid + os.path.basename( fichier_mid) + " & "
    ##        fichier_synthese.write("Liste des fichiers MID : " + nom_mid[:-3] + "\n")
    ##        physiocap_log( "Liste des MID : " + nom_mid[:-3], leModeDeTrace)
        fichier_synthese.write( "Campagne {}\n".format( campagne))
        
        # Progress BAR 5 %
        dialogue.progressBar.setValue( 5)
        dialogue.progressBarInter.setValue( 0)
        dialogue.progressBarIntra.setValue( 0)
        #physiocap_log( self.tr( "Fin de la création csv et début de synthèse"), leModeDeTrace)
        if (version_3 == "NO"):
            rep_csv = REPERTOIRE_TEXTES
        else:
            rep_csv = REPERTOIRE_TEXTES_V3
        # Vérification de l'existance ou création du répertoire textes
        chemin_textes = os.path.join(chemin_session, rep_csv)
        if not (os.path.exists( chemin_textes)):
            try :
                os.mkdir( chemin_textes)
            except :
                raise physiocap_exception_rep( rep_csv)
                       
        # Ouverture du fichier des diamètres     
        nom_court_fichier_diametre = "diam" + SUFFIXE_BRUT_CSV
        nom_data_histo_diametre, data_histo_diametre = physiocap_open_file( nom_court_fichier_diametre, 
            chemin_textes)
        
        # Ouverture du fichier des sarments     
        nom_court_fichier_sarment = "nbsarm" + SUFFIXE_BRUT_CSV
        nom_data_histo_sarment, data_histo_sarment = physiocap_open_file( nom_court_fichier_sarment, 
            chemin_textes)

        # Ouverture du fichier des vitesses     
        nom_court_fichier_vitesse = "vitesse" + SUFFIXE_BRUT_CSV
        nom_data_histo_vitesse, data_histo_vitesse = physiocap_open_file( nom_court_fichier_vitesse, 
            chemin_textes)

        # Todo: ? Supprimer le fichier erreur
        nom_fichier_erreur, erreur = physiocap_open_file( "erreurs.csv" , chemin_textes)

        # ouverture du fichier source
        csv_concat = open(nom_csv_concat, "r")
        # Appeler la fonction de vérification du format du fichier csv
        # Si plus de 20 % d'erreur exception est monté
        try:
            pourcentage_erreurs = physiocap_assert_csv( self, csv_concat, erreur)
            if ( pourcentage_erreurs > TAUX_LIGNES_ERREUR):
                fichier_synthese.write("\nTrop d'erreurs dans les données brutes")
                # Todo : V3 question selon le taux de lignes en erreur autorisées
                raise physiocap_exception_trop_err_csv( pourcentage_erreurs)
        except:
            raise

        # Progress BAR 10 %
        dialogue.progressBar.setValue( 9)        
        fichier_synthese.write("\n\nPARAMETRES SAISIS ")
        
        if os.path.getsize( nom_csv_concat ) == 0 :
            uMsg = self.tr( "Le fichier {0} a une taille nulle !").\
                format( nom_court_csv_concat)            
            physiocap_message_box( self, uMsg)
            return physiocap_error( self, uMsg)

        # ouverture du fichier source
        csv_concat.close()
        csv_concat = open(nom_csv_concat, "r")

        # Appeler la fonction de traitement
        if histogrammes == "YES":
            #################
            physiocap_fichier_histo( self, csv_concat, data_histo_diametre,    
                        data_histo_sarment, data_histo_vitesse,  erreur)
            #################
        # Fermerture des fichiers
        data_histo_diametre.close()
        data_histo_sarment.close()
        data_histo_vitesse.close()
        csv_concat.close()
        erreur.close()
 
        # Progress BAR 10 %
        dialogue.progressBar.setValue( 10) 

        quel_vecteur_demande = dialogue.fieldComboFormats.currentText()

        physiocap_log( self.tr( "{0} Vecteurs demandés dans le format {1}").\
                format( PHYSIOCAP_UNI, quel_vecteur_demande), leModeDeTrace)
        chemin_shapes = None
        nom_dir_vecteur_segment = None
        if quel_vecteur_demande == SHAPEFILE_NOM:
            # Verification de l'existance ou création du répertoire des SHAPEFILE
            if (version_3 == "NO"):
                rep_vecteur = REPERTOIRE_SHAPEFILE
            else:
                rep_vecteur = REPERTOIRE_SHAPEFILE_V3
            chemin_shapes = os.path.join(chemin_session, rep_vecteur)
            if not (os.path.exists( chemin_shapes)):
                try :
                    os.mkdir( chemin_shapes)
                except :
                    raise physiocap_exception_rep( rep_vecteur)

            if (version_3 == "NO"):
                nom_dir_vecteur_segment = os.path.join(chemin_session, rep_vecteur)
            else:
                # Création du dir des shapes de segments
                nom_dir_vecteur_segment = os.path.join( chemin_shapes, REPERTOIRE_SEGMENT_V3)
                
            if not (os.path.exists( nom_dir_vecteur_segment)):
                try :
                    os.mkdir( nom_dir_vecteur_segment)
                except :
                    raise physiocap_exception_rep( REPERTOIRE_SEGMENT_V3)

        # Progress BAR 12 %
        dialogue.progressBar.setValue( 12)
        
        # Verification de l'existance 
        if version_3 == "YES":
            chemin_histos = os.path.join(chemin_session, REPERTOIRE_HISTO_V3)
        else:
            chemin_histos = os.path.join(chemin_session, REPERTOIRE_HISTOS)
        if not (os.path.exists( chemin_histos)):
            try:
                os.mkdir( chemin_histos)
            except:
                raise physiocap_exception_rep( REPERTOIRE_HISTOS)

        # Si version 4 ne pas tracer les histo ici        
        if histogrammes == "YES":
            # creation d'un histo
            nom_data_histo_sarment, data_histo_sarment = physiocap_open_file( nom_court_fichier_sarment, chemin_textes, 'r')
            nom_histo_sarment, histo_sarment = physiocap_open_file( FICHIER_HISTO_SARMENT, chemin_histos)
            name = nom_histo_sarment
            physiocap_tracer_histo( data_histo_sarment, name, 0, 50, "SARMENT au m", "FREQUENCE", "HISTOGRAMME NBSARM AVANT TRAITEMENT")
            data_histo_sarment.close()
            
            nom_data_histo_vitesse, data_histo_vitesse = physiocap_open_file( nom_court_fichier_vitesse, chemin_textes, 'r')
            nom_histo_vitesse, histo_vitesse = physiocap_open_file( FICHIER_HISTO_VITESSE, chemin_histos)
            name = nom_histo_vitesse
            physiocap_tracer_histo( data_histo_vitesse, name, 0, 15, "VITESSE en km/h", "FREQUENCE", "HISTOGRAMME VITESSE AVANT TRAITEMENT")
            data_histo_vitesse.close()  
            histo_vitesse.close()  

            nom_data_histo_diametre, data_histo_diametre = physiocap_open_file( nom_court_fichier_diametre, chemin_textes, 'r')
            nom_histo_diametre, histo_diametre = physiocap_open_file( FICHIER_HISTO_DIAMETRE, chemin_histos)
            name = nom_histo_diametre
            physiocap_tracer_histo( data_histo_diametre, name, 0, 30, "DIAMETRE en mm", "FREQUENCE", "HISTOGRAMME DIAMETRE AVANT TRAITEMENT")
            data_histo_diametre.close()        
            histo_diametre.close()        
            
            #physiocap_log( self.tr( "Fin de la création des histogrammes bruts"), leModeDeTrace)
        else:
            physiocap_log( self.tr( "Pas de création des histogrammes"), leModeDeTrace)

        # Progress BAR 15 %
        dialogue.progressBar.setValue( 15) 
                  
        # Création des csv
        if (version_3 == "NO"):
            nom_court_csv_sans_0 = Nom_Session + SEPARATEUR_ + "OUT.csv"
            nom_court_csv_avec_0 = Nom_Session + SEPARATEUR_ + "OUT0.csv"
            nom_court_csv_0_seul = Nom_Session + SEPARATEUR_ + "0SEUL.csv"
        else:
            nom_court_csv_sans_0 = Nom_Session + EXTENSION_SANS_ZERO + EXTENSION_CSV
            nom_court_csv_avec_0 = Nom_Session + EXTENSION_AVEC_ZERO + EXTENSION_CSV
            nom_court_csv_0_seul  = Nom_Session + EXTENSION_ZERO_SEUL + EXTENSION_CSV
        
        nom_csv_sans_0, csv_sans_0 = physiocap_open_file( 
            nom_court_csv_sans_0, chemin_textes)
        nom_csv_avec_0, csv_avec_0 = physiocap_open_file( 
            nom_court_csv_avec_0, chemin_textes)
        nom_csv_0_seul, csv_0_seul = physiocap_open_file( 
            nom_court_csv_0_seul, chemin_textes)
       
        nom_court_fichier_diametre_filtre = "diam_FILTERED.csv"
        nom_fichier_diametre_filtre, diametre_filtre = physiocap_open_file( 
            nom_court_fichier_diametre_filtre, chemin_textes )

        # Ouverture du fichier source et re ouverture du ficheir erreur
        csv_concat = open(nom_csv_concat, "r")       
        erreur = open(nom_fichier_erreur,"a")

        # Filtrage des données Physiocap qui rend deux segements
        #################            
        try:
            nom_layer_segment,  nom_layer_segment_brise = physiocap_filtrer( dialogue,
                csv_concat, csv_sans_0, csv_avec_0, csv_0_seul, 
                nom_dir_vecteur_segment, Nom_Session, chemin_session, 
                diametre_filtre, nom_fichier_synthese, erreur, 
                mindiam, maxdiam, max_sarments_metre, 
                segment_mini_vitesse, segment_maxi_vitesse, segment_mini_point, segment_max_pdop, 
                segment_max_derive,  segment_pas_de_derive, 
                details, interrangs, interceps, densite, hauteur,
                laProjectionCRS, laProjectionTXT, version_3)
            # Fermeture du fichier destination
            physiocap_ferme_csv( csv_sans_0, csv_avec_0, csv_0_seul, diametre_filtre, erreur, csv_concat)
        #################
        except physiocap_exception_err_csv as e: 
            # Fermeture du fichier destination
            physiocap_ferme_csv( csv_sans_0, csv_avec_0, csv_0_seul, diametre_filtre, erreur, csv_concat)
            raise physiocap_exception_err_csv( nom_court_csv_concat)
        # On remonte les autres exceptions
        except:
            raise
        # Progress BAR 30 %
        dialogue.progressBar.setValue( 30)

        if histogrammes == "YES":
            # Histo apres filtration
            nom_fichier_diametre_filtre, diametre_filtre = physiocap_open_file( 
                nom_court_fichier_diametre_filtre, chemin_textes , "r")
            histo_diametre.close()
            nom_histo_diametre_filtre, histo_diametre = physiocap_open_file( FICHIER_HISTO_DIAMETRE_FILTRE, chemin_histos)

            physiocap_tracer_histo( diametre_filtre, nom_histo_diametre_filtre, 0, 30, \
                "DIAMETRE en mm", "FREQUENCE", "HISTOGRAMME DIAMETRE APRES TRAITEMENT")
            diametre_filtre.close()        
            #physiocap_log( self.tr( "Fin de la création de l'histogramme filtré"), leModeDeTrace)
                                              
        # On écrit dans le fichiers résultats les paramètres du modéle
        fichier_synthese.close()
        fichier_synthese = open(nom_fichier_synthese, "a")
        if details == "NO":
            fichier_synthese.write("\nAucune information parcellaire saisie\n")
        else:
            fichier_synthese.write("\n")
#            fichier_synthese.write( "Cépage : %s \n" % leCepage)
#            fichier_synthese.write( "Type de taille : %s\n" %laTaille)        
            fichier_synthese.write( "Hauteur de végétation : %s cm\n" %hauteur)
            fichier_synthese.write( "Densité des bois de taille : %s \n" %densite)
            fichier_synthese.write( "Ecartement entre rangs : %s cm\n" %interrangs)
            fichier_synthese.write( "Ecartement entre ceps : %s cm\n" %interceps)        

        fichier_synthese.write("\n")
        fichier_synthese.write("Nombre de sarments max au mètre linéaire: %s \n" %max_sarments_metre)
        fichier_synthese.write("Diamètre minimal : %s mm\n" %mindiam)
        fichier_synthese.write("Diamètre maximal : %s mm\n" %maxdiam)
        fichier_synthese.close()

        # Progress BAR 40%
        dialogue.progressBar.setValue( 40)

        nom_base_vecteur = Nom_Session + NOM_POINTS
        # Création des vecteurs sans 0
        if (version_3 == "NO"):
            nom_court_vecteur_sans_0 = nom_base_vecteur
        else: 
            nom_court_vecteur_sans_0 = nom_base_vecteur + EXTENSION_SANS_ZERO                     
        nom_layer_sans_0 = physiocap_csv_vers_vecteur( dialogue, chemin_session, Nom_Session, 
            40, EXTENSION_SANS_ZERO, 
            nom_csv_sans_0,  chemin_shapes, nom_court_vecteur_sans_0,
            "NO", details, version_3)
 
        # Progress BAR 50 %
        dialogue.progressBar.setValue( 50)

        # Création des vecteurs avec 0
        if (version_3 == "NO"):
            nom_court_vecteur_avec_0 = nom_base_vecteur + EXTENSION_AVEC_ZERO_V2
        else:
            nom_court_vecteur_avec_0 =nom_base_vecteur + EXTENSION_AVEC_ZERO        
        nom_layer_avec_0 = physiocap_csv_vers_vecteur( dialogue, chemin_session, Nom_Session, 
            60, EXTENSION_AVEC_ZERO, 
            nom_csv_avec_0,  chemin_shapes, nom_court_vecteur_avec_0, 
            nom_fichier_synthese, details, version_3)
 
        # Progress BAR 
        dialogue.progressBar.setValue( 65)

        # Création des vecteurs O seul
        if (version_3 == "NO"):
            pass
        else: # V3 seulement
            # Création des shapes avec seulement les 0
            nom_court_vecteur_0_seul = nom_base_vecteur + EXTENSION_ZERO_SEUL
            nom_layer_0_seul = physiocap_csv_vers_vecteur( dialogue, chemin_session, Nom_Session, 
                80, EXTENSION_ZERO_SEUL, 
                nom_csv_0_seul,  chemin_shapes, nom_court_vecteur_0_seul,
                "NO", details, version_3) 

        # Progress BAR 
        dialogue.progressBar.setValue( 70)

        if dialogue.checkBoxContourSolo.isChecked():
            physiocap_log( "{0} {1} Avant création du contour à partir des points.". \
                format( PHYSIOCAP_INFO, PHYSIOCAP_UNI), leModeDeTrace)
            nom_contour = generer_contour_depuis_points( dialogue, nom_layer_sans_0, listeTriee)                
            physiocap_log( "{0} {1} Création du contour OK : {2}.". \
                format( PHYSIOCAP_INFO, PHYSIOCAP_UNI, nom_contour), leModeDeTrace)
                
        # Progress BAR 80%
        dialogue.progressBar.setValue( 80)
        
        # Creer un groupe pour cette analyse
        # Attention il faut qgis > 2.4 metadata demande V2.4 mini
        mon_projet = QgsProject.instance()
        root = mon_projet.layerTreeRoot()
        # Nommmer le groupe chemin_base_session
        sous_groupe = root.addGroup( chemin_base_session)
        
        # Récupérer des styles pour chaque shape
        dir_template = dialogue.fieldComboThematiques.currentText()
        # Affichage des différents shapes dans QGIS
        SHAPE_A_AFFICHER = []
        qml_is = ""
        if dialogue.checkBoxDiametre.isChecked():
            qml_is = dialogue.lineEditThematiqueDiametre.text().strip('"') + EXTENSION_QML
            # Pas de choix du shape, car il faut pour Inter un diam sans 0
            SHAPE_A_AFFICHER.append( (nom_layer_sans_0, 'DIAMETRE mm', qml_is))
        if dialogue.checkBoxSarment.isChecked():
            qml_is = dialogue.lineEditThematiqueSarment.text().strip('"') + EXTENSION_QML
            # Choix du shape à afficher
            if ( dialogue.fieldComboShapeSarment.currentIndex() == 0):
                SHAPE_A_AFFICHER.append( (nom_layer_sans_0, 'SARMENT par m', qml_is))
            else:
                SHAPE_A_AFFICHER.append( (nom_layer_avec_0, 'SARMENT par m', qml_is))
        if dialogue.checkBoxBiomasse.isChecked():
            qml_is = dialogue.lineEditThematiqueBiomasse.text().strip('"') + EXTENSION_QML
            # Choix du shape à afficher
            if ( dialogue.fieldComboShapeBiomasse.currentIndex() == 0):
                SHAPE_A_AFFICHER.append( (nom_layer_sans_0, 'BIOMASSE', qml_is))
            else:
                SHAPE_A_AFFICHER.append( (nom_layer_avec_0, 'BIOMASSE', qml_is))
        if dialogue.checkBoxVitesse.isChecked():
            qml_is = dialogue.lineEditThematiqueVitesse.text().strip('"') + EXTENSION_QML
            # Choix du shape à afficher
            if ( dialogue.fieldComboShapeVitesse.currentIndex() == 0):
                SHAPE_A_AFFICHER.append( (nom_layer_sans_0, 'VITESSE km/h', qml_is))
            else:
                SHAPE_A_AFFICHER.append( (nom_layer_avec_0, 'VITESSE km/h', qml_is))       
        if dialogue.checkBoxContour.isChecked():
            qml_is = dialogue.lineEditThematiqueContour.text().strip('"') + EXTENSION_QML
            # Choix du shape à afficher
            if dialogue.checkBoxContourSolo.isChecked() and os.path.exists(nom_contour):
                SHAPE_A_AFFICHER.append( (nom_contour, 'Contour généré', qml_is))
                
        if (version_3 != "NO") and dialogue.checkBoxPasMesure.isChecked():
            qml_is = dialogue.lineEditThematiquePasMesure.text().strip('"') + EXTENSION_QML
            SHAPE_A_AFFICHER.append( (nom_layer_0_seul, 'PAS DE MESURE', qml_is))
            
        if (version_3 != "NO") and dialogue.checkBoxSegment.isChecked():
            qml_is = dialogue.lineEditThematiqueSegment.text().strip('"') + EXTENSION_QML
            SHAPE_A_AFFICHER.append( (nom_layer_segment, 'SEGMENT', qml_is))

        if (version_3 != "NO") and dialogue.checkBoxSegmentBrise.isChecked():
            qml_is = dialogue.lineEditThematiqueSegmentBrise.text().strip('"') + EXTENSION_QML
            SHAPE_A_AFFICHER.append( (nom_layer_segment_brise, 'SEGMENT BRISE', qml_is))

        for shapename, titre, un_template in SHAPE_A_AFFICHER:
##            if ( dialogue.fieldComboFormats.currentText() == POSTGRES_NOM ):
##                uri_nom = physiocap_quel_uriname( dialogue)
##                #physiocap_log( "URI nom : " +  uri_nom, leModeDeTrace)
##                uri_modele = physiocap_get_uri_by_layer( dialogue, uri_nom )
##                if uri_modele != None:
##                    uri_connect, uri_deb, uri_srid, uri_fin = physiocap_tester_uri( dialogue, uri_modele)            
##                    nom_court_shp = os.path.basename( shapename)
##                    #TABLES = "public." + nom_court_shp
##                    uri = uri_deb +  uri_srid + \
##                       " key='gid' type='POINTS' table=" + nom_court_shp[ :-4] + " (geom) sql="            
##    ##              "dbname='testpostgis' host='localhost' port='5432'" + \
##    ##              " user='postgres' password='postgres' SRID='2154'" + \
##    ##              " key='gid' type='POINTS' table=" + nom_court_shp[ :-4] + " (geom) sql="
##    ##                physiocap_log( "Création dans POSTGRES : >>" + uri + "<<", leModeDeTrace)
##    ##                vectorPG = QgsVectorLayer( uri, titre, POSTGRES_NOM)
##                else:
##                    aText = self.tr( "Pas de connecteur vers Postgres : {0}. On continue avec des shapefiles").\
##                         format ((str( uri_nom)))
##                    physiocap_log( aText, leModeDeTrace)
##                    # Remettre le choix vers ESRI shape file
##                    dialogue.fieldComboFormats.setCurrentIndex( 0)

            vector = QgsVectorLayer( shapename, titre, 'ogr')
            mon_projet.addMapLayer( vector, False)
            # Ajouter le vecteur dans un groupe
            sous_groupe.addLayer( vector)
            le_template = os.path.join( dir_template, un_template)
            if ( os.path.exists( le_template)):
                #physiocap_log( "Physiocap le template : " + os.path.basename( le_template), TRACE_TOOLS)
                vector.loadNamedStyle( le_template)
        
        # Fichier de synthese dans la fenetre resultats   
        fichier_synthese = open(nom_fichier_synthese, "r")
        while True :
            ligne = fichier_synthese.readline() # lit les lignes 1 à 1
            physiocap_write_in_synthese( dialogue, ligne)
            if not ligne: 
                #fichier_synthese.close
                break
        fichier_synthese.close

        # Progress BAR 90 %
        dialogue.progressBar.setValue( 90)
                    
        # Mettre à jour les histogrammes dans fenetre resultat
        if histogrammes == "YES":
            dialogue.label_histo_sarment.setPixmap( QPixmap( nom_histo_sarment))
            dialogue.label_histo_vitesse.setPixmap( QPixmap( nom_histo_vitesse))
            if ( dialogue.label_histo_diametre_avant.setPixmap( QPixmap( nom_histo_diametre))):
                physiocap_log( self.tr( "Physiocap histogramme diamètre chargé"), leModeDeTrace)                
            if ( dialogue.label_histo_diametre_apres.setPixmap( QPixmap( nom_histo_diametre_filtre))):
                physiocap_log( self.tr( "Physiocap histogramme diamètre filtré chargé"), leModeDeTrace)    
        else:
            dialogue.label_histo_sarment.setPixmap( QPixmap( FICHIER_HISTO_NON_CALCULE))
            dialogue.label_histo_vitesse.setPixmap( QPixmap( FICHIER_HISTO_NON_CALCULE))
            dialogue.label_histo_diametre_avant.setPixmap( QPixmap( FICHIER_HISTO_NON_CALCULE))
            dialogue.label_histo_diametre_apres.setPixmap( QPixmap( FICHIER_HISTO_NON_CALCULE))
            physiocap_log( self.tr( "Physiocap pas d'histogramme calculé"), leModeDeTrace)    
                           
        # Progress BAR 100 %
        dialogue.progressBar.setValue( 100)
        # Fin 
        physiocap_log( self.tr( "{0} {1} a affiché les couches demandées dans le groupe {2}").\
            format( PHYSIOCAP_INFO , PHYSIOCAP_UNI, chemin_base_session), leModeDeTrace)
        quel_poly_point_INTER( dialogue)

        return 0 
