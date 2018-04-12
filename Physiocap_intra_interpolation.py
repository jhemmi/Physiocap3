# -*- coding: utf-8 -*-
"""
/***********************************************************************
 Physiocap_intra_interpolation
                                 A QGIS 3 plugin
 Physiocap3 plugin helps analyse raw data from Physiocap in QGIS 3 and 
 creates a synthesis of Physiocap measures' campaign
 Physiocap3 plugin permet l'analyse les données brutes de Physiocap dans QGIS 3 et
 crée une synthese d'une campagne de mesures Physiocap
 
 Le module Intra gère l(interpolation des données le chaque parcelle
 à partir d'un shapefile de contour de parcelles et d'un shape de points de
 chaque parcelle
 Il tourne après qu'inter ait tourné

 Les variables et fonctions sont nommées dans la même langue
  en Anglais pour les utilitaires
  en Francais pour les données Physiocap

                             -------------------
        begin                : 2015-11-04
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
from .Physiocap_tools import physiocap_message_box,\
        physiocap_log, physiocap_error, \
        physiocap_PHY_nom_entite_sans_cote,  physiocap_rename_existing_file, \
        physiocap_quelle_projection_demandee, \
        physiocap_get_layer_by_ID

from .Physiocap_var_exception import *

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from qgis.core import ( Qgis, QgsProject, QgsVectorLayer, \
    QgsLayerTreeGroup, QgsRasterLayer, QgsMessageLog,  \
    QgsFeatureRequest, QgsExpression,  QgsProcessingOutputRasterLayer)
    
def physiocap_affiche_raster_iso( nom_raster_final, nom_court_raster, le_template_raster, affiche_raster,
                    nom_iso_final, nom_court_isoligne, le_template_isolignes, affiche_iso,
                    vignette_group_intra, mon_projet):
    """ Affichage du raster et Iso"""
  
#    physiocap_log ( "= Template raster {0}".format( le_template_raster), TRACE_INTRA)
    physiocap_log ( "= Dans affichage iso final  {0}".format( nom_iso_final), TRACE_INTRA)
  
    if ( nom_raster_final != ""):
        intra_raster = QgsRasterLayer( nom_raster_final, 
            nom_court_raster)
        if ( nom_iso_final != ""):
            intra_isoligne = QgsVectorLayer( nom_iso_final, 
                nom_court_isoligne, 'ogr')
    
        if vignette_group_intra != None:
            if (( affiche_iso == "YES") and ( nom_iso_final != "")):
                mon_projet.addMapLayer( intra_isoligne, False)
                vignette_group_intra.addLayer( intra_isoligne)
            if ( affiche_raster == "YES"): 
                mon_projet.addMapLayer( intra_raster, False)
                vignette_group_intra.addLayer( intra_raster)
        else:
            if (( affiche_iso == "YES") and ( nom_iso_final != "")):
                mon_projet.addMapLayer( intra_isoligne)
            if ( affiche_raster == "YES"): 
                mon_projet.addMapLayer( intra_raster)
    
        if (( affiche_raster == "YES") and 
            ( os.path.exists( le_template_raster))):
            intra_raster.loadNamedStyle( le_template_raster)
            intra_raster.setRefreshOnNotifyEnabled( True)
        if (( affiche_iso == "YES") and ( nom_iso_final != "") and 
            ( os.path.exists( le_template_isolignes))):
            intra_isoligne.loadNamedStyle( le_template_isolignes)

class PhysiocapIntra( QtWidgets.QDialog):
    """QGIS Pour voir les messages traduits."""
    
    
    def __init__(self, parent=None):
        """Class constructor."""
        super( PhysiocapIntra, self).__init__()
        
    def quelle_librairie_interpolation(self, dialogue, versionSAGA, leModeDeTrace):
        """
        Traite des cas de choix et version SAGA QGIS ou GDAL avant appel des Processing (Traitement) correspondants
        """        
        # Test version de SAGA, sinon annonce de l'utilisation de GDAL
        PROCESSING_INTERPOLATION = "INCONNU"
        if dialogue.radioButtonSAGA.isChecked():
            if versionSAGA == None:
                versionNum = -1
            else:
                unite, dixieme, centieme = versionSAGA.split( ".")
                versionNum = round( (float(unite) + float(dixieme)/10 + float(centieme)/100 ), 2)
                physiocap_log ( self.tr( "= Version SAGA = {0}".format( versionNum)), TRACE_TOOLS)

            if ( versionNum >= 2.31) and ( versionNum <= 2.32):
                physiocap_log ( self.tr( "= Version SAGA OK : {0}".format( versionSAGA)), TRACE_INTRA)
                PROCESSING_INTERPOLATION = "SAGA"
            else:
                physiocap_log ( self.tr( "= Version SAGA %s est inférieure à 2.3.1 " % ( str( versionSAGA))), \
                    leModeDeTrace)
                physiocap_log ( self.tr( "= ou supérieure à 2.3.2"), leModeDeTrace)
                physiocap_log ( self.tr( "= On force l'utilisation de Gdal : "), leModeDeTrace)
                PROCESSING_INTERPOLATION = "GDAL"
                dialogue.radioButtonSAGA.setEnabled( False)
                dialogue.radioButtonGDAL.setChecked(  Qt.Checked)
                dialogue.radioButtonSAGA.setChecked(  Qt.Unchecked)
                dialogue.spinBoxPower.setEnabled( False)
                physiocap_message_box( dialogue,
                    self.tr( "= Saga a une version incompatible : on force l'utilisation de Gdal" ),
                    "information")
        
        else: # cas GDAL
            PROCESSING_INTERPOLATION = "GDAL"
        
        return PROCESSING_INTERPOLATION

    def physiocap_appel_processing(self, dialogue, 
        nom_point, algo_court, algo, params_algo,  
        nom_produit_algo,  deuxieme_nom = None):
        """
        Traite les appels à processing avec gestion du nom_produit_algo attendu
        Emet exception si pas de retour 
        """
           
        import processing
        lettre_algo = algo[0]

        physiocap_log( self.tr( "={0}= Parametres pour algo {1} de nom long {2}\n{3}".\
                        format( lettre_algo, algo_court, algo , params_algo )), TRACE_INTRA) 
         
        textes_sortie_algo = {}
        try:
            if lettre_algo == "s":
                # Pour SAGA
###                # no function prepare : algo_prepare = processing.prepare(algo, params_algo)        
###                physiocap_log( self.tr( "={0}= SAGA Préparé pour algo {1} de nom long {2}\n{3}".\
###                        format( lettre_algo, algo_court, algo , params_algo )), TRACE_INTRA) 
                textes_sortie_algo = processing.run( algo, params_algo)        
            else:
                textes_sortie_algo = processing.run( algo, params_algo)        
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
            physiocap_log( "={0}= texte en sortie {1}". \
                format( lettre_algo, textes_sortie_algo[ nom_produit_algo]), TRACE_INTRA)
             
        except:
            erreur_processing = self.tr("{0} Erreur durant analyse du rendu de produit de {1} : texte produit {2}".\
                    format( PHYSIOCAP_STOP, algo_court,  textes_sortie_algo ))
            physiocap_error( self, erreur_processing)
            physiocap_log( erreur_processing, TRACE_INTRA)
            raise
            # raise physiocap_exception_interpolation( nom_point)
  
        #TODO: Tester la cohérence ? selon un type attendu
        physiocap_log( "={0}= Produit en sortie de {1}\n{2}".\
                        format( lettre_algo, algo_court, produit_algo), TRACE_INTRA)
        return produit_algo
        
    def physiocap_creer_raster_iso( self, dialogue, choix_interpolation, 
                nom_noeud_arbre, chemin_raster, chemin_iso,
                nom_court_vignette, nom_vignette, nom_court_point, nom_point,
                le_champ_choisi, le_choix_INTRA_continue, le_nom_entite):
        """ Creation du raster et Iso
        Cas Saga ou Gdal : appel des Processing (Traitement) correspondants
        """
        leModeDeTrace = dialogue.fieldComboModeTrace.currentText() 

        # Récupération des deux parametres d'Intra
        rayonDoubleIntra = float ( dialogue.spinBoxDoubleRayon.value())
        rayonMultiplieIntra = float ( dialogue.spinBoxMultiplieRayon.value())
        if rayonMultiplieIntra > 0:
            deuxieme_rayon = rayonDoubleIntra * rayonMultiplieIntra
        else:
            deuxieme_rayon = rayonDoubleIntra
        physiocap_log( self.tr( "=~= Rayon saisi =>> {0} et rayon ellipse {1} ").\
            format(  rayonDoubleIntra,  deuxieme_rayon), TRACE_INTRA)
        
        pixelIntra = float ( dialogue.spinBoxPixel.value())

         # Pour isolignes
        isoMin = float ( dialogue.spinBoxIsoMin.value())
        isoMax = float ( dialogue.spinBoxIsoMax.value())
        #isoNombreIso = float ( dialogue.spinBoxNombreIso.value())
        isoInterlignes = float ( dialogue.spinBoxDistanceIso.value())
     
#        # Parametres fixes
#        angle = 0    # Pas utiliser
#        val_nulle = 0 # Valeur nulle reste nulle
#        float_32 = 5
#        float_64 = 6
      
        # Trace des entités en entrée
        physiocap_log( self.tr( "=~= Nom ==>> {0} <<==").\
            format(  le_nom_entite), leModeDeTrace)
#        physiocap_log( self.tr( "Vignette (moyenne Inter) {0} et chemin à la vignette \n{1}").\
#            format( nom_court_vignette, nom_vignette), TRACE_INTRA)
#        physiocap_log( self.tr( "Point {0} et chemin aux points \n{1}").\
#            format( nom_court_point, nom_point), TRACE_INTRA)
#        physiocap_log( self.tr( "=~= Champ == {0} == ").\
#            format(  le_champ_choisi), leModeDeTrace)
        # Lire points_vector et vignette_vector
        try:
            # Attrapper l'existance du fichier moyenne pour monter erreur (cas BIOMGM2)
            # V3 : mais aussi pour trouver Orientation pour GDAL
            vignette_vector = QgsVectorLayer( nom_vignette, nom_court_vignette, 'ogr')
        except:
            physiocap_log( self.tr( "{0} ne retrouve pas vos moyennes par contours {1}").\
                format( PHYSIOCAP_UNI, nom_court_vignette), TRACE_INTRA)
            raise physiocap_exception_project_contour_incoherence( nom_court_vignette)     
        try:
            QgsVectorLayer( nom_point, nom_court_point, 'ogr')
        except:
            physiocap_log( self.tr( "{0} ne retrouve pas la couche de point {1}").\
                format( PHYSIOCAP_UNI, nom_court_point), TRACE_INTRA)
            raise physiocap_exception_project_point_incoherence( nom_court_point)       
     
        # Recuperer le CRS choisi, les extensions et le calculateur de distance
        distancearea, EXT_CRS_SHP, EXT_CRS_PRJ, EXT_CRS_RASTER, \
        laProjectionCRS, laProjectionTXT, EPSG_NUMBER = \
            physiocap_quelle_projection_demandee( dialogue)

        # ###################
        # CRÉATION raster cible et temporaire
        # ###################
        # Nom du raster cible avec le_champ_choisi
        nom_court_raster = nom_noeud_arbre + NOM_INTRA + SEPARATEUR_ + le_champ_choisi +  \
            SEPARATEUR_ + physiocap_PHY_nom_entite_sans_cote( le_nom_entite) + EXT_CRS_RASTER
         
        nom_court_isoligne = nom_noeud_arbre + NOM_INTRA  + SEPARATEUR_  + le_champ_choisi  + \
            SEPARATEUR_ + "ISOLIGNE_" + physiocap_PHY_nom_entite_sans_cote( le_nom_entite) + EXT_CRS_SHP
 
        le_raster_possible = os.path.join( chemin_raster, nom_court_raster) 
        l_iso_possible = os.path.join( chemin_iso, nom_court_isoligne)
        if le_choix_INTRA_continue == 1:
            # on vérifie si le raster existe déjà
            if os.path.exists( le_raster_possible) and os.path.exists( l_iso_possible):
                    return "PAS NOUVEAU", le_raster_possible, nom_court_raster, l_iso_possible, nom_court_isoligne
            else:
                if os.path.exists( le_raster_possible) or os.path.exists( l_iso_possible):
                    raise physiocap_exception_raster_sans_iso( le_champ_choisi + '_POUR_'+  le_nom_entite)
                else:
                    # il faut creer les deux
                    nom_raster =  physiocap_rename_existing_file( le_raster_possible) # utile physiocap_rename_existing_file()
                    nom_isoligne =  physiocap_rename_existing_file( l_iso_possible) # utile physiocap_rename_existing_file()        
        elif le_choix_INTRA_continue == 2 or le_choix_INTRA_continue == 0:        
            nom_raster =  physiocap_rename_existing_file( le_raster_possible) # utile physiocap_rename_existing_file()
            nom_isoligne =  physiocap_rename_existing_file( l_iso_possible) # utile physiocap_rename_existing_file()        
        else:
            raise physiocap_exception_no_choix_raster_iso( le_nom_entite)
            
        # Création d'un raster temporaire
        try:
            from processing.tools.system import getTempFilename
            if choix_interpolation == "SAGA":
                #nom_raster_temp = getTempFilename( EXTENSION_RASTER_SAGA_SANS_POINT)
                nom_raster_temp = getTempFilename( "tiff")
            else:
                # cas GDAL (ou QGIS) : tiff
                nom_raster_temp = getTempFilename( EXTENSION_RASTER_SANS_POINT)                
        except:
            physiocap_log( self.tr( "Exception durant nommage temporaire {0} et chemin \n{1}").\
            format( nom_court_raster, nom_raster_temp), TRACE_INTRA)
            raise
        try:
            raster_temp = QgsProcessingOutputRasterLayer( nom_raster_temp)
            physiocap_log( self.tr( "Création raster {0} et chemin \n{1}").\
            format( raster_temp.description(), raster_temp.name()), TRACE_INTRA)
        except:
            physiocap_log( self.tr( "Exception durant création raster {0} et chemin \n{1}").\
            format( nom_court_raster, nom_raster_temp), TRACE_INTRA)
            raise
        physiocap_log( self.tr( "Apres rename isoligne {0} et chemin vers isoligne\n{1}<<<===").\
            format( nom_court_isoligne, nom_isoligne), TRACE_INTRA)
        
        
        # Récuperer pour GDAL orientation et Passage
        if choix_interpolation == "GDAL":
            orientation = 0
            #passage = 0 
            ellipse_orientee = 0
            # Si le le_nom_entite contient une cote on ne rentre pas 
            mon_expression = "\"{0}\" = '{1}'".format( CHAMP_NOM_ID, physiocap_PHY_nom_entite_sans_cote( le_nom_entite))                
            try:
                physiocap_log( self.tr( "avant Expression ==>{0}<===").\
                    format( mon_expression), TRACE_INTRA)
                for ma_moyenne in vignette_vector.getFeatures( QgsFeatureRequest( \
                    QgsExpression( mon_expression))):
                    # en D° horaire par rapport au N
                    orientation = ma_moyenne[ "ORIENT_A"]
                    # en d° antihoraire et perpenpendiculaire
                    ellipse_orientee = 90 + (180 - orientation)
                    #passage = ma_moyenne[ "PASSAGE"]
                    # on suppose un seul retour
                    break
            except:
                physiocap_log( self.tr( "Exception durant recherche orientation & passage pour {0}").\
                format( le_nom_entite), TRACE_INTRA)
                raise                

            # Cas sans orientation retrouvé
            if  ellipse_orientee == 0:
                deuxieme_rayon = rayonDoubleIntra

            physiocap_log( self.tr( "=~= Orientation du rang soit ellipse == {0} soit= {1} == {2}*{3} == ").\
                format(  orientation, ellipse_orientee,  rayonDoubleIntra,  deuxieme_rayon), leModeDeTrace)     
     
        
        #TODO: Verifier si inutile supprimer les controles Sous Windows :attraper les exceptions processing SAGA ascii        
#        try:
#            # Gérer le cas de la valeur d'un champ à part
#            if platform.system() == 'Windows':            
#                physiocap_log( "Type de le_nom_entite " + str( type( le_nom_entite)), , TRACE_INTRA)
#                le_nom_entite.decode("ascii")
#        except UnicodeEncodeError:
#            physiocap_log( self.tr( "{0} ne peut pas dialoguer avec Saga et des caractères non ascii").\
#                format( PHYSIOCAP_UNI), TRACE_INTRA)
#            raise physiocap_exception_windows_value_ascii( le_nom_entite)  
#        
#        try:
#            if platform.system() == 'Windows':            
#                unicode( nom_isoligne)
#                physiocap_log( "Type de isoligne " + str( type( nom_isoligne)), TRACE_INTRA)
#        excpt UnicodeEncodeError:
#            physiocap_log( self.tr( "{0} ne peut pas dialoguer avec Saga et des caractères non ascii").\
#                format( PHYSIOCAP_UNI), TRACE_INTRA)
#            raise physiocap_exception_windows_saga_ascii( nom_isoligne)  

        # Initialisation avant Interpolation
        nom_raster_final = ""
        raster_dans_poly = ""
        iso_dans_poly = ""
        nom_iso_final = ""
        # Et pour la SAGA
        iso_dans_poly_brut = ""
        nom_iso_sans_ELEV = ""
        iso_dans_poly_plus = ""
        nom_iso_avec_ELEV = ""
        
        # Récuperer Extent du polygone en cours
        ex = vignette_vector.extent()
        xmin, xmax, ymin, ymax = ex.xMinimum(),ex.xMaximum(), ex.yMinimum(), ex.yMaximum()
        info_extent = str(xmin) + "," + str(ymin) + "," + str(xmax) + "," + str(ymax)
        #physiocap_log( "=~= Extent layer >>> " + info_extent + " <<<", leModeDeTrace)
        
        info_extent_epsg = info_extent + " [EPSG:" + str( EPSG_NUMBER) + "]"
        
        if choix_interpolation == "SAGA":
            # Appel SAGA : power à 2 fixe
#            physiocap_log( self.tr( "=~= Interpolation SAGA dans {0}").\
#                format(  nom_court_raster), leModeDeTrace)
            # Les parametres proviennent du modele d'interpolation Physiocap du CIVC
            # apres le champ, 1 veut dire Linearly discreasing with search radius
            # 2 est power
            # 1 est bande pour expo ou gauss (non utilisé)
            # 0 recherche locale dans le rayon
            # rayon de recherche (defaut saga est 100) : local maximum search distance given in map units
            # 0 all directions et non quadrans
            # 1 tous les points ce qui annule ? le 10 qui suit
            # 10 nombre de point max
            # extent calculé precedemment
            # cellsize ou taille du pixel (unité de la carte)
# OK avec V3  : 
### 'FIELD' : 'DIAM', 
### 'DW_WEIGHTING' : 1, 
### 'DW_IDW_POWER' : 2,
### 'DW_IDW_OFFSET' : False, 
### 'DW_BANDWIDTH' : 0, 
### 'SEARCH_RANGE' : 0, 
### 'SEARCH_RADIUS' : 30, 
### 'SEARCH_POINTS_ALL' : 0, 
### 'SEARCH_POINTS_MIN' : 1, 
### 'SEARCH_POINTS_MAX' : 20, 
### 'SEARCH_DIRECTION' : 0, 
### 'OUTPUT_EXTENT' : '796023.0,6674128.2,796089.6,6674263.2 [EPSG:2154]', 
# ????  ### 'TARGET_USER_SIZE' : 1.8, 
### 'TARGET_DEFINITION' : 0, 
### 'TARGET_USER_FITS' : 0, 
### 'TARGET_TEMPLATE' : , 
#'TARGET_OUT_GRID' : 'C:/Users/Utilisateur/AppData/Local/Temp        
 
            IDW_SAGA = { 'SHAPES' : nom_point, 
                'FIELD' : le_champ_choisi, 
                'OUTPUT_EXTENT' : info_extent_epsg,
                'DW_WEIGHTING' : pixelIntra,
                'DW_IDW_POWER' : 2, 
                'DW_IDW_OFFSET' : False, 
                'DW_BANDWIDTH' : 1, 
                'SEARCH_RANGE' : 0, 
                'SEARCH_RADIUS' : rayonDoubleIntra, 
                'SEARCH_POINTS_ALL' : 1, 
                'SEARCH_POINTS_MIN' : 1, 
                'SEARCH_POINTS_MAX' : 20, 
                'SEARCH_DIRECTION' : 0, 
                'TARGET_USER_SIZE' : 1.8, 
                'TARGET_DEFINITION' : 0, 
                'TARGET_USER_FITS' : 0,
                'TARGET_TEMPLATE' : "",
                'TARGET_OUT_GRID' : nom_raster_temp
                }
#                 
# KO                'TARGET_OUT_GRID' :  raster_temp.name(), 


            nom_raster_produit = self.physiocap_appel_processing(dialogue, nom_point, \
                "IDW_SAGA", "saga:inversedistanceweightedinterpolation", \
                IDW_SAGA, "OUTPUT_GRID")       
                                            
#####            # On passe ETAPE CLIP si nom_raster_temp existe
#####            if ( nom_raster_produit != ""):
#####                raster_dans_poly = processing.runalg("saga:clipgridwithpolygon",
#####                nom_raster_produit,
#####                nom_vignette,
#####                nom_raster)
#####            
#####            if (( raster_dans_poly != None) and ( str( list( raster_dans_poly)).find( "OUTPUT") != -1)):
#####                if raster_dans_poly[ 'OUTPUT'] != None:
#####                    nom_raster_final = raster_dans_poly[ 'OUTPUT']
#####                    physiocap_log( self.tr("=~= Raster clippé : clipgridwithpolygon\n{0}").\
#####                        format( nom_raster_final), TRACE_INTRA)
#####                else:
#####                    physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
#####                        format("clipgridwithpolygon","B"))
#####                    raise physiocap_exception_interpolation( nom_point)
#####            else:
#####                physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
#####                    format("clipgridwithpolygon","A"))
#####                raise physiocap_exception_interpolation( nom_point)
#####
#####            # On passe ETAPE ISO si nom_raster_final existe
#####            if ( nom_raster_final != ""):
#####                # Isolignes
#####                iso_dans_poly_brut = processing.runalg("saga:contourlinesfromgrid",
#####                    nom_raster_final,
#####                    isoMin, isoMax, isoInterlignes,
#####                    None)
#####                physiocap_log( self.tr( "=~= Interpolation SAGA - Etape 2 - FIN"), TRACE_INTRA)
#####            
#####                if (( iso_dans_poly_brut != None) and ( str( list( iso_dans_poly_brut)).find( "CONTOUR") != -1)):
#####                    if iso_dans_poly_brut[ 'CONTOUR'] != None:
#####                        nom_iso_sans_ELEV = iso_dans_poly_brut[ 'CONTOUR']
#####                        physiocap_log( self.tr("=~= Iso sans LEVEL : contourlinesfromgrid\n{0}").\
#####                            format( nom_iso_sans_ELEV), TRACE_INTRA)
#####                    else:
#####                        physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
#####                            format("contourlinesfromgrid","B"))
#####                        raise physiocap_exception_interpolation( nom_point)
#####                else:
#####                    physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
#####                        format("contourlinesfromgrid","A"))
#####                    raise physiocap_exception_interpolation( nom_point)
#####
#####                # On passe ETAPE FIELD si nom_iso_sans_ELEV existe
#####                if ( nom_iso_sans_ELEV != ""):                              
#####                    iso_dans_poly_plus = processing.runalg("qgis:addfieldtoattributestable", \
#####                        nom_iso_sans_ELEV, \
#####                        "ELEV", 1, 15, 2 , None)
##### 
#####                if (( iso_dans_poly_plus != None) and ( str( list( iso_dans_poly_plus)).find( "OUTPUT_LAYER") != -1)):
#####                    if iso_dans_poly_plus[ 'OUTPUT_LAYER'] != None:
#####                        nom_iso_avec_ELEV = iso_dans_poly_plus[ 'OUTPUT_LAYER']
#####                        physiocap_log( self.tr("=~= Iso avec LEVEL ajouté : addfieldtoattributestable\n{0}").\
#####                            format( nom_iso_avec_ELEV), TRACE_INTRA)
#####                    else:
#####                        physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
#####                            format("addfieldtoattributestable","B"))
#####                        raise physiocap_exception_interpolation( nom_point)
#####                else:
#####                    physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
#####                        format("addfieldtoattributestable","A"))
#####                    raise physiocap_exception_interpolation( nom_point)
#####
#####                # On passe ETAPE CALCULATOR si nom_iso_final existe
#####                if ( nom_iso_avec_ELEV != ""):                              
#####                    # Retrouver le nom de l'attribut créé
#####                    intra_iso_modifie = QgsVectorLayer( nom_iso_avec_ELEV, 
#####                            "Ne pas voir serait mieux", 'ogr')
#####                    fields = intra_iso_modifie.pendingFields()
#####                    field_probable = fields[1]
#####                    field_name = field_probable.name()
#####                    # A_TESTER: sans str et à suivre ensuite
#####                    field_formule = '"' + str( field_name) + '"'  
#####                    physiocap_log( "=~= Isolignes formule : " + str( field_formule), TRACE_INTRA)                    
#####                    QgsMessageLog.logMessage( "PHYSIOCAP : Avant calculator ", "Processing", Qgis.Warning)
#####                    # Le remplacer par "ELEV", en fait on le copie dans "ELEV"
#####                    iso_dans_poly = processing.runalg("qgis:fieldcalculator", \
#####                        nom_iso_avec_ELEV, "ELEV", 0, 15, 2, False, field_formule , nom_isoligne)
#####
#####                if (( iso_dans_poly != None) and ( str( list( iso_dans_poly)).find( "OUTPUT_LAYER") != -1)):
#####                    if iso_dans_poly[ 'OUTPUT_LAYER'] != None:
#####                        nom_iso_final = iso_dans_poly[ 'OUTPUT_LAYER']
#####                        physiocap_log( self.tr("=~= Iso final : fieldcalculator\n{0}").\
#####                            format( nom_iso_final), TRACE_INTRA)
#####                    else:
#####                        physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
#####                            format("fieldcalculator","B"))
#####                        raise physiocap_exception_interpolation( nom_point)
#####                else:
#####                    physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
#####                        format("fieldcalculator","A"))
#####                    raise physiocap_exception_interpolation( nom_point)
#####            else:
#####                physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
#####                    format("clipgridwithpolygon","0"))
#####                raise physiocap_exception_interpolation( nom_point)
            physiocap_log( self.tr( "=~= Interpolation SAGA - Fin iso - {0}").\
                format( nom_iso_final), TRACE_INTRA)   
                
        elif choix_interpolation == "GDAL":
            # Appel GDAL
            # Paramètres apres le champ
            # Power vaut 2 
            # Lissage à 0 car ce lissage peut se faire dans les propriétés du raster
            # Rayon identique 
            # Max points à 20 (si non atteint, forcage à valeur 0    
            # Min à 5 
            # Angle à 0 (c'est l'angle de l'ellipse)
            # TODO: trouver syntaxe où appeller gdalwarp directement 
              # KO dans IDW
            #option_outsize = "-outsize {0} {0}".format( pixelIntra)
##            # KO pour idw et clip VOIR Avec \" ou ' et "
            # KO pour idw et clip
            # option_resolution = "-tr \"{0} {0}\"".format( pixelIntra)

            # IDW GDAL
            IDW_GDAL = {'INPUT':nom_point,  'Z_FIELD' : le_champ_choisi, 
                'POWER':2,'SMOOTHING':0,
                'RADIUS_1':rayonDoubleIntra,'RADIUS_2':deuxieme_rayon,
                'ANGLE':ellipse_orientee,
                'MAX_POINTS':20,'MIN_POINTS':1,'NODATA':0,
                'OPTIONS':'','DATA_TYPE':6, 'OUTPUT': nom_raster_temp}

            nom_raster_produit = self.physiocap_appel_processing( dialogue, nom_point, \
                "IDW_GDAL", "gdal:gridinversedistance", \
                IDW_GDAL, "OUTPUT")  
                
          
            QgsMessageLog.logMessage( "PHYSIOCAP : Avant clip", "Processing", Qgis.Warning)

            # On passe ETAPE CLIP si nom_raster_temp existe
            if ( nom_raster_produit != ""):
                CLIP_GDAL = {'INPUT':nom_raster_produit,
                    'MASK':nom_vignette,
                    'NODATA':0,
                    'ALPHA_BAND':False,
                    'CROP_TO_CUTLINE':True,
                    'KEEP_RESOLUTION':True,
                    'OPTIONS':'',
                    'DATA_TYPE':6,
                    'OUTPUT':nom_raster}
                    
                nom_raster_final = self.physiocap_appel_processing( dialogue, nom_point, \
                "CLIP_GDAL", "gdal:cliprasterbymasklayer", \
                CLIP_GDAL, "OUTPUT")                 
                
#######                raster_dans_poly = processing.run( "gdal:cliprasterbymasklayer", param_cli)                    

###            option_clip_raster = ""
###            if ( EPSG_NUMBER == EPSG_NUMBER_L93 ):
###                #physiocap_log( "=x= Projection à translater vers : " + str( EPSG_NUMBER) , TRACE_INTRA)
###                #option_clip_raster = '-s_2015-12-09T16:17:46	1	PHYSIOCAP : Avant calculator 
###                #srs "EPSG:' + str(EPSG_NUMBER_GPS) + '" -t_srs "EPSG:' + str(EPSG_NUMBER_L93) + '"'
###                # A_TESTER: old était str(EPSG_NUMBER_L93)
###                option_clip_raster = "-t_srs \"EPSG:" + EPSG_NUMBER_L93 + "\""


###                    # Version à 7 arg
###                    raster_dans_poly = processing.runalg("gdalogr:cliprasterbymasklayer",
###                    nom_raster_temp,
###                    nom_vignette,
###                    "-9999",False,False,
###                    option_clip_raster, 
###                    nom_raster)
###            
            # On passe ETAPE ISO si nom_raster_final existe
            if ( nom_raster_final != ""):
                # Isolignes
                ISO_GDAL = {'INPUT':nom_raster,
                    'BAND' : 1,
                    'INTERVAL' : isoInterlignes,
                    'FIELD_NAME' : 'ELEV',
                    'CREATE_3D' : False, 'IGNORE_NODATA' : False, 'NODATA' : 0, 'OFFSET' : 0,
                    'OUTPUT' : nom_isoligne }

                nom_iso_final = self.physiocap_appel_processing( dialogue, nom_point, \
                "ISO_GDAL", "gdal:contour", \
                ISO_GDAL, "OUTPUT")
                
        else:
            # Autres choix
            physiocap_error( self, self.tr( "=~= Pas d'autre méthode d'interpolation que GDAL et SAGA"))
           
        return "NOUVEAUX", nom_raster_final, nom_court_raster, nom_iso_final, nom_court_isoligne            

    def physiocap_interpolation_IntraParcelles( self, dialogue):
        """Interpolation des données de points intra parcellaires"""
        NOM_PROJET = dialogue.lineEditProjet.text()
        leModeDeTrace = dialogue.fieldComboModeTrace.currentText() 
    
#        if LE_MODE_PROD == "NO":
#            pass
#        else:
#            aText = self.tr( "Pas d'interpolation disponible avec Physiocap 3. Interpolez avec les versions QGIS 2.14 et l'extension 1.8.3.")
#            physiocap_error( self, aText)
#            return physiocap_message_box( dialogue, aText, "information")
#            
        version_3 = "NO"
        if dialogue.checkBoxV3.isChecked():
            version_3 = "YES"

        # Répertoire
        repertoire_data = dialogue.lineEditDirectoryPhysiocap.text()
        if ((repertoire_data == "") or ( not os.path.exists( repertoire_data))):
            aText = self.tr( "Pas de répertoire de données brtutes spécifié")
            physiocap_error( self, aText)
            return physiocap_message_box( dialogue, aText, "information")
        repertoire_cible = dialogue.lineEditDirectoryFiltre.text()
        if ((repertoire_cible == "") or ( not os.path.exists( repertoire_cible))):
            aText = self.tr( "Pas de répertoire de données cibles spécifié")
            physiocap_error( self, aText)
            return physiocap_message_box( dialogue, aText, "information")
               
        # Pour polygone de contour   
        nom_complet_poly = dialogue.comboBoxPolygone.currentText().split( SEPARATEUR_NOEUD)
        if ( len( nom_complet_poly) != 2):
            aText = self.tr( "Le polygone de contour n'est pas choisi. ")
            aText = aText + self.tr( "Avez-vous ouvert votre shapefile de contour ?")
            physiocap_error( self, aText)
            return physiocap_message_box( dialogue, aText, "information")            
        #nom_poly = nom_complet_poly[ 0] 
        id_poly = nom_complet_poly[ 1] 
        vecteur_poly = physiocap_get_layer_by_ID( id_poly)

        # Pour attribut en cours d'interpolation
        le_champ_poly = dialogue.fieldComboContours.currentText()
            
        # Pour les points
        nom_complet_point = dialogue.comboBoxPoints.currentText().split( SEPARATEUR_NOEUD)
        if ( len( nom_complet_point) != 2):
            aText = self.tr( "Le shape de points n'est pas choisi. ")
            aText = aText + self.tr( "Lancez le traitement initial - bouton Filtrer les données brutes puis Inter - ")
            aText = aText + self.tr( "avant de faire votre calcul de Moyenne Intra Parcellaire")
            physiocap_error( self, aText) 
            return physiocap_message_box( dialogue, aText, "information")            
        nom_noeud_arbre = nom_complet_point[ 0] 
        id_point = nom_complet_point[ 1] 
        vecteur_point = physiocap_get_layer_by_ID( id_point)

        # Vérifier disponibilité de processing (on attend d'etre dans Intra)
        try :
            import processing
            try:
                from processing.core.Processing import Processing
                Processing.initialize()
            except:
                physiocap_log( self.tr( "{0} nécessite l'extension {1}").\
                    format( PHYSIOCAP_UNI, self.tr("Traitement")), leModeDeTrace)
                raise physiocap_exception_no_processing( "Pas d'extension Traitement - initialize")               
            versionGDAL = processing.tools.raster.gdal.__version__
            versionSAGA = processing.algs.saga.SagaUtils.getInstalledVersion()
        except ImportError:
            physiocap_log( self.tr( "{0} nécessite l'extension {1}").\
                format( PHYSIOCAP_UNI, self.tr("Traitement")), leModeDeTrace)
            raise physiocap_exception_no_processing( "Pas d'extension Traitement")
        except AttributeError:
            # Todo : Vérifier syntaxe en Win 32 bits et attraper cette erreur
            physiocap_log( self.tr( "{0} nécessite SAGA version 2.3.1 à 2.3.2").\
                format( PHYSIOCAP_UNI), leModeDeTrace)
            # TODO install saga LINUX
            machine = platform.system()
            if (machine == "Linux"):
                physiocap_log ( self.tr( "= On force l'utilisation de Gdal : "), leModeDeTrace)
                dialogue.radioButtonSAGA.setEnabled( False)
                dialogue.radioButtonGDAL.setChecked(  Qt.Checked)
                dialogue.radioButtonSAGA.setChecked(  Qt.Unchecked)
                dialogue.spinBoxPower.setEnabled( False)
                physiocap_message_box( dialogue,
                    self.tr( "= Saga a une version incompatible : on force l'utilisation de Gdal" ),
                    "information")
                pass
            else:
                raise physiocap_exception_no_saga( "Erreur attribut")

        physiocap_log ( self.tr( "= Version SAGA = %s" % ( versionSAGA)), TRACE_INTRA)
        physiocap_log ( self.tr( "= Version GDAL = %s" % ( versionGDAL)), TRACE_INTRA)

        physiocap_log( self.tr( "=~= {0} début de l'interpolation des points de {1}").\
            format( PHYSIOCAP_UNI, nom_noeud_arbre), leModeDeTrace)

        # Progress BAR 2%
        dialogue.progressBarIntra.setValue( 2)
        
        # Appel une seule fois des vérification Processing dispo et choix de Librairie 
        choix_interpolation = self.quelle_librairie_interpolation( dialogue, \
                versionSAGA, leModeDeTrace)
   
        physiocap_log ( self.tr( "=~= Choix de la librairie d'interpolation : {0}".\
            format( choix_interpolation)), leModeDeTrace)

       
        # Vérification de l'arbre
        mon_projet = QgsProject.instance()
        root = mon_projet.layerTreeRoot()        
        un_groupe = root.findGroup( nom_noeud_arbre)
        if ( not isinstance( un_groupe, QgsLayerTreeGroup)):
            aText = self.tr( "Le projet {0} n'existe pas. ").\
                format(  nom_noeud_arbre)
            aText = aText + self.tr( "Créer une nouvelle instance de projet - bouton Filtrer les données brutes puis Inter - ")
            aText = aText + self.tr( "avant de faire votre interpolation Intra Parcellaire")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( dialogue, aText, "information" )            
        
        # Vérification 
        if ( vecteur_point == None):
            aText = self.tr( "Le jeu de points choisi n'est pas valide. ")
            aText = aText + self.tr( "Créer une nouvelle instance de projet - bouton Filtrer les données brutes puis Inter - ")
            aText = aText + self.tr( "avant de faire votre interpolation Intra Parcellaire")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( dialogue, aText, "information" )  

        if ( vecteur_poly == None) or ( not vecteur_poly.isValid()):
            aText = self.tr( "Le contour choisi n'est pas valide. ")
            aText = aText + self.tr( "Créer une nouvelle instance de projet - bouton Filtrer les données brutes puis Inter - ")
            aText = aText + self.tr( "avant de faire votre interpolation Intra Parcellaire")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( dialogue, aText, "information" ) 
                   
        # Recuperer le CRS choisi, les extensions et le calculateur de distance
        distancearea, EXT_CRS_SHP, EXT_CRS_PRJ, EXT_CRS_RASTER, \
        laProjectionCRS, laProjectionTXT, EPSG_NUMBER = \
            physiocap_quelle_projection_demandee( dialogue)

        # Assert repertoire shapefile 
        # A_TESTER: pourquoi ces unicode et le point virgule !
        #chemin_shapes = os.path.dirname( unicode( vecteur_point.dataProvider().dataSourceUri() ) )
        nom_point_en_cours = vecteur_point.dataProvider().dataSourceUri()
        chemin_shapes = os.path.dirname( nom_point_en_cours ) 
        chemin_projet = os.path.dirname( chemin_shapes)
        shape_point_extension = os.path.basename( nom_point_en_cours)
        pos_extension = shape_point_extension.rfind(".")
        shape_point_sans_extension = shape_point_extension[:pos_extension]
        if ( not os.path.exists( chemin_shapes)):
            raise physiocap_exception_rep( chemin_shapes)

        consolidation = "NO"
        if dialogue.checkBoxConsolidation.isChecked():
            consolidation = "YES"
            
        # Test selon Consolidation
        if (consolidation == "YES"):
            # Rajout pour consolidation du nom du shape
            chemin_shape_nom_point = os.path.join( chemin_shapes, shape_point_sans_extension)
            if not (os.path.exists( chemin_shape_nom_point)):
                os.mkdir( chemin_shape_nom_point)                    
            chemin_vignettes = os.path.join( chemin_shape_nom_point, VIGNETTES_INTER)
        else:            
            if version_3 == "NO":                
                chemin_vignettes = os.path.join( chemin_shapes, VIGNETTES_INTER)
            else:
                chemin_vignettes = os.path.join( chemin_projet , REPERTOIRE_INTER_V3)
        # Assert repertoire vignette inter 
        if not (os.path.exists( chemin_vignettes)):
            raise physiocap_exception_rep( VIGNETTES_INTER)

       # QT Confiance 
        les_champs_INTRA_choisis = dialogue.fieldComboIntra.currentText().split( SEPARATEUR_NOEUD)
        physiocap_log( self.tr( "=~= Les champs à traiter {0}". \
            format( les_champs_INTRA_choisis)), TRACE_INTRA)
        le_choix_INTRA_continue = dialogue.fieldComboIntraContinue.currentIndex()

        # Création du REP RASTER et ISOLIGNES
        # Test selon Consolidation
        if (consolidation == "YES"):
            chemin_raster = os.path.join( chemin_shape_nom_point, REPERTOIRE_RASTERS)
            chemin_iso = chemin_raster
        else:
            if version_3 == "NO":                
                chemin_raster = os.path.join( chemin_shapes, REPERTOIRE_RASTERS)
                chemin_iso = chemin_raster
            else:
                chemin_intra =  os.path.join( chemin_projet , REPERTOIRE_INTRA_V3)
                chemin_raster =  os.path.join( chemin_intra, REPERTOIRE_RASTER_V3)
                chemin_iso =  os.path.join( chemin_intra, REPERTOIRE_ISO_V3)

        if version_3 == "YES":
            if not (os.path.exists( chemin_intra)):
                try:
                    os.mkdir( chemin_intra)
                except:
                    raise physiocap_exception_rep( REPERTOIRE_INTRA_V3)
        if not (os.path.exists( chemin_raster)):
            try:
                os.mkdir( chemin_raster)
            except:
                raise physiocap_exception_rep( REPERTOIRE_RASTERS)
        if not (os.path.exists( chemin_iso)):
            try:
                os.mkdir( chemin_iso)
            except:
                raise physiocap_exception_rep( REPERTOIRE_ISO_V3)

       

        ##################
        # Progress BAR 4%
        ##################
        dialogue.progressBarIntra.setValue( 4)
        # Compter le nombre de formes pour la barre d'avancement
        i_forme_min = vecteur_poly.featureCount()
        # Affinage selon les demandes de tous et/ou de chaque
        if  (( dialogue.checkBoxIntraUnSeul.isChecked()) and \
             (( dialogue.checkBoxIntraIsos.isChecked()) or \
              ( dialogue.checkBoxIntraImages.isChecked()))):
            i_forme = i_forme_min * 2
        else:
            i_forme = i_forme_min
        # Multiplier par le nombre d'attribut 
        i_entite = i_forme * len( les_champs_INTRA_choisis)
#        physiocap_log( self.tr( "=~= Nombre de formes {0} soit : {1} à dessiner et {2} entites avec les champs ").\
#            format( i_forme_min,  i_forme, i_entite ), TRACE_INTRA)
        stepBar = int( 60 / i_entite)
        positionBar = 5
        
        for idx, le_champ_choisi in enumerate( les_champs_INTRA_choisis):
            # Pour chaque attribut à interpoler
            physiocap_log( self.tr( "=~= {0} Champ == {1} est le {2} parmi {3} ==").\
                format( PHYSIOCAP_UNI, le_champ_choisi, idx, len( les_champs_INTRA_choisis)), leModeDeTrace)

            # Si plusieurs champs choisis : mettre à jour les parametres depuis affichage
            if len( les_champs_INTRA_choisis) > 1:
                # Forcer pour éviter le calcul d'aide
                dialogue.fieldComboAideIso.setCurrentIndex( 2) 
                if idx == 0:
                    # récuperer les saisies nommées DIAM
                    # ASSERT : 
                    leChoixEncours = dialogue.fieldComboIntraDIAM.currentText()
                    if le_champ_choisi != leChoixEncours:
                        raise physiocap_exception_attribut_multiple_incoherent( leChoixEncours)
                    physiocap_log( self.tr( "=~= {0} Synchro iso == {1} ==").\
                        format( PHYSIOCAP_UNI, leChoixEncours), leModeDeTrace)                    
                    dialogue.spinBoxIsoMax.setValue( int( dialogue.spinBoxIsoMax_Fixe_DIAM.value()))
                    dialogue.spinBoxIsoMin.setValue( int( dialogue.spinBoxIsoMin_Fixe_DIAM.value()))
                    dialogue.spinBoxDistanceIso.setValue( int( dialogue.spinBoxDistanceIso_Fixe_DIAM.value()))                    
                elif idx == 1:
                    # récuperer les saisies nommées SARM
                    # ASSERT : 
                    leChoixEncours = dialogue.fieldComboIntraSARM.currentText()
                    if le_champ_choisi != leChoixEncours:
                        raise physiocap_exception_attribut_multiple_incoherent( leChoixEncours)
                    physiocap_log( self.tr( "=~= {0} Synchro iso == {1} ==").\
                        format( PHYSIOCAP_UNI, leChoixEncours), leModeDeTrace)                    
                    dialogue.spinBoxIsoMax.setValue( int( dialogue.spinBoxIsoMax_Fixe_SARM.value()))
                    dialogue.spinBoxIsoMin.setValue( int( dialogue.spinBoxIsoMin_Fixe_SARM.value()))
                    dialogue.spinBoxDistanceIso.setValue( int( dialogue.spinBoxDistanceIso_Fixe_SARM.value()))
                elif idx == 2:
                    # récuperer les saisies nommées BIOM
                    # ASSERT : 
                    leChoixEncours = dialogue.fieldComboIntraBIOM.currentText()
                    if le_champ_choisi != leChoixEncours:
                        raise physiocap_exception_attribut_multiple_incoherent( leChoixEncours)
                    physiocap_log( self.tr( "=~= {0} Synchro iso == {1} ==").\
                        format( PHYSIOCAP_UNI, leChoixEncours), leModeDeTrace)                    
                    dialogue.spinBoxIsoMax.setValue( int( dialogue.spinBoxIsoMax_Fixe_BIOM.value()))
                    dialogue.spinBoxIsoMin.setValue( int( dialogue.spinBoxIsoMin_Fixe_BIOM.value()))
                    dialogue.spinBoxDistanceIso.setValue( int( dialogue.spinBoxDistanceIso_Fixe_BIOM.value()))
                else:
                    raise physiocap_exception_attribut_multiple_incoherent( "Autre choix")

            # Récupérer des styles pour chaque shape
            # Pour les templates
            dir_template = dialogue.fieldComboThematiques.currentText()
            qml_prefix = dialogue.lineEditThematiqueIntraImage.text().strip('"')
            nom_intra_attribut = qml_prefix + le_champ_choisi + EXTENSION_QML
            le_template_raster = os.path.join( dir_template, nom_intra_attribut)
            qml_prefix = dialogue.lineEditThematiqueIntraIso.text().strip('"')
            nom_isolignes_attribut = qml_prefix + le_champ_choisi + EXTENSION_QML
            le_template_isolignes  = os.path.join( dir_template, nom_isolignes_attribut)
#            physiocap_log( self.tr( "=~= {0} Template raster == {1} ==").\
#                format( PHYSIOCAP_UNI, le_template_raster), leModeDeTrace)      
                
            # On passe sur le contour général
            contour_avec_point = 0
            contours_possibles = 0
           
            # #####################
            # Cas d'une image seule
            # #####################
            if ( dialogue.checkBoxIntraUnSeul.isChecked() and 
                choix_interpolation != "GDAL") :
                #A_TESTER: Pas dans le cas GDAL
                contours_possibles = contours_possibles + 1

                # Nom du Shape moyenne et de sa vignette dans l'arbre
                nom_vecteur_contour = vecteur_poly.name()
                nom_court_du_contour = os.path.basename( nom_vecteur_contour + EXTENSION_SHP)
                nom_court_vignette = nom_noeud_arbre + NOM_MOYENNE + nom_court_du_contour
                nom_vignette = os.path.join( chemin_vignettes, nom_court_vignette)        
                                                       
                # Nom point 
                if consolidation == "YES" :
                    # Dans le cas de consolidation, on s'appuie sur le repertoire 
                    # shapefile fictif (celui de la consolidation, en verité)
                    # On cherche le nom de base dans le vecteur de consolitatioin choisi 
                    
                    # Assert repertoire shapefile : c'est le repertoire qui contient le vecteur point
                    # Ca doit fonctionner pour consolidation
                    if ( not os.path.exists( chemin_shapes)):
                        raise physiocap_exception_rep( chemin_shapes)
                    # A_TESTER: cet unicode !!!
                    nom_base_point = os.path.basename( unicode( vecteur_point.name() ) )
                    nom_court_point = nom_base_point + EXTENSION_SHP
                else:
                    nom_court_point = NOM_PROJET + NOM_POINTS + EXTENSION_SANS_ZERO + EXT_CRS_SHP   
                nom_point = os.path.join( chemin_shapes, nom_court_point)                    

                # Vérifier si le point et la vignette existent
                if not (os.path.exists( nom_vignette)):
                    physiocap_log( self.tr( "=~=  Pas d'interpolation, Vignette absente : {0}").\
                        format( nom_vignette), TRACE_INTRA)
                if not (os.path.exists( nom_point)):
                    physiocap_log( self.tr( "=~=  Pas d'interpolation, Points absents : {0}").\
                        format( nom_point), TRACE_INTRA)
                else:
                    try:
                        # ###############
                        # Calcul raster et iso
                        # ###############
                        physiocap_log( self.tr( "=~=  Le contour : {0}").\
                            format( nom_vecteur_contour), TRACE_INTRA)
                        nouveau = "NON"
                        nouveau, nom_raster_final, nom_court_raster, nom_iso_final, nom_court_isoligne = \
                            self.physiocap_creer_raster_iso( dialogue, choix_interpolation, 
                            nom_noeud_arbre, chemin_raster, chemin_iso,  
                            nom_court_vignette, nom_vignette, nom_court_point, nom_point,
                            le_champ_choisi, nom_vecteur_contour[:-4]) 
                        contour_avec_point = contour_avec_point + 1
                    except physiocap_exception_windows_value_ascii as e:
                        aText = self.tr( "La valeur {0} a ").\
                            format( e)
                        aText = aText + self.tr( "des caractères (non ascii) incompatibles avec l'interpolation SAGA.")
                        aText = aText + self.tr( "Erreur bloquante sous Windows qui empêche de traiter cette interpolation.")
                        physiocap_error( self, aText, "CRITICAL")        
                    except:
                        raise
                    finally:
                        pass
                    # Fin de capture des err
                                
                # CRÉATION groupe INTRA
                if (( contour_avec_point == 1) and (un_groupe != None)):
                    if (consolidation == "YES"):
                        vignette_projet = nom_noeud_arbre + SEPARATEUR_ + shape_point_sans_extension + \
                            SEPARATEUR_ + le_champ_choisi + \
                            SEPARATEUR_ + VIGNETTES_INTRA
                        # modifier les noms courts raster et iso
                        longueur_nom_arbre = len(nom_noeud_arbre)
                        nom_court_raster_ori = nom_court_raster
                        nom_court_raster = shape_point_sans_extension + \
                            nom_court_raster_ori[longueur_nom_arbre:]
                        nom_court_isoligne_ori = nom_court_isoligne
                        nom_court_isoligne = shape_point_sans_extension + \
                            nom_court_isoligne_ori[longueur_nom_arbre:]
                    else:
                        vignette_projet = nom_noeud_arbre + SEPARATEUR_ + le_champ_choisi + \
                            SEPARATEUR_ + VIGNETTES_INTRA 
                    vignette_existante = un_groupe.findGroup( vignette_projet)
                    if ( vignette_existante == None ):
                        vignette_group_intra = un_groupe.addGroup( vignette_projet)
                    else:
                        if le_choix_INTRA_continue == 0:
                            # Si vignette preexiste, on ne recommence pas
                            raise physiocap_exception_vignette_exists( vignette_projet) 

                if ( contour_avec_point >  0 ):                                            
                    # Affichage dans panneau QGIS                           
                    if ( dialogue.checkBoxIntraUnSeul.isChecked()):
                        if nouveau == "NOUVEAUX":
                            physiocap_affiche_raster_iso( \
                                nom_raster_final, nom_court_raster, le_template_raster, "YES",
                                nom_iso_final, nom_court_isoligne, le_template_isolignes, "YES",
                                vignette_group_intra, mon_projet)

            # Progress BAR + un stepBar%
            positionBar = positionBar + ( stepBar * i_forme_min)     
            dialogue.progressBarIntra.setValue( positionBar)
            positionBarInit = positionBar

            # Eviter de tourner en Intra sur chaque parcelle
            if (( dialogue.checkBoxIntraIsos.isChecked()) or 
                        ( dialogue.checkBoxIntraImages.isChecked())):        
              
                # On tourne sur les contours qui ont été crée par Inter
                # On passe sur les differents contours de chaque parcelle
                # A_TESTER: Apres test Enumeration vers id_contour OK propager aux boucles for
                # Attention au test sur id_contour > 0 ne marchait plus
                for id_contour, un_contour in enumerate( vecteur_poly.getFeatures()): #iterate poly features
                    contours_possibles = contours_possibles + 1
                    try:
                        # A_TESTER: sans str
                        #un_nom = str( un_contour[ le_champ_poly]) #get attribute of poly layer
                        un_nom = un_contour[ le_champ_poly] 
                    except:
                        un_nom = NOM_CHAMP_ID + SEPARATEUR_ + str(id_contour)
                        pass

                    physiocap_log ( self.tr( "=~= {0} Début d'interpolation de {1} index {2} >>>>").\
                        format( PHYSIOCAP_UNI, un_nom,  id_contour), leModeDeTrace)

                    # Nom du Shape moyenne 
                    nom_court_vignette = nom_noeud_arbre + NOM_MOYENNE + physiocap_PHY_nom_entite_sans_cote(un_nom) +  EXT_CRS_SHP     
                    # Attention j'ai enleve physiocap_rename_existing_file(
                    nom_vignette = os.path.join( chemin_vignettes, nom_court_vignette)        
                                
                    
                    # Nom point 
                    nom_court_point = nom_noeud_arbre + NOM_POINTS + SEPARATEUR_ + physiocap_PHY_nom_entite_sans_cote(un_nom) + EXT_CRS_SHP     
                    # Attention j'ai enleve physiocap_rename_existing_file(
                    nom_point = os.path.join( chemin_vignettes, nom_court_point)                    
                    #physiocap_log( "=~= Vignette court : " +  nom_court_vignette , TRACE_INTRA)  

                    # Verifier si le point et la vignette existent
                    if not (os.path.exists( nom_vignette)):
                        physiocap_log( self.tr( "=~= {0} Vignette {1} absente : pas d'interpolation").\
                            format( PHYSIOCAP_WARNING, un_nom ), leModeDeTrace)
                        continue
                    if not (os.path.exists( nom_point)):
                        physiocap_log( self.tr( "=~= {0} Points de {1} absents : pas d'interpolation").\
                            format( PHYSIOCAP_WARNING, un_nom ), leModeDeTrace)
                        continue
                    else:
                        contour_avec_point = contour_avec_point + 1
                        #physiocap_log( "=~= Points - nom court : " +  nom_court_point , TRACE_INTRA)
                        #physiocap_log( "=~= Points - nom  : " +  nom_point , TRACE_INTRA)

                    # ###################
                    # CRÉATION groupe INTRA
                    # ###################
                    if ( contour_avec_point == 1):
                        if un_groupe != None:
                            vignette_projet = nom_noeud_arbre + SEPARATEUR_ + le_champ_choisi + SEPARATEUR_ + VIGNETTES_INTRA 
                            vignette_existante = un_groupe.findGroup( vignette_projet)
                            if ( vignette_existante == None ):
                                vignette_group_intra = un_groupe.addGroup( vignette_projet)
                            else:
                                if le_choix_INTRA_continue == 0:
                                    # Si vignette preexiste, on ne recommence pas
                                    raise physiocap_exception_vignette_exists( vignette_projet)            
                    try:
                        # ###############
                        # Calcul raster et iso
                        # ###############
        ##            physiocap_log( "=~= Points CHAQUE - nom court : " + nom_court_point , TRACE_INTRA)
        ##            physiocap_log( "=~= Points CHAQUE - nom  : " + nom_point , TRACE_INTRA)
                        nouveau = "NON"
                        nouveau, nom_raster_final, nom_court_raster, nom_iso_final, nom_court_isoligne = \
                            self.physiocap_creer_raster_iso( dialogue, choix_interpolation, 
                            nom_noeud_arbre, chemin_raster, chemin_iso,
                            nom_court_vignette, nom_vignette, nom_court_point, nom_point,
                            le_champ_choisi, le_choix_INTRA_continue, un_nom)
                    except physiocap_exception_windows_value_ascii as e:
                        aText = self.tr( "La valeur {0} a ").\
                            format( e)
                        aText = aText + self.tr( "des caractères (non ascii) incompatibles avec l'interpolation SAGA.")
                        aText = aText + self.tr( "Erreur bloquante sous Windows qui empêche de traiter cette interpolation.")
                        physiocap_error( self, aText, "CRITICAL")        
                        continue    
                    except:
                        raise
                    finally:
                        pass
                    # Fin de capture des err        
                    
                    
                    # Progress BAR + un stepBar%
                    positionBar = positionBarInit + ( stepBar * id_contour)    
                    dialogue.progressBarIntra.setValue( positionBar)
                    physiocap_log( "=~= Barre {0}".format( positionBar) , TRACE_INTRA)                     
                       
                    if ( id_contour >=  0 ):                                            
                        # Affichage dans panneau QGIS                           
                        if (( dialogue.checkBoxIntraIsos.isChecked()) or 
                            ( dialogue.checkBoxIntraImages.isChecked())):

                            if (consolidation == "YES"):
                                # modifier les noms courts raster et iso
                                longueur_nom_arbre = len(nom_noeud_arbre)
                                nom_court_raster_ori = nom_court_raster
                                # nom_court_raster = nom_court_raster_ori[0:longueur_nom_arbre +1] + \
                                nom_court_raster = shape_point_sans_extension + \
                                    nom_court_raster_ori[longueur_nom_arbre:]
                                nom_court_isoligne_ori = nom_court_isoligne
                                # nom_court_isoligne = nom_court_isoligne_ori[0:longueur_nom_arbre +1] + \
                                nom_court_isoligne = shape_point_sans_extension + \
                                    nom_court_isoligne_ori[longueur_nom_arbre:]

                            afficheIso = "NO"
                            if ( dialogue.checkBoxIntraIsos.isChecked()):
                                afficheIso = "YES"                
                            afficheRaster = "NO"
                            if ( dialogue.checkBoxIntraImages.isChecked()):
                                afficheRaster = "YES"
                                if nouveau == "NOUVEAUX":
                                    physiocap_affiche_raster_iso( \
                                    nom_raster_final, nom_court_raster, le_template_raster, afficheRaster,
                                    nom_iso_final, nom_court_isoligne, le_template_isolignes, afficheIso,
                                    vignette_group_intra, mon_projet)
                        physiocap_log ( self.tr( "=~= Fin Interpolation de {0} <<<<").\
                            format( un_nom), leModeDeTrace)

            if ( contour_avec_point >  0 ):                                            
                physiocap_log( self.tr( "=~= Fin des {0}/{1} interpolation(s) intra parcellaire").\
                    format( str(contour_avec_point), str( contours_possibles)), leModeDeTrace)
            else:
                aText = self.tr( "=~= Aucun point dans votre contour. ")
                aText = aText + self.tr( "Pas d'interpolation intra parcellaire.")       
                aText = aText + self.tr( "\nUn changement a eu lieu depuis votre calcul inter parcellaire.")       
                aText = aText + self.tr( "\nVérifiez le champ identifiant votre contour.")       
                physiocap_log( aText, leModeDeTrace)
                return physiocap_message_box( dialogue, aText, "information")
            
        dialogue.progressBarIntra.setValue( 100)

        return physiocap_message_box( dialogue, 
                        self.tr( "Fin de l'interpolation intra-parcellaire"),
                        "information")
                        
