# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Physiocap_CIVC
                                 A QGIS 3 plugin
 Physiocap3  plugin helps analyse raw data from Physiocap in QGIS 3 and 
 creates a synthesis of Physiocap measures' campaign
 Physiocap3 plugin permet l'analyse les données brutes de Physiocap dans QGIS 3 et
 crée une synthese d'une campagne de mesures Physiocap
 
 Le module CIVC contient le filtre de données, de creation des csv 
 et shapfile, de creation des histogrammes
 
 Partie Calcul non modifié par rapport à physiocap_V8
 Les variables et fonctions sont nommées en Francais par compatibilité avec 
 la version physiocap_V8
                             -------------------
        begin                : 2015-07-31
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
 *- Plugin builder et QGIS 3 API API et à ce titre porte aussi la licence GNU    *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *   http://www.gnu.org/licenses/gpl-2.0.html                              *
 *                                                                         *
***************************************************************************/
"""

from .Physiocap_tools import ( physiocap_log, physiocap_error, \
    physiocap_quelle_projection_demandee, \
    physiocap_create_projection_file) 
from .Physiocap_var_exception import *

from PyQt5.QtCore import QVariant
from qgis.core import (QgsFields, QgsField, \
        QgsFeature, QgsGeometry, QgsCoordinateReferenceSystem,  QgsCoordinateTransform,  \
        QgsPoint, QgsPointXY, QgsVectorFileWriter, QgsMessageLog, QgsWkbTypes)
        
try :
    import csv
except ImportError:
    aText = "Erreur bloquante : module csv n'est pas accessible." 
    QgsMessageLog.logMessage( aText, "\u03D5 Erreurs", Qgis.Warning)

try :
    import matplotlib.pyplot as plt
except ImportError:
    aText ="Erreur bloquante : module matplotlib.pyplot n'est pas accessible\n" 
    aText = aText + 'Sous Ubuntu : installez python3-matplotlib par "sudo apt-get install python3-matplotlib"'
    aText = aText + "Sous Fedora : installez python-matplotlib-qt4" 
    QgsMessageLog.logMessage( aText, "\u03D5 Erreurs", Qgis.Warning)
    
try :
    import numpy as np
except ImportError:
    aText ="Erreur bloquante : module numpy n'est pas accessible" 
    QgsMessageLog.logMessage( aText, "\u03D5 Erreurs", Qgis.Warning)

def physiocap_segment_vers_shapefile( self, nom_shape,  nom_prj,  segment,  info_segment, 
        laProjectionCRS, laProjectionTXT, 
        segment_simplifie="YES"):
    """ Creation de shape file à partir des données de segment """
    # Prepare les attributs
    les_champs = QgsFields()
    les_champs.append( QgsField("GID", QVariant.Int, "integer", 10))
    les_champs.append( QgsField("GID_10", QVariant.Int, "integer", 10))
    les_champs.append( QgsField("NB_POINTS", QVariant.Int, "integer", 10))
    les_champs.append( QgsField("DATE_DEB", QVariant.String, "string", 25))
    les_champs.append( QgsField("DATE_FIN", QVariant.String, "string", 25))
    les_champs.append( QgsField("DERIVE", QVariant.Double, "double", 10,2))
    les_champs.append( QgsField("GID_GARDE", QVariant.String, "varchar", 100))
    les_champs.append( QgsField("GID_TROU", QVariant.String, "varchar", 100))
#    
    # Creation du Shape
    writer = QgsVectorFileWriter( nom_shape, "utf-8", les_champs, 
            QgsWkbTypes.MultiLineString, laProjectionCRS , 
            "ESRI Shapefile")
            
    # Ecriture du shp
    numero_ligne = 0
    for un_segment  in segment:
        feat = QgsFeature()
        le_gid = info_segment[numero_ligne][NUM_SEG]
        gid_modulo_10 = le_gid % 10
        nombre = info_segment[numero_ligne][NOMBRE]
        # GID gardé
        gid_points_gardes = info_segment[numero_ligne][GID_GARDE]
        nb_points_gardes = len( gid_points_gardes)
        if  nb_points_gardes > 30:
            str_gid_points_gardes = str( gid_points_gardes[0:2]) + "... " + \
                str(nb_points_gardes) + " points gardés ..." + \
                str( gid_points_gardes[nb_points_gardes-2:])
        else:
            str_gid_points_gardes  = str(  gid_points_gardes)
        # GID manquants
        gid_points_manquants = info_segment[numero_ligne][GID_TROU]
        nb_points_manquants = len( gid_points_manquants)
        if  nb_points_manquants > 30:
            str_gid_points_manquants = str( gid_points_manquants[0:2]) + "... " + \
                str(nb_points_manquants) + " points manquants ..." + \
                str( gid_points_manquants[nb_points_manquants-2:])
        else:
            str_gid_points_manquants  = str(  gid_points_manquants)
            
        if (segment_simplifie == "YES"):   # Premier et dernier  
            feat.setGeometry( QgsGeometry.fromPolylineXY( [ un_segment[0], un_segment[nombre-1]] )) #écrit la géométrie
        else:  # Tous les poins
            feat.setGeometry( QgsGeometry.fromPolylineXY( un_segment )) #écrit la géométrie            
        feat.setAttributes([ le_gid, gid_modulo_10, nombre, 
                                        info_segment[numero_ligne][DATE_DEBUT],    
                                        info_segment[numero_ligne][DATE_FIN],
                                        round( float( info_segment[numero_ligne][DERIVE]), 2), 
                                        str_gid_points_gardes, str_gid_points_manquants
                                    ])
        numero_ligne = numero_ligne + 1
        # Ecrit le feature
        writer.addFeature( feat)

    # PRJ file
    physiocap_create_projection_file( nom_prj,  laProjectionTXT)

    return
def physiocap_csv_vers_shapefile( self, progress_barre, donnee_3D ,  csv_name, shape_name, prj_name, 
    laProjectionCRS, laProjectionTXT, 
    nom_fichier_synthese = "NO", details = "NO",  version_3 = "NO"):
    """ Creation de shape file à partir des données des CSV
    Si nom_fichier_synthese n'est pas "NO", on produit les moyennes dans le fichier 
    qui se nomme nom_fichier_synthese
    Selon la valeur de détails , on crée les 5 premiers ("NO") ou tous les attibuts ("YES")
    """
    leModeDeTrace = self.fieldComboModeTrace.currentText()
    #physiocap_log( "Le nom du csv : {0}".format( csv_name),  TRACE_TOOLS)
    
    # Préparation de la liste d'arguments
    gid, x,y,nbsarm,diam,biom,date_capture,vitesse= [],[],[],[],[],[],[],[]
    altitude, pdop,  distance,  derive =  [],[],[],[]
    azimuth, nbsart =  [],[]
    nbsarmm2,nbsarcep,biommm2,biomgm2,biomgcep=[],[],[],[],[]
    
    un_fic = open( csv_name, "r")
    lignes = un_fic.readlines()
    nombre_mesures = len( lignes)
    un_fic.close()
    progress_step = int( nombre_mesures / 19)
    barre = 1
    
    #Lecture des data dans le csv et stockage dans une liste
    with open(csv_name, "rt") as csvfile:
        try:
            r = csv.reader(csvfile, delimiter=";")
        except NameError:
            uText = "Erreur bloquante : module csv n'est pas accessible."
            physiocap_error( self, uText)
            return -1

        for numrow, row in enumerate( r):
            #skip header
            if numrow > 0: 
                # Aavancer la barre de progression de 19 points
                if ( numrow > progress_step * barre):
                    barre = barre + 1
                    progress_barre = progress_barre + 1
                    self.progressBar.setValue( progress_barre)
                    
                if version_3 == "NO":
                    if ( laProjectionTXT == "L93"):
                        x.append(float(row[2]))
                        y.append(float(row[3]))
                    if ( laProjectionTXT == "GPS"):
                        x.append(float(row[0]))
                        y.append(float(row[1]))
                    nbsarm.append(float(row[4]))
                    diam.append(float(row[5]))
                    biom.append(float(row[6]))
                    # A_TESTER : sans str
                    date_capture.append(str(row[7]))
                    vitesse.append(float(row[8]))
                else: # Changement de position dans cvs
                    gid.append(float(row[0]))
                    if ( laProjectionTXT == "L93"):
                        x.append(float(row[3]))
                        y.append(float(row[4]))
                    if ( laProjectionTXT == "GPS"):
                        x.append(float(row[1]))
                        y.append(float(row[2]))
                    altitude.append(float(row[5]))
                    pdop.append(float(row[6]))
                    distance.append(float(row[7]))
                    derive.append(float(row[8]))
                    azimuth.append(float(row[9]))
                    nbsart.append(int(row[10]))
                    nbsarm.append(float(row[11]))
                    diam.append(float(row[12]))
                    biom.append(float(row[13]))
                    date_capture.append(str(row[14]))
                    vitesse.append(float(row[15]))
                    
                if details == "YES":
                    if version_3 == "NO":
                        # Niveau de detail demandé
                        # assert sur len row
                        if len(row) != 14:
                            return physiocap_error( self, "Le nombre de colonnes :" +
                                    str( len(row)) + 
                                    " du cvs ne permet pas le calcul détaillé")
                        nbsarmm2.append(float(row[9]))
                        nbsarcep.append(float(row[10]))
                        biommm2.append(float(row[11]))
                        biomgm2.append(float(row[12]))
                        biomgcep.append(float(row[13]))
                    else:
                        if len(row) != 21:
                            return physiocap_error( self, "Le nombre de colonnes :" +
                                    str( len(row)) + 
                                    " du cvs ne permet pas le calcul détaillé")
                        nbsarmm2.append(float(row[16]))
                        nbsarcep.append(float(row[17]))
                        biommm2.append(float(row[18]))
                        biomgm2.append(float(row[19]))
                        biomgcep.append(float(row[20]))                        
                
    # Prepare les attributs
    les_champs = QgsFields()
    # V1.0 Ajout du GID
    les_champs.append( QgsField("GID", QVariant.Int, "integer", 10))
    les_champs.append( QgsField("DATE", QVariant.String, "string", 25))
    les_champs.append( QgsField("VITESSE", QVariant.Double, "double", 10,2))
    if version_3 == "YES":
        les_champs.append( QgsField("ALTITUDE", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("PDOP", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("DISTANCE", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("DERIVE", QVariant.Double, "double", 10,1))
        les_champs.append( QgsField("AZIMUTH", QVariant.Double, "double", 10,1))
        les_champs.append( QgsField("NBSART",  QVariant.Int, "integer", 10))
    les_champs.append(QgsField("NBSARM",  QVariant.Double, "double", 10,2))
    les_champs.append(QgsField("DIAM",  QVariant.Double, "double", 10,2))
    les_champs.append(QgsField("BIOM", QVariant.Double,"double", 10,2)) 
    if details == "YES":
        # Niveau de detail demandé
        les_champs.append(QgsField("NBSARMM2", QVariant.Double,"double", 10,2))
        les_champs.append(QgsField("NBSARCEP", QVariant.Double,"double", 10,2))
        les_champs.append(QgsField("BIOMM2", QVariant.Double,"double", 10,2))
        les_champs.append(QgsField("BIOMGM2", QVariant.Double,"double", 10,2))
        les_champs.append(QgsField("BIOMGCEP", QVariant.Double,"double", 10,2))

    # Creation du Shape
    if version_3 == "YES":
        writer = QgsVectorFileWriter( shape_name, "utf-8", les_champs, 
            QgsWkbTypes.PointZ, laProjectionCRS , "ESRI Shapefile")
    else:
        writer = QgsVectorFileWriter( shape_name, "utf-8", les_champs, 
            QgsWkbTypes.Point, laProjectionCRS , "ESRI Shapefile")        
    # Ecriture du shp
    for numPoint,Xpoint in enumerate(x):
        feat = QgsFeature()
        if version_3 == "YES":
            # choix de la données dans Z
            val_3D = 0.0
            if donnee_3D == "SANS_0":
                val_3D = diam[numPoint]
            if donnee_3D == "AVEC_0":
                val_3D = altitude[numPoint]
            if donnee_3D == "O_SEUL":
                val_3D = vitesse[numPoint]                
            #écrit la géométrie avec le Z = diametre (ou altitude ou vitesse)
            feat.setGeometry( QgsGeometry(QgsPoint( 
                Xpoint, y[numPoint], val_3D))) 
        else:
            # TODO: test sans fromPointXY
            feat.setGeometry( QgsGeometry.fromPointXY(QgsPointXY( Xpoint,y[numPoint]))) #écrit la géométrie
        
        if details == "YES":
            if version_3 == "NO":
                # Ecrit tous les attributs
               feat.setAttributes( [ numPoint, date_capture[numPoint], vitesse[numPoint], 
                                    nbsarm[numPoint], diam[numPoint], biom[numPoint],
                                    nbsarmm2[numPoint], nbsarcep[numPoint], biommm2[numPoint], 
                                    biomgm2[numPoint], biomgcep[numPoint]
                                   ])
            else:
                feat.setAttributes( [ gid[numPoint], date_capture[numPoint], vitesse[numPoint], 
                                    altitude[numPoint], pdop[numPoint],  distance[numPoint],  derive [numPoint], 
                                    azimuth[numPoint], nbsart[numPoint],
                                    nbsarm[numPoint], diam[numPoint], biom[numPoint],
                                    nbsarmm2[numPoint], nbsarcep[numPoint], biommm2[numPoint], 
                                    biomgm2[numPoint], biomgcep[numPoint]
                                   ])                
        else: # sans les détails
            if version_3 == "NO":
                # Ecrit les 5 premiers attributs
                feat.setAttributes( [ numPoint, date_capture[numPoint], vitesse[numPoint], 
                                    nbsarm[numPoint], diam[numPoint], biom[numPoint]
                                    ])
            else:
                # Ecrit les 10 premiers attributs
                feat.setAttributes( [ gid[numPoint], date_capture[numPoint], vitesse[numPoint], 
                                    altitude[numPoint], pdop[numPoint], distance[numPoint],  derive[numPoint], 
                                    azimuth[numPoint], nbsart[numPoint],
                                    nbsarm[numPoint], diam[numPoint], biom[numPoint]
                                    ])                
        # Ecrit le feature
        writer.addFeature( feat)
        
  
    # Cas PG
##    if (self.fieldComboFormats.currentText() == POSTGRES_NOM ):
##        # Todo ; fonction physiocap_creer_PG_par_copie_vecteur( uri_nom, shape_modele)
##        # Vérifier si une connexion Physiocap existe
##        uri_nom = physiocap_quel_uriname( self)
##        uri_modele = physiocap_get_uri_by_layer( self, uri_nom )
##        if uri_modele != None:
##            uri_connect, uri_deb, uri_srid, uri_fin = physiocap_tester_uri( self, uri_modele)
##            if uri_deb != None:
##                nom_court_shp = os.path.basename( shape_name)
##                #laTable = "'public.\"" + nom_court_shp[ :-4] + "\"'"
##                laTable = "'\"" + nom_court_shp[ :-4] + "\"'"
##                reponse = physiocap_existe_table_uri( self, uri_deb, laTable)
##                if reponse != None:
##                    if reponse == True:
##                        laTable = "\"" + nom_court_shp[ :-4] + "\""
##                        #physiocap_log( "Table existe déjà : " +  laTable, TRACE_PG)
##                        # Cette table existe déjà = > drop 
##                        reponse_drop = physiocap_detruit_table_uri( self, uri_deb, laTable)
##                        if reponse_drop == None:
##                            aText = "Problème lors de la destruction de la table : " +  laTable
##                            physiocap_log( aText, TRACE_PG)
##                            physiocap_error( self, aText)  
##                            # Todo : V3 gérer par exception physiocap_exception_pg
##                            return physiocap_message_box( self, 
##                                self.tr( aText),
##                                "warning")                   
##                    # Creer la table
##                    laTable = nom_court_shp[ :-4] 
##                    vector = QgsVectorLayer( shape_name, "INUTILE", 'ogr')
##                    uri = uri_deb + uri_srid + \
##                        " key=gid type=POINTS table=" + laTable + uri_fin
## #       uri = "dbname='testpostgis' host=localhost port=5432" + \
## #             " user='postgres' password='postgres'" + \
## #              " key=gid type=POINTS table=" + nom_court_shp[ :-4] + " (geom) sql="
##                    error = QgsVectorLayerImport.importLayer( vector, uri, POSTGRES_NOM, laProjectionCRS, False, False)
##                    if error[0] != 0:
##                        physiocap_error( self, "Problème Postgres : " + str(error[0]) + " => " + str(error[1]))
##                        #iface.messageBar().pushMessage('Physiocap Error', error[1], QgsMessageBar.CRITICAL, 5)    
## #                    else:
## #                        # Sans erreur on détruit le shape file
## #                        if os.path.isfile( shape_name):
## #                            os.remove( shape_name)
##                else:
##                    aText = "Vérification problématique pour la table : " + laTable + \
##                        ". On continue avec des shapefiles"
##                    physiocap_log( aText, TRACE_PG)
##                    piocap_error( aText)
##                    # Remettre le choix vers ESRI shape file
##                    self.fieldComboFormats.setCurrentIndex( 0)   
##            else:
##                aText = "Pas de connection possible à Postgres : " + uri_nom + \
##                    ". On continue avec des shapefiles"
##                physiocap_log( aText, TRACE_PG)
##                physiocap_error( self, aText)
##                # Remettre le choix vers ESRI shape file
##                self.fieldComboFormats.setCurrentIndex( 0)   
##                
##        else:
##            aText = "Pas de connecteur vers Postgres : " +  uri_nom + \
##                        ". On continue avec des shapefiles"
##            physiocap_log( aText, TRACE_PG)
##            physiocap_error( self, aText)
##            # Remettre le choix vers ESRI shape file
##            self.fieldComboFormats.setCurrentIndex( 0)   
##    else:
 
    # Create the PRJ file
    physiocap_create_projection_file( prj_name,  laProjectionTXT)
 
        
    # Création de la synthese
    if nom_fichier_synthese != "NO":
        # ASSERT Le fichier de synthese existe
        if not os.path.isfile( nom_fichier_synthese):
            uMsg ="Le fichier de synthese " + nom_fichier_synthese + "n'existe pas"
            physiocap_log( uMsg, leModeDeTrace)
            return physiocap_error( self, uMsg)
        
        # Ecriture des resulats
        fichier_synthese = open(nom_fichier_synthese, "a")
        try:
            fichier_synthese.write("\n\nSTATISTIQUES\n")
            fichier_synthese.write("Vitesse moyenne d'avancement km/h \n	mean : %0.1f \n" %np.mean(vitesse))
            if version_3 == "YES":
                fichier_synthese.write("Altitude moyenne GPS en m \n	mean : %0.1f\t std : %0.1f\n" \
                    %(np.mean(altitude), np.std(altitude)))
                fichier_synthese.write("Pdop  moyen du GPS \n	mean : %0.1f\t std : %0.1f\n" \
                    %(np.mean(pdop), np.std(pdop)))
                fichier_synthese.write("Distance moyenne entre point m \n	mean : %0.1f\t std : %0.1f\n" \
                    %(np.mean(distance), np.std(distance)))
#                fichier_synthese.write("Dérive moyenne entre point % \n	mean : %0.1f\t std : %0.1f\n" \
#                    %(np.mean(derive), np.std(derive)))
        except:
            msg = "Erreur bloquante durant premiers calculs de moyennes\n"
            physiocap_error( self, msg )
            return -1
        
        try:
            fichier_synthese.write("Section moyenne mm\n	mean : %0.1f \t std : %0.1f\n" %(np.mean(diam), np.std(diam)))
            fichier_synthese.write("Nombre de sarments au m \n	mean : %0.1f \t std : %0.1f\n" %(np.mean(nbsarm), np.std(nbsarm)))
            fichier_synthese.write("Biomasse en mm²/m linéaire \n	mean : %0.1f\t std : %0.1f\n" %(np.mean(biom), np.std(biom)))
            if details == "YES":
                fichier_synthese.write("Nombre de sarments au m² \n	 mean : %0.1f  \t std : %0.1f\n" %(np.mean(nbsarmm2), np.std(nbsarmm2)))
                fichier_synthese.write("Nombre de sarments par cep \n	mean : %0.1f \t\t std : %0.1f\n" %(np.mean(nbsarcep), np.std(nbsarcep)))
                fichier_synthese.write("Biomasse en mm²/m² \n	mean : %0.1f\t std : %0.1f\n" %(np.mean(biommm2), np.std(biommm2)))
                fichier_synthese.write("Biomasse en gramme/m² \n	mean : %0.1f\t std : %0.1f\n" %(np.mean(biomgm2), np.std(biomgm2)))
                fichier_synthese.write("Biomasse en gramme/cep \n	mean : %0.1f\t std : %0.1f\n" %(np.mean(biomgcep), np.std(biomgcep))) 
        except:
            msg = "Erreur bloquante durant deuxièmes calculs de moyennes\n"
            physiocap_error( self, msg )
            return -1
                    
        fichier_synthese.close()

#    # TODO : Création des histogrammes 
#    try :
#        import processing
#        try:
#            from processing.core.Processing import Processing
#            Processing.initialize()
#        except:
#            physiocap_log( self.tr( "{0} nécessite l'extension {1}").\
#                format( PHYSIOCAP_UNI, self.tr("Traitement")), leModeDeTrace)
#            raise physiocap_exception_no_processing( "Pas d'extension Traitement")               
#        versionGDAL = processing.tools.raster.gdal.__version__
#        #versionSAGA = processing.algs.saga.SagaUtils.getInstalledVersion()
#    except ImportError:
#        physiocap_log( self.tr( "{0} nécessite l'extension {1}").\
#            format( PHYSIOCAP_UNI, self.tr("Traitement")), leModeDeTrace)
#        raise physiocap_exception_no_processing( "Pas d'extension Traitement")
#        
#    physiocap_log( self.tr( "Gdal version {0}").format(versionGDAL), TRACE_TOOLS)
#    physiocap_log( self.tr( "L'extension {1} est prete pour les histogrammes de {0}").\
#        format( PHYSIOCAP_UNI, self.tr("Traitement")), TRACE_TOOLS)    

    # Rendre la memoire 
    x,y,nbsarm,diam,biom,date_capture,vitesse= [],[],[],[],[],[],[]
    azimuth, nbsart =  [],[]
    altitude,  pdop,  distance,  derive =  [],[],[],[]
    nbsarmm2,nbsarcep,biommm2,biomgm2,biomgcep=[],[],[],[],[]

    return 0
    
# Fonction pour vérifier le fichier csv de concatenation (projet_RAW.csv)   
def physiocap_assert_csv(self, src, err):
    """Fonction d'assert. 
    Vérifie si le csv de concatenation des MID est au bon format: 
    58 virgules
    une date en première colonne
    des float ensuite
    """
    #leModeDeTrace = self.fieldComboModeTrace.currentText()
    numero_ligne = 0     
    nombre_erreurs = 0     
    while True :
        ligne = src.readline() # lit les lignes 1 à 1
        if not ligne: break 
        # Vérifier si ligne OK
        numero_ligne = numero_ligne + 1
        #physiocap_log( "Assert CVS ligne lue %d" % (numero_ligne), leModeDeTrace)

        result = ligne.split(",") # split en fonction des virgules        
        # Vérifier si le champ date a bien deux - et 2 deux points
        tirets = result[ 0].count("-") 
        deux_points = result[ 0].count(":") 
        #physiocap_log( "Champ date contient %d tirets et %d deux points" % (tirets, deux_points), leModeDeTrace)
        if ((tirets != 2) or (deux_points != 2)):
            aMsg = "La ligne numéro %d ne commence pas par une date" % (numero_ligne)
            nombre_erreurs = nombre_erreurs + 1
            if nombre_erreurs < 10:
                physiocap_error( self, aMsg )
            err.write( aMsg + '\n' ) # on écrit la ligne dans le fichier ERREUR
            
            continue # on a tracé erreur et on saute la ligne         

        # Vérifier si tous les champs sont des float        
        i = 0
        for x in result[1:58]:
            i = i+1
            try:
                y = float( x)
                # pour usage
                y = y + 1
                #physiocap_log( "%d Champ  %s est de type %s" % (i, x, type( y)), leModeDeTrace)
            except:
                aMsg = "La ligne brute numéro %d a des colonnes mal formatées (x.zzz attendu)" % (numero_ligne)
                nombre_erreurs = nombre_erreurs + 1
                if nombre_erreurs < 10:
                    physiocap_error( self, aMsg )
                    err.write( aMsg + "\n") # on écrit la ligne dans le fichier ERREUR
                break # on a tracé une erreur et on saute la ligne            

        comptage = ligne.count(",") # compte le nombre de virgules
        if comptage > NB_VIRGULES:
            # Assert Trouver les lignes de données invalides ( sans 58 virgules ... etc)
            aMsg = "La ligne brute numéro %d n'a pas %s virgules" % (numero_ligne, NB_VIRGULES)
            nombre_erreurs = nombre_erreurs + 1
            if nombre_erreurs < 10:
                physiocap_error( self, aMsg )
            err.write( aMsg + '\n') # on écrit la ligne dans le fichier ERREUR
            continue # on a tracé erreur et on saute la ligne


    # Au bilan
    if (numero_ligne != 0):
        #physiocap_log( "Assert CVS a lu %d lignes et trouvé %d erreurs" % \
        #    (numero_ligne, nombre_erreurs ), leModeDeTrace)
        pourcentage_erreurs = float( nombre_erreurs * 100 / numero_ligne)
        return pourcentage_erreurs
    else:
        return 0
          
# Fonction pour créer les fichiers histogrammes    
def physiocap_fichier_histo( self, src, histo_diametre, histo_nbsarment, err):
    """Fonction de traitement. Creation des fichiers pour réaliser les histogrammes
    Lit et traite ligne brute par ligne brute le fichier source (src).
    Les résultats est écrit au fur et à mesure dans histo_diametre ou histo_nbsarment
    Il se fait un filtre des diam qui ne sont pas entre 2 et 28
    """
   
    numero_ligne = 0     
    while True :
        ligne = src.readline() # lit les lignes 1 à 1
        if not ligne: break 
        # Vérifier si ligne OK
        numero_ligne = numero_ligne + 1
        comptage = ligne.count(",") # compte le nombre de virgules
        if comptage != NB_VIRGULES:
            # Assert ligne sans 58 virgules 
            continue # on saute la ligne
        
        result = ligne.split(",") # split en fonction des virgules
        # Intégrer ici les autres cas d'erreurs
                
        try : # accompli cette fonction si pas d'erreur sinon except
            XY = [float(x) for x in result[1:9]]   # on extrait les XY et on les transforme en float  > Données GPS 
            diams = [float(x) for x in result[9:NB_VIRGULES+1]] # on extrait les diams et on les transforme en float 
            diamsF = [i for i in diams if i > 2 and i < 28 ] # on filtre les diams > diamsF correspond aux diams filtrés entre 2 et 28       
            if comptage==NB_VIRGULES and len(diamsF)>0 : # si le nombre de diamètre après filtrage != 0 alors mesures
                if XY[7] != 0:
                    nbsarm = len(diamsF)/(XY[7]*1000/3600) #8eme donnée du GPS est la vitesse. Dernier terme : distance entre les sarments
                else:
                    nbsarm = 0
                histo_nbsarment.write("%f%s" %(nbsarm,";"))                
                for n in range(len(diamsF)) :
                    histo_diametre.write("%f%s" %(diamsF[n],";"))
        except : # accompli cette fonction si erreur
            msg = "%s%s\n" %("Erreur histo",ligne)
            physiocap_error( self, msg )
            # A_TESTER : sans str
            err.write( str( msg) ) # on écrit la ligne dans le fichier ERREUR
            pass # on mange l'exception

def physiocap_tracer_histo(src, name, min=0, max =28, labelx = "Lab X", labely = "Lab Y", titre = "Titre", bins = 100):
    """Fonction de traitement.
    Lit et traite ligne brute par ligne brute le fichier source (src).
    Le résultat est écrit au fur et à mesure dans le
    fichier destination (dst). 
    """
    ligne2 = src.readline()
    histo = ligne2.split(";") # split en fonction des virgules
    # Assert len(histo)
    XY = [float(x) for x in histo[0:-1]]   # on extrait les XY et on les transforme en float  
    #nb_valeur = len(XY)
    #physiocap_log( "Histo min %d et nombre de valeurs : %d " % (min, nb_valeur), TRACE_TOOLS)
    classes = np.linspace(min, max, max+1)
    plt.hist(XY,bins=classes,normed=1, facecolor='green', alpha=0.75) 
    plt.xlabel(labelx)
    plt.ylabel(labely)
    plt.title(titre)
    plt.xlim((min, max))
    plt.grid(True)
    plt.savefig(name)
    plt.show( block = 'false')
    plt.close()
    

# Fonction de filtrage et traitement des données
def physiocap_filtrer(self,  src, csv_sans_0, csv_avec_0, csv_0_seul,
    nom_shape_segment,  nom_prj_segment, nom_shape_segment_details, nom_prj_segment_details,
    diametre_filtre, nom_fichier_synthese, err, 
    mindiam, maxdiam, max_sarments_metre, 
    segment_mini_vitesse,  segment_mini_point, segment_max_pdop, 
    segment_max_derive,  segment_pas_de_derive, 
    details, eer, eec, d, hv,
    laProjectionCRS, laProjectionTXT, 
    version_3 = "NO" ):
    """Fonction de traitement.
    Filtre ligne brute par ligne brute les données de source (src) pour les valeurs 
    comprises entre mindiam et maxdiam et verifie si on n'a pas atteint le max_sarments_metre.
    Le résultat est écrit au fur et à mesure dans les fichiers 
    csv_sans_0, csv_avec_0 et depuis v3 dans csv_0_seul mais aussi diametre_filtre 
    La synthese est allongé
    "details" pilote l'ecriture de 5 parametres ou de la totalité des 10 parametres 
    """
    leModeDeTrace = self.fieldComboModeTrace.currentText()    
    # S'il n'existe pas de données parcellaire, le script travaille avec les données brutes
    titre = ""
    titre_partie_details = " ; NBSARMM2 ; NBSARCEP ; BIOMMM2 ; BIOMGM2 ; BIOMGCEP "
    if version_3 == "NO":
        titre_sans_detail = "X ; Y ; XL93 ; YL93 ; NBSARM ; DIAM ; BIOM ; DATE ; VITESSE"
    else: # Ajout en version 3 de l'altitude 
        titre_sans_detail = "ID;X ; Y ; XL93 ; YL93 ; ALTITUDE; PDOP ; DISTANCE; DERIVE; AZIMUTH; NBSART; NBSARM ; DIAM ; BIOM ; DATE ; VITESSE"
        
    if details == "NO" :
        titre = titre_sans_detail
    else:
        # Assert details == "YES"
        if details != "YES" : 
            return physiocap_error( self, self.tr("Problème majeur dans le choix du détail du parcellaire"))
        #S'il existe des données parcellaire, le script travaille avec les données brutes et les données calculées
        titre = titre_sans_detail + titre_partie_details
    
    # Ecriture de l'entete pour tous les cas
    csv_sans_0.write("{0}\n".format( titre)) 
    csv_avec_0.write("{0}\n".format( titre))
    csv_0_seul.write("{0}\n".format( titre))

    # Pour progress bar entre 15 et 40
    lignes_brutes = src.readlines()
    max_lignes = len( lignes_brutes)
    progress_step = int( max_lignes / 25)
    #physiocap_log("Bar step: " + str( progress_step), leModeDeTrace)
    progress_bar = 15
    barre = 1
    precedent = []
    on_coupe = "PREMIER"
    segment_en_cours = []
    gid_en_cours = []
    gid_sans_mesure = []
    manquant_en_cours = []                   
    info_en_cours = {}    
    derive_en_cours = [] 
    mes_lignes_sans_coupure = []
    info_lignes_sans_coupure = []
    nombre_segments_sans_coupure = 0

    # Recuperer le CRS choisi, les extensions et le calculateur de distance
    distancearea, EXT_CRS_SHP, EXT_CRS_PRJ, EXT_CRS_RASTER, \
    laProjectionCRS, laProjectionTXT, EPSG_NUMBER = \
            physiocap_quelle_projection_demandee( self)

    
    for numero_point, ligne_brute in enumerate( lignes_brutes):
        if not ligne_brute: break 
        
        # Progress BAR de 15 à 40 %
        if ( numero_point > barre * progress_step):
            progress_bar = progress_bar + 1
            barre = barre + 1
            self.progressBar.setValue( progress_bar)  
                
        comptage = ligne_brute.count(",") # compte le nombre de virgules
        result = ligne_brute.split(",") # split en fonction des virgules
        
        try :  # Transform GPS en L93
            # on extrait les Colonnnes 1 à 8 (XY, puis GPS jusqu'à vitesse)
            # en on les transforme en float  
            ### On utilise XY[0 et 1] puis Altitude XY[2] Pdop XY[5] et vitesse XY[7] 
            XY = [float(x) for x in result[1:9]]     
            
            # Puis on transforme les WGS84 (du capteur) en L93 (certainement utile)
            crsDest = QgsCoordinateReferenceSystem.fromEpsgId( EPSG_NUMBER_L93)   # Lambert 93
            crsSrc = QgsCoordinateReferenceSystem.fromEpsgId( EPSG_NUMBER_GPS)  # WGS 84
            transformer = QgsCoordinateTransform()
            transformer.setSourceCrs( crsSrc)
            transformer.setDestinationCrs( crsDest)
            if not transformer.isValid():
                aMsg = "Erreur bloquante durant transformation GPS vers L93 ligne numéro %d" %( numero_point)
                physiocap_error( self, aMsg )
                err.write( aMsg) # on écrit la ligne dans le fichier ERREUR
                # TODO: monter une exception
                break
            
            # On assure la tranformation par compatibilité du CVS en GPS et L93
            # TODO d'autre EPSG ?
            point_L93 = transformer.transform( QgsPointXY( XY[0],XY[1]))
            XY_L93 = [ point_L93.x(), point_L93.y() ]
            # aMsg = "Transformation faite X {0} et Y {1}". \
            #           format( XY_L93[0], XY_L93[1])            
            # physiocap_log( aMsg , leModeDeTrace)
            # physiocap_log( "La projection {0}". format( laProjectionTXT), leModeDeTrace)
            if ( laProjectionTXT == "GPS"):
                le_point_projete = QgsPointXY( XY[0],XY[1])
            else: # Pour le moment seulement L93
                le_point_projete = QgsPointXY( XY_L93[0],XY_L93[1])
            XY_projete = [ le_point_projete.x(), le_point_projete.y() ]

        except :
            aMsg = "{0} Erreur bloquante durant tranformation CRS : pour la ligne brute numéro {1}". \
                format ( PHYSIOCAP_STOP,  numero_point)
            physiocap_error( self, aMsg )
            err.write( aMsg) # on écrit la ligne dans le fichier ERREUR
            # monter directemenr exception
            raise

        # TODO: envisager de marquer les points à conserver (non filtré et dans un segment)
        # pour creer un 4eme csv POINTS_VALIDES
        # ce qui est complique pour les segments courts que je ne connais pas encore
        
        try:  # SEGMENT si V3
            # On regarde les points sans mesure avant SEGMENT
            diams = [float(x) for x in result[9:NB_VIRGULES+1]] # on extrait les diams et on les transforme en float 
            diamsF = [i for i in diams if i > mindiam and i < maxdiam ] # on filtre les diams avec les paramètres entrés ci-dessus
            derive = 0.0
            ma_distance = 0.0
            mon_azimuth = 0.0
            # SEGMENT si V3
            if version_3 == "NO":
                pass
            elif precedent == [] or on_coupe == "PREMIER":
                #physiocap_log( "SEGMENT ==>> point {0} PREMIER".format( numero_point), TRACE_SEGMENT + "_DEBUG")
                # Stocker le premier point pour comparer au prochain tour    
                # et la Date début
                precedent = XY_projete    
                # TODO: Mettre en Z la dérive
                info_en_cours[ DATE_DEBUT] = result[0]
                if len(diamsF) == 0:
                    # On ne STOCKE pas les points sans MESURE 
                    gid_sans_mesure.append( numero_point)
                else:
                    gid_en_cours.append( numero_point)
                derive_en_cours.append( 0)
                segment_en_cours.append( QgsPointXY( le_point_projete))
                on_coupe = "NON"
            else:            
                # On vérifie qualité de mesure
                # ################################################
                # Filtre des points pour découpage en SEGMENT ou 
                # pour montrer les limites de la capture 
                # On cherche si le point est dans la zone attendue
                # calcul basé sur la vitesse annoncé par GPS sur 
                # le point en cours et PDOP
                # #################################################

                # Quand vitesse 2.5 et plus et pdop reste cohérent segment_max_pdop
                if XY[7] >= segment_mini_vitesse and XY[5] < segment_max_pdop:
                    # on est en vitesse de croisière                        
                    # Calcul de la distance théorique par rapport au precedent
                    # Introduire un calcul de distance length et l'azimuth
                    le_point_precedent = QgsPointXY( precedent[0] ,  precedent[1])
                    ma_distance = distancearea.measureLine( le_point_projete, le_point_precedent)
                    mon_azimuth = le_point_projete.azimuth( le_point_precedent)
                    # TODO JHJHJH Traiter l'azimuth depuis le début du segment
                    
                    distance_theorique = XY[7]*1000/3600 # On suppose une seconde d'avancement
                    derive = ( ma_distance - distance_theorique) / distance_theorique *100
#                    physiocap_log( "Vitesse {3} Distance théorique {1:.2f} et ma distance {0:.2f}  \
#                        sont distantes de \n  {2:.1f} soit une derive de {4:.1f}".\
#                            format(ma_distance,  distance_theorique, \
#                            ( ma_distance - distance_theorique),  XY[7],  derive ), \
#                            TRACE_SEGMENT)
                    #remplacer le precedent par l'actuel
                    precedent = XY_projete    
                    
                    # Vérification de dérive
                    if abs( derive) > (segment_max_derive + (2 * segment_pas_de_derive)):
                        physiocap_log( "{0} DECOUPAGE point {1} : l'avancée dérive GRAVE ===> {2:.1f} ! ".\
                            format(PHYSIOCAP_WARNING,   numero_point,   derive ), \
                            TRACE_SEGMENT_DECOUPES)
                        on_coupe = "OUI"
                    elif abs( derive) > (segment_max_derive + segment_pas_de_derive ):
                        physiocap_log( "{0} DECOUPAGE point {1} : l'avancée dérive de PLUS d'un PAS ==> {2:.1f} ! ".\
                            format(PHYSIOCAP_WARNING,   numero_point,   derive ), \
                            TRACE_SEGMENT_DECOUPES)
                        on_coupe = "OUI"
                    elif abs( derive) > segment_max_derive:
                        physiocap_log("{0} DECOUPAGE point {1} : l'avancée dérive => {2:.1f} ! ".\
                            format(PHYSIOCAP_WARNING,   numero_point,   derive ), \
                            TRACE_SEGMENT_DECOUPES)
                        on_coupe = "OUI"
                    else:                          
                        # La derive < segment_max_derive en % :
                        # Stocker ligne "droite" = orientation et sens d'avancement
                        # Créer un flux des avancement stables pour identifier l'écartement problable
                        # Ajouter un point à la ligne
                        segment_en_cours.append( QgsPointXY( le_point_projete))
                        info_en_cours[ DATE_FIN] = result[0]
                        if len(diamsF) == 0:
                            # On ne STOCKE pas les points sans MESURE 
                            gid_sans_mesure.append( numero_point)
                        else:
                            gid_en_cours.append( numero_point)
                        derive_en_cours.append( derive)
                        on_coupe = "NON"
                            
                else: # Cas d'arret (fin de rang) ou pdop
                    on_coupe = "OUI"
                    # Tracer cas decoupe vitessse
                    if XY[7] < segment_mini_vitesse:
                        if  len(segment_en_cours) > 0:
                            physiocap_log("{0} DECOUPAGE point {1} : vitesse {2:.1f} min est  {3:.1f}! ".\
                            format(PHYSIOCAP_WARNING, numero_point, XY[7],  segment_mini_vitesse), \
                            TRACE_SEGMENT_DECOUPES)                           
                    # Tracer cas decoupe pdop
                    if XY[5] >= segment_max_pdop:
                        physiocap_log("{0} DECOUPAGE point {1} : pdop {2:.1f} max est  {3:.1f}! ".\
                            format(PHYSIOCAP_WARNING, numero_point, XY[5], segment_max_pdop ), \
                            TRACE_SEGMENT_DECOUPES)  
       
                if on_coupe == "OUI": # Cas de fin de ligne
                    if  len(segment_en_cours) > segment_mini_point:
                        # Le segment est à garder
                        manquant_en_cours.append( numero_point)
                        # Mémoriser la ligne des points cohérents                           
                        mes_lignes_sans_coupure.append( segment_en_cours)
                        info_en_cours[ NUM_SEG] = nombre_segments_sans_coupure
                        info_en_cours[ DATE_FIN] = result[0]
                        info_en_cours[ NOMBRE] = len( segment_en_cours)
                        info_en_cours[ GID_GARDE] = gid_en_cours
                        info_en_cours[ GID_SANS_MESURE] = gid_sans_mesure
                        info_en_cours[ GID_TROU] = manquant_en_cours
                        info_en_cours[ DERIVE] = np.mean( derive_en_cours)
                        # stocker jour_heure début et fin et derive moyenne ...
                        info_lignes_sans_coupure.append( info_en_cours)
                        nombre_segments_sans_coupure  = nombre_segments_sans_coupure  + 1                              
                        manquant_en_cours = []

                    else:
                        # TODO: Vérifier les gid_sans_mesure
                        # On ne perd pas les points manquants qui seront ajouter dans GID_TROU pour le segment suivant
                        # On aditionne des gid en cours avec les manquants...
                        for gid_perdu in gid_en_cours:
                            manquant_en_cours.append( gid_perdu)
                        manquant_en_cours.append( numero_point)
                       
                        if  len(segment_en_cours) > 0:
                            physiocap_log("{0} SEGMENT {1} IGNORE : trop cours == {2} points, le mini est {3} ".\
                                format(PHYSIOCAP_WARNING, nombre_segments_sans_coupure, 
                                len(segment_en_cours),  segment_mini_point ),
                                TRACE_SEGMENT_DECOUPES)
                                
                    info_en_cours = {}
                    gid_en_cours = []
                    gid_sans_mesure = []
                    precedent = []
                    on_coupe = "PREMIER"
                    segment_en_cours = []
                        
        except :
            aMsg = "{0} Erreur bloquante durant extraction des segments : pour la ligne brute numéro {1}". \
                format ( PHYSIOCAP_STOP,  numero_point)
            physiocap_error( self, aMsg )
            err.write( aMsg) # on écrit la ligne dans le fichier ERREUR
            # monter directemenr exception
            raise
 
           
        try: # On filtre vraiement           
            if details == "NO" :
                if len(diamsF)==0: # si le nombre de diamètre après filtrage = 0 alors pas de mesures
                    nbsarm = 0
                    nbsart = 0
                    diam =0
                    biom = 0
                    # Ecrire les seuls_0 et aussi les points avec 0
                    if version_3 == "NO":
                        csv_0_seul.write("%.7f%s%.7f%s%.7f%s%.7f%s%i%s%i%s%i%s%s%s%0.2f\n" \
                            %(XY[0],";",XY[1],";",XY_L93[0],";",XY_L93[1],";",nbsarm,";",diam ,";",biom,";",result[0],";",XY[7]))  # on écrit la ligne dans le csv avec ZERO SEUL
                        csv_avec_0.write("%.7f%s%.7f%s%.7f%s%.7f%s%i%s%i%s%i%s%s%s%0.2f\n" \
                            %(XY[0],";",XY[1],";",XY_L93[0],";",XY_L93[1],";",nbsarm,";",diam ,";",biom,";",result[0],";",XY[7]))  # on écrit la ligne dans le fcsv avec ZERO
                    else:   # V3 on ajoute altitude, pdop, distance au point precedent et la dérive
                            # puis AZIMUTH et NBSART = 0
                        a_ecrire = "{0};{1:.7f};{2:.7f};{3:.7f};{4:.7f}; \
                                    {5:.2f};{6:.2f};{7:.2f};{8:.2f};{9:.2f};0;0;0;0;{10};{11:.7f}\n". \
                                format(numero_point, XY[0],XY[1],XY_L93[0],XY_L93[1], \
                                    XY[2],XY[5],ma_distance,derive,mon_azimuth,       result[0],XY[7])
                        csv_0_seul.write( a_ecrire)  
                        csv_avec_0.write( a_ecrire)
                        
                elif comptage==NB_VIRGULES and len(diamsF)>0 : # si le nombre de diamètre après filtrage != 0 alors mesures
                    # Nombre sarment total 
                    nbsart  = len(diamsF)
                    if XY[7] != 0: # Si vitesse non nulle
                        nbsarm = len(diamsF)/(XY[7]*1000/3600)
                    else:
                        nbsarm = 0
                    if nbsarm > 1 and nbsarm < max_sarments_metre :                   
                        diam =sum(diamsF)/len(diamsF)
                        biom = 3.1416*(diam/2)*(diam/2)*nbsarm
                        if version_3 == "NO":
                            csv_avec_0.write("%.7f%s%.7f%s%.7f%s%.7f%s%0.2f%s%.2f%s%.2f%s%s%s%0.2f\n" \
                                %(XY[0],";",XY[1],";",XY_L93[0],";",XY_L93[1],";",nbsarm,";",diam,";",biom,";",result[0],";",XY[7])) # on écrit la ligne dans le csv avec ZERO
                            csv_sans_0.write("%.7f%s%.7f%s%.7f%s%.7f%s%0.2f%s%.2f%s%.2f%s%s%s%0.2f\n" \
                                %(XY[0],";",XY[1],";",XY_L93[0],";",XY_L93[1],";",nbsarm,";",diam,";",biom,";",result[0],";",XY[7])) # on écrit la ligne dans le csv sans ZERO
                        else: # V3 on ajoute altitude, pdop,distance au point precedent et risque de dérive
                              # puis AZIMUTH et NBSART
                            a_ecrire = "{0};{1:.7f};{2:.7f};{3:.7f};{4:.7f}; \
                                {5:.2f};{6:.2f};{7:.2f};{8:.2f};{9:.2f};{10}; \
                                {11:.2f}; {12:.2f};{13:.2f};{14};{15:.7f}\n". \
                                format( numero_point, XY[0],  XY[1], XY_L93[0] ,XY_L93[1], \
                                    XY[2],XY[5],ma_distance,derive,mon_azimuth,nbsart, \
                                    nbsarm,diam,biom,result[0],XY[7])
                            csv_avec_0.write( a_ecrire) 
                            csv_sans_0.write(a_ecrire)   
    
                        for n in range(len(diamsF)) :
                            diametre_filtre.write("%f%s" %(diamsF[n],";"))
            elif details == "YES" :
                if len(diamsF)==0: # si le nombre de diamètre après filtrage = 0 alors pas de mesures
                    nbsart = 0
                    nbsarm = 0
                    diam =0
                    biom = 0
                    nbsarmm2 = 0
                    nbsarcep = 0
                    biommm2 = 0
                    biomgm2 = 0
                    biomgcep = 0
                    if version_3 == "NO":
                        csv_0_seul.write("%.7f%s%.7f%s%.7f%s%.7f%s%i%s%i%s%i%s%s%s%0.2f%s%i%s%i%s%i%s%i%s%i\n" \
                        %(XY[0],";",XY[1],";",XY_L93[0],";",XY_L93[1],";",nbsarm,";",diam ,";",biom,";",result[0],";",XY[7],";",nbsarmm2,";",nbsarcep,";",biommm2,";",biomgm2,";",biomgcep))  
                        csv_avec_0.write("%.7f%s%.7f%s%.7f%s%.7f%s%i%s%i%s%i%s%s%s%0.2f%s%i%s%i%s%i%s%i%s%i\n" \
                        %(XY[0],";",XY[1],";",XY_L93[0],";",XY_L93[1],";",nbsarm,";",diam ,";",biom,";",result[0],";",XY[7],";",nbsarmm2,";",nbsarcep,";",biommm2,";",biomgm2,";",biomgcep)) 
                    else: # Q3 on ajoute altitude, pdop, distance au point precedent et la dérive
                            # puis AZIMUTH et NBSART = 0
                        a_ecrire = "{0};{1:.7f};{2:.7f};{3:.7f};{4:.7f}; \
                                    {5:.2f};{6:.2f};{7:.2f};{8:.2f};{9:.2f};0;0;0;0;{10};{11:.7f}". \
                                format(numero_point, XY[0],XY[1],XY_L93[0],XY_L93[1], 
                                    XY[2],XY[5],ma_distance,derive,mon_azimuth,       result[0],XY[7])
                        a_ecrire_detail = ";0;0;0;0;0\n"                     
                        a_ecrire_complet = a_ecrire + a_ecrire_detail
                        csv_0_seul.write( a_ecrire_complet)  
                        csv_avec_0.write(a_ecrire_complet)
                        
                elif comptage==NB_VIRGULES and len(diamsF)>0 : # si le nombre de diamètre après filtrage != 0 alors mesures
                    nbsart  = len(diamsF)
                    if XY[7] != 0:
                        nbsarm = len(diamsF)/(XY[7]*1000/3600)
                    else:
                        nbsarm = 0
                    if nbsarm > 1 and nbsarm < max_sarments_metre :                   
                        diam =sum(diamsF)/len(diamsF)
                        biom=3.1416*(diam/2)*(diam/2)*nbsarm
                        nbsarmm2 = nbsarm/eer*100
                        nbsarcep = nbsarm*eec/100
                        biommm2 = biom/eer*100
                        biomgm2 = biom*d*hv/eer
                        biomgcep = biom*d*hv*eec/100/100
                        if version_3 == "NO":
                            csv_avec_0.write("%.7f%s%.7f%s%.7f%s%.7f%s%.2f%s%.2f%s%.2f%s%s%s%.2f%s%.2f%s%.2f%s%.2f%s%.2f%s%.2f\n" \
                            %(XY[0],";",XY[1],";",XY_L93[0],";",XY_L93[1],";",nbsarm,";",diam ,";",biom,";",result[0],";",XY[7],";",nbsarmm2,";",nbsarcep,";",biommm2,";",biomgm2,";",biomgcep))
                            csv_sans_0.write("%.7f%s%.7f%s%.7f%s%.7f%s%.2f%s%.2f%s%.2f%s%s%s%.2f%s%.2f%s%.2f%s%.2f%s%.2f%s%.2f\n" \
                            %(XY[0],";",XY[1],";",XY_L93[0],";",XY_L93[1],";",nbsarm,";",diam ,";",biom,";",result[0],";",XY[7],";",nbsarmm2,";",nbsarcep,";",biommm2,";",biomgm2,";",biomgcep)) 
                        else: # Q3 on ajoute altitude, pdop,distance au point precedent et risque de dérive
                              # puis AZIMUTH et NBSART
                            a_ecrire = "{0};{1:.7f};{2:.7f};{3:.7f};{4:.7f}; \
                                {5:.2f};{6:.2f};{7:.2f};{8:.2f};{9:.2f};{10}; \
                                {11:.2f}; {12:.2f};{13:.2f};{14};{15:.7f}". \
                                format( numero_point, XY[0],  XY[1], XY_L93[0] ,XY_L93[1],
                                    XY[2],XY[5],ma_distance,derive,mon_azimuth,nbsart,
                                    nbsarm,diam,biom,result[0],XY[7])
                            a_ecrire_detail = ";{0:.7f};{1:.7f};{2:.7f};{3:.7f};{4:.7f}\n". \
                                format( nbsarmm2, nbsarcep,biommm2,biomgm2,biomgcep)
                            a_ecrire_complet = a_ecrire + a_ecrire_detail
                            csv_avec_0.write( a_ecrire_complet) 
                            csv_sans_0.write(a_ecrire_complet) 

                        # Memorise diametre filtré pour histo
                        for n in range(len(diamsF)) :
                            diametre_filtre.write("%f%s" %(diamsF[n],";"))

        except :
            aMsg = "{0} Erreur bloquante durant filtrage : pour la ligne brute numéro {1}". \
                format ( PHYSIOCAP_STOP,  numero_point)
            physiocap_error( self, aMsg )
            err.write( aMsg) # on écrit la ligne dans le fichier ERREUR
            # Pour monter directement exception 
            raise
            return -1 # ce retour est géré comme une exception

    if version_3 == "NO":
        pass
    else:
        if len( info_lignes_sans_coupure) != nombre_segments_sans_coupure:
            physiocap_error( self, "{0} on a trouvé {1} segments et {2} infos". \
            format( PHYSIOCAP_INFO,  nombre_segments_sans_coupure, len( info_lignes_sans_coupure)))
            raise physiocap_exception_calcul_segment_invalid( "Segment et leurs infos sont différents")
        i=0
        for info_segment in info_lignes_sans_coupure:
            i=i+1
            try:
                physiocap_log( "{0} Segment {1} contient {2} points et une dérive moyenne de {3:.1f}". \
                    format( PHYSIOCAP_INFO,  i,  info_segment[NOMBRE],  info_segment[DERIVE]),  TRACE_SEGMENT)
                physiocap_log( "gid des points :{0} \net les sans mesure\n{1}". \
                    format(info_segment[GID_GARDE],  info_segment[GID_SANS_MESURE]), TRACE_SEGMENT)
            except:
                physiocap_error( self, "Problème : manque attribut dans info segment")
                raise physiocap_exception_calcul_segment_invalid( "Un  attribut n'est pas présent")
#            try:
#                physiocap_log( "Date début {0} et fin {1}". \
#                format( info_segment[DATE_DEBUT], info_segment[DATE_FIN]), 
#                TRACE_SEGMENT)  
#            except:
#                physiocap_error( self, "Problème : pas de date dans le segment")
#                raise physiocap_exception_calcul_segment_invalid( "Date non présente")
                
        # Creer les lignes simplifiés ou brisés de ces segments et infos
        # A_TESTER: passer L93 ou GPS
        physiocap_segment_vers_shapefile( self, nom_shape_segment,  nom_prj_segment, 
            mes_lignes_sans_coupure,  info_lignes_sans_coupure, 
            laProjectionCRS, laProjectionTXT)
        physiocap_segment_vers_shapefile( self, nom_shape_segment_details, nom_prj_segment_details,
            mes_lignes_sans_coupure,  info_lignes_sans_coupure, 
            laProjectionCRS, laProjectionTXT, "BRISE")
            
    physiocap_log( "{0} {1} Fin du filtrage OK des {2} lignes.". \
        format( PHYSIOCAP_INFO, PHYSIOCAP_UNI, str(numero_point - 1)), leModeDeTrace)
    return 0


