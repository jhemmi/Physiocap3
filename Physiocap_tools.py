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
from PyQt5.QtCore import QVariant

from qgis.core import (Qgis, QgsDistanceArea, QgsProject, QgsMessageLog, \
        QgsMapLayer, QgsCoordinateReferenceSystem, QgsFields, QgsField, \
        QgsFeature, QgsGeometry, QgsPoint, QgsPointXY,  \
        QgsVectorFileWriter, QgsWkbTypes)
from PyQt5.QtWidgets import QMessageBox

try :
    from osgeo import ogr
except ImportError:
    aText = "Erreur bloquante : module ogr n'est pas accessible." 
    QgsMessageLog.logMessage( aText, "\u03D5 Erreurs", Qgis.Warning)

try :
    import csv
except ImportError:
    aText = "Erreur bloquante : module csv n'est pas accessible." 
    QgsMessageLog.logMessage( aText, "\u03D5 Erreurs", Qgis.Warning)
    
try :
    import numpy as np
except ImportError:
    aText ="Erreur bloquante : module numpy n'est pas accessible" 
    QgsMessageLog.logMessage( aText, "\u03D5 Erreurs", Qgis.Warning)

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
    journal_nom = "{0} Informations".format( PHYSIOCAP_UNI)
    if modeTrace == TRACE_PAS:
        QgsMessageLog.logMessage( "Pas de trace : " + aText,  journal_nom, Qgis.Info)
        return
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
                if modeTrace in ["OK"]:
                    journal_nom = modeTrace
                else:
                    journal_nom = "{0} {1}".format( PHYSIOCAP_UNI, modeTrace)
                QgsMessageLog.logMessage( aText, journal_nom, Qgis.Info)
        else:
            # Cas général
            QgsMessageLog.logMessage( aText, journal_nom, Qgis.Info)
    return
    
def physiocap_error( self, aText, level ="WARNING"):
    """Send a text to the Physiocap error
    Call Class Tools For translation"""
    toolsObject = PhysiocapTools( self)
    toolsObject.physiocap_tools_log_error( aText, level)
    return -1      

def physiocap_write_in_synthese( self, aText):
    """Write a text in the results list"""
    self.textEditSynthese.insertPlainText( aText)   
  
def physiocap_is_only_ascii(s):
    if isinstance( s, unicode):
        physiocap_log( "physiocap_is_only_ascii {0}".format( "Cas unicode"), leModeTrace)
        try:
            s.encode('ascii')
            physiocap_log( "physiocap_is_only_ascii {0} : resultat OK {1}".format( "apres encode", s.encode('ascii')), leModeTrace)
        except UnicodeEncodeError:
            physiocap_log( "physiocap_is_only_ascii {0}".format( "dans exception"), leModeTrace)
            return False
    else:
        physiocap_log( "physiocap_is_only_ascii {0}".format( "Non unicode"), leModeTrace)
        try:
            s.decode('ascii')
        except UnicodeDecodeError:
            return False
    return True

def physiocap_is_int_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
 
def physiocap_create_projection_file( prj_name,  laProjection):
    """Creer le fichier de projection du layer avec la description de EPSG"""
    if (prj_name == None) or (prj_name == ""):
        return
        
    prj = open(prj_name, "w")
    epsg = 'inconnu'
    if ( laProjection == PROJECTION_L93) or ( laProjection == EPSG_NUMBER_L93):
        epsg = EPSG_DESCRIPTION_L93
    if ( laProjection == PROJECTION_GPS) or ( laProjection == EPSG_NUMBER_GPS):
        epsg = EPSG_DESCRIPTION_GPS
    prj.write(epsg)
    prj.close()
    return
    
def  physiocap_nom_entite_sans_pb_caractere( un_nom,  mon_unique = 0):
    """Change la chaine un_nom selon qu'elle contient ou non le caractère ' ou blanc"""
    ## Cela peut ne rien faire
    return un_nom.replace(" ",SEPARATEUR_).replace("\'", SEPARATEUR_)
    #return un_nom
#    if un_nom.find('\'') < 0:
#        return un_nom
#    elif mon_unique == 0:
#        return un_nom.replace("\'", "")
#    else:
#        # on veut un nom unique
#        return PHYSIOCAP_UNI + SEPARATEUR_+ un_nom.replace("\'", "") + SEPARATEUR_ + str( unique)
     
def  physiocap_nom_entite_avec_pb_caractere( un_nom, un_texte = "GDAL"):
    """rend True si la chaine un_nom contient un caractère ' problématique pour la librairie : un_texte"""
    if un_texte == "GDAL" and type(un_nom) == str:
        # Tester si une cote '
        if un_nom.find('\'') >= 0:
            return True
        if un_nom.find(' ') >= 0:
            return True
#    else:
#        physiocap_log( "pb GDAL {0}".format( type(un_nom)), leModeTrace)
#        
    # On a rien trouvé
    return False
    
def physiocap_get_layer_by_URI( layerURI ):
    """Rend le layer affiché dans le projet QGIS
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
            physiocap_log( "Layer retrouvé  {0}".format( layer.name()), leModeTrace)
            # The layer is found
            break
    if ( trouve == "YES"):
        if layer.isValid():
            return layer
        else:
            physiocap_log( "Layer trouvé  {0} mais invalide".format( layer.name()), leModeTrace)
            return None
    else:
        return None

def physiocap_get_layer_by_name( layerName ):
    """Rend le layer affiché dans le projet QGIS 
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
            physiocap_log( "OK Couche valide : {0}".format ( le_layer.name()), leModeTrace)
            return le_layer
        else:
            physiocap_log( "Couche invalide : {0}".format ( le_layer.name()), leModeTrace)
            return None
    else:
        physiocap_log( "Aucune couche retrouvée pour ID : {0}".\
            format( ( str( layerID))), leModeTrace)
        return None

def physiocap_quelles_informations_vignoble_agro( self):
    """ Mettre les info vignobles dans un dict """ 
    infoVignoble = {}
    infoVignoble[ "nom_parcelle"] = self.lineEditNomParcelle.text()
    details = "YES" if self.groupBoxDetailVignoble.isChecked() else "NO"
    infoVignoble[ "details"] = details
    infoVignoble[ "max_sarments_metre"] = float( self.spinBoxMaxSarmentsParMetre.value())
    infoVignoble[ "interrangs"] = float( self.spinBoxInterrangs.value())
    infoVignoble[ "interceps"] = float( self.spinBoxInterceps.value())
    infoVignoble[ "hauteur"] = float( self.spinBoxHauteur.value())
    infoVignoble[ "densite"] = float( self.doubleSpinBoxDensite.value())
    infoVignoble[ "le_cepage"] = self.comboBoxCepage.currentText()
    infoVignoble[ "la_taille"] = self.comboBoxTaille.currentText()
    #        # Informations agronomiques ___Nadia___
#        if self.radioButtonInfoRenseign.isChecked():
#            infoAgro = "Renseign"

    #infoVignoble[ ""] = 
#            self.settings.setValue("Physiocap/info_agro", infoAgro)#___definir les valeurs des variables : details : yes/no
#            self.settings.setValue("Physiocap/nom_parcelle", self.lineEditNomParcelle.text())#___definir les valeurs des variables : nom de la parcelle 
#            self.settings.setValue("Physiocap/annee_plant", int( self.spinBoxAnneePlant.value()))#___definir les valeurs des variables : année de plantation
#            self.settings.setValue("Physiocap/comuune",  self.comboBoxCommune.currentText())#___definir les valeurs des variables : commune
#            self.settings.setValue("Physiocap/region",  self.lineEditRegion.text())#___definir les valeurs des variables : region
#            self.settings.setValue("Physiocap/clone",self.lineEditClone.text())#___définir les valeurs des variables : clone
#            self.settings.setValue("Physiocap/porte_greffe", self.lineEditPorteGreffe.text())#___definir les valeurs des variables : porte-greffe
#            self.settings.setValue("Physiocap/sol_argile", self.lineEditSolArgile.text())#___definir les valeurs des variables : sol pourcentage argile
#            self.settings.setValue("Physiocap/sol_mo", self.lineEditSolMO.text())#___definir les valeurs des variables : sol pourcentage MO
#            self.settings.setValue("Physiocap/sol_caco3", self.lineEditSolCaCO3.text())#___definir les valeurs des variables : sol pourcentage CaCO3
#            self.settings.setValue("Physiocap/rendement", self.lineEditRendement.text())#___definir les valeurs des variables : rendement annee courante
#            self.settings.setValue("Physiocap/nb_grappes", self.lineEditNbGrappes.text())#___definir les valeurs des variables : nombre de grappes annee courante
#            self.settings.setValue("Physiocap/poids_moy_grappes", self.lineEditPoidsMoyGrap.text())#___definir les valeurs des variables : poids moyen de grappes annee courante
#            self.settings.setValue("Physiocap/rendement_1", self.lineEditRendement_1.text())#___definir les valeurs des variables : rendement annee precedente
#            self.settings.setValue("Physiocap/nb_grappes_1", self.lineEditNbGrappes_1.text())#___definir les valeurs des variables : nombre de grappes annee precedente
#            self.settings.setValue("Physiocap/poids_moy_grappes_1",self.lineEditPoidsMoyGrap_1.text())#___definir les valeurs des variables : poids moyen de grappes annee precedente
#            liste_apports_nb=len(TYPE_APPORTS)
#            choix_user_ind=self.comboBoxTypeApportFert.currentIndex()
#            if(choix_user_ind==liste_apports_nb-1):
#                self.settings.setValue("Physiocap/type_apports", self.lineEditTypeApportFert_Autres.text().replace(',',' '))#___definir les valeurs des variables : apport ,cas autre à préciser
#            else : 
#                self.settings.setValue("Physiocap/type_apports", self.comboBoxTypeApportFert.currentText())#___definir les valeurs des variables : type apports fertilisation
#            self.settings.setValue("Physiocap/produit",self.lineEditProduitFert.text())#___definir les valeurs des variables : produit
#            self.settings.setValue("Physiocap/dose", self.lineEditDoseFert.text())#___definir les valeurs des variables : dose(t/ha)
#            liste_strategies_nb=len(ENTRETIEN_SOL)
#            choix_user_ind=self.comboBoxStrategieSol.currentIndex()
#            if(choix_user_ind==liste_strategies_nb-1):
#                self.settings.setValue("Physiocap/strategie_entretien_sol", self.lineEditStrategieSol_Autres.text().replace(',',' '))#___definir les valeurs des variables : strategie entretien sol , cas autre à préciser
#            else : 
#                self.settings.setValue("Physiocap/strategie_entretien_sol", self.comboBoxStrategieSol.currentText())#___definir les valeurs des variables : strategie entretien de sol
#            self.settings.setValue("Physiocap/etat_sanitaire", str(self.spinBoxEtatSanitaire_intensite.value())+"*"+str(self.spinBoxEtatSanitaire_frequence.value()))#___definir les valeurs des variables : etat sanitaire intensité*frequance

    return infoVignoble
def physiocap_quelle_projection_et_lib_demandee( self):
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
    # A_TESTER: Récuperer le CRS du projet QGIS et le compare au choix
#    laProjection_str = str( la_projection_CRS.postgisSrid())
#    if la_projection_CRS.isValid():
#        physiocap_log("Projection {0} des shapefiles est demandée : {1} est un EPSG valide".\
#            format( la_projection_TXT, laProjection_str), leModeTrace)
        
    EXTENSION_SHP_COMPLET = SEPARATEUR_ + la_projection_TXT + EXTENSION_SHP
    EXTENSION_PRJ_COMPLET = SEPARATEUR_ + la_projection_TXT + EXTENSION_PRJ
   
    # Cas du nom du raster 
    if self.radioButtonSAGA.isChecked():
        if self.checkBoxSagaTIFF.isChecked():
            EXTENSION_RASTER_COMPLET = SEPARATEUR_ + la_projection_TXT + EXTENSION_RASTER
        else:
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
        physiocap_log( "Calcul de distance Description SCR {0}".\
        format( laProjectionCRS.description()), TRACE_TOOLS)
        physiocap_log( "PROJ.4 SCR {0}".\
        format( laProjectionCRS.toProj4()), TRACE_TOOLS)
    else:
        physiocap_log( "INVALIDE SCR", TRACE_TOOLS)
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
        si "chemin_session + [1]" existe déjà, on crée un "chemin_session + [2]" etc         
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
        si "chemin_session + (1)" existe déjà, on crée un "chemin_session + (2)" etc         
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
        si "chemin_session + (1)" existe déjà, on crée un "chemin_session + (2)" etc         
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
    """ Crée ou detruit et re-crée un fichier"""
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
    
def physiocap_vecteur_vers_gpkg( self, chemin_session, nom_base_gpkg, 
        nom_court_vecteur = None, nom_vecteur = None):
    """Création du GPKG pour les vecteurs de la session (le nom de base est le nom_session)
    On cree un gpkg à partir du modele (vide)
    si un vecteur est proposé, on complète le GPKG. On rend le nom du nouveau vecteur dans GPKG
    sinon on crée un GPKG avec le modele de contour - qui se nomme nom_base_gpkg et on rend ce GPKG"""

    # Création du GPKG pour les vecteurs de la session 
    # toujours le nom de la session (non incrementé)
    nom_gpkg_court = nom_base_gpkg + EXTENSION_GPKG
    nom_gpkg_modele = os.path.join( REPERTOIRE_MODELE_GPKG, MODELE_CONTOUR_GPKG )
    nom_gpkg = os.path.join( chemin_session, nom_gpkg_court)

    if not os.path.isfile( nom_gpkg):
        if not os.path.isfile( nom_gpkg_modele):
            # Vérifier si GPKG modele n'existe pas
            uMsg = self.tr( "Erreur bloquante : problème lors de recherche du géopackage modele {0}").\
                format( nom_gpkg_modele)
            physiocap_error( self, uMsg)
            raise physiocap_exception_no_gpkg( nom_gpkg_modele)
        else:
            # Creation
            mon_nouveau_gpkg = ogr.GetDriverByName( GEOPACKAGE_DRIVER).CreateDataSource( nom_gpkg)
            mes_vecteurs = ogr.Open( nom_gpkg_modele)
            mon_vecteur = mes_vecteurs.GetLayerByIndex(0)
            mon_nouveau_gpkg.CopyLayer( mon_vecteur,  MODELE_CONTOUR_NOM,  [])
            physiocap_log( "Physiocap : Création GPKG contour : {0}".format( nom_gpkg_modele), TRACE_TOOLS)
            # pour clore et ecrire le GPKG
            mon_nouveau_gpkg = None
      
    # Assert GPKG existe
    if not os.path.isfile( nom_gpkg):
        # Vérifier si GPKG existe bien
        uMsg = self.tr( "Erreur bloquante : problème lors de recherche du géopackage {0}").\
            format( nom_gpkg)
        physiocap_error( self, uMsg)
        raise physiocap_exception_no_gpkg( nom_gpkg) 

    # Pas de vecteur à ajouter, on rend le GPKG modele
    if ( nom_court_vecteur == None) or ( nom_vecteur == None):
        return nom_gpkg

    # Ajout du nouveau vecteur dans GPKG sortie de la copie OGR
    le_nom_gpkg_complete = nom_gpkg + SEPARATEUR_GPKG + nom_court_vecteur
    physiocap_log( "Physiocap : Création GPKG  {0}".format( le_nom_gpkg_complete), TRACE_TOOLS)
    mon_shape = ogr.Open( nom_vecteur)
    mon_layer = mon_shape.GetLayerByIndex(0)
    le_gpkg = ogr.Open( nom_gpkg,  True)
    le_gpkg.CopyLayer( mon_layer,  nom_court_vecteur,  [])
    # pour ecrire
    le_gpkg = None
    # Sous windows lacher les vecteurs aussi
    mon_layer = None
    mon_shape = None
    # Détruire le GPKG intermediaire
    os.remove( nom_vecteur)
    
        
#  AUTRE solution   Ne crée que l'enveloppe mais ne copie pas les données
# CAS Géopackage par QgsVectorLayerExporter
#    if self.fieldComboFormats.currentText() == GEOPACKAGE_NOM  and version_3 == "YES":
#        # Copie dans geopackage et remplace  nom_vecteur_sans_0
#        nom_court_gpkg = NOM_POINTS[1:] + extension_point
#        layer_modele  = QgsVectorLayer( nom_vecteur, "INUTILE",  'ogr')
#        options = QgsVectorFileWriter.SaveVectorOptions()
#        options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer 
#        options.layerName = nom_court_gpkg
#        nom_layer_cree = nom_gpkg + SEPARATEUR_GPKG + nom_court_gpkg
#        QgsVectorFileWriter.writeAsVectorFormat( layer_modele, nom_gpkg,   options)           
#        layer_cree = QgsVectorLayer( nom_layer_cree, "INUTILE",  'ogr')
#        QgsVectorLayerExporter.exportLayer( layer_modele, layer_cree.name(), GEOPACKAGE_DRIVER, 
#            laProjectionCRS)
#    else:
#        nom_layer_cree = nom_vecteur
#        

#    Ne crée que l'enveloppe mais ne copie pas les données
# CAS Géopackage par QgsVectorFileWriter.writeAsVectorFormat
#    if self.fieldComboFormats.currentText() == GEOPACKAGE_NOM  and version_3 == "YES":
#        # Copie dans geopackage et remplace  nom_vecteur_sans_0
#        nom_court_gpkg_sans_0 = NOM_POINTS[1:] + extension_point
#        layer_modele  = QgsVectorLayer( nom_vecteur, "INUTILE",  'ogr')
#        options = QgsVectorFileWriter.SaveVectorOptions()
#        options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer 
#        options.layerName = nom_court_gpkg_sans_0
#        QgsVectorFileWriter.writeAsVectorFormat( layer_modele, nom_gpkg,   options)           
#        nom_layer_cree = nom_gpkg + SEPARATEUR_GPKG + nom_court_gpkg_sans_0
#    else:
#        nom_layer_cree = nom_vecteur    
    return le_nom_gpkg_complete     

def physiocap_segment_vers_vecteur( self, chemin_session,  nom_repertoire, nom_session,  segment,  info_segment, 
        version_3 = "NO",  segment_simplifie="YES"):
    """ Creation de shape file à partir des données de segment """

    distancearea, EXT_CRS_SHP, EXT_CRS_PRJ, EXT_CRS_RASTER, \
        laProjectionCRS, laProjectionTXT, EPSG_NUMBER = \
            physiocap_quelle_projection_et_lib_demandee( self)        
    nom_court_vecteur_segment = None
    nom_court_prj_segment = None
    nom_vecteur_segment = None
    nom_prj = None
    #nom_gpkg = None
    quel_vecteur_demande = self.fieldComboFormats.currentText()
    if segment_simplifie == "YES":
        nom_court_vecteur = nom_session + NOM_SEGMENTS
    else:
        nom_court_vecteur = nom_session + NOM_SEGMENTS + NOM_SEGMENTS_SUITE_DETAILS    
    if quel_vecteur_demande == SHAPEFILE_NOM: 
        nom_court_vecteur_segment = nom_court_vecteur + EXT_CRS_SHP
        nom_court_prj_segment = nom_court_vecteur + EXT_CRS_PRJ
        nom_vecteur_segment = os.path.join( nom_repertoire, nom_court_vecteur_segment)
        nom_prj = os.path.join( nom_repertoire, nom_court_prj_segment)
        # Si le shape existe dejà il faut le détruire
        if os.path.isfile( nom_vecteur_segment):
            # A_TESTER: je doute que ca marche
            physiocap_log( self.tr( "Le shape file existant déjà, il est détruit."), TRACE_TOOLS)
            os.remove( nom_vecteur_segment) 
    elif quel_vecteur_demande == GEOPACKAGE_NOM  and version_3 == "YES":
        # Assert GPKG existe : nom_gpkg = 
        physiocap_vecteur_vers_gpkg( self, chemin_session, nom_session)
        nom_court_gpkg_extension = nom_court_vecteur + EXTENSION_GPKG
        nom_gpkg_intermediaire = os.path.join( chemin_session, nom_court_gpkg_extension)
    else:
        # Assert type vecteur supporté
        raise physiocap_exception_vecteur_type_inconnu( quel_vecteur_demande)

    # Assert GPKG existe

    # Prepare les attributs
    les_champs = QgsFields()
    if quel_vecteur_demande == GEOPACKAGE_NOM  and version_3 == "YES":
        les_champs.append( QgsField("fid", QVariant.Int, "integer", 10))
    else:
        les_champs.append( QgsField("GID", QVariant.Int, "integer", 10))
    les_champs.append( QgsField("GID_10", QVariant.Int, "integer", 10))
    les_champs.append( QgsField("NB_POINTS", QVariant.Int, "integer", 10))
    les_champs.append( QgsField("DATE_DEB", QVariant.String, "string", 25))
    les_champs.append( QgsField("DATE_FIN", QVariant.String, "string", 25))
    les_champs.append( QgsField("DERIVE", QVariant.Double, "double", 10,2))
    les_champs.append( QgsField("GID_GARDE", QVariant.String, "varchar", 100))
    les_champs.append( QgsField("GID_TROU", QVariant.String, "varchar", 100))

    # Creation du vecteur
    if quel_vecteur_demande == GEOPACKAGE_NOM  and version_3 == "YES":
        # CAS Géopackage
        writer = QgsVectorFileWriter( nom_gpkg_intermediaire, "utf-8", les_champs, 
            QgsWkbTypes.MultiLineString, laProjectionCRS, GEOPACKAGE_DRIVER)
    else:    
        writer = QgsVectorFileWriter( nom_vecteur_segment, "utf-8", les_champs, 
            QgsWkbTypes.MultiLineString, laProjectionCRS, SHAPEFILE_DRIVER)
            
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
    writer = None

    # PRJ file
    physiocap_create_projection_file( nom_prj,  laProjectionTXT)

    nom_layer_cree = nom_vecteur_segment
    # Cas geopackage
    if quel_vecteur_demande == GEOPACKAGE_NOM  and version_3 == "YES":
        nom_layer_cree = physiocap_vecteur_vers_gpkg( self, chemin_session, nom_session,  
            nom_court_vecteur, nom_gpkg_intermediaire)
        
    return nom_layer_cree

def physiocap_csv_vers_vecteur( self, chemin_session, Nom_Session, progress_barre, extension_point,  
    csv_name,  chemin_shapes, nom_court_vecteur,
    nom_fichier_synthese = "NO", details = "NO",  version_3 = "NO"):
    """ Creation de shape file à partir des données des CSV
    Si nom_fichier_synthese n'est pas "NO", on produit les moyennes dans le fichier 
    qui se nomme nom_fichier_synthese
    Selon la valeur de détails , on crée les 5 premiers ("NO") ou tous les attibuts ("YES")
    """
    leModeDeTrace = self.fieldComboModeTrace.currentText()
    # Recuperer le CRS choisi, les extensions et le calculateur de distance
    distancearea, EXT_CRS_SHP, EXT_CRS_PRJ, EXT_CRS_RASTER, \
        laProjectionCRS, laProjectionTXT, EPSG_NUMBER = \
            physiocap_quelle_projection_et_lib_demandee( self)        
    
    # Initialisation
    nom_vecteur = None
    prj_name = None
    #nom_gpkg = None
    quel_vecteur_demande = self.fieldComboFormats.currentText()
    if quel_vecteur_demande == SHAPEFILE_NOM:
        nom_court_shapefile = nom_court_vecteur + EXT_CRS_SHP
        nom_court_projection = nom_court_vecteur + EXT_CRS_PRJ
        nom_vecteur = os.path.join(chemin_shapes, nom_court_shapefile)
        prj_name = os.path.join(chemin_shapes, nom_court_projection)
        # Si le shape existe dejà il faut le détruire
        if os.path.isfile( nom_vecteur):
            # A_TESTER: je doute que ca marche : detruire plutot par une option de creation
            os.remove( nom_vecteur)            
    elif quel_vecteur_demande == GEOPACKAGE_NOM  and version_3 == "YES":
        # Creer seulement le geopackage
        #nom_gpkg = <<< Inutile
        physiocap_vecteur_vers_gpkg( self, chemin_session, Nom_Session)
        nom_court_gpkg = NOM_POINTS[1:] + extension_point
        nom_court_gpkg_extension = nom_court_gpkg + EXTENSION_GPKG
        nom_gpkg_intermediaire = os.path.join( chemin_session, nom_court_gpkg_extension)
        #nom_gpkg_final = nom_gpkg + SEPARATEUR_GPKG + nom_court_gpkg
    else:
        # Assert type vecteur supporté
        raise physiocap_exception_vecteur_type_inconnu( quel_vecteur_demande)
    
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
    nom_layer_cree = None
    
    #Lecture des data dans le csv et stockage dans une liste
    with open(csv_name, "rt") as csvfile:
        try:
            r = csv.reader(csvfile, delimiter=";")
        except NameError:
            uText = "Erreur bloquante : module csv n'est pas accessible."
            # TODO: ?V3.12 LTR tester les exceptions ou passer à Panda
            raise physiocap_exception_csv( csv_name)

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
                            uText = "Le nombre de colonnes : {0} du cvs ne permet pas le calcul détaillé - lors création du shape {1}".\
                                format( len(row),  nom_court_vecteur)
                            raise physiocap_exception_err_csv(  uText)
                        nbsarmm2.append(float(row[9]))
                        nbsarcep.append(float(row[10]))
                        biommm2.append(float(row[11]))
                        biomgm2.append(float(row[12]))
                        biomgcep.append(float(row[13]))
                    else:
                        if len(row) != 21:
                            uText = "Le nombre de colonnes : {0} du cvs ne permet pas le calcul détaillé - lors création dushape {1}".\
                                format( len(row),  nom_court_vecteur)
                            raise physiocap_exception_err_csv( uText)
                        nbsarmm2.append(float(row[16]))
                        nbsarcep.append(float(row[17]))
                        biommm2.append(float(row[18]))
                        biomgm2.append(float(row[19]))
                        biomgcep.append(float(row[20]))                        
                
    # Prepare les attributs
    les_champs = QgsFields()
    # V1.0 Ajout du GID puis V3.1.8 pas fid si GPKG
    if quel_vecteur_demande == GEOPACKAGE_NOM  and version_3 == "YES":
        les_champs.append( QgsField("fid", QVariant.Int, "integer", 10))
    else:
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


    # Creation du vecteur
    if quel_vecteur_demande == GEOPACKAGE_NOM  and version_3 == "YES":
        # CAS Géopackage
        writer = QgsVectorFileWriter( nom_gpkg_intermediaire, "utf-8", les_champs, 
                QgsWkbTypes.PointZM, laProjectionCRS , GEOPACKAGE_DRIVER)
    else:
        if version_3 == "YES":
            # Cas V3
            writer = QgsVectorFileWriter( nom_vecteur, "utf-8", les_champs, 
                    QgsWkbTypes.PointZM, laProjectionCRS , SHAPEFILE_DRIVER)
        else:
            writer = QgsVectorFileWriter( nom_vecteur, "utf-8", les_champs, 
                    QgsWkbTypes.Point, laProjectionCRS , SHAPEFILE_DRIVER)

### CAS Géopackage BAD ne n'a pas creer de vecteur, mais un tuple
###    if self.fieldComboFormats.currentText() == GEOPACKAGE_NOM  and version_3 == "YES":
###        # Copie dans geopackage
###        nom_court_gpkg = NOM_POINTS[1:] + extension_point
###        layer_modele  = QgsVectorLayer( nom_vecteur, "INUTILE",  'ogr')
###        options = QgsVectorFileWriter.SaveVectorOptions()
###        options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer 
###        options.layerName = nom_court_gpkg
###        # BAD BAD ==> 
###        writer_gpkg = QgsVectorFileWriter.writeAsVectorFormat( layer_modele, nom_gpkg,   options)
###        nom_gpkg_cree = nom_gpkg + SEPARATEUR_GPKG + nom_court_gpkg
###        # BAD BAD ==> writer_gpkg = QgsVectorLayerExporter.exportLayer( layer_modele, nom_layer_cree,
###        #GEOPACKAGE_DRIVER,  laProjectionCRS)

    for numPoint,Xpoint in enumerate(x):
        feat = QgsFeature()
        if version_3 == "YES":
            # choix de la données dans Z
            val_Z = 0.0
            val_M = altitude[numPoint]
            if extension_point == EXTENSION_SANS_ZERO:
                val_Z = diam[numPoint]
            if extension_point == EXTENSION_AVEC_ZERO:
                val_Z = derive[numPoint]
            if extension_point == EXTENSION_ZERO_SEUL:
                val_Z = vitesse[numPoint]                
            #écrit la géométrie avec le Z = diametre (ou altitude ou vitesse) et M
            feat.setGeometry( QgsGeometry(QgsPoint( Xpoint, y[numPoint], val_Z, val_M))) 
        else:
            # A_TESTER: test sans fromPointXY
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
    # Fermer le vecteur
    writer = None

    # Create the PRJ file
    physiocap_create_projection_file( prj_name,  laProjectionTXT)
 
    # Progress BAR + 5 %
    progress_barre = progress_barre + 5
    self.progressBar.setValue( progress_barre)
 
    nom_layer_cree = None
    # Cas geopackage il faut faire une copie du gpkg intermediaire
    if quel_vecteur_demande == GEOPACKAGE_NOM  and version_3 == "YES":
        nom_layer_cree = physiocap_vecteur_vers_gpkg( self, chemin_session, Nom_Session,
            nom_court_gpkg, nom_gpkg_intermediaire )
    else:
        nom_layer_cree = nom_vecteur
        
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
            fichier_synthese.write("\n\nVECTEURS FORMAT : {0}\n".format( self.fieldComboFormats.currentText()))
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
            raise physiocap_exception_fic( nom_fichier_synthese )
            
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
            raise physiocap_exception_fic( msg )
                    
        fichier_synthese.close()

    # Rendre la memoire 
    x,y,nbsarm,diam,biom,date_capture,vitesse= [],[],[],[],[],[],[]
    azimuth, nbsart =  [],[]
    altitude,  pdop,  distance,  derive =  [],[],[],[]
    nbsarmm2,nbsarcep,biommm2,biomgm2,biomgcep=[],[],[],[],[]
    
    # on rend le nom du shapefile ou du geopackage
    return nom_layer_cree
  
class PhysiocapTools( QtWidgets.QDialog):
    """QGIS Pour voir les messages traduits."""
    def __init__(self, parent=None):
        """Class constructor."""
        print("TOOLS init class")
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

