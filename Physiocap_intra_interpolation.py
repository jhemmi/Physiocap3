# -*- coding: utf-8 -*-
"""
/***************************************************************************
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
        physiocap_rename_existing_file, physiocap_quelle_projection_demandee, \
        physiocap_get_layer_by_ID

from .Physiocap_var_exception import *

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from qgis.core import QgsProject, QgsVectorLayer, \
    QgsLayerTreeGroup, QgsRasterLayer, QgsMessageLog
    
def physiocap_affiche_raster_iso( nom_raster_final, nom_court_raster, le_template_raster, affiche_raster,
                    nom_iso_final, nom_court_isoligne, le_template_isolignes, affiche_iso,
                    vignette_group_intra):
    """ Affichage du raster et Iso"""
    
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
        if (( affiche_iso == "YES") and ( nom_iso_final != "") and 
            ( os.path.exists( le_template_isolignes))):
            intra_isoligne.loadNamedStyle( le_template_isolignes)

class PhysiocapIntra( QtWidgets.QDialog):
    """QGIS Pour voir les messages traduits."""

    def __init__(self, parent=None):
        """Class constructor."""
        super( PhysiocapIntra, self).__init__()
        
    def physiocap_creer_raster_iso( self, dialogue,
                nom_noeud_arbre, chemin_raster, 
                nom_court_vignette, nom_vignette, nom_court_point, nom_point,
                le_champ_choisi, un_nom):
        """ Creation du raster et Iso
        Cas Saga ou Gdal : appel des Processing (Traitement) correspondants
        """
        # Pour appel de processing on attend d'etre dans QGIS et Intra
        try :
            import processing
            try:
                from processing.core.Processing import Processing
                Processing.initialize()
            except:
                physiocap_log( self.tr( "{0} nécessite l'extension {1}").\
                    format( PHYSIOCAP_UNI, self.tr("Traitement")))
                raise physiocap_exception_no_processing( "Pas d'extension Traitement")               
            versionGDAL = processing.tools.raster.gdal.__version__
            versionSAGA = processing.algs.saga.SagaUtils.getInstalledVersion()
        except ImportError:
            physiocap_log( self.tr( "{0} nécessite l'extension {1}").\
                format( PHYSIOCAP_UNI, self.tr("Traitement")))
            raise physiocap_exception_no_processing( "Pas d'extension Traitement")
        except AttributeError:
            # Todo : Vérifier syntaxe en Win 32 bits et attraper cette erreur
            physiocap_log( self.tr( "{0} nécessite SAGA version 2.3.1 à 2.3.2").\
                format( PHYSIOCAP_UNI))
            # TODO install saga LINUX
            machine = platform.system()
            if (machine == "Linux"):
                physiocap_log ( self.tr( "= On force l'utilisation de Gdal : "))
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

        physiocap_log ( self.tr( "= Version SAGA = %s" % ( versionSAGA)))
        physiocap_log ( self.tr( "= Version GDAL = %s" % ( versionGDAL)))
        
        # Test version de SAGA, sinon annonce de l'utilisation de GDAL
        if dialogue.radioButtonSAGA.isChecked():
            unite, dixieme, centieme = versionSAGA.split( ".")
            versionNum = round( (float(unite) + float(dixieme)/10 + float(centieme)/100 ), 2)
            physiocap_log ( self.tr( "= Version SAGA = %s" % ( str( versionNum))))

            if ( versionNum >= 2.31) and ( versionNum <= 2.32):
                physiocap_log ( self.tr( "= Version SAGA OK : %s" % ( str( versionSAGA))), "INTRA")
            else:
                physiocap_log ( self.tr( "= Version SAGA %s est inférieure à 2.3.1 " % ( str( versionSAGA))))
                physiocap_log ( self.tr( "= ou supérieure à 2.3.2"))
                physiocap_log ( self.tr( "= On force l'utilisation de Gdal : "))
                dialogue.radioButtonSAGA.setEnabled( False)
                dialogue.radioButtonGDAL.setChecked(  Qt.Checked)
                dialogue.radioButtonSAGA.setChecked(  Qt.Unchecked)
                dialogue.spinBoxPower.setEnabled( False)
                physiocap_message_box( dialogue,
                    self.tr( "= Saga a une version incompatible : on force l'utilisation de Gdal" ),
                    "information")

        # Récupération des parametres d'Intra
        rayonDoubleIntra = float ( dialogue.spinBoxDoubleRayon.value())
        physiocap_log( self.tr( "== Double rayon saisi =>> {0} ==== ").\
            format(  str(rayonDoubleIntra)), "INTRA")
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
      
        # Trace des entités en entrée
        physiocap_log( self.tr( "== Nom =>> {0} ==== ").\
            format(  un_nom), "INTRA")
        physiocap_log( self.tr( "Vignette (moyenne Inter) {0} et chemin à la vignette \n{1}").\
            format( nom_court_vignette, nom_vignette), "INTRA")
        physiocap_log( self.tr( "Point {0} et chemin aux points \n{1}").\
            format( nom_court_point, nom_point), "INTRA")
        physiocap_log( self.tr( "== Champ = {0} <<=== ").\
            format(  le_champ_choisi), "INTRA")
        # Lire points_vector et vignette_vector
        try:
            # Attrapper l'existance du fichier pour monter erreur (cas BIOMGM2)
            vignette_vector = QgsVectorLayer( nom_vignette, nom_court_vignette, 'ogr')
        except:
            physiocap_log( self.tr( "{0} ne retrouve pas vos contours {1}").\
                format( PHYSIOCAP_UNI, nom_court_vignette))
            raise physiocap_exception_project_contour_incoherence( nom_court_vignette)     
        try:
            QgsVectorLayer( nom_point, nom_court_point, 'ogr')
        except:
            physiocap_log( self.tr( "{0} ne retrouve pas la couche de point {1}").\
                format( PHYSIOCAP_UNI, nom_court_point))
            raise physiocap_exception_project_point_incoherence( nom_court_point)       
     
        laProjectionCRS, laProjectionTXT, EXT_CRS_SHP, EXT_CRS_PRJ, EXT_CRS_RASTER, EPSG_NUMBER = \
            physiocap_quelle_projection_demandee(dialogue)

        # ###################
        # CRÉATION raster
        # ###################
        # Nom du raster avec le_champ_choisi
        nom_court_raster = nom_noeud_arbre + NOM_INTRA + SEPARATEUR_ + le_champ_choisi +  \
            SEPARATEUR_ + un_nom + EXT_CRS_RASTER
        nom_raster =  physiocap_rename_existing_file( os.path.join( chemin_raster, nom_court_raster)) # utile physiocap_rename_existing_file()        
        nom_raster_temp = physiocap_rename_existing_file( os.path.join( MON_TEMP, nom_court_raster))
        nom_court_isoligne = nom_noeud_arbre + NOM_INTRA  + SEPARATEUR_  + le_champ_choisi  + \
            SEPARATEUR_ + "ISOLIGNE_" + un_nom + EXT_CRS_SHP
        nom_isoligne =  physiocap_rename_existing_file( os.path.join( chemin_raster, nom_court_isoligne)) # utile physiocap_rename_existing_file()        
        
        physiocap_log( self.tr( "isoligne {0} et chemin vers isoligne\n{1}").\
            format( nom_court_isoligne, nom_isoligne), "INTRA")
        
        
        # TODO : supprimer les controles Sous Windows :attraper les exceptions processing SAGA ascii        
        try:
            # Gérer le cas de la valeur d'un champ à part
            if platform.system() == 'Windows':            
                physiocap_log( "Type de un_nom " + str( type( un_nom)), "INTRA")
                un_nom.decode("ascii")
        except UnicodeEncodeError:
            physiocap_log( self.tr( "{0} ne peut pas dialoguer avec Saga et des caractères non ascii").\
                format( PHYSIOCAP_UNI))
            raise physiocap_exception_windows_value_ascii( un_nom)  
        
        try:
            if platform.system() == 'Windows':            
                unicode( nom_isoligne)
                physiocap_log( "Type de isoligne " + str( type( nom_isoligne)), "INTRA")
                nom_isoligne.decode("ascii")
        except UnicodeEncodeError:
            physiocap_log( self.tr( "{0} ne peut pas dialoguer avec Saga et des caractères non ascii").\
                format( PHYSIOCAP_UNI))
            #physiocap_log( e)
            raise physiocap_exception_windows_saga_ascii( nom_isoligne)  

        # Initialisation avant Interpolation
        premier_raster =""
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
        info_extent = str(xmin) + "," + str(xmax) + "," + str(ymin) + "," + str(ymax)
        physiocap_log( "=~= Extent layer >>> " + info_extent + " <<<")  
        
        info_extent_epsg = info_extent + " [EPSG:" + str( EPSG_NUMBER) + "]"
        
        if dialogue.radioButtonSAGA.isChecked():
            # Appel SAGA power à 2 fixe
            physiocap_log( self.tr( "=~= Interpolation SAGA dans {0}").\
                format(  nom_court_raster))
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
        
            IDW_SAGA = { 'SHAPES' : nom_point, 
                'SEARCH_POINTS_ALL' : 1, 
                'TARGET_DEFINITION' : 1, 
                'DW_IDW_OFFSET' : False, 
                'DW_IDW_POWER' : 2, 
                'SEARCH_RANGE' : 0, 
                'TARGET_TEMPLATE' : '', 
                'SEARCH_POINTS_MIN' : -1, 
                'FIELD' : le_champ_choisi, 
                'SEARCH_POINTS_MAX' : 1, 
                'TARGET_USER_SIZE' : 100, 
                'DW_BANDWIDTH' : 1, 
                'TARGET_USER_FITS' : 0, 
                'SEARCH_DIRECTION' : 0, 
                'DW_WEIGHTING' : pixelIntra, 
                'TARGET_OUT_GRID' : nom_raster_temp, 
                'SEARCH_RADIUS' : rayonDoubleIntra, 
                'OUTPUT_EXTENT' : info_extent_epsg }
                
            physiocap_log( "=xg= Parametre d'IDW {0}".\
                        format( IDW_SAGA ))   
            premier_raster = processing.run("saga:inversedistanceweightedinterpolation", IDW_SAGA)
    
#            premier_raster = processing.runalg("saga:inversedistanceweighted",
#                nom_point, le_champ_choisi, 1, 2, 1, 0,rayonDoubleIntra, 0, 1,
#                10, info_extent, pixelIntra,
#                None) 
                                       
            if (( premier_raster != None) and ( str( list( premier_raster)).find( "USER_GRID") != -1)):
                if premier_raster[ 'USER_GRID'] != None:
                    nom_raster_temp = premier_raster[ 'USER_GRID']
                    physiocap_log( "=~= Premier raster : inversedistanceweighted \n{0}".\
                        format( nom_raster_temp), "INTRA")
                else:
                    physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
                        format("inversedistanceweighted","B"))
                    raise physiocap_exception_interpolation( nom_point)
            else:
                physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
                    format("inversedistanceweighted","A"))
                raise physiocap_exception_interpolation( nom_point)
                                            
            # On passe ETAPE CLIP si nom_raster_temp existe
            if ( nom_raster_temp != ""):
                raster_dans_poly = processing.runalg("saga:clipgridwithpolygon",
                nom_raster_temp,
                nom_vignette,
                nom_raster)
            
            if (( raster_dans_poly != None) and ( str( list( raster_dans_poly)).find( "OUTPUT") != -1)):
                if raster_dans_poly[ 'OUTPUT'] != None:
                    nom_raster_final = raster_dans_poly[ 'OUTPUT']
                    physiocap_log( self.tr("=~= Raster clippé : clipgridwithpolygon\n{0}").\
                        format( nom_raster_final), "INTRA")
                else:
                    physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
                        format("clipgridwithpolygon","B"))
                    raise physiocap_exception_interpolation( nom_point)
            else:
                physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
                    format("clipgridwithpolygon","A"))
                raise physiocap_exception_interpolation( nom_point)

            # On passe ETAPE ISO si nom_raster_final existe
            if ( nom_raster_final != ""):
                # Isolignes
                iso_dans_poly_brut = processing.runalg("saga:contourlinesfromgrid",
                    nom_raster_final,
                    isoMin, isoMax, isoInterlignes,
                    None)
                # physiocap_log( self.tr( "=~= Interpolation SAGA - Etape 2 - FIN"))
            
                if (( iso_dans_poly_brut != None) and ( str( list( iso_dans_poly_brut)).find( "CONTOUR") != -1)):
                    if iso_dans_poly_brut[ 'CONTOUR'] != None:
                        nom_iso_sans_ELEV = iso_dans_poly_brut[ 'CONTOUR']
                        physiocap_log( self.tr("=~= Iso sans LEVEL : contourlinesfromgrid\n{0}").\
                            format( nom_iso_sans_ELEV), "INTRA")
                    else:
                        physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
                            format("contourlinesfromgrid","B"))
                        raise physiocap_exception_interpolation( nom_point)
                else:
                    physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
                        format("contourlinesfromgrid","A"))
                    raise physiocap_exception_interpolation( nom_point)

                # On passe ETAPE FIELD si nom_iso_sans_ELEV existe
                if ( nom_iso_sans_ELEV != ""):                              
                    iso_dans_poly_plus = processing.runalg("qgis:addfieldtoattributestable", \
                        nom_iso_sans_ELEV, \
                        "ELEV", 1, 15, 2 , None)
 
                if (( iso_dans_poly_plus != None) and ( str( list( iso_dans_poly_plus)).find( "OUTPUT_LAYER") != -1)):
                    if iso_dans_poly_plus[ 'OUTPUT_LAYER'] != None:
                        nom_iso_avec_ELEV = iso_dans_poly_plus[ 'OUTPUT_LAYER']
                        physiocap_log( self.tr("=~= Iso avec LEVEL ajouté : addfieldtoattributestable\n{0}").\
                            format( nom_iso_avec_ELEV), "INTRA")
                    else:
                        physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
                            format("addfieldtoattributestable","B"))
                        raise physiocap_exception_interpolation( nom_point)
                else:
                    physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
                        format("addfieldtoattributestable","A"))
                    raise physiocap_exception_interpolation( nom_point)

                # On passe ETAPE CALCULATOR si nom_iso_final existe
                if ( nom_iso_avec_ELEV != ""):                              
                    # Retrouver le nom de l'attribut créé
                    intra_iso_modifie = QgsVectorLayer( nom_iso_avec_ELEV, 
                            "Ne pas voir serait mieux", 'ogr')
                    fields = intra_iso_modifie.pendingFields()
                    field_probable = fields[1]
                    field_name = field_probable.name()
                    # A_TESTER: sans str et à suivre ensuite
                    field_formule = '"' + str( field_name) + '"'  
                    physiocap_log( "=~= Isolignes formule : " + str( field_formule), "INTRA")                                                 
                    QgsMessageLog.logMessage( "PHYSIOCAP : Avant calculator ", "Processing", QgsMessageLog.WARNING)
                    # Le remplacer par "ELEV", en fait on le copie dans "ELEV"
                    iso_dans_poly = processing.runalg("qgis:fieldcalculator", \
                        nom_iso_avec_ELEV, "ELEV", 0, 15, 2, False, field_formule , nom_isoligne)

                if (( iso_dans_poly != None) and ( str( list( iso_dans_poly)).find( "OUTPUT_LAYER") != -1)):
                    if iso_dans_poly[ 'OUTPUT_LAYER'] != None:
                        nom_iso_final = iso_dans_poly[ 'OUTPUT_LAYER']
                        physiocap_log( self.tr("=~= Iso final : fieldcalculator\n{0}").\
                            format( nom_iso_final), "INTRA")
                    else:
                        physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
                            format("fieldcalculator","B"))
                        raise physiocap_exception_interpolation( nom_point)
                else:
                    physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
                        format("fieldcalculator","A"))
                    raise physiocap_exception_interpolation( nom_point)
            else:
                physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
                    format("clipgridwithpolygon","0"))
                raise physiocap_exception_interpolation( nom_point)
            physiocap_log( self.tr( "=~= Interpolation SAGA - Fin iso - {0}").\
                format( nom_iso_final), "INTRA")          
        else:
            # Appel GDAL
##            physiocap_log( self.tr( "=xg= Interpolation GDAL {0}").\
##                format( nom_court_raster))
            # Paramètres apres le champ
            # Power vaut 2 
            # lissage à 0 car ce lissage peut se faire dans les propriétés du raster
            # Rayon identique (unité douteuse)
            # Max points à 1000 difference avec SAGA    
            # Min à 5 
            # Angle à 0 (c'est l'angle de l'elipse
            try:
                index_metrique = ATTRIBUTS_INTRA_INDEX[le_champ_choisi]
            except:
                physiocap_log( "=xg= Pas de {0} dans le vecteur \n{1}".\
                        format( le_champ_choisi, nom_point ))
                index_metrique = 4  # On force le DIAM
                # TODO raise

####   KO troisieme param syntaxe ???
                # TEST IDW
####            a_interpoler = [ nom_point, False, str(index_metrique) , '0']
####            parametres_IDW = {'INTERPOLATION_DATA' : a_interpoler,
####                'DISTANCE_COEFFICIENT' : rayonDoubleIntra,
####                'COLUMNS': pixelIntra,
####                'ROWS': pixelIntra,
####                'EXTENT':info_extent_epsg, 
####                'OUTPUT':nom_raster_temp
####                }
####            physiocap_log( "=xg= Parametre d'IDW {0}".\
####                        format( parametres_IDW ))           
####            premier_raster = processing.run("qgis:idwinterpolation",
####                parametres_IDW)
            
            # TEST GDAL
            
####    KO incorrect OUTPUT avec None
            parametres_gridinv = {'INPUT':nom_point,
            'POWER':2,'SMOOTHING':1,'RADIUS_1':0,'RADIUS_2':0,'ANGLE':0,'MAX_POINTS':1000,'MIN_POINTS':5,'NODATA':0,
            'OPTIONS':'','DATA_TYPE':5,'OUTPUT':nom_raster_temp}
            premier_raster = processing.run("gdal:gridinversedistance", 
            parametres_gridinv)

#  OLD GDAL      premier_raster = processing.runalg("gdalogr:gridinvdist",
#                nom_point, le_champ_choisi, powerIntra, 0.0, rayonDoubleIntra, rayonDoubleIntra, 
#                1000, 5, angle, val_nulle ,float_32, 
#                None)
          
            if (( premier_raster != None) and ( str( list( premier_raster)).find( "OUTPUT") != -1)):
                if premier_raster[ 'OUTPUT'] != None:
                    nom_raster_temp = premier_raster[ 'OUTPUT']
                    physiocap_log( "=xg= Premier raster : gridinvdist \n{0}".\
                        format( nom_raster_temp), "INTRA")
                else:
                    physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
                        format("gridinvdist","B"))
                    raise physiocap_exception_interpolation( nom_point)
            else:
                physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
                    format("gridinvdist","A"))
                raise physiocap_exception_interpolation( nom_point)           
            QgsMessageLog.logMessage( "PHYSIOCAP : Avant clip", "Processing", QgsMessageLog.WARNING)
            
###            option_clip_raster = ""
###            if ( EPSG_NUMBER == EPSG_NUMBER_L93 ):
###                #physiocap_log( "=xg= Projection à translater vers : " + str( EPSG_NUMBER) )
###                #option_clip_raster = '-s_2015-12-09T16:17:46	1	PHYSIOCAP : Avant calculator 
###                #srs "EPSG:' + str(EPSG_NUMBER_GPS) + '" -t_srs "EPSG:' + str(EPSG_NUMBER_L93) + '"'
###                # A_TESTER: old était str(EPSG_NUMBER_L93)
###                option_clip_raster = "-t_srs \"EPSG:" + EPSG_NUMBER_L93 + "\""
            

            # On passe ETAPE CLIP si nom_raster_temp existe
            if ( nom_raster_temp != ""):
###                physiocap_log( self.tr( "=xg= Option du clip: {0}").\
###                    format( option_clip_raster), "INTRA") 
###                # Tester la version de GDAL ou de processing
###                unite, dixieme, millieme = versionGDAL.split( ".")
###                versionNum = float(unite) + float(dixieme)/10 + float(millieme)/100

                param_cli = {'INPUT':nom_raster_temp,
                    'MASK':nom_vignette,
                    'NODATA':-9999,
                    'ALPHA_BAND':False,
                    'CROP_TO_CUTLINE':True,
                    'KEEP_RESOLUTION':False,
                    'OPTIONS':'',
                    'DATA_TYPE':5,
                    'OUTPUT':nom_raster}
                raster_dans_poly = processing.run( "gdal:cliprasterbymasklayer", param_cli)                    

###                # 2.1 tester sous ubuntu et 2.02 sous Fedora 23
###                if ( versionNum >= 2.02):
###                    physiocap_log ( self.tr( "= Version GDAL %s => 16 arguments" % ( str( versionGDAL))))
###                    raster_dans_poly = processing.runalg("gdalogr:cliprasterbymasklayer",
###                    nom_raster_temp,
###                    nom_vignette,
###                    "-9999",False,True,
###                    True, 5, 4, 75, 6, 1, False, 0, False,
###                    "", 
###                    nom_raster)
###                else:
###                    # Version à 7 arg
###                    raster_dans_poly = processing.runalg("gdalogr:cliprasterbymasklayer",
###                    nom_raster_temp,
###                    nom_vignette,
###                    "-9999",False,False,
###                    option_clip_raster, 
###                    nom_raster)
###            
            if (( raster_dans_poly != None) and ( str( list( raster_dans_poly)).find( "OUTPUT") != -1)):
                if raster_dans_poly[ 'OUTPUT'] != None:
                    nom_raster_final = raster_dans_poly[ 'OUTPUT']
                    physiocap_log( self.tr("=xg= Raster clippé : cliprasterbymasklayer \n{0}").\
                        format( nom_raster_temp), "INTRA")
                else:
                    physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
                        format("cliprasterbymasklayer","B"))
                    raise physiocap_exception_interpolation( nom_point)
            else:
                physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
                    format("cliprasterbymasklayer","A"))
                raise physiocap_exception_interpolation( nom_point)
            
            QgsMessageLog.logMessage( "PHYSIOCAP : Avant Iso", "Processing", QgsMessageLog.WARNING)

            # On passe ETAPE ISO si nom_raster_final existe
            if ( nom_raster_final != ""):
                # Isolignes
                iso_dans_poly = processing.runalg("gdalogr:contour",
                    nom_raster,
                    isoInterlignes,
                    "ELEV",
                    "",
                    nom_isoligne)
                                
            if (( iso_dans_poly != None) and ( str( list( iso_dans_poly)).find( "OUTPUT_VECTOR") != -1)):
                if iso_dans_poly[ 'OUTPUT_VECTOR'] != None:
                    nom_iso_final = iso_dans_poly[ 'OUTPUT_VECTOR']
                    physiocap_log( self.tr("=xg= isoligne FINAL : contour \n{0}").\
                        format( nom_iso_final), "INTRA")
                else:
                    physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
                        format("contour","B"))
                    raise physiocap_exception_interpolation( nom_point)
            else:
                physiocap_error( self, self.tr( "=~= Problème bloquant durant {0} partie-{1}").\
                    format("contour","A"))
                raise physiocap_exception_interpolation( nom_point)
        
        return nom_raster_final, nom_court_raster, nom_iso_final, nom_court_isoligne            

    def physiocap_interpolation_IntraParcelles( self, dialogue):
        """Interpolation des données de points intra parcellaires"""
        NOM_PROJET = dialogue.lineEditProjet.text()

        # QT Confiance 
        le_champ_choisi = dialogue.fieldComboIntra.currentText()
        # Récupérer des styles pour chaque shape
        #dir_template = os.path.join( os.path.dirname(__file__), 'modeleQgis')       
        dir_template = dialogue.fieldComboThematiques.currentText()
        qml_prefix = dialogue.lineEditThematiqueIntraImage.text().strip('"')
        # A_TESTER: sans str
        nom_intra_attribut = qml_prefix + str( le_champ_choisi) + EXTENSION_QML
        le_template_raster = os.path.join( dir_template, nom_intra_attribut)
        qml_prefix = dialogue.lineEditThematiqueIntraIso.text().strip('"')
        nom_isolignes_attribut = qml_prefix + le_champ_choisi + EXTENSION_QML
        le_template_isolignes  = os.path.join( dir_template, nom_isolignes_attribut)
        
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
        leChampPoly = dialogue.fieldComboContours.currentText()
            
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
       
        physiocap_log( self.tr( "=~= {0} début de l'interpolation des points de {1}").\
            format( PHYSIOCAP_UNI, nom_noeud_arbre))
        # Progress BAR 2%
        dialogue.progressBarIntra.setValue( 2)
        
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
                   
        # Récupération de la projection en cours
        laProjectionCRS, laProjectionTXT, EXT_CRS_SHP, EXT_CRS_PRJ, EXT_CRS_RASTER, EPSG_NUMBER = \
            physiocap_quelle_projection_demandee(dialogue)

        # Assert repertoire shapefile 
        # TODO pourquoi unicode
        chemin_shapes = os.path.dirname( unicode( vecteur_point.dataProvider().dataSourceUri() ) )
        shape_point_extension = os.path.basename( unicode( vecteur_point.dataProvider().dataSourceUri() ) ) ;
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
            chemin_vignettes = os.path.join( chemin_shapes, VIGNETTES_INTER)
        # Assert repertoire vignette inter 
        if not (os.path.exists( chemin_vignettes)):
            raise physiocap_exception_rep( VIGNETTES_INTER)

        # Création du REP RASTER
        #chemin_projet = os.path.join( repertoire_data, nom_noeud_arbre)
        #chemin_raster = os.path.join(chemin_projet, REPERTOIRE_RASTERS)
        # Test selon Consolidation
        if (consolidation == "YES"):
            chemin_raster = os.path.join( chemin_shape_nom_point, REPERTOIRE_RASTERS)
        else:
            chemin_raster = os.path.join( chemin_shapes, REPERTOIRE_RASTERS)
        if not (os.path.exists( chemin_raster)):
            try:
                os.mkdir( chemin_raster)
            except:
                raise physiocap_exception_rep( REPERTOIRE_RASTERS)

        # Progress BAR 4%
        dialogue.progressBarIntra.setValue( 4)

        lesFormes = vecteur_poly.getFeatures()
        iforme = 0
        for f in lesFormes:
            iforme = iforme + 1
        stepBar = int( 60 / iforme)
        positionBar = 5
        


        # On passe sur le contour général
        contour_avec_point = 0
        contours_possibles = 0
       
        # #####################
        # Cas d'une image seule
        # #####################
        if ( dialogue.checkBoxIntraUnSeul.isChecked()):
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
                nom_court_point = NOM_PROJET + NOM_POINTS + EXT_CRS_SHP     
            nom_point = os.path.join( chemin_shapes, nom_court_point)                    

            # Vérifier si le point et la vignette existent
            if not (os.path.exists( nom_vignette)):
                physiocap_log( self.tr( "=~=  Pas d'interpolation, Vignette absente : {0}").\
                    format( nom_vignette))
            if not (os.path.exists( nom_point)):
                physiocap_log( self.tr( "=~=  Pas d'interpolation, Points absents : {0}").\
                    format( nom_point))
            else:
                try:
                    # ###############
                    # Calcul raster et iso
                    # ###############
                    physiocap_log( self.tr( "=~=  Le contour : {0}").\
                        format( nom_vecteur_contour), "INTRA")
                    nom_raster_final, nom_court_raster, nom_iso_final, nom_court_isoligne = \
                        self.physiocap_creer_raster_iso( dialogue,
                        nom_noeud_arbre, chemin_raster, 
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
                    # Si vignette preexiste, on ne recommence pas
                    raise physiocap_exception_vignette_exists( vignette_projet) 

            if ( contour_avec_point >  0 ):                                            
                # Affichage dans panneau QGIS                           
                if ( dialogue.checkBoxIntraUnSeul.isChecked()):
                    physiocap_affiche_raster_iso( \
                        nom_raster_final, nom_court_raster, le_template_raster, "YES",
                        nom_iso_final, nom_court_isoligne, le_template_isolignes, "YES",
                        vignette_group_intra)


        # Progress BAR + un stepBar%
        positionBar = positionBar + stepBar     
        dialogue.progressBarIntra.setValue( positionBar)
        positionBarInit = positionBar

        #Eviter de tourner en Intra sur chaque parcelle
        if (( dialogue.checkBoxIntraIsos.isChecked()) or 
                    ( dialogue.checkBoxIntraImages.isChecked())):        
          
            # On tourne sur les contours qui ont été crée par Inter
            # On passe sur les differents contours de chaque parcelle
            id_contour = 0
            for un_contour in vecteur_poly.getFeatures(): #iterate poly features
                id_contour = id_contour + 1
                contours_possibles = contours_possibles + 1
                try:
                    # A_TESTER: sans str
                    un_nom = str( un_contour[ leChampPoly]) #get attribute of poly layer
                    #un_nom = un_contour[ leChampPoly] #get attribute of poly layer
                except:
                    un_nom = "PHY_ID_" + str(id_contour)
                    pass

                physiocap_log ( self.tr( "=~= Début Interpolation de {0} >>>>").\
                    format( un_nom))

                # Nom du Shape moyenne 
                nom_court_vignette = nom_noeud_arbre + NOM_MOYENNE + un_nom +  EXT_CRS_SHP     
                # Attention j'ai enleve physiocap_rename_existing_file(
                nom_vignette = os.path.join( chemin_vignettes, nom_court_vignette)        
                                                       
                # Nom point 
                nom_court_point = nom_noeud_arbre + NOM_POINTS + SEPARATEUR_ + un_nom + EXT_CRS_SHP     
                # WARNING: JH Attention j'ai enleve physiocap_rename_existing_file(
                nom_point = os.path.join( chemin_vignettes, nom_court_point)                    
                #physiocap_log( "=~= Vignette court : " +  nom_court_vignette )       

                # Verifier si le point et la vignette existent
                if not (os.path.exists( nom_vignette)):
                    physiocap_log( self.tr( "=~= Vignette absente : pas d'interpolation"))
                    continue
                if not (os.path.exists( nom_point)):
                    physiocap_log( self.tr( "=~= Points absents : pas d'interpolation"))
                    continue
                else:
                    contour_avec_point = contour_avec_point + 1
                    #physiocap_log( "=~= Points - nom court : " +  nom_court_point )
                    #physiocap_log( "=~= Points - nom  : " +  nom_point )

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
                            # Si vignette preexiste, on ne recommence pas
                            raise physiocap_exception_vignette_exists( vignette_projet) 
         
                try:
                    # ###############
                    # Calcul raster et iso
                    # ###############
    ##            physiocap_log( "=~= Points CHAQUE - nom court : " + nom_court_point )
    ##            physiocap_log( "=~= Points CHAQUE - nom  : " + nom_point )
                    nom_raster_final, nom_court_raster, nom_iso_final, nom_court_isoligne = \
                        self.physiocap_creer_raster_iso( dialogue, nom_noeud_arbre, chemin_raster, 
                        nom_court_vignette, nom_vignette, nom_court_point, nom_point,
                        le_champ_choisi, un_nom)
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
                # A_TESTER: sans str
                physiocap_log( "=~= Barre " + str( positionBar) )                      
                   
                if ( id_contour >  0 ):                                            
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
                        physiocap_affiche_raster_iso( \
                            nom_raster_final, nom_court_raster, le_template_raster, afficheRaster,
                            nom_iso_final, nom_court_isoligne, le_template_isolignes, afficheIso,
                            vignette_group_intra)
                    physiocap_log ( self.tr( "=~= Fin Interpolation de {0} <<<<").\
                        format( un_nom))

        if ( contour_avec_point >  0 ):                                            
            physiocap_log( self.tr( "=~= Fin des {0}/{1} interpolation(s) intra parcellaire").\
                format( str(contour_avec_point), str( contours_possibles)))
        else:
            aText = self.tr( "=~= Aucun point dans votre contour. ")
            aText = aText + self.tr( "Pas d'interpolation intra parcellaire")       
            physiocap_log( aText)
            return physiocap_message_box( dialogue, aText, "information")
            
        dialogue.progressBarIntra.setValue( 100)

        return physiocap_message_box( dialogue, 
                        self.tr( "Fin de l'interpolation intra-parcellaire"),
                        "information")
                        
