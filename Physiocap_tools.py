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

from qgis.core import (Qgis, QgsDistanceArea, QgsProject, QgsMessageLog,  \
        QgsLayerTreeGroup, QgsLayerTreeLayer, QgsMapLayer, QgsCoordinateReferenceSystem, \
        QgsFields, QgsField, QgsFeature, QgsGeometry, QgsPoint, QgsPointXY,  \
        QgsVectorFileWriter, QgsWkbTypes, QgsFeatureRequest, \
        QgsProcessingFeedback, QgsVectorLayer) 
from PyQt5.QtWidgets import QMessageBox

import shutil
import glob
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


# MESSAGES & LOG
def physiocap_message_bar( self, text, level="warning"):
    """Send a message box by default Warning"""
    title = self.tr( "{0} Physiocap").format( PHYSIOCAP_UNI)
    text = title + ' ' + text
    if level == "info":
        iface.messageBar().pushMessage( text, level=Qgis.Info)
    elif level == "warning":
        iface.messageBar().pushMessage( text, level=Qgis.Warning)
    elif level == "succes":
        iface.messageBar().pushMessage( text, level=Qgis.Succes)
    elif level == "error":
        iface.messageBar().pushMessage( text, level=Qgis.Critical)
    else:
        iface.messageBar().pushMessage( text, level=Qgis.Warning)

def physiocap_message_box( self, text, level="warning"):
    """Send a message box by default Warning"""
    title = self.tr( "{0} Physiocap").format( PHYSIOCAP_UNI)
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
    title = self.tr( "{0} Physiocap").format( PHYSIOCAP_UNI)
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
        if LE_MODE_PROD == "NO":
            QgsMessageLog.logMessage( "#NO# " + aText,  journal_nom, Qgis.Info)
        return
    elif modeTrace == TRACE_MINI:
        # On monte warning et message debut et fin
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
            if LE_MODE_PROD == "YES" and modeTrace not in TRACES_DEMASQUEES:
                pass
            else:
                if modeTrace in TRACES_MASQUEES:
                    journal_nom = modeTrace
                else:
                    journal_nom = "{0} {1}".format( PHYSIOCAP_UNI, modeTrace)
                QgsMessageLog.logMessage( aText, journal_nom, Qgis.Info)
        else:
            # Cas général et info
            QgsMessageLog.logMessage( aText, journal_nom, Qgis.Info)
    return
    
def physiocap_error( self, aText, level ="WARNING"):
    """Send a text to the Physiocap error
    Call Class Tools For translation"""
    toolsObject = PhysiocapTools( self)
    toolsObject.physiocap_tools_log_error( aText, level)
    return -1      

# Utilitaire liste poly inter
def quel_type_vecteur( self, vector):
    """Vérifie le type de forme du vector : on simplifie au cas multiple pour Wbk et """

    try:
        # A_TESTER: V3 ? vérifier multiType couvre plus de cas
        # et cas vecteur non shape
        geomWkbType = vector.wkbType()
        geomWkbMultiType = QgsWkbTypes.multiType( geomWkbType) # multiple sous processing
        geomType = QgsWkbTypes.geometryType( geomWkbType) 
        geomTypeText = QgsWkbTypes.geometryDisplayString( geomType)
        geomWkbTypeText = QgsWkbTypes.displayString( geomWkbType)
#        physiocap_log( "-- Vecteur Text {0} type geom {1} et WkbType {2}".\
#            format( geomTypeText, geomType,  geomWkbType), TRACE_JH)
        return geomTypeText, geomWkbTypeText, geomWkbType,  geomWkbMultiType  
    except:
#        physiocap_error( self, self.tr("Warning : couche (layer) {0} n'est ni (is nor) point, ni (nor) polygone").\
#            format( vector.id()))
        pass
        # On evite les cas imprévus
        return "Inconnu", "WkbInconnu",  None,  None

def quel_sont_vecteurs_choisis( self, source = "Intra"):
        distancearea, quel_vecteur_demande, EXTENSION_CRS_VECTEUR, DRIVER_VECTEUR, EXTENSION_RASTER_COMPLET, \
            transform_context, laProjectionCRS, laProjectionTXT, EPSG_NUMBER = quelle_projection_et_format_vecteur( self)
        derniere_session = self.lineEditDerniereSession.text()
        # Pour polygone de contour   
        infos_poly = self.comboBoxPolygone.currentText().split( SEPARATEUR_NOEUD)
        #physiocap_log("Vecteur {}".format( infos_poly), TRACE_TOOLS)
        if ( len( infos_poly) == 3) and infos_poly[1] == "CSV NON OUVERT DANS QGIS":
            chemin_vecteur = infos_poly[ 2]
            uri = "file:///{0}?delimiter={1}&crs=epsg:{2}&wktField={3}".\
                format( chemin_vecteur, CSV_DELIMITER_POINT_VIRGULE, EPSG_NUMBER, CSV_GEOM)
            vecteur_poly = QgsVectorLayer( uri , infos_poly[ 0], CSV_DRIVER)
            origine_poly = "AGRO_CSV"
        elif ( len( infos_poly) == 3) and infos_poly[1] == "SHAPE NON OUVERT DANS QGIS":
            chemin_vecteur = infos_poly[ 2]
            vecteur_poly = QgsVectorLayer( chemin_vecteur , infos_poly[ 0], 'ogr')            
            origine_poly = "AGRO_SHP"
        elif ( len( infos_poly) == 3) and infos_poly[1] == "OUVERT DANS QGIS":
            vecteur_poly = physiocap_get_layer_by_ID( infos_poly[ 2], infos_poly[0])
            URI_complet = vecteur_poly.dataProvider().dataSourceUri()
            physiocap_log("URI du vecteur OUVERT {}".format( URI_complet), TRACE_AGRO)
            if URI_complet.find("|") > 0:
                URI_decoupe = URI_complet.split( "|")
                chemin_vecteur = URI_decoupe[0]
            else:
                chemin_vecteur = URI_complet
            extension = chemin_vecteur[-3:]
            #physiocap_log("extension vecteur OUVERT {}".format( extension), TRACE_AGRO)
            origine_poly = "INCONNUE"
            if extension == "shp":
                origine_poly = "SHP"
            if extension == "csv":
                origine_poly = "CSV"
        else:
            aText = self.tr( "Le polygone de contour n'est pas choisi.")
            physiocap_error( self, aText)
#            aText = aText + "\n" + self.tr( "Avez-vous créer votre vecteur de contours ?")
#            aText = aText + "\n" + self.tr( "Créer une nouvelle session Physiocap - bouton Filtrer les données brutes - ")
#            physiocap_message_box( self, aText)
            return derniere_session, None, None, None, None 
        if source == "Filtrer":
            return derniere_session, None, origine_poly, vecteur_poly, chemin_vecteur

        # Pour les points
        nom_complet_point = self.comboBoxPoints.currentText().split( SEPARATEUR_NOEUD)
        if (len( nom_complet_point) == 3) and (nom_complet_point[ 1] == "OUVERT DANS QGIS"):
            nom_noeud_arbre = nom_complet_point[ 0] 
            id_point = nom_complet_point[ 2] 
            vecteur_point = physiocap_get_layer_by_ID( id_point)
        else:
            aText = self.tr( "Le vecteur de points n'est pas choisi. ")
            aText = aText + self.tr( "Créer une nouvelle session Physiocap - bouton Filtrer les données brutes - ")
            if souce == "Inter":
                aText = aText + self.tr( "avant de faire votre calcul de Moyenne Inter Parcellaire")
            else:
                aText = aText + self.tr( "avant de faire votre calcul de Moyenne Intra Parcellaire")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        return nom_noeud_arbre, vecteur_point, origine_poly, vecteur_poly, chemin_vecteur
    
def quel_poly_point_INTER( self, isRoot = None, node = None ):
    """ Recherche dans l'arbre Physiocap (recursif)
    les Polygones,
    les Points de nom DIAMETRE qui correspondent aux données filtreés
    Remplit deux listes pour le comboxBox des vecteurs "inter Parcellaire"
    et la liste des parcelles pour INTRA
    Rend aussi le nombre de poly et point retrouvé
    """
    #leModeDeTrace = self.fieldComboModeTrace.currentText() 
    derniere_session = self.lineEditDerniereSession.text()
    Repertoire_Donnees_Brutes = self.lineEditDirectoryPhysiocap.text()
    Nom_Profil =  self.fieldComboProfilPHY.currentText()
    nombre_poly = 0
    nombre_point = 0
   
    if ( isRoot == None):
        root = QgsProject.instance().layerTreeRoot()
        self.comboBoxPolygone.clear()
        self.comboBoxPoints.clear()
        noeud_en_cours = ""
        noeud = root
    else:
        # On force root comme le noeud
        noeud = node
        noeud_en_cours = node.name()

    #physiocap_log( "- noeud en cours {0}".format( noeud_en_cours), TRACE_JH)        

    # On descend de l'arbre par la racine
    for child in noeud.children():
        if isinstance( child, QgsLayerTreeGroup):
            noeud_en_cours = child.name()
            #physiocap_log( "--Group: " + noeud_en_cours, TRACE_JH)
            if noeud_en_cours != derniere_session:
                continue
            physiocap_log( "--Group: " + noeud_en_cours, TRACE_TOOLS)
            groupe_inter = noeud_en_cours + SEPARATEUR_ + VIGNETTES_INTER
            physiocap_log( "--Group inter : " + groupe_inter, TRACE_TOOLS)
            if ( noeud_en_cours != groupe_inter):
                # On exclut les vignettes INTER : sinon on descend dans le groupe
                try:
                    un_nombre_poly, un_nombre_point = quel_poly_point_INTER( self, noeud, child)
                except TypeError:
                    physiocap_log( "--type error ", TRACE_TOOLS)
                    un_nombre_poly = 0
                    un_nombre_point = 0
                    pass
                nombre_point = nombre_point + un_nombre_point
                nombre_poly = nombre_poly + un_nombre_poly
        elif isinstance( child, QgsLayerTreeLayer):
#            physiocap_log( "--Layer >> {0}  ID>> {1} ". \
#                format( child.name(),  child.layerId()), TRACE_TOOLS)) 
#           physiocap_log( "--Layer parent le groupe >> " + child.parent().name() , TRACE_TOOLS)) 
            # Tester si poly ou point
            type_layer,  type_Wkb_layer,  numero_Wkb_layer,  numero_Multi_Wkb = quel_type_vecteur( self, child.layer())
#            physiocap_log( "--Layer a pour type >> {0} WkbType  >> {1} et numero_Wkb  >> {2} ".\
#            format( type_layer,  type_Wkb_layer,  numero_Wkb_layer), TRACE_TOOLS))
            if ( type_layer == "Point"):
                if (((not self.checkBoxConsolidation.isChecked()) and \
                    ( child.name() == "DIAMETRE mm")) \
                    or \
                    ((self.checkBoxConsolidation.isChecked()) and \
                    ( child.parent().name() == CONSOLIDATION))):
                    physiocap_log( "- layer POINT: " + child.name() + "  ID: " + child.layerId(), TRACE_TOOLS) 
                    node_layer = noeud_en_cours + SEPARATEUR_NOEUD + "OUVERT DANS QGIS" + \
                        SEPARATEUR_NOEUD + child.layerId()
                    self.comboBoxPoints.addItem( node_layer)
                    nombre_point = nombre_point + 1
            elif ( type_layer == "Polygon"):
                physiocap_log( "- layer POLY: " + child.name() + "  ID: " + child.layerId(), TRACE_TOOLS) 
                node_layer = child.name() + SEPARATEUR_NOEUD + "OUVERT DANS QGIS" + \
                    SEPARATEUR_NOEUD + child.layerId()        
                self.comboBoxPolygone.addItem( node_layer)
                nombre_poly = nombre_poly + 1
            elif ( type_layer == "Line"):
                pass # cas de segments
            else:
                pass
#                physiocap_log( "- Layer de type {0} rejeté : {1} ID: ".\
#                    format( type_layer, child.name(),  child.layerId()), TRACE_TOOLS) 
    if Nom_Profil == 'Champagne' and nombre_poly == 0:
        # On prend un eventuel shp ou CSV dans rep des données brutes
        nom_vecteur, nom_court_vecteur,  libelle = \
            quel_vecteur_dans_donnees_brutes( Repertoire_Donnees_Brutes)
        if ((nom_vecteur != None) and len( nom_vecteur) > 0):                
            node_layer = nom_court_vecteur + SEPARATEUR_NOEUD + libelle + \
                SEPARATEUR_NOEUD + nom_vecteur
            self.comboBoxPolygone.clear()
            self.comboBoxPolygone.addItem( node_layer)
            nombre_poly = 1

    if nombre_poly > 0:
        _, _, origine_poly, vecteur_poly, chemin_vecteur = quel_sont_vecteurs_choisis( self, "Filtrer")
        physiocap_log( "Dans quel_poly_point_INTER origine est {} pour vecteur {}".\
                format( origine_poly, chemin_vecteur), TRACE_TOOLS)
        if Nom_Profil == 'Champagne':
            if self.radioButtonContour.isChecked():
                # Assert vecteur poly champ obligatoire
                try:
                    _, champs_agro_fichier, _, _, champs_vignoble_requis, champs_vignoble_requis_fichier, _, _, les_parcelles_agro, _ = \
                        assert_champs_agro_obligatoires( self, vecteur_poly, origine_poly)
                except physiocap_exception_agro_obligatoire as e:
                    aText = "{}".format(e)
                    les_parcelles_agro = []
                    physiocap_message_box( self, aText, 'information')
                    return 0, 0
                    
                if les_parcelles_agro != None and len( les_parcelles_agro) > 0:
                    # Remplir la liste des parcelles diponibles
                    lister_parcelles_INTRA( self, None,  les_parcelles_agro)

        else:
            # Remplir la liste des parcelles diponibles dans poly
            lister_parcelles_INTRA( self, vecteur_poly)
            
    return nombre_poly, nombre_point
    
# Vignobles Moyennes et CSVT
def quelles_informations_moyennes():
    """ Mettre les info moyennes dans l'ordre et dans un dict entete """ 
    champsMoyenneOrdonnes = [ "diam", "vitesse", "biomm2", "nbsarmm2", "biomgcep", "nbsarcep"]
    listeEnteteMoyenne = [ "DIAM_AVG", "VITESSE_AVG", "BIOMM2", "NBSARMM2", "BIOMGCEP", "NBSARMCEP"]
    listeEnteteMoyenneSHP = [ "DIAM_AVG", "VITESSE_AV", "BIOMM2", "NBSARMM2", "BIOMGCEP", "NBSARMCEP"]
    return champsMoyenneOrdonnes, listeEnteteMoyenne, listeEnteteMoyenneSHP

def structure_informations_vignoble( self, format_entre_sortie ='AGRO_CSV'):
    """ Structure des info vignobles dans une liste ordonnée, 
        dans une liste des requis et dans un dict pour les entete et type """ 
    position_dic = 0
    position_autre = 2
    if format_entre_sortie in [ 'AGRO_CSV',  "CSV"]:
        position_dic = 0
        position_autre = 2
    elif format_entre_sortie in [ "AGRO_SHP",  "SHP"]:
        position_dic = 2
        position_autre = 0
    # TODO ? Erreur autres
    dictEnteteVignoble = {}  # dict de liste [ "nom champ csv", "type_QGIS", "champ shp"] 
    # pour entete manque pH non demandé et CaCO3 non necessaire
    champsVignobleOrdonnes = [ "campagne", "nom_parcelle", "commune", "region", "cepage", "clone", "porte_greffe", \
      "annee_plantation", "taille", "argile", "mo", "CN", "rendement", "poids_moy_grappes", "nb_grappes", \
      "interrangs", "interceps", "hauteur", "densite"]
    
    dictEnteteVignoble[ "campagne"] = [ "Campagne", "Integer", "Campagne"]
    dictEnteteVignoble[ "nom_parcelle"] = [ "Nom_Parcel", "String", "Nom_Parcel"]
    dictEnteteVignoble[ "commune"]      = [ "Commune", "String", "Commune"]
    dictEnteteVignoble[ "region"]       = [ "Region", "String", "Region"]
    dictEnteteVignoble[ "cepage"]       = [ "Cepage", "String", "Cepage"]
    dictEnteteVignoble[ "clone"]        = [ "Clone", "String", "Clone"]
    dictEnteteVignoble[ "porte_greffe"] = [ "Porte_gref", "String", "Porte_gref"]
    dictEnteteVignoble[ "annee_plantation"] = [ "Annee_plan", "Integer", "Annee_plan"]
    dictEnteteVignoble[ "taille"]       = [ "Type_taill", "String", "Type_taill" ]
    dictEnteteVignoble[ "argile"]       = [ "Sol_argile", "Integer",  "Sol_argile"]
    dictEnteteVignoble[ "mo"]       = [ "Sol_MO", "Real",  "Sol_MO"]      
    dictEnteteVignoble[ "CN"]       = [ "Sol_CsurN", "Integer",  "Sol_CsurN"]      
    #dictEnteteVignoble[ "PH"]       = ["sol_PH","Real","sol_PH"]   
    dictEnteteVignoble[ "rendement"]       = [ "Rendement", "Real",  "Rendement"]      
    dictEnteteVignoble[ "poids_moy_grappes"]       = [ "Poids_moye", "Integer",  "Poids_moye"]      
    dictEnteteVignoble[ "nb_grappes"]       = [ "Nombre_gra", "Integer",  "Nombre_gra"]      
    dictEnteteVignoble[ "interrangs"]   = [ "interrang", "Integer", "interrang"]
    dictEnteteVignoble[ "interceps"]    = [ "intercep" , "Integer",  "intercep"]
    dictEnteteVignoble[ "hauteur"] = [ "hauteur" , "Integer",  "hauteur"]
    dictEnteteVignoble[ "densite"] = [ "densite_sarment", "Real",  "densite_sa"] 
    
    # Requis, on trouve le nom pour chaque cas de format de sortie (CSV ou SHP)
    champs_vignoble_requis = [ "campagne", "nom_parcelle", "interrangs", "interceps", "hauteur", "densite"]
    champs_agro_fichier = []
    champs_agro_autre_fichier = []
    types_agro = []
    for champ in champsVignobleOrdonnes:
        champs_agro_fichier.append( dictEnteteVignoble[champ][ position_dic])
        champs_agro_autre_fichier.append( dictEnteteVignoble[champ][ position_autre])
        types_agro.append( dictEnteteVignoble[champ][ 1])
    #physiocap_log("Les types {}".format( types_agro), TRACE_AGRO)
    champs_vignoble_requis_fichier = []
    for champ in champs_vignoble_requis:
        champs_vignoble_requis_fichier.append( dictEnteteVignoble[champ][ position_dic])
    return champsVignobleOrdonnes, champs_agro_fichier, types_agro, champs_agro_autre_fichier, \
        champs_vignoble_requis, champs_vignoble_requis_fichier, dictEnteteVignoble
    
def quelles_informations_vignoble_source_onglet( self, format_sortie ='AGRO_CSV'):
    """ Mettre les valeurs d'info vignobles dans l'ordre et dans un dict 
        puis création de deux listes entetes et valeurs pretes à écrite dans 
        CSVT si format_sortie = CSV ou Shape sinon""" 
    position_dic = 0
    if format_sortie in [ "AGRO_CSV",  "CSV"]:
        position_dic = 0
    elif format_sortie in [ "AGRO_SHP",  "SHP"]:
        position_dic = 2
    champsVignobleOrdonnes, champs_agro_fichier, _, _, champs_vignoble_requis, champs_vignoble_requis_fichier, dictEnteteVignoble \
        = structure_informations_vignoble( self, format_sortie)
    dictInfoVignoble = {}
    valeurNA = ""    
    dictInfoVignoble[ "campagne"]       = self.lineEditCampagne.text()
    dictInfoVignoble[ "nom_parcelle"]   = self.lineEditNomParcelle.text()
    dictInfoVignoble[ "commune"]        = self.comboBoxCommune.currentText()
    dictInfoVignoble[ "region"]         = self.comboBoxRegion.currentText()
    dictInfoVignoble[ "cepage"]         = self.comboBoxCepage.currentText()
    dictInfoVignoble[ "clone"]          = self.lineEditClone.text()
    dictInfoVignoble[ "porte_greffe"]   = self.lineEditPorteGreffe.text()
    dictInfoVignoble[ "annee_plantation"] = int( self.spinBoxAnneePlant.value())
    details = "YES" if self.groupBoxDetailVignoble.isChecked() else "NO"
    dictInfoVignoble[ "details"] = details
    dictInfoVignoble[ "max_sarments_metre"]  = int( self.spinBoxMaxSarmentsParMetre.value())
    dictInfoVignoble[ "interrangs"]          = int( self.spinBoxInterrangs.value())
    dictInfoVignoble[ "interceps"]           = int( self.spinBoxInterceps.value())
    dictInfoVignoble[ "hauteur"]             = int( self.spinBoxHauteur.value())
    dictInfoVignoble[ "densite"]             = float( self.doubleSpinBoxDensite.value())
    dictInfoVignoble[ "taille"]              = self.comboBoxTaille.currentText()
    if self.spinBoxArgile.value() != 'Inconnu':
        dictInfoVignoble[ "argile"] = int( self.spinBoxArgile.value())
    else:
        dictInfoVignoble[ "argile"] = valeurNA
    if self.doubleSpinBoxMO.value() != 'Inconnu':
        dictInfoVignoble[ "mo"] = float( self.doubleSpinBoxMO.value())
    else:
        dictInfoVignoble[ "mo"] = valeurNA
    if self.spinBoxCsurN.value() != 'Inconnu':
        dictInfoVignoble[ "CN"] = int( self.spinBoxCsurN.value())
    else:
        dictInfoVignoble[ "CN"] = valeurNA    
    if self.doubleSpinBoxPH.value() != 'Inconnu':
        dictInfoVignoble[ "PH"] = float( self.doubleSpinBoxPH.value())
    else:
        dictInfoVignoble[ "PH"] = valeurNA
    if self.doubleSpinBoxRendement.value() != 'Inconnu':
        dictInfoVignoble[ "rendement"] = float( self.doubleSpinBoxRendement.value())
    else:
        dictInfoVignoble[ "rendement"] = valeurNA
    if self.spinBoxPoidsMoyenGrappes.value() != 'Inconnu':
        dictInfoVignoble[ "poids_moy_grappes"] = int( self.spinBoxPoidsMoyenGrappes.value())
    else:
        dictInfoVignoble[ "poids_moy_grappes"] = valeurNA    
    if self.spinBoxNbGrappes.value() != 'Inconnu':
        dictInfoVignoble[ "nb_grappes"] = int( self.spinBoxNbGrappes.value())
    else:
        dictInfoVignoble[ "nb_grappes"] = valeurNA    
    listeEntete = []
    listeInfo = []
    for unChamp in champsVignobleOrdonnes:
        listeEntete.append( dictEnteteVignoble[ unChamp][position_dic])
        listeInfo.append( dictInfoVignoble[ unChamp])
    #physiocap_log( "Derniere liste Agro : {}".format(listeInfo), TRACE_TOOLS)
    return champsVignobleOrdonnes, champs_vignoble_requis_fichier,  dictInfoVignoble, listeInfo,  dictEnteteVignoble, listeEntete

def quel_qml_existe( qml_court, repertoire_template, repertoire_secours):
    """ Rend le template qui existe"""
    le_template = os.path.join( repertoire_template, qml_court)
    if ( os.path.exists( le_template)):
        return le_template
    else:
        le_template = os.path.join( repertoire_secours, qml_court)
        if ( os.path.exists( le_template)):
            return le_template
    return None

def quel_chemin_templates( self):
    self.dans_Quel_Settings()
    Nom_Profil =  self.fieldComboProfilPHY.currentText()
    # Remplissage de la liste de CHEMIN_TEMPLATES
    self.fieldComboThematiques.setCurrentIndex( 0)   
    if len( CHEMIN_TEMPLATES) == 0:
        self.fieldComboThematiques.clear( )
        aText = self.tr( "Pas de répertoire de thématiques pré définie")
        physiocap_log( aText, leModeDeTrace)
        physiocap_error( self, aText)
    else:
        leChoixDeThematiques = int( self.settings.value("Style/leChoixDeThematiques", 0)) 
        # Cas inital
        CHEMIN_TEMPLATES_USER = []
        self.fieldComboThematiques.clear( )
        CHEMIN_TEMPLATES_COURT = os.path.join( self.plugin_dir, CHEMIN_TEMPLATES[0])
        if Nom_Profil == 'Champagne':
            chemin_qml = os.path.join( CHEMIN_TEMPLATES_COURT, Nom_Profil)
            CHEMIN_TEMPLATES_USER.append( chemin_qml)
            chemin_secours = os.path.join( CHEMIN_TEMPLATES_COURT, 'Standard')
        else:
            chemin_qml = os.path.join( CHEMIN_TEMPLATES_COURT, 'Standard')
            chemin_secours = chemin_qml
            CHEMIN_TEMPLATES_USER.append( chemin_qml)
        # On donne le chemin QGIS ou celui présent dans les preferences
        if leChoixDeThematiques == 1:
            chemin_preference_court = self.settings.value("Style/leDirThematiques", \
                os.path.join( self.gis_dir, CHEMIN_TEMPLATES[1]))
        else:
            # cas QGIS pour le premier cas
            chemin_preference_court = os.path.join( self.gis_dir, CHEMIN_TEMPLATES[1])
        chemin_preference = os.path.join( chemin_preference_court, 'Standard')                
        CHEMIN_TEMPLATES_USER.append( chemin_preference)
        self.fieldComboThematiques.addItems( CHEMIN_TEMPLATES_USER )

        # Le combo a déjà été rempli, on retrouve le choix
        self.fieldComboThematiques.setCurrentIndex( leChoixDeThematiques)
        if ( leChoixDeThematiques == 1): 
            # Qans le cas où l'utilisateur a pris la main sur ces qml
            # autorisation de modifier les noms de qml
            self.groupBoxThematiques.setEnabled( True)
            # Renommage V3
            themeDiametre = self.settings.value("Style/themeDiametre", "Filtre diamètre")
            self.lineEditThematiqueDiametre.setText( themeDiametre )
            themeSarment = self.settings.value("Style/themeSarment", "Filtre sarment")
            self.lineEditThematiqueSarment.setText( themeSarment )
            themeBiomasse = self.settings.value("Style/themeBiomasse", "Filtre biomasse")
            self.lineEditThematiqueBiomasse.setText( themeBiomasse )
            themeVitesse = self.settings.value("Style/themeVitesse", "Filtre vitesse")
            self.lineEditThematiqueVitesse.setText( themeVitesse )
            themePasMesure = self.settings.value("Style/themePasMesure", "Filtre pas de mesure")
            self.lineEditThematiquePasMesure.setText( themePasMesure )
            themeSegment = self.settings.value("Style/themeSegment", "Filtre segment")
            self.lineEditThematiqueSegment.setText( themeSegment )
            themeSegmentBrise = self.settings.value("Style/themeSegmentBrise", "Filtre segment brisé")
            self.lineEditThematiqueSegmentBrise.setText( themeSegmentBrise )
            themeContour = self.settings.value("Style/themeContour", "Contours")
            self.lineEditThematiqueContour.setText( themeContour )
            # Inter
            themeDiametre = self.settings.value("Style/themeInterDiametre", "Inter diamètre")
            self.lineEditThematiqueInterDiametre.setText( themeDiametre )
            themeSarment = self.settings.value("Style/themeInterSarment", "Inter sarment")
            self.lineEditThematiqueInterSarment.setText( themeSarment )
            themeBiomasse = self.settings.value("Style/themeInterBiomasse", "Inter biomasse")
            self.lineEditThematiqueInterBiomasse.setText( themeBiomasse )

            themeAltitude = self.settings.value("Style/themeInterAltitude", "Inter altitude")
            self.lineEditThematiqueInterAltitude.setText( themeAltitude )
            # inter Libelle
            themeLibelle = self.settings.value("Style/themeInterLibelle", "Inter parcelles")
            self.lineEditThematiqueInterLibelle.setText( themeLibelle )
            # inter moyenne et points
            themeMoyenne = self.settings.value("Style/themeInterMoyenne", "Inter parcelle")
            self.lineEditThematiqueInterMoyenne.setText( themeMoyenne )
            themePoints = self.settings.value("Style/themeInterPoints", "Filtre diamètre 3D")
            self.lineEditThematiqueInterPoints.setText( themePoints )
            themeInterPasMesure = self.settings.value("Style/themeInterPasMesure", "Inter pieds manquants")
            self.lineEditThematiqueInterPasMesure.setText( themeInterPasMesure )
            themeSegment = self.settings.value("Style/themeInterSegment", "Inter Segment")
            self.lineEditThematiqueInterSegment.setText( themeSegment )
            themeSegmentBrise = self.settings.value("Style/themeInterSegmentBrise", "Inter Segment Brise")
            self.lineEditThematiqueInterSegmentBrise.setText( themeSegmentBrise )
            # intra
            themeIso = self.settings.value("Style/themeIntraIso", "Isolignes")
            self.lineEditThematiqueIntraIso.setText( themeIso )
            themeImage = self.settings.value("Style/themeIntraImage", "Intra")
            self.lineEditThematiqueIntraImage.setText( themeImage )
            themePDF = self.settings.value("Style/themeIntraPDF", "PDF")
            self.lineEditThematiqueIntraPDF.setText( themePDF )
        else:
            # Cas répertoire du plugin
            self.groupBoxThematiques.setEnabled( False)
            # Remettre les nom de thematiques par defaut 
            self.lineEditThematiqueDiametre.setText("Filtre diamètre")
            self.settings.setValue("Style/themeDiametre", "Filtre diamètre")
            self.lineEditThematiqueSarment.setText("Filtre sarment")
            self.settings.setValue("Style/themeSarment", "Filtre sarment")
            self.lineEditThematiqueBiomasse.setText("Filtre biomasse")
            self.settings.setValue("Style/themeBiomasse", "Filtre biomasse")
            self.lineEditThematiqueVitesse.setText("Filtre vitesse")
            self.settings.setValue("Style/themeVitesse", "Filtre vitesse")
            self.lineEditThematiquePasMesure.setText("Filtre pas de mesure")
            self.settings.setValue("Style/themePasMesure", "Filtre pas de mesure")
            self.lineEditThematiqueSegment.setText("Filtre segment")
            self.settings.setValue("Style/themeSegment","Filtre segment")
            self.lineEditThematiqueSegmentBrise.setText("Filtre segment brisé")
            self.settings.setValue("Style/themeSegmentBrise","Filtre segment brisé")
            self.lineEditThematiqueContour.setText("Contours")
            self.settings.setValue("Style/themeContour","Contours")
            # Inter
            self.lineEditThematiqueInterDiametre.setText("Inter diamètre")
            self.settings.setValue("Style/themeInterDiametre", "Inter diamètre")
            self.lineEditThematiqueInterSarment.setText("Inter sarment")
            self.settings.setValue("Style/themeInterSarment", "Inter sarment")
            self.lineEditThematiqueInterBiomasse.setText("Inter biomasse")
            self.settings.setValue("Style/themeInterBiomasse", "Inter biomasse")

            self.lineEditThematiqueInterAltitude.setText("Inter altitude")
            self.settings.setValue("Style/themeInterAltitude", "Inter altitude")
            
            self.lineEditThematiqueInterLibelle.setText("Inter parcelles")
            self.settings.setValue("Style/themeInterLibelle", "Inter parcelles")
            # inter moyenne et points
            self.lineEditThematiqueInterMoyenne.setText("Inter parcelle")
            self.settings.setValue("Style/themeInterMoyenne", "Inter parcelle")
            self.lineEditThematiqueInterPoints.setText("Filtre diamètre 3D")
            self.settings.setValue("Style/themeInterPoints", "Filtre diamètre 3D")     
            self.lineEditThematiqueInterPasMesure.setText("Inter pieds manquants")
            self.settings.setValue("Style/themeInterPasMesure", "Inter pieds manquants")
            self.lineEditThematiqueInterSegment.setText("Inter segment")
            self.settings.setValue("Style/themeInterSegment", "Inter segment")
            self.lineEditThematiqueInterSegmentBrise.setText("Inter segment brisé")
            self.settings.setValue("Style/themeInterSegmentBrise", "Inter segment brisé")
            # Intra
            self.lineEditThematiqueIntraIso.setText("Isolignes")
            self.settings.setValue("Style/themeIntraIso", "Isolignes")
            self.lineEditThematiqueIntraImage.setText("Intra")
            self.settings.setValue("Style/themeIntraImage", "Intra")
            self.lineEditThematiqueIntraPDF.setText( "PDF" )
            self.settings.setValue("Style/themeIntraPDF", "PDF")
    return chemin_qml, chemin_secours

def quel_noms_CSVT_synthese( self):
    """Rend les nom du CSV & CSVT & PRJ à créer"""
    #leModeDeTrace = self.fieldComboModeTrace.currentText()
    derniere_session = self.lineEditDerniereSession.text()
    chemin_session = os.path.join( self.lineEditDirectoryFiltre.text(), derniere_session)
    #quel_vecteur_demande = self.fieldComboFormats.currentText()
    version_3 = "YES" if self.checkBoxV3.isChecked() else "NO"
    # Nom du contour et du CSVT
    if version_3 == "YES":
        #chemin_MID = os.path.join( chemin_session, REPERTOIRE_SOURCE_V3)
        chemin_vecteur = os.path.join( chemin_session, REPERTOIRE_INTER_V3)        
    else:
        #chemin_MID = os.path.join( chemin_session, REPERTOIRE_SOURCES)
        chemin_vecteur = os.path.join( chemin_session, REPERTOIRE_SHAPEFILE)        
#    if quel_vecteur_demande == SHAPEFILE_NOM:
#        nomLongContour = os.path.join( chemin_MID, FICHIER_CONTOUR_GENERE + EXTENSION_SHP)
#    else:
#        physiocap_log( self.tr( "{0} ne reconnait pas les vecteurs {1} ").\
#                format( PHYSIOCAP_UNI, quel_vecteur_demande), leModeDeTrace)
#        raise physiocap_exception_vecteur_type_inconnu( quel_vecteur_demande)
    if self.fieldComboProfilPHY.currentText() == 'Champagne':
        nom_CSV = os.path.join( chemin_session, CVST_VIGNOBLE + EXTENSION_CSV)
        nom_CSVT = os.path.join( chemin_session, CVST_VIGNOBLE + EXTENSION_CSVT)
    else:
        nom_CSV = os.path.join( chemin_vecteur, CVST_VIGNOBLE + EXTENSION_CSV)
        nom_CSVT = os.path.join( chemin_vecteur, CVST_VIGNOBLE + EXTENSION_CSVT)

    return derniere_session, nom_CSV, nom_CSVT  

def appel_simplifier_processing( self, nom_point, algo_court, algo, params_algo,  
    nom_produit_algo,  deuxieme_nom = None):
    """
    Traite les appels à processing avec gestion du nom_produit_algo attendu
    Emet exception si pas de retour 
    """
    try :
        import processing
        try:
            from processing.core.Processing import Processing
            Processing.initialize()
        except:
            physiocap_log( self.tr( "{0} nécessite l'extension {1}").\
                format( PHYSIOCAP_UNI, self.tr("Traitement")), TRACE_TOOLS)
            raise physiocap_exception_no_processing( "Pas d'extension Traitement - initialize")               
    except ImportError:
        physiocap_log( self.tr( "{0} nécessite l'extension {1}").\
            format( PHYSIOCAP_UNI, self.tr("Traitement")), TRACE_TOOLS)
        raise physiocap_exception_no_processing( "Pas d'extension Traitement")

    mon_feedback = QgsProcessingFeedback()
    
    lettre_algo = algo[0]

    physiocap_log( self.tr( "={0}= Parametres pour algo {1} de nom long {2}\n{3}".\
                    format( lettre_algo, algo_court, algo , params_algo )), TRACE_TOOLS)       
    textes_sortie_algo = {}
    try:
        textes_sortie_algo = processing.run( algo, params_algo, feedback=mon_feedback)        
    except: # QgsProcessingException
        erreur_processing = self.tr("{0} Erreur durant création du produit par Processing de {1} nom long {2} : exception".\
                format( PHYSIOCAP_STOP, algo_court,  algo ))
        physiocap_error( self, erreur_processing)
        physiocap_log( erreur_processing, TRACE_INTRA)
        raise

    # Recherche nom_retour dans sortie_algo
    produit_algo = None
    try:
        produit_algo = textes_sortie_algo[ nom_produit_algo]
    except:
        erreur_processing = self.tr("{0} Erreur durant analyse du rendu de produit de {1} : texte produit {2}".\
                format( PHYSIOCAP_STOP, algo_court,  textes_sortie_algo ))
        physiocap_error( self, erreur_processing)
        physiocap_log( erreur_processing, TRACE_TOOLS)
        raise physiocap_exception_interpolation( nom_point)

    physiocap_log( "={0}= Produit en sortie de {1}\n{2}".\
                    format( lettre_algo, algo_court, produit_algo), TRACE_TOOLS)
    return produit_algo

def generer_contour_depuis_points( self, nom_fichier_shape_sans_0,  mids_trie):
    """ Générer un Contour à partir des points bruts"""

    version_3 = "YES" if self.checkBoxV3.isChecked() else "NO"
    # Assert points existent bien
    if ( os.path.exists( nom_fichier_shape_sans_0)):
        champsVignobleOrdonnes, _, dictInfoVignobleAgro, _, dictEnteteVignoble, _ = \
            quelles_informations_vignoble_source_onglet(self)
#        physiocap_log( 'Information vignoble et agro == Nom de parcelle contiendra Entete "{}" et Info "{}"'.\
#            format( champsVignobleOrdonnes[1], dictInfoVignobleAgro[ champsVignobleOrdonnes[1]]))
        nom_parcelle = dictInfoVignobleAgro[ champsVignobleOrdonnes[1]]        
        if nom_parcelle == "à préciser":
            nom_parcelle = self.lineEditSession.text()

        chemin_vecteur = os.path.dirname( nom_fichier_shape_sans_0)
        if version_3 == "YES":
            chemin_acces = os.path.join( os.path.dirname( chemin_vecteur), REPERTOIRE_SOURCE_V3)
        else:
            chemin_acces = os.path.join( os.path.dirname( chemin_vecteur), REPERTOIRE_SOURCES)
        chemin_fichier_convex = os.path.join( chemin_acces,  FICHIER_CONTOUR_GENERE + "_" + nom_parcelle + EXTENSION_SHP)
        QGIS_CONVEX = { 'FIELD' : None, 
         'INPUT' : nom_fichier_shape_sans_0, 
         'OUTPUT' : chemin_fichier_convex, 
         'TYPE' : 3 } # Enveloppe convexe
        algo = "qgis:minimumboundinggeometry"
        appel_simplifier_processing( self, nom_fichier_shape_sans_0, \
                "QGIS_CONVEX", algo, \
                QGIS_CONVEX, "OUTPUT")      
        #physiocap_log( "Sortie algo {} contient {}".format( algo, nom_retour), TRACE_JH)
        QgsMessageLog.logMessage( "PHYSIOCAP : après création du contour", "Processing", Qgis.Warning)

        # Changer attributs FID=0 nom parcelle
        convexhull_layer = QgsVectorLayer( chemin_fichier_convex, FICHIER_CONTOUR_GENERE , 'ogr')
        convexhull_layer.dataProvider().addAttributes([QgsField("FID", QVariant.Int, "integer", 10), \
                                                       QgsField("Nom_Parcel", QVariant.String, "string", 25)])
        convexhull_layer.updateFields()
        prov = convexhull_layer.dataProvider()
        field_names = [field.name() for field in prov.fields()]
           
        convexhull_layer.startEditing()
        for feat in convexhull_layer.getFeatures():
            convexhull_layer.changeAttributeValue(feat.id(), field_names.index('FID'), 0)
            convexhull_layer.changeAttributeValue(feat.id(), field_names.index('Nom_Parcel'),
                    nom_parcelle)
        convexhull_layer.commitChanges()
        self.settings.setValue("Physiocap/chemin_contour_genere", chemin_fichier_convex)
    else:
        msg = "Erreur durant génération automatique de contour : fichier de point {} n'existe pas\n".\
            format( nom_fichier_shape_sans_0)
        physiocap_error( self, msg )
    return chemin_fichier_convex

def assert_quel_format_entete( self, origine_poly):
    indice_dict_Entete = 2
    if origine_poly in [ "AGRO_CSV",  "CSV"]:
        indice_dict_Entete = 0
    elif origine_poly in [ "AGRO_SHP",  "SHP"]:
        indice_dict_Entete = 2
    else:
        aText = "Vecteur AGRO de format {} n'est pas pris en compte par l'extension".format( origine_poly)
        physiocap_log( aText)
        physiocap_error( self, aText, "CRITICAL")
    return indice_dict_Entete
    
def assert_parcelle_attendue( self, un_contour, les_parcelles_agro, modele_agro_retenu, \
    indice_dict_Entete, dictEnteteVignoble, champsVignobleOrdonnes,  libelle="INTRA"):
    """ Vérifier si la parcelle-campagne est bien celle qui va être utiliser pour 
    les informations agronomiques et INTER INTRA"""
    # La campagne_en_cours "n'est pas concerné" = self.lineEditCampagne.text()
    champ_campagne = dictEnteteVignoble[ champsVignobleOrdonnes[0]][indice_dict_Entete]
    champ_parcelle = dictEnteteVignoble[ champsVignobleOrdonnes[1]][indice_dict_Entete]
    nom_parcelle = un_contour[ champ_parcelle]
    nom_campagne = un_contour[ champ_campagne]
#                        nom_unique = "{1}{2}{0}{3}{0}{4}".format( SEPARATEUR_NOEUD, \
#                                NOM_PAR_DEFAUT, nombre_contours,  une_campagne, un_nom)
    if nom_parcelle not in les_parcelles_agro:
        physiocap_log( "XXX REJET P {} Parcelle {} rejettée sans modele dans parcelle agro".\
            format(libelle, nom_parcelle), TRACE_JH)
        return None
    try:
        un_unique = modele_agro_retenu[ nom_parcelle]
    except:
        # la parcelle n'est pas à calculer
        physiocap_log( "XXX REJET {} M Parcelle {} rejettée sans modele_agro_retenu {}".\
            format(libelle, nom_parcelle, modele_agro_retenu), TRACE_JH)
        return None

    nom_phy,  campagne_attendue, parcelle_attendue = un_unique.split( SEPARATEUR_NOEUD)
#    physiocap_log( "Parcelle {} attendue pour la campagne {}".\
#        format( parcelle_attendue, campagne_attendue), TRACE_JH)
    if nom_campagne != None and campagne_attendue != None:
        if int(nom_campagne) != int(campagne_attendue):                            
            physiocap_log( "XXX REJET C {} Parcelle {} rejettée ; sa campagne {} ne ne correspond pas à celle attendue {}".\
                format( libelle,  nom_parcelle, nom_campagne, campagne_attendue), TRACE_JH)
            # la campagne n'est pas à calculer
            return None
    if nom_campagne != None and campagne_attendue == None:
        physiocap_log( "XXX REJET C vide {} Parcelle {} rejettée ; sa campagne {} ne ne correspond pas à celle attendue {}".\
                format( libelle,  nom_parcelle, nom_campagne, campagne_attendue), TRACE_JH)
        return None
    if nom_campagne != None and campagne_attendue == None:
        physiocap_log( "XXX REJET C vide {} Parcelle {} rejettée ; sa campagne {} ne ne correspond pas à celle attendue {}".\
                format( libelle,  nom_parcelle, nom_campagne, campagne_attendue), TRACE_JH)
        return None
        
    #physiocap_log( "Parcelle {} retenue pour {} limiter par agro {}".format( nom_parcelle,libelle,  un_unique), TRACE_JH)
    return nom_parcelle

def assert_campagne( self, campagne, derniere_info_mid):
    """ Vérifier que campagne debut mid est la même que fin"""
    hemisphere = "Nord" if self.radioButtonNordPrecedent.isChecked() else "Sud"
    campagne_fin = quelle_campagne( self, derniere_info_mid)
    if campagne_fin != campagne:
        aText = "Les captures (MIDs) présentées pour cette session concernent deux campagnes {} et {}".\
            format( campagne, campagne_fin)
        aText = atext + "\nCe cas n'est pas prévu par l'extension. Choisir des MIDs d'une même campagne"
        return physiocap_error( self, aText )
    else:
        physiocap_log( "Choix hémisphère {} donne campagne {}".format( hemisphere, campagne))
        return campagne
        
def quelle_campagne( self, premiere_info_mid):
    """ A partir des dates debut des mid définir la campagne """
#    precedent = False
#    if self.radioButtonNordPrecedent.isChecked() or self.radioButtonSudPrecedent.isChecked():
#    precedent = True
    hemisphere = "Nord" if self.radioButtonNordPrecedent.isChecked() else "Sud"
    mon_info = premiere_info_mid.split(";")
    date_mid = mon_info[ 2]
    annee, mois = date_mid[0:7].split("-")
    if hemisphere == "Nord":
        if mois in ["01", "02", "03", "04"]:
            campagne_int = int( annee) - 1
        else:
            campagne_int = int( annee)
    else: # SUD
        campagne_int = int( annee)
#    physiocap_log( "Données {} an {} mois {} hémisphere {} : campagne {}".\
#        format( mon_info, annee, mois, hemisphere, str( campagne_int)))
    return str( campagne_int)

def quelle_liste_attributs( self, vecteur):
    provider = vecteur.dataProvider()
    field_names = [field.name() for field in provider.fields()]
    #physiocap_log( "Liste de champ a pour type {}".format( type( field_names)))
    #physiocap_log( "Attributs de {} sont {}".format( vecteur.name(), field_names ), TRACE_AGRO)
    provider = None
    return field_names
    
# Fonction pour générer le CSVT : csv avec info agro, moyenne et geometrie en WKT
def assert_champs_agro_obligatoires( dialogue, vecteur_poly, origine_poly):
    """ Controler les champs obligatoires dans CSV ou SHP du fichier agro d'origine 
        Retrouver les info agro servant de modeles
    """
    champsVignobleOrdonnes, champs_agro_fichier, type_agro, champs_agro_autre_fichier,  champs_vignoble_requis, \
        champs_vignoble_requis_fichier, dictEnteteVignoble = \
        structure_informations_vignoble( dialogue,  origine_poly)
    champExistants = quelle_liste_attributs( dialogue, vecteur_poly) 
    for champ in champs_vignoble_requis_fichier:
        if champ not in champExistants:
            physiocap_log("CAS ERREUR champs Existants {}".format( champExistants),  TRACE_JH)
            raise physiocap_exception_agro_obligatoire( "{} obligatoire (les champs obligatoires sont {}".\
                format(champ, champs_vignoble_requis_fichier))
    # Retrouver les campagne-parcelle qui servent d'informations
    nombre_contours = 0
    les_parcelles_agro = []
    liste_uniques = []
    modele_agro_retenu = {}
    # TODO CAMPAGNE Trier nom et campagne( ? Coallenscence ie champs_vignoble_requis_fichier[0]) et vérifier cas NULL
    for un_contour in vecteur_poly.getFeatures( QgsFeatureRequest().\
                    addOrderBy( champs_vignoble_requis_fichier[1])): #, champs_vignoble_requis_fichier[0])):
        un_nom = un_contour[ champs_vignoble_requis_fichier[1]]
        une_campagne = un_contour[ champs_vignoble_requis_fichier[0]]
        #physiocap_log( "Parcelle {} campagne {}".format( un_nom,une_campagne), TRACE_JH)
        if nombre_contours == 0:
            parcelle_en_cours = un_nom
            les_parcelles_agro.append(un_nom)
        if un_nom != parcelle_en_cours:
            # memoriser le dernier utile pour info agro
            modele_agro_retenu[ parcelle_en_cours] = nom_unique # le precedent
            parcelle_en_cours = un_nom
            les_parcelles_agro.append(un_nom)
        nom_unique = "{1}{2}{0}{3}{0}{4}".format( SEPARATEUR_NOEUD, \
            NOM_PAR_DEFAUT, nombre_contours,  une_campagne, un_nom)
        liste_uniques.append( nom_unique)
        nombre_contours = nombre_contours + 1
    # le dernier
    modele_agro_retenu[ parcelle_en_cours] = nom_unique # le precedent
    #physiocap_log( "Liste tous {0}".format( liste_uniques), TRACE_JH)
    #physiocap_log( "Liste parcelles agro {0}".format( les_parcelles_agro), TRACE_JH)
    for parcelle in les_parcelles_agro:
        try:
            un_unique = modele_agro_retenu[ parcelle]
            physiocap_log( "Parcelle {} retenue pour agro {}".format( parcelle, un_unique), TRACE_JH)
        except:
            physiocap_error( "Parcelle {} orpheline de données agro ".format( parcelle), TRACE_AGRO)
            pass
    return champsVignobleOrdonnes, champs_agro_fichier, type_agro, champs_agro_autre_fichier, champs_vignoble_requis, \
        champs_vignoble_requis_fichier, dictEnteteVignoble, champExistants, les_parcelles_agro, modele_agro_retenu        

def lister_parcelles_INTRA( self, vecteur = None,  liste = None):
    """ Met à jour la liste des parcelles à partir 
        du vecteur 
        ou une liste calculée """
    la_liste = []
    if vecteur != None:
        champ_choisi = self.fieldComboContours.currentText()
        self.fieldComboParcelleIntra.clear()
        for un_contour in vecteur.getFeatures( QgsFeatureRequest().addOrderBy( champ_choisi)):
            self.fieldComboParcelleIntra.addItem(  un_contour[ champ_choisi])
            la_liste.append( un_contour[ champ_choisi]) 
    elif liste != None:
        self.fieldComboParcelleIntra.clear()
        for un_contour in liste:
            self.fieldComboParcelleIntra.addItem(  un_contour)
        la_liste = liste
    
    laParcelle = self.settings.value("Intra/attributUneParcelle", "xx") 
    for idx, une in enumerate( la_liste):
        if ( une == laParcelle):
            self.fieldComboParcelleIntra.setCurrentIndex( idx)


def quelles_listes_info_agro( self): 
    """ Trouver les informations agro de toutes les parcelles
    les_infos_vignoble sont indexé par le nom du champ générique
    les_infos_agronomique sont indexé par le nom du champ dans le vecteur
    """
    Nom_Profil =  self.fieldComboProfilPHY.currentText()
    repertoire_data = self.lineEditDirectoryPhysiocap.text()
    if Nom_Profil != 'Champagne':
        raise physiocap_exception_agro_profil( 'Champagne')
        return None,  None, None
    else:
        # On prend un eventuel shp ou CSV dans rep des données brutes
        nom_vecteur, nom_court_vecteur,  libelle = quel_vecteur_dans_donnees_brutes( repertoire_data)
        if ((nom_vecteur != None) and len( nom_vecteur) > 0):                
            node_layer = nom_court_vecteur + SEPARATEUR_NOEUD + libelle + \
                SEPARATEUR_NOEUD + nom_vecteur
            self.comboBoxPolygone.addItem( node_layer)

        _, _, origine_poly, vecteur_poly, chemin_vecteur = quel_sont_vecteurs_choisis( self, "Filtrer")

        if ( vecteur_poly == None) or ( not vecteur_poly.isValid()):
            aText = self.tr( "Le contour précisant vos données agronomiques n'a pas toutes ces géométries valides pour QGIS.")
            aText = aText + self.tr( " Vérifiez-le dans QGIS=> Vecteur => Vérifier la validité ")
            aText = aText + self.tr( "Créer une nouvelle session Physiocap - bouton Filtrer les données brutes - ")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" ) 

        champsVignobleOrdonnes, champs_agro_fichier, types_agro, _, champs_vignoble_requis, champs_vignoble_requis_fichier, \
            dictEnteteVignoble, champExistants, les_parcelles_agro, modele_agro_retenu = \
            assert_champs_agro_obligatoires( self, vecteur_poly, origine_poly)

        les_infos_agronomiques_presence = []  # juste pour assertion de présence
        les_infos_agronomique = []
        les_infos_vignoble = []
        les_geometries_agronomique = []
        infos_agronomique_en_cours = {} # Conteneur provisoire
        # CSV ou SHP
        indice_dict_Entete = assert_quel_format_entete( self, origine_poly)

        for un_contour in vecteur_poly.getFeatures(QgsFeatureRequest().addOrderBy( champs_vignoble_requis_fichier[1])):
            # CSV
            nom_parcelle = dictEnteteVignoble[champsVignobleOrdonnes[1]][indice_dict_Entete]
            un_nom = un_contour[ nom_parcelle]
            if un_nom not in les_parcelles_agro:
                continue
            # Champs requis on tester la présence et le type
            for pos_champ, le_champ in enumerate( champs_vignoble_requis):
                champ_fichier = champs_vignoble_requis_fichier[ pos_champ]
                try:
                    les_infos_agronomiques_presence.append( un_contour[ champ_fichier])
                except:
                    raise physiocap_exception_agro_obligatoire( "{} obligatoire (les champs obligatoires sont {})".\
                        format( champ_fichier, champs_vignoble_requis_fichier))
                    
            # ASSERT type
            for pos_champ, le_champ in enumerate( champs_vignoble_requis):
                champ_fichier = champs_vignoble_requis_fichier[ pos_champ]
                try:
                    type_attendu = dictEnteteVignoble[ le_champ][1]
                    if type_attendu == "String":
                        infos_agronomique_en_cours[ le_champ] = un_contour[ champ_fichier]
                    elif type_attendu == "Real":
                        infos_agronomique_en_cours[ le_champ] = float( un_contour[ champ_fichier])
                    elif type_attendu == "Integer":
                        infos_agronomique_en_cours[ le_champ] = int( un_contour[ champ_fichier])
                    else:
                        physiocap_error("Type {} n'est pas prévu par extension".format(type_attendu),  TRACE_JH)
                except:
                    raise physiocap_exception_agro_type_champ( "{} n'a pas le type attendu {}".\
                        format( champ_fichier, type_attendu))
            #physiocap_log( "Info vignoble : {}".format( infos_agronomique_en_cours),  "TOUS")
            les_infos_vignoble.append( infos_agronomique_en_cours)
            
            infos_agronomique_en_cours = {}
            # Autres champs agro
            for pos_champ, le_champ in enumerate( champs_agro_fichier):
                champ_fichier = champs_agro_fichier[ pos_champ]
                infos_agronomique_en_cours[ champ_fichier] = un_contour[ champ_fichier]
            les_infos_agronomique.append( infos_agronomique_en_cours)
            infos_agronomique_en_cours = {}
            # Geometrie
            if origine_poly in [ "AGRO_CSV", "CSV"]:
                try:
                    les_geometries_agronomique.append(  un_contour.geometry())
                except:
                    physiocap_error( self, "Contour CSV n'a pas de géométrie")
                    raise
            else:
                les_geometries_agronomique.append(  un_contour.geometry())
        #physiocap_log( "Synthèse geom : {}".format( les_geometries_agronomique))

        return les_parcelles_agro, les_geometries_agronomique, les_infos_agronomique, les_infos_vignoble 
 
def ajouter_csvt_source_contour( self, la_projection_TXT, vecteur_poly, les_parcelles,  les_geoms_poly, les_moyennes_par_contour):
    """Ajouter au CSVT AGRO les informations de moyennes calculées et du vignoble """
    # Retrouver le nom du CSVT ou SHP pour copie (sauf les infos du shp)
    campagne_en_cours = self.lineEditCampagne.text()
####    Repertoire_Donnees_Brutes = self.lineEditDirectoryPhysiocap.text()
####    nom_vecteur, nom_court_vecteur,  libelle = \
####        quel_vecteur_dans_donnees_brutes( Repertoire_Donnees_Brutes)
    _, _, origine_poly, vecteur_poly, chemin_vecteur = quel_sont_vecteurs_choisis( self, "Filtrer")
    _, nom_CSV, nom_CSVT = quel_noms_CSVT_synthese( self)        
    if ((vecteur_poly != None) and len( chemin_vecteur) > 0):
        if origine_poly in [ "AGRO_CSV",  "CSV"]:
            # Copier le CSV de contour
            shutil.copyfile( nom_vecteur, nom_CSV)
        else:
            aText = "Dans le cas d'un shapefile AGRO, le CSVT de synthese ne contient pas les "
            aText = aText + "informations agro des autres campagnes"
            physiocap_log( aText, "Attention")
            exemple_CSV = os.path.join( os.path.join( self.plugin_dir, CHEMIN_DATA), 'exemple_vide_contour_vignoble.csv')        
            if os.path.isfile( exemple_CSV):
                shutil.copyfile( exemple_CSV, nom_CSV)
        # Base exemple CSV
        exemple_CSVT = os.path.join( os.path.join( self.plugin_dir, CHEMIN_DATA), 'exemple_contour_vignoble.csvt')        
        if os.path.isfile( exemple_CSVT):
            shutil.copyfile( exemple_CSVT, nom_CSVT)
        # Creer .prj et .qpj
        creer_extensions_pour_projection( nom_CSV, la_projection_TXT)
    # Récuperer les infos agro
    les_parcelles_agro, les_vecteurs_agronomique, les_infos_agronomique, _ = quelles_listes_info_agro(self)
    champsMoyenneOrdonnes, listeEnteteMoyenne, listeEnteteMoyenne_SHP = quelles_informations_moyennes()    
    # Pour retrouver l'entete mais pas les infos saisie dans onglet
    champsVignobleOrdonnes, _, dictInfoVignoble, _,  dictEnteteVignoble, listeEntete = \
        quelles_informations_vignoble_source_onglet( self)    
    
    # TODO si besoin ASSERT Entetes identiques
    
    # ASSERT Le fichier de synthese existe
    if not os.path.isfile( nom_CSV):
        uMsg =u"Le CSVT " + nom_CSV + " n'existe pas..."
        physiocap_log( uMsg)
        return physiocap_error( self, uMsg)
    else:
        # Ecriture CSVT avec agro et moyenne
        fichier_CSVT = open( nom_CSV, "a")
        writerCSVT = csv.writer( fichier_CSVT, delimiter=CSV_DELIMITER_POINT_VIRGULE)        
        # Retrouver l'entete mais pas les infos saisie dans onglet
        if origine_poly in [ "AGRO_CSV",  "CSV"]:
            _, _, _, _,  _, listeEntete = quelles_informations_vignoble_source_onglet( self, origine_poly)    
            if self.checkBoxDoubleEnteteCSV.isChecked():
                # Ecriture de l'entête et des infos vignobles
                writerCSVT.writerow( [  CSV_GEOM] + listeEntete + listeEnteteMoyenne)
        if origine_poly in [ "AGRO_SHP",  "SHP"]:
            _, _, _, _,  _, listeEntete = quelles_informations_vignoble_source_onglet( self, origine_poly)    
        
        # Boucler sur les parcelles
        for parcelleId,  parcelleNom in enumerate( les_parcelles):
#            physiocap_log ( "AJOUT Physiocap moyenne de {} la {} ieme parcelle a pour diam : {}".
#            format( parcelleNom,  parcelleId, les_moyennes_par_contour[parcelleId].get( 'diam')), TRACE_AGRO)
            geomContour = QgsGeometry.fromMultiPolygonXY( les_geoms_poly[ parcelleId])
            # Calculer geomWKT à partir de geom du contour
            geomWKT = str( geomContour.asWkt())
            
            lesMoyennesOrdonnees = []
            for unChamp in champsMoyenneOrdonnes:
                lesMoyennesOrdonnees.append( round( les_moyennes_par_contour[parcelleId].get( unChamp), 2)) 
#            physiocap_log ( "AJOUT Physiocap moyennes du contour {}: {}".\
#                format( les_parcelles[parcelleId], lesMoyennesOrdonnees), TRACE_AGRO)
            # Retrouver index de la parcelle dans parcelle agro
            listeInfo = []
            if parcelleNom in les_parcelles_agro:
                index_parcelle = les_parcelles_agro.index( parcelleNom)
#                physiocap_log ( "Parcelle {}: id {} et valeur {}".\
#                    format( parcelleNom, index_parcelle,  parcelleId), TRACE_AGRO)
                for un_champ in listeEntete:
                    if un_champ == 'Nom_Parcel':
                        listeInfo.append( parcelleNom)
                        continue
                    if un_champ == 'Campagne':
                        listeInfo.append( campagne_en_cours)
                        continue
                    listeInfo.append( les_infos_agronomique[ index_parcelle].get( un_champ)) 
                physiocap_log ( "AJOUT Physiocap agro du contour {}: {}".\
                    format( les_parcelles_agro[ index_parcelle], listeInfo), "IMPORT_CSV")
                writerCSVT.writerow( [ geomWKT] + listeInfo  +  lesMoyennesOrdonnees)
            else:
                # envisager un message
                pass
        fichier_CSVT.close()
    
    return 0
   
def creer_csvt_source_onglet( self, la_projection_TXT, les_parcelles, les_geoms_poly, les_moyennes_par_contour):
    """Créer CSVT avec les informations de moyenne & l'onglet Agronomie"""
    #leModeDeTrace = self.fieldComboModeTrace.currentText()
    # Récupération des moyennes du contour
    lesMoyennesOrdonnees = []
    champsMoyenneOrdonnes, listeEnteteMoyenne, _ = quelles_informations_moyennes()    
#    physiocap_log ( "CREER Physiocap parcelles : {}".format( les_parcelles), TRACE_JH)
#    physiocap_log ( "CREER Physiocap moyennes par contour : {}".format( les_moyennes_par_contour), TRACE_JH)
    for parcelleId,  parcelleNom in enumerate( les_parcelles):
#        physiocap_log ( "CREER Physiocap moyenne de {} la {} ieme parcelle a pour diam : {}".
#         format( parcelleNom,  parcelleId, les_moyennes_par_contour[parcelleId].get( 'diam')), TRACE_JH)
        geomContour = QgsGeometry.fromMultiPolygonXY( les_geoms_poly[ parcelleId])
#        physiocap_log ( "CREER Physiocap geom de {} pour geom : {}".
#         format( parcelleNom,  geomContour), TRACE_JH)

        for unChamp in champsMoyenneOrdonnes:
            lesMoyennesOrdonnees.append( round( les_moyennes_par_contour[parcelleId].get( unChamp), 1)) 
    physiocap_log ( "CREER Physiocap moyennes du contour {}: {}".\
        format( les_parcelles[parcelleId], lesMoyennesOrdonnees), TRACE_JH)
    # Identifier ? si plusieurs parcelles ?
    #Calculer geomWKT à partir de geom du contour
    geomWKT = str( geomContour.asWkt())

    _, nom_CSV, nom_CSVT = quel_noms_CSVT_synthese( self)
    champsVignobleOrdonnes, _, dictInfoVignoble, listeInfo,  dictEnteteVignoble, listeEntete = \
        quelles_informations_vignoble_source_onglet( self)
    
    # ASSERT listes ont la même taille
    if (len( listeEntete) != len( listeInfo)):
        uMsg = "CREER Liste entete CSVT ({}) et info vignoble ({}) n'ont pas la même taille".\
            format( len( listeEntete), len( listeInfo))
        physiocap_log( uMsg, "Attention")
        return physiocap_error( self, uMsg)
        
    # ASSERT Le fichier de synthese existe
    if os.path.isfile( nom_CSV):
        uMsg =u"Le CSVT " + nom_CSV + " existe dejà"
        physiocap_log( uMsg)
        return physiocap_error( self, uMsg)
    else:
        # Ecriture CSVT avec agro et moyenne
        fichier_CSVT = open( nom_CSV, "w")
        writerCSVT = csv.writer( fichier_CSVT, delimiter=CSV_DELIMITER_POINT_VIRGULE)
        # Ecriture de l'entête et des infos vignobles
        writerCSVT.writerow( [  CSV_GEOM] + listeEntete + listeEnteteMoyenne)
        writerCSVT.writerow( [ geomWKT] + listeInfo  +  lesMoyennesOrdonnees)
        fichier_CSVT.close()
        
        # Base exemple CSV
        exemple_CSVT = os.path.join( os.path.join( self.plugin_dir, CHEMIN_DATA), 'exemple_contour_vignoble.csvt')        
        if os.path.isfile( exemple_CSVT):
            shutil.copyfile( exemple_CSVT, nom_CSVT)
        # Creer .prj et .qpj
        creer_extensions_pour_projection( nom_CSV, la_projection_TXT)
    return 0

# TOOLS
def physiocap_write_in_synthese( self, aText):
    """Write a text in the results list"""
    self.textEditSynthese.insertPlainText( aText)   
  
def physiocap_is_only_ascii(s):
    if isinstance( s, unicode):
        physiocap_log( "physiocap_is_only_ascii {0}".format( "Cas unicode"), TRACE_TOOLS)
        try:
            s.encode('ascii')
            physiocap_log( "physiocap_is_only_ascii {0} : resultat OK {1}".format( "apres encode", s.encode('ascii')), TRACE_TOOLS)
        except UnicodeEncodeError:
            physiocap_log( "physiocap_is_only_ascii {0}".format( "dans exception"), TRACE_TOOLS)
            return False
    else:
        physiocap_log( "physiocap_is_only_ascii {0}".format( "Non unicode"), TRACE_TOOLS)
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
    
def creer_extensions_pour_projection( nom_couche, laProjection):
    """Creer les fichiers de projection de la couche pour .prj et .qpj"""
    if (nom_couche == None) or (nom_couche == ""):
        return
    # Supprimer extension
    pos_extension = nom_couche.rfind(".")
    #physiocap_log( "Nom sans extension {} ".format( nom_couche[:pos_extension]),  TRACE_JH )
    for une_extension in [ EXTENSION_PRJ, EXTENSION_QPJ]:
        nouveau_nom = nom_couche[:pos_extension] + une_extension
        #physiocap_log( "Nouvelle extension {} ".format( nouveau_nom), TRACE_JH )
        if (not os.path.exists(nouveau_nom)) :
            # Retrouver le modele pour la projection
            if ( laProjection == PROJECTION_L93) or ( laProjection == EPSG_NUMBER_L93):
                chemin_modele = os.path.join( CHEMIN_PROJECTION, PROJECTION_L93 + une_extension)
            elif ( laProjection == PROJECTION_GPS) or ( laProjection == EPSG_NUMBER_GPS):
                chemin_modele = os.path.join( CHEMIN_PROJECTION, PROJECTION_GPS + une_extension)
            elif ( laProjection == PROJECTION_CC45) or ( laProjection == EPSG_NUMBER_CC45):
                chemin_modele = os.path.join( CHEMIN_PROJECTION, PROJECTION_CC45 + une_extension)
            else:
                chemin_modele = "inconnu"
            #physiocap_log( "Chemin modele {} ".format( chemin_modele), TRACE_JH)
            if chemin_modele == "inconnu" or not os.path.exists( chemin_modele):
                # TODO ? message erreur 
                physiocap_log( "Aucun modèle n'existant pour la projection {} (dans {}) : l'extension {} n'estpas créée".\
                    format( laProjection, CHEMIN_PROJECTION, une_extension), TRACE_TOUT )
                continue
            # Copie
            shutil.copyfile( chemin_modele, nouveau_nom)
    return

def physiocap_nom_entite_sans_pb_caractere( un_nom,  mon_unique = 0):
    """Change la chaine un_nom selon qu'elle contient ou non le caractère ' ou blanc"""
    ## Cela peut ne rien faire
    return un_nom.replace(" ",SEPARATEUR_).replace("\'", SEPARATEUR_)
     
def physiocap_nom_entite_avec_pb_caractere( un_nom, un_texte = "GDAL"):
    """rend True si la chaine un_nom contient un caractère ' problématique pour la librairie : un_texte"""
    if un_texte == "GDAL" and type(un_nom) == str:
        # Tester si une cote '
        if un_nom.find('\'') >= 0:
            return True
        if un_nom.find(' ') >= 0:
            return True
#    else:
#        physiocap_log( "pb GDAL {0}".format( type(un_nom)), TRACE_TOOLS)
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
    physiocap_log( "Recherche {0}".format( layerURI), TRACE_TOOLS)
    # BUG 7 melange des / et \ en V3. On repasse tout en "/"
    layerURI_nettoye = layerURI.replace("\\", "/")
    physiocap_log( "Modifié>> {0}".format( layerURI_nettoye), TRACE_TOOLS)
    for layerID in ids:
        # Retrouver le layer
        layer = root.findLayer( layerID).layer()
        URI_complet = layer.dataProvider().dataSourceUri()
        # Enlever la mention |layerid à la fin de l'URI
        pos_fin_layer = URI_complet.rfind( "|layerid=")
        URI_vecteur = URI_complet[:pos_fin_layer]
        physiocap_log( "Layer URI {0}".format( URI_vecteur), TRACE_TOOLS)
        if layer is not None and layer.type() == QgsMapLayer.VectorLayer and \
            (URI_vecteur == layerURI_nettoye or URI_vecteur == layerURI):
            trouve = "YES"
            physiocap_log( "Layer retrouvé  {0}".format( layer.name()), TRACE_TOOLS)
            # The layer is found
            break
    if ( trouve == "YES"):
        if layer.isValid():
            return layer
        else:
            physiocap_log( "Layer trouvé  {0} mais invalide".format( layer.name()), "Attention")
            return None
    else:
        return None

def physiocap_get_layer_by_name( layerName):
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

def physiocap_get_layer_by_ID( layerID,  layerName = None):
    """ Retrouve un layer ID dans la map Tree Root
       Option si layerName est proposé et que l'on ne trouve pas par id, on cherche par nom
    Rend le layer si il est valide
    """
    layer_trouve = None
    root = QgsProject.instance().layerTreeRoot()
    ids = root.findLayerIds() #  Inutile : root.findLayers()

    trouve = "NO"
    for id in ids:
        if id == layerID:
            #physiocap_log( "Layer retrouvé : " + str( layerID), TRACE_TOOLS)
            layer_trouve = root.findLayer( layerID)
            le_layer = layer_trouve.layer()
            trouve = "YES"
            break
    if ( trouve == "YES"):
        if ( le_layer.isValid()):
            return le_layer
        else:
            return None
    else:
#        physiocap_log( "=#=#=#=#=#=#  Aucune couche retrouvée pour ID : {0} et par nom ?".\
#            format(  str( layerID)), TRACE_TOOLS)
        if  layerName != None:
#            physiocap_log( "=#=#=#=#=#=# Recherche par nom : {}".\
#                format( layerName), TRACE_TOOLS)
            le_layer = physiocap_get_layer_by_name( layerName )
            return le_layer
        return None
  
def quelle_projection_et_format_vecteur( self):
    """ Selon la valeur cochée dans le radio de projection 
    positionne laProjection (en QgsCoordinateReferenceSystem, texte et nombre (epsg)
    les nom d'extensions EXTENSION_VECTEUR sont rendu avec la projection de l'EPSG
    pour les EXTENSION_RASTER en tiff ou selon la demande SAGA
    Rend aussi un transform_context & QgsDistanceArea pour cet EPSG
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
    # TODO : A_TESTER Récuperer le CRS du projet QGIS et le compare au choix
#    laProjection_str = str( la_projection_CRS.postgisSrid())
#    if la_projection_CRS.isValid():
#        physiocap_log("Projection {0} des shapefiles est demandée : {1} est un EPSG valide".\
#            format( la_projection_TXT, laProjection_str), TRACE_TOOLS)

    quel_vecteur_demande = self.fieldComboFormats.currentText()
    if quel_vecteur_demande == SHAPEFILE_NOM:
        EXTENSION_CRS_VECTEUR = SEPARATEUR_ + la_projection_TXT + EXTENSION_SHP
        DRIVER_VECTEUR = SHAPEFILE_DRIVER
    elif quel_vecteur_demande == GEOJSON_NOM:
        EXTENSION_CRS_VECTEUR = SEPARATEUR_ + la_projection_TXT + EXTENSION_GEOJSON
        DRIVER_VECTEUR = GEOJSON_DRIVER  
    else:  # GEOPACKAGE est traité dans le code filtrer
        EXTENSION_CRS_VECTEUR = SEPARATEUR_ + la_projection_TXT + EXTENSION_SHP
        DRIVER_VECTEUR = SHAPEFILE_DRIVER
        
    # Cas du nom du raster 
    if self.radioButtonSAGA.isChecked():
        if self.checkBoxSagaTIFF.isChecked():
            EXTENSION_RASTER_COMPLET = SEPARATEUR_ + la_projection_TXT + EXTENSION_RASTER
        else:
            EXTENSION_RASTER_COMPLET = SEPARATEUR_ + la_projection_TXT + EXTENSION_RASTER_SAGA            
    else:
        EXTENSION_RASTER_COMPLET = SEPARATEUR_ + la_projection_TXT + EXTENSION_RASTER

    # Preparer les calculs de distance et de surface : distanceArea objet
    transform_context = QgsProject.instance().transformContext()
    distanceArea = physiocap_preparer_calcul_distance( self, mon_EPSG_number, la_projection_CRS, transform_context)

    return  distanceArea, self.fieldComboFormats.currentText(), EXTENSION_CRS_VECTEUR, DRIVER_VECTEUR, EXTENSION_RASTER_COMPLET, \
        transform_context, la_projection_CRS, la_projection_TXT, mon_EPSG_number

def physiocap_preparer_calcul_distance( self, EPSG_NUMBER, laProjectionCRS, transform_context):
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
        physiocap_log( "Calcul de distance Description SCR {0} est valide".\
        format( laProjectionCRS.description()), TRACE_TOOLS)
#        physiocap_log( "PROJ.4 SCR {0}".\
#        format( laProjectionCRS.toProj4()), TRACE_TOOLS)
    else:
        physiocap_log( "INVALIDE SCR", TRACE_TOOLS)
        return None
        
# OLD    distancearea.setSourceCrs( laProjectionCRS, QgsProject.instance().transformContext())            
    distancearea.setSourceCrs( laProjectionCRS, transform_context)            
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
            #physiocap_log("Nouveau chemin" + chemin, TRACE_TOOLS)
            
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
        #physiocap_log( "Chemin pour la création du fichier ==" + chemin, TRACE_TOOLS)
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
def quel_MID_dans_donnees_brutes( repertoire, recursif, exclusion="fic_sources"):
    """Fonction de recherche des ".MID". 
    Si recursif vaut "Oui", on scrute les sous repertoires à la recheche de MID 
    mais on exclut le repertoire de Exclusion dont on ignore les MID 
    """
    root_base = ""
    MIDs = []
    for root, dirs, files in os.walk( repertoire, topdown=True):
        if root_base == "":
            root_base = root
##        physiocap_log("ALL Root :" + str(root), TRACE_TOOLS)
##        physiocap_log("ALL DIR :" + str(dirs), TRACE_TOOLS)
##        physiocap_log("ALL FILE :" + str(files), TRACE_TOOLS)
        if exclusion in root:
            continue
        for name_file in files:
            if ".MID" in name_file[-4:]:
                MIDs.append( os.path.join( root, name_file))
    return sorted( MIDs)

def quel_vecteur_dans_donnees_brutes( Repertoire_Donnees_Brutes):
    """Cherche premier vecteur (shp puis csv) dans répertoire des données brutes (qui contient MID) 
    SHP prioritaires sur CSVT """
    #SHP
    nom_fichiers_recherches = os.path.join( Repertoire_Donnees_Brutes, RECHERCHE_EXTENSION_SHP)
    listeSHPTriee = sorted(glob.glob( nom_fichiers_recherches))
    if len( listeSHPTriee) == 0:
        physiocap_log( "Aucun vecteur de type SHAPEFILE dans répertoire des données brutes", TRACE_JH)
    else:
        physiocap_log( "Vecteur de type SHAPEFILE {}".format( listeSHPTriee[0]))
        
        return listeSHPTriee[0], os.path.basename( listeSHPTriee[0]), "SHAPE NON OUVERT DANS QGIS"        
####    #CSVT
####    nom_fichiers_recherches = os.path.join( Repertoire_Donnees_Brutes, RECHERCHE_EXTENSION_CSV)
####    listeCSVTriee = sorted(glob.glob( nom_fichiers_recherches))
####    if len( listeCSVTriee) == 0:
####        physiocap_log( "Aucun vecteur de type CSV dans répertoire des données brutes", TRACE_JH)
####    else:
####        return listeCSVTriee[0], os.path.basename( listeCSVTriee[0]), "CSV NON OUVERT DANS QGIS"
    return None, None, None

def lister_MIDs_pour_synthese( repertoire, MIDs, synthese="xx"):
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

    distancearea, quel_vecteur_demande, EXTENSION_CRS_VECTEUR, DRIVER_VECTEUR, _, \
        transform_context, laProjectionCRS, laProjectionTXT, EPSG_NUMBER = quelle_projection_et_format_vecteur( self)        
    nom_court_vecteur_segment = None
    nom_vecteur_segment = None
    #nom_gpkg = None
    if segment_simplifie == "YES":
        nom_court_vecteur = nom_session + NOM_SEGMENTS
    else:
        nom_court_vecteur = nom_session + NOM_SEGMENTS + NOM_SEGMENTS_SUITE_DETAILS    
    if quel_vecteur_demande == SHAPEFILE_NOM: 
        nom_court_vecteur_segment = nom_court_vecteur + EXTENSION_CRS_VECTEUR
        nom_vecteur_segment = os.path.join( nom_repertoire, nom_court_vecteur_segment)
        # Si le shape existe dejà il faut le détruire
        if os.path.isfile( nom_vecteur_segment):
            # A_TESTER: je doute que ca marche sous windows mais voir nouvelle api V3.22 vector delete
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

    # Creer .PRJ et .QPJ
    creer_extensions_pour_projection( nom_vecteur_segment,  laProjectionTXT)

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
    distancearea, quel_vecteur_demande, EXTENSION_CRS_VECTEUR, DRIVER_VECTEUR, _, \
        transform_context, laProjectionCRS, laProjectionTXT, EPSG_NUMBER = quelle_projection_et_format_vecteur( self)        
    
    # Initialisation
    nom_vecteur = None
    if quel_vecteur_demande == SHAPEFILE_NOM:
        nom_court_shapefile = nom_court_vecteur + EXTENSION_CRS_VECTEUR
        nom_vecteur = os.path.join(chemin_shapes, nom_court_shapefile)
        # Si le shape existe dejà il faut le détruire
        if os.path.isfile( nom_vecteur):
            # A_TESTER: je doute que ca marche : detruire plutot par une option de creation
            os.remove( nom_vecteur)            
    elif quel_vecteur_demande == GEOPACKAGE_NOM  and version_3 == "YES":
        # Creer seulement le geopackage
        physiocap_vecteur_vers_gpkg( self, chemin_session, Nom_Session)
        nom_court_gpkg = NOM_POINTS[1:] + extension_point
        nom_court_gpkg_extension = nom_court_gpkg + EXTENSION_GPKG
        nom_gpkg_intermediaire = os.path.join( chemin_session, nom_court_gpkg_extension)
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
            # TODO: ?V3.z LTR tester les exceptions ou passer à Panda
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
                            uText = "Le nombre de colonnes : {0} du cvs ne permet pas le calcul détaillé - lors création du vecteur {1}".\
                                format( len(row),  nom_court_vecteur)
                            raise physiocap_exception_err_csv(  uText)
                        nbsarmm2.append(float(row[9]))
                        nbsarcep.append(float(row[10]))
                        biommm2.append(float(row[11]))
                        biomgm2.append(float(row[12]))
                        biomgcep.append(float(row[13]))
                    else:
                        if len(row) != 21:
                            uText = "Le nombre de colonnes : {0} du cvs ne permet pas le calcul détaillé - lors création du vecteur {1}".\
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

    # Creer .PRJ et .QPJ
    creer_extensions_pour_projection( nom_vecteur, laProjectionTXT)
 
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
        super( PhysiocapTools, self).__init__()
        
    def physiocap_tools_log_for_error( self):
        """ Renvoi un message dans la log pour pointer l'utilisateur vers la liste des erreurs"""
        message_log_court = self.tr( "{0} n'a pas correctement fini son analyse").\
            format( PHYSIOCAP_UNI)
        message_log = message_log_court + self.tr( ". Consultez le journal {0} Attention").\
            format( PHYSIOCAP_UNI)
        physiocap_log( message_log, TRACE_TOUT, Qgis.Warning)
        self.physiocap_tools_log_error( message_log_court, "Critical" )

    def physiocap_tools_log_error( self, aText, level="WARNING"):
        """Send a text to the Physiocap error"""
        journal_nom = self.tr( "{0} Attention").format( PHYSIOCAP_UNI)
        if level == "WARNING":
            QgsMessageLog.logMessage( aText, journal_nom, Qgis.Warning)
        else:
            QgsMessageLog.logMessage( aText, journal_nom, Qgis.Critical)

