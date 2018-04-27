# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Physiocap_tools
                                 A QGIS 3 plugin
 Physiocap3 plugin helps analyse raw data from Physiocap in QGIS 3 and 
 creates a synthesis of Physiocap measures' campaign
 Physiocap3 plugin permet l'analyse les données brutes de Physiocap dans QGIS 3 et
 crée une synthese d'une campagne de mesures Physiocap
 
 Le module tools contient les utilitaires
 Les fonctions sont nommées en Anglais 
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
 *- Plugin builder et QGIS 3 API et à ce titre porte aussi la licence GNU    *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *   http://www.gnu.org/licenses/gpl-2.0.html                              *
 *                                                                         *
***************************************************************************/
"""
from .Physiocap_var_exception import *

from PyQt5 import QtWidgets
from qgis.core import (Qgis, QgsDistanceArea, QgsProject, QgsMessageLog, \
    QgsMapLayer, QgsCoordinateReferenceSystem)
from PyQt5.QtWidgets import QMessageBox  

# Pour les traces de Tools
leModeTrace = TRACE_TOOLS


# MESSAGES & LOG
def physiocap_message_box( self, text, level="warning"):
    """Send a message box by default Warning"""
    title = self.tr( "{0} Physiocap").\
        format( PHYSIOCAP_UNI)
    if level == "about":
        QMessageBox.about( self, title, text)
    elif level == "information":
        QMessageBox.information( self, title, text)
    elif level == "error":
        QMessageBox.error( self, title, text)
    else:
        #QMessageBox.warning( self, title, text)
        QMessageBox.information( self, title, text)

def physiocap_question_box( self, text= "Etes-vous sûr(e)? Are you sure ?"):
    """Send a question box """
    title = self.tr( "{0} Physiocap").\
        format( PHYSIOCAP_UNI)
    reply = QMessageBox.question(self, title, text,
            QMessageBox.Yes|QMessageBox.Cancel)
    if reply == QMessageBox.Cancel:
        return False
    if reply == QMessageBox.Yes:
        return True
    return False

def physiocap_log_for_error( dialogue):
    """ Renvoi un message dans la log Infomation pour pointer l'utilisateur 
    vers la log des erreurs
    Call Class Tools For translation"""
    toolsObject = PhysiocapTools( dialogue)
    toolsObject.physiocap_tools_log_for_error()

def physiocap_log( aText, modeTrace = TRACE_PAS,  level = "INFO"):
    """Send a text to the Physiocap log
    Ce module encapsaule QgsMessageLog en choississant le mode
    de trace et le niveau de message
    Il permet de supprimer les traces détaillées en Prodcution"""
    journal_nom = "{0} Informations".\
        format( PHYSIOCAP_UNI)
    if modeTrace == TRACE_PAS:
        #QgsMessageLog.logMessage( "Pas de trace : " + aText,  journal_nom, Qgis.Info)
        pass
    elif modeTrace == TRACE_MINI:
        # On monte warning et message debut et fin
#        if level == "WARNING" or level == Qgis.Warning :
#            QgsMessageLog.logMessage( aText, journal_nom, Qgis.Warning)
        if level == "WARNING" or level == Qgis.Warning :
            QgsMessageLog.logMessage( aText, journal_nom, Qgis.Warning)
        elif (len( aText) >2):
            if ( aText[0:2] in ( PHYSIOCAP_2_ETOILES, PHYSIOCAP_2_EGALS)) or \
               ( aText[0:3] == PHYSIOCAP_INFO + " " + PHYSIOCAP_UNI):
                QgsMessageLog.logMessage( aText, journal_nom, Qgis.Info)
    else:
        if level == "WARNING" or level == Qgis.Warning :
            QgsMessageLog.logMessage( aText, journal_nom, Qgis.Warning)
        elif modeTrace != TRACE_TOUT:
            # Journal spécifique (TOOLS ou SEGMENT ou INTRA) et de niveau INFO
            if LE_MODE_PROD == "YES":
                pass
            else:
                if modeTrace in ["OGR"]:
                    journal_nom = modeTrace
                else:
                    journal_nom = "{0} {1}".format( PHYSIOCAP_UNI, modeTrace)
                QgsMessageLog.logMessage( aText, journal_nom, Qgis.Info)
        else:
            # Cas général
            QgsMessageLog.logMessage( aText, journal_nom, Qgis.Info)
           
def physiocap_error( self, aText, level ="WARNING"):
    """Send a text to the Physiocap error
    Call Class Tools For translation"""
    toolsObject = PhysiocapTools( self)
    toolsObject.physiocap_tools_log_error( aText, level)
    return -1      

def physiocap_write_in_synthese( self, aText):
    """Write a text in the results list"""
    self.textEditSynthese.insertPlainText( aText)   
    
def physiocap_is_int_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
 
def physiocap_create_projection_file( prj_name,  laProjection):
    """Creer le fichier de projection du layer avec la description de EPSG"""

    prj = open(prj_name, "w")
    epsg = 'inconnu'
    if ( laProjection == PROJECTION_L93) or ( laProjection == EPSG_NUMBER_L93):
        epsg = EPSG_DESCRIPTION_L93
    if ( laProjection == PROJECTION_GPS) or ( laProjection == EPSG_NUMBER_GPS):
        epsg = EPSG_DESCRIPTION_GPS
        
    prj.write(epsg)
    prj.close()
    return
    
def  physiocap_PHY_nom_entite_sans_cote( un_nom,  mon_unique = 0):
    """Change la chaine un_nom selon qu'elle contient ou non le caractère '
    peut creer aussi un champ unique"""
    ## Peut ne rien faire
    return un_nom.replace(" ","")
    #return un_nom
#    if un_nom.find('\'') < 0:
#        return un_nom
#    elif mon_unique == 0:
#        return un_nom.replace("\'", "")
#    else:
#        # on veut un nom unique
#        return PHYSIOCAP_UNI + SEPARATEUR_+ un_nom.replace("\'", "") + SEPARATEUR_ + str( unique)
     
def  physiocap_nom_entite_avec_pb_caractere( un_nom, un_texte = "GDAL"):
    """rend True si la chaine un_nom contient un caractère ' problematique pour la librairie : un_texte"""
    if un_texte == "GDAL":
        # Tester si une cote '
        if un_nom.find('\'') >= 0:
            return True
    # fin c'est OK on a rien trouvé
    return False
    
       
def physiocap_get_layer_by_URI( layerURI ):
    """Rend le layer affiché dans le projet 
    qui répond à l'URI layerURI"""
    root = QgsProject.instance().layerTreeRoot()
    ids = root.findLayerIds()              
    trouve = "NO"
    layer = None
    physiocap_log( "Recherche {0}".format( layerURI), leModeTrace)
    # BUG 7 melange des / et \ en V3. On repasse tout en "/"
    layerURI_nettoye = layerURI.replace("\\", "/")
    physiocap_log( "Modifié>> {0}".format( layerURI_nettoye), leModeTrace)
    for layerID in ids:
        # Retrouver le layer
        layer = root.findLayer( layerID).layer()
        URI_complet = layer.dataProvider().dataSourceUri()
        # Attention il faut enlever la mention |layerid à la fin de l'URI
        pos_fin_layer = URI_complet.rfind( "|layerid=")
        URI_vecteur = URI_complet[:pos_fin_layer]
        physiocap_log( "Layer URI {0}".format( URI_vecteur), leModeTrace)
        if layer is not None and layer.type() == QgsMapLayer.VectorLayer and \
            (URI_vecteur == layerURI_nettoye or URI_vecteur == layerURI):
            trouve = "YES"
            #physiocap_log( "Layer retrouvé  {0}".format( layer.name()), leModeTrace)
            # The layer is found
            break
    if ( trouve == "YES"):
        if layer.isValid():
            return layer
        else:
            return None
    else:
        return None


def physiocap_get_layer_by_name( layerName ):
    """Rend le layer affiché dans le projet  
    qui est affiché sous le nom layerName"""
    root = QgsProject.instance().layerTreeRoot()
    ids = root.findLayerIds()        
    trouve = "NO"
    layer = None
    for layerID in ids:
        # Retrouver le layer
        layer = root.findLayer( layerID).layer()
        if layer is not None and layer.type() == QgsMapLayer.VectorLayer and layer.name() == layerName:
            trouve = "YES"
            # The layer is found
            break
    if ( trouve == "YES"):
        if layer.isValid():
            return layer
        else:
            return None
    else:
        return None


def physiocap_get_layer_by_ID( layerID):
    """ Retrouve un layer ID dans la map Tree Root
    Rend le layer si il est valide
    """
    layer_trouve = None
    root = QgsProject.instance().layerTreeRoot()
    ids = root.findLayerIds() #  Inutile : root.findLayers()

    trouve = "NO"
    for id in ids:
        if id == layerID:
            #physiocap_log( "Layer retrouvé : " + str( layerID), leModeTrace)
            layer_trouve = root.findLayer( layerID)
            le_layer = layer_trouve.layer()
            trouve = "YES"
            break
    if ( trouve == "YES"):
        if ( le_layer.isValid()):
            physiocap_log( "OK Layer(Couche) valid(e) : {0}".format ( le_layer.name()), leModeTrace)
            return le_layer
        else:
            physiocap_log( "Layer(Couche) invalid(e) : {0}".format ( le_layer.name()), leModeTrace)
            return None
    else:
        physiocap_log( "No layer (Aucune couche) find for (retrouvée pour) ID : {0}".\
            format( ( str( layerID))), leModeTrace)
        return None

def physiocap_quelle_projection_demandee( self):
    """ Selon la valeur cochée dans le radio de projection 
    positionne laProjection (en QgsCoordinateReferenceSystem, texte et nombre (epsg)
    les extensions EXTENSION_SHP, EXTENSION_PRJ et RASTER selon la demande SAGA
    Rend aussi un QgsDistanceArea pour cet EPSG
    """
    # defaut L93
    mon_EPSG_number = EPSG_NUMBER_L93
    la_projection_TXT = PROJECTION_L93
    if self.radioButtonGPS.isChecked():
        mon_EPSG_number = EPSG_NUMBER_GPS
        la_projection_TXT = PROJECTION_GPS
    if self.radioButtonL93.isChecked():
        mon_EPSG_number = EPSG_NUMBER_L93
        la_projection_TXT = PROJECTION_L93

    la_projection_CRS = QgsCoordinateReferenceSystem.fromEpsgId( mon_EPSG_number)
    # TODO: Récuperer le CRS du projet et le compare au choix
#    laProjection_str = str( la_projection_CRS.postgisSrid())
#    if la_projection_CRS.isValid():
#        physiocap_log("Projection {0} des shapefiles est demandée : {1} est un EPSG valide".\
#            format( la_projection_TXT, laProjection_str), leModeTrace)
        
    EXTENSION_SHP_COMPLET = SEPARATEUR_ + la_projection_TXT + EXTENSION_SHP
    EXTENSION_PRJ_COMPLET = SEPARATEUR_ + la_projection_TXT + EXTENSION_PRJ
   
    # Cas du nom du raster 
    if self.radioButtonSAGA.isChecked():
        EXTENSION_RASTER_COMPLET = SEPARATEUR_ + la_projection_TXT + EXTENSION_RASTER_SAGA
    else:
        EXTENSION_RASTER_COMPLET = SEPARATEUR_ + la_projection_TXT + EXTENSION_RASTER

    # Preparer les calculs de distance et de surface : distanceArea objet
    distanceArea = physiocap_preparer_calcul_distance( self, mon_EPSG_number, la_projection_CRS)

    return  distanceArea, \
    EXTENSION_SHP_COMPLET, EXTENSION_PRJ_COMPLET, EXTENSION_RASTER_COMPLET, \
    la_projection_CRS, la_projection_TXT, mon_EPSG_number


def physiocap_preparer_calcul_distance( self, EPSG_NUMBER, laProjectionCRS):
    """ Selon l'EPSG prépare l'objet distance area
    """
    # pour le calcul des distances
    spheroid = 'inconnu'
    if ( EPSG_NUMBER == EPSG_NUMBER_L93):
        spheroid = SPHEROID_L93    
    if (EPSG_NUMBER == EPSG_NUMBER_GPS):
        spheroid = SPHEROID_GPS    
    distancearea = QgsDistanceArea()
    if laProjectionCRS.isValid():
        physiocap_log( "Calcul de distance Description CRS {0}".\
        format( laProjectionCRS.description()), TRACE_TOOLS)
        physiocap_log( "PROJ.4 CRS {0}".\
        format( laProjectionCRS.toProj4()), TRACE_TOOLS)
    else:
        physiocap_log( "INVALIDE CRS", TRACE_TOOLS)
        return None
        
    distancearea.setSourceCrs( laProjectionCRS, QgsProject.instance().transformContext())            
    distancearea.setEllipsoid( spheroid)
    physiocap_log( "Calcul de distance sous ellipsoide {0}".\
        format( distancearea.ellipsoid()), TRACE_TOOLS)
    return distancearea

##def physiocap_quel_uriname( self):
##    """ Retourne l'uriName attendu """
##    return None
##
##def physiocap_detruit_table_uri( self, uri_deb, laTable):
##    return None
##
##def physiocap_existe_table_uri( self, uri_deb, laTable):
##    return None
##
##def physiocap_tester_uri( self, uriSource, verbose = "NO"):
##    return None
##
##def physiocap_get_uri_by_layer( self, uriName = "INIT" ):
##    return None
##        
def physiocap_rename_existing( chemin):
    """ Retourne le nom qu'il est possible de creer
        si chemin existe deja, on creer un "chemin + [1]"
        si "chemin_projet + [1]" existe déjà, on crée un "chemin_projet + [2]" etc         
    """
    # Exception suffixe
    extension = ""
    pos_extension = -1
    if ( os.path.isfile(chemin)):
        pos_extension = chemin.rfind( ".")
        extension = chemin[ pos_extension:]
        if ( pos_extension != -1):
            chemin = chemin[: pos_extension]
            #physiocap_log("Nouveau chemin" + chemin, leModeTrace)
            
    # Si chemin a déjà une parenthèse dans la 3 derniers caracteres
    longueur = len(chemin)
    if chemin[-1:] == "]":
        # cas du chemin qui a été déjà renommer
        pos = -2
        while chemin[ pos:][0] != "[":
            pos = pos - 1
            if pos == (-1 * longueur): 
                pos = -1
                break
        if pos != (-1):
            # ici la "(" est à pos et la ")" est à -1:
            un_num_parenthese = chemin[ pos+1:]
            un_num = un_num_parenthese[ :-1]
            nouveau_numero = 1
            if physiocap_is_int_number( un_num):
                nouveau_numero = int(un_num) + 1
                nouveau_chemin = chemin[:pos] + "[" +str(nouveau_numero) +"]"
            else:
                # cas d'un nom etrange
                nouveau_chemin = chemin + "[1]"        
        else:
            # cas d'un nom etrange
            nouveau_chemin = chemin + "[1]" 
    else:
        # cas du premier fichier renommer
        nouveau_chemin = chemin + "[1]"

    # Remettre extension
    if (extension != ""):
        nouveau_chemin = nouveau_chemin + extension
               
    return nouveau_chemin


def physiocap_rename_existing_file( chemin):
    """ Retourne le nom de fichier qu'il est possible de creer
        si chemin existe deja, on creer un "chemin + (1)"
        si "chemin_projet + (1)" existe déjà, on crée un "chemin_projet + (2)" etc         
    """
    if ( os.path.exists( chemin)):
        nouveau_chemin = physiocap_rename_existing( chemin)
        return physiocap_rename_existing_file( nouveau_chemin) 
    else:
        #physiocap_log( "Chemin pour la création du fichier ==" + chemin, leModeTrace)
        return chemin

def physiocap_rename_create_dir( chemin):
    """ Retourne le repertoire qu'il est possible de creer
        si chemin existe deja, on creer un "chemin + (1)"
        si "chemin_projet + (1)" existe déjà, on crée un "chemin_projet + (2)" etc         
    """
    if ( os.path.exists( chemin)):
        nouveau_chemin = physiocap_rename_existing( chemin)
        return physiocap_rename_create_dir( nouveau_chemin) 
    else:
        try:
            os.mkdir( chemin)
        except:
            raise physiocap_exception_rep( chemin)
        return chemin


def physiocap_open_file( nom_court, chemin, type_ouverture="w"):
    """ Créer ou detruit et re-crée un fichier"""
    # Fichier des diamètres     
    nom_fichier = os.path.join(chemin, nom_court)
    if ((type_ouverture == "w") and os.path.isfile( nom_fichier)):
        os.remove( nom_fichier)
    try :
        fichier_pret = open(nom_fichier, type_ouverture)
    except :
        raise physiocap_exception_fic( nom_court)
    return nom_fichier, fichier_pret


# Fonction pour vérifier le fichier csv    
def physiocap_look_for_MID( repertoire, recursif, exclusion="fic_sources"):
    """Fonction de recherche des ".MID". 
    Si recursif vaut "Oui", on scrute les sous repertoires à la recheche de MID 
    mais on exclut le repertoire de Exclusion dont on ignore les MID 
    """
    root_base = ""
    MIDs = []
    for root, dirs, files in os.walk( repertoire, topdown=True):
        if root_base == "":
            root_base = root
##        physiocap_log("ALL Root :" + str(root), leModeTrace)
##        physiocap_log("ALL DIR :" + str(dirs), leModeTrace)
##        physiocap_log("ALL FILE :" + str(files), leModeTrace)
        if exclusion in root:
            continue
        for name_file in files:
            if ".MID" in name_file[-4:]:
                MIDs.append( os.path.join( root, name_file))
    return sorted( MIDs)

def physiocap_list_MID( repertoire, MIDs, synthese="xx"):
    """Fonction qui liste les MID.
    En entrée la liste des MIDs avec leurs nom complet
    nom court, taille en ligne, centroide GPS, vitesse moyenne
    sont ajoutés à la synthèse
    """
    resultats = []
    un_MIDs_court = ""
    nom_tiny = ""
    
    for un_mid in MIDs: 
        texte_MID = ""
        if (os.path.isfile( un_mid)):
            fichier_mid = open(un_mid, "r")
            lignes = fichier_mid.readlines()
            if un_mid.find( repertoire) == 0:
                un_MIDs_court = un_mid[ len( repertoire) + 1:]
                le_MID_court = os.path.basename( un_MIDs_court)
                nom_tiny = le_MID_court[0:2]
            gps_x = []
            gps_y = []
            vitesse = []
            for ligne in lignes:
                try:
                    champ = ligne.split( ",")
                    if len(champ) >= 2:
                        gps_x.append( float(champ[ 1]))
                        gps_y.append( float(champ[ 2]))
                    if len(champ) >= 8:
                        vitesse.append( float(champ[ 8]))
                except ValueError:
                    pass
            texte_MID = un_MIDs_court + ";" + nom_tiny + ";" + lignes[0][0:19] + \
                ";" + lignes[-1][10:19]
            if ((len( gps_x) > 0) and (len( gps_y) > 0) ):
                texte_MID = texte_MID + ";" + str( len(gps_x))                  
                if (len( vitesse) > 0 ):
                    texte_MID = texte_MID + ";" + \
                        str(sum(vitesse)/len(vitesse))
                else:
                    texte_MID = texte_MID + ";"
                texte_MID = texte_MID + ";" + \
                    str(sum(gps_x)/len(gps_x))+ ";" +   \
                    str(sum(gps_y)/len(gps_y))

            resultats.append( texte_MID)
            fichier_mid.close()    
    # Mettre dans Synthese
    return resultats

class PhysiocapTools( QtWidgets.QDialog):
    """QGIS Pour voir les messages traduits."""
    def __init__(self, parent=None):
        """Class constructor."""
        super( PhysiocapTools, self).__init__()
        
    def physiocap_tools_log_for_error( self):
        """ Renvoi un message dans la log pour pointer l'utilisateur vers la liste des erreurs"""
        message_log_court = self.tr( "{0} n'a pas correctement fini son analyse").\
            format( PHYSIOCAP_UNI)
        message_log = message_log_court + self.tr( ". Consultez le journal {0} Erreurs").\
            format( PHYSIOCAP_UNI)
        physiocap_log( message_log, TRACE_TOUT,"WARNING")
        self.physiocap_tools_log_error( message_log_court, "Critical" )

    def physiocap_tools_log_error( self, aText, level="WARNING"):
        """Send a text to the Physiocap error"""
        journal_nom = self.tr( "{0} Erreurs").\
            format( PHYSIOCAP_UNI)
        if level == "WARNING":
            QgsMessageLog.logMessage( aText, journal_nom, Qgis.Warning)
        else:
            QgsMessageLog.logMessage( aText, journal_nom, Qgis.Critical)

