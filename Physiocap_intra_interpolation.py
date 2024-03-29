# -*- coding: utf-8 -*-
""""
/***********************************************************************
 Physiocap_intra_interpolation
                                 A QGIS 3 plugin
 Physiocap3 plugin helps analyse raw data from Physiocap in QGIS 3 and 
 creates a synthesis of Physiocap measures' campaign
 Physiocap3 plugin permet l'analyse les données brutes de Physiocap dans QGIS 3 et
 crée une synthese d'une campagne de mesures Physiocap
 
 Le module Intra gère l'interpolation des données le chaque parcelle
 à partir d'un vecteur de contour de parcelles et d'un vecteur de points de
 chaque parcelle
 Il s'appuie sur les créations du module Inter

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
from .Physiocap_tools import ( physiocap_message_box,\
        physiocap_log, physiocap_error, physiocap_is_only_ascii, \
        physiocap_nom_entite_sans_pb_caractere,  physiocap_nom_entite_avec_pb_caractere, \
        physiocap_rename_existing_file, quelle_projection_et_format_vecteur, \
        quel_chemin_templates, quel_qml_existe, quel_sont_vecteurs_choisis, \
        assert_parcelle_attendue, assert_champs_agro_obligatoires, assert_quel_format_entete)

from .Physiocap_var_exception import *

from PyQt5 import QtWidgets
from PyQt5.QtXml import QDomDocument
from PyQt5.QtCore import ( Qt)

from qgis.core import ( Qgis, QgsProject, QgsVectorLayer, \
    QgsLayerTreeGroup, QgsRasterLayer, QgsMessageLog,  \
    QgsFeatureRequest, QgsExpression, QgsProcessingUtils,  QgsProcessingFeedback, \
    QgsRectangle, QgsLayout, QgsReadWriteContext, QgsLayoutExporter, QgsLayerTree)

### copy qpt import shutil

class PhysiocapIntra( QtWidgets.QDialog):
    """QGIS Pour voir les messages traduits."""
    
    def __init__(self, parent=None):
        """Class constructor."""
        #print("INTRA init class")
        super( PhysiocapIntra, self).__init__()

    def dump_noeuds_legende(self, le_modele,  libelle = "Modèle de la légende"):
        if le_modele == None:
            physiocap_log( "{} : la légende sans noeud".format( libelle), TRACE_PDF)
        else:
            physiocap_log( "{} : le modele contient {} niveau".format( libelle, le_modele.rowCount()), TRACE_PDF)
            for un_noeud in le_modele.children():
#                print( un_noeud.__class__)
#                print( dir( un_noeud))
#                print( type( un_noeud))                
#                print( "==============================")
                physiocap_log( "{} : le noeud a une classe {}".format( libelle, un_noeud.__class__), TRACE_PDF)
                physiocap_log( "{} : le noeud a un parent {}".format( libelle, dir( un_noeud.parent)), TRACE_PDF)
                physiocap_log( "{} : la noeud a un dump {}".format( libelle, un_noeud.dumpObjectInfo), TRACE_PDF)
                #physiocap_log( "{} : le noeud a un nom {}".format( libelle, dir( un_noeud)), TRACE_PDF)
                physiocap_log( "{} : la noeud a une property {}".format( libelle, dir( un_noeud.property)), TRACE_PDF)
##                for sous_noeud in un_noeud.children():
##                    physiocap_log( "== {} : le sous_noeud a un nom {}".format( libelle, sous_noeud.objectName), TRACE_PDF)
                
    def dump_couches(self, itemCarte,  libelle = "Pour PDF"):
        les_couches = itemCarte.layers()
        if les_couches == None:
            physiocap_log( "{} : la carte sans couche".format( libelle), TRACE_PDF)
        else:
            physiocap_log( "{} : la carte a {} couches".format( libelle, len(  les_couches)), TRACE_PDF)
            for une_couche in les_couches:
                physiocap_log( "{} : la couche a un nom {}".format( libelle, une_couche.name()), TRACE_PDF)

    def imprimer_raster( self, dialogue, nom_raster_final, nom_court_raster, 
                    nom_parcelle, nom_attribut, moyenne = 'Inconnue'):
        """ Impression PDF du raster"""
        leModeDeTrace = dialogue.fieldComboModeTrace.currentText() 
        derniere_session = dialogue.lineEditDerniereSession.text()
        repertoire_resultat = dialogue.lineEditDirectoryFiltre.text()
        chemin_session = os.path.join( repertoire_resultat, derniere_session)
        profil_physiocap = dialogue.fieldComboProfilPHY.currentText()
        chemin_pdf = os.path.join( chemin_session, "cartes")
        if not os.path.exists( chemin_pdf):           
            os.mkdir( chemin_pdf)
        nom_pdf = os.path.join( chemin_pdf, nom_attribut + SEPARATEUR_+ nom_parcelle + EXTENSION_PDF)
        if os.path.exists( nom_pdf):           
            physiocap_log( "PDF existe déjà pour {} et parcelle {}".\
                format( nom_attribut, nom_parcelle),  leModeDeTrace)
            return physiocap_error( self, "Pour {} et parcelle {}, le PDF existe déjà {}".\
                format( nom_attribut, nom_parcelle, nom_pdf))

        # Charger un modele qpt dans les composer_template
######        chemin_composer = os.path.join( dialogue.gis_dir, 'composer_templates')
######   OK linux et windows JH     tmpfile = os.path.join( chemin_composer, profil_physiocap + EXTENSION_QPT)
######        if not os.path.exists( tmpfile):
######            chemin_modele = os.path.join( dialogue.plugin_dir,'modeleQGIS')
######            chemin = os.path.join( chemin_modele,'Mise_en_page')
######            modele_file = os.path.join( chemin, profil_physiocap + EXTENSION_QPT)
######            if not os.path.exists( modele_file):
######                raise physiocap_exception_agro_no_pdf_modele( modele_file)
######            # Copier le template pour chaque utilisateur
######            shutil.copy( modele_file, chemin_composer)
        chemin_modele = os.path.join( dialogue.plugin_dir,'modeleQGIS')
        chemin = os.path.join( chemin_modele,'Mise_en_page')
        modele_file = os.path.join( chemin, profil_physiocap + EXTENSION_QPT)
        if not os.path.exists( modele_file):
            raise physiocap_exception_agro_no_pdf_modele( modele_file)
        
#### OK        with open(tmpfile) as f:
        with open(modele_file) as f:
            template_content = f.read()
        doc = QDomDocument()
        doc.setContent(template_content)

        if ( nom_raster_final != ""):
            if not os.path.exists( nom_raster_final):           
                physiocap_log( "=~= {2} {0} ne retrouve pas votre raster {1} pour impresssion PDF".\
                    format( PHYSIOCAP_UNI, nom_court_raster, PHYSIOCAP_WARNING), TRACE_INTRA)
                raise physiocap_exception_raster_manquant( nom_court_raster)     

            p = QgsProject.instance()
            miseEnPage = QgsLayout( p)
            miseEnPage.initializeDefaults()
            mes_couches = QgsProject.instance().mapLayersByName( nom_court_raster)
            
            # Customisation des items Titre Moyenne 
            items, ok = miseEnPage.loadFromTemplate(doc, QgsReadWriteContext(), False)       
            #physiocap_log( "PDF : OK de la mise en page {} ".format( ok), TRACE_PDF)
            itemTitre = miseEnPage.itemById( "Titre")
            libelle, unite = DICT_ATTRTIBUT_UNITE[ nom_attribut]
            itemTitre.setText( "Parcelle {1} - {0} ({2})".format( libelle, nom_parcelle, unite))
            itemMoyenne = miseEnPage.itemById( "Moyenne")
            itemMoyenne.setText( "Moyenne : {}".format( moyenne))
            # raster dans la carte 
            itemCarte = miseEnPage.itemById( "Carte")
            itemCarte.setLayers( mes_couches)
            # Reglage Extend
            rect = QgsRectangle(  mes_couches[0].extent())
            rect.scale(1.0)
            itemCarte.zoomToExtent(rect)

            # Légende
            itemLegende = miseEnPage.itemById( "Légende")
            # OK mais toutes les entrées dans légende : itemLegende.setLinkedMap( itemCarte) 
            layerTree = QgsLayerTree()
            layerTree.addLayer( mes_couches[0])
            itemLegende.model().setRootGroup(layerTree)
            #physiocap_log( "PDF : la {} contient \n{} ".format( itemLegende.id(),  dir( itemLegende)), TRACE_PDF)

            exporter = QgsLayoutExporter(miseEnPage)
            exporter.exportToPdf(nom_pdf, QgsLayoutExporter.PdfExportSettings())
            physiocap_log( "Impression en PDF (au format {}) pour attribut {} et parcelle {}".format( profil_physiocap, nom_attribut, nom_parcelle), leModeDeTrace)
        
    def afficher_raster_iso( self, dialogue, nom_raster_final, nom_court_raster, 
                    le_template_raster, affiche_raster,
                    nom_iso_final, nom_court_isoligne, le_template_isolignes, affiche_iso,
                    vignette_group_intra, mon_projet):
        """ Affichage du raster et Iso"""
        #leModeDeTrace = dialogue.fieldComboModeTrace.currentText() 
        #Nom_Profil =  dialogue.fieldComboProfilPHY.currentText()
        #physiocap_log( "=~= Template sont ici {} et pour le profil {}".format( le_template_raster, Nom_Profil))
        if ( nom_raster_final != ""):
            if os.path.exists( nom_raster_final):           
                intra_raster = QgsRasterLayer( nom_raster_final, nom_court_raster)
                if ( nom_iso_final != "") and affiche_iso == "YES":
                    if os.path.exists( nom_iso_final):           
                        intra_isoligne = QgsVectorLayer( nom_iso_final, 
                            nom_court_isoligne, 'ogr')
                    else:
                        physiocap_log( "=~= {2} {0} ne retrouve pas votre isoligne pour {1}. \nVérifiez votre paramètrage pour isolignes".\
                            format( PHYSIOCAP_UNI, nom_court_isoligne, PHYSIOCAP_WARNING), TRACE_INTRA)
                        # Bloque tout pour cas particulier : raise physiocap_exception_iso_manquant( nom_court_isoligne)  
                        affiche_iso = "NO"
            else:
                physiocap_log( "=~= {2} {0} ne retrouve pas votre raster pour {1}".\
                    format( PHYSIOCAP_UNI, nom_court_raster, PHYSIOCAP_WARNING), TRACE_INTRA)
                raise physiocap_exception_raster_manquant( nom_court_raster)     
                
            
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
      
            if (( affiche_raster == "YES") and ( le_template_raster != None)):
                # Pour transparence dans le template valeur -99999
                intra_raster.loadNamedStyle( le_template_raster)
                #physiocap_log ( "= pendant LOAD STYLE {0} RASTER".format( le_template_raster), TRACE_INTRA)
            if (( affiche_iso == "YES") and ( nom_iso_final != "") and 
                ( le_template_isolignes != None)):
                intra_isoligne.loadNamedStyle( le_template_isolignes)

    def creer_raster_iso( self, dialogue, choix_interpolation, choix_force_interpolation, 
                nom_noeud_arbre, chemin_raster, chemin_iso,
                nom_court_vignette, nom_vignette, nom_court_point, nom_point,
                le_champ_choisi, le_choix_INTRA_continue, le_nom_entite_libere):
        """ Creation du raster et Iso
        Cas Saga ou Gdal : appel des Processing (Traitement) correspondants
            choix_interpolation est la librairie choisie et 
            choix_force_interpolation est une librairie qui a été forcé
        """
        leModeDeTrace = dialogue.fieldComboModeTrace.currentText() 
     
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
        distancearea, quel_vecteur_demande, EXTENSION_CRS_VECTEUR, DRIVER_VECTEUR, EXTENSION_RASTER_COMPLET, \
            transform_context, laProjectionCRS, laProjectionTXT, EPSG_NUMBER = quelle_projection_et_format_vecteur( dialogue)
            
        # Récupération des deux parametres d'Intra pour GDAL demandé et non forcé
        rayonDoubleIntra = float ( dialogue.spinBoxDoubleRayon.value())
        if choix_interpolation == "GDAL":
            rayonMultiplieIntra = float ( dialogue.spinBoxMultiplieRayon.value())
            if rayonMultiplieIntra > 0:
                deuxieme_rayon = rayonDoubleIntra * rayonMultiplieIntra
            else:
                deuxieme_rayon = rayonDoubleIntra
            physiocap_log( self.tr( "=~= Rayon saisi = {0} et rayon ellipse {1} ").\
                format(  rayonDoubleIntra,  deuxieme_rayon), TRACE_INTRA)
        else:
            deuxieme_rayon = rayonDoubleIntra
            
        pixelIntra = float ( dialogue.spinBoxPixel.value())

         # Pour isolignes
        isoMin = float ( dialogue.spinBoxIsoMin.value())
        isoMax = float ( dialogue.spinBoxIsoMax.value())
        #isoNombreIso = float ( dialogue.spinBoxNombreIso.value())
        isoInterlignes = float ( dialogue.spinBoxDistanceIso.value())
     
#        # Parametres fixes
#        val_nulle = 0 # Valeur nulle reste nulle
#        float_32 = 5
#        float_64 = 6
            
        # ###################
        # CRÉATION raster cible et temporaire
        # ###################
        
        # Nom du raster cible avec le_champ_choisi
        nom_court_raster = nom_noeud_arbre + NOM_INTRA + SEPARATEUR_ + le_champ_choisi +  \
            SEPARATEUR_ + le_nom_entite_libere + EXTENSION_RASTER_COMPLET
        nom_court_isoligne = nom_noeud_arbre + NOM_INTRA  + SEPARATEUR_  + le_champ_choisi  + \
            SEPARATEUR_ + "ISOLIGNE_" + le_nom_entite_libere + EXTENSION_CRS_VECTEUR
        le_raster_possible = os.path.join( chemin_raster, nom_court_raster) 
        l_iso_possible = os.path.join( chemin_iso, nom_court_isoligne)
        # 3.28.11 SAGA7 
        nom_contour = os.path.join( chemin_iso,  nom_noeud_arbre + NOM_INTRA  + SEPARATEUR_  + le_champ_choisi  + \
            SEPARATEUR_ + "LIGNE_CONTOUR_" + le_nom_entite_libere + EXTENSION_CRS_VECTEUR)
        if le_choix_INTRA_continue == 0:
            # CAS 0 : Arrêt si une interpolation existe
            if os.path.exists( le_raster_possible) or os.path.exists( l_iso_possible):
                raise physiocap_exception_raster_ou_iso_existe_deja( le_champ_choisi + ' pour ' +  le_nom_entite_libere)  
            else:
                # il faut creer les deux
                nom_raster =  physiocap_rename_existing_file( le_raster_possible)
                nom_isoligne =  l_iso_possible # ? utile physiocap_rename_existing_file()
        
        elif le_choix_INTRA_continue == 1:
            # CAS 1 : Ne pas re-créer 
            # on vérifie si le raster existe déjà
            if os.path.exists( le_raster_possible) and os.path.exists( l_iso_possible):
                physiocap_log( self.tr( "=~= Interpolation pour {0} existe déjà. Pas de nouveau calcul").\
                    format(  le_nom_entite_libere), leModeDeTrace)
                return "PAS NOUVEAU", le_raster_possible, nom_court_raster, l_iso_possible, nom_court_isoligne
            elif os.path.exists( le_raster_possible) or os.path.exists( l_iso_possible):
                # Il existe un seul des deux fichiers
                physiocap_log( self.tr( "=~= Une partie de l'interpolation pour {0} existe déjà : nouveau calcul").\
                    format(  le_nom_entite_libere), leModeDeTrace)
                if os.path.exists( le_raster_possible):
                    nom_raster = physiocap_rename_existing_file( le_raster_possible)
                    nom_isoligne =  l_iso_possible
                elif os.path.exists( l_iso_possible):
                    nom_raster = le_raster_possible
                    nom_isoligne =  physiocap_rename_existing_file( l_iso_possible)
                else:
                    # Cas impossible ?
                    raise physiocap_exception_raster_sans_iso( le_champ_choisi  + ' pour ' +  le_nom_entite_libere)
            else:
                # il faut creer les deux
                nom_raster = le_raster_possible
                nom_isoligne =  l_iso_possible       
        else:
            raise physiocap_exception_no_choix_raster_iso( le_nom_entite_libere)
            
        # Création d'un raster temporaire
        try:
            from processing.tools.system import ( getTempFilename)
            if choix_force_interpolation in [ "SAGA", "SAGA7"]:
                # on crée un repertoire temporaire 
                nom_dir_temp = QgsProcessingUtils.tempFolder()
                # OLD nom_dir_temp = getTempDirInTempFolder()
                nom_raster_temp = os.path.join( nom_dir_temp, "TMP_RASTER_SAGA" + EXTENSION_RASTER_SAGA)
                nom_raster_temp_clip = os.path.join( nom_dir_temp, "TMP_RASTER_SAGA_CLIP" + EXTENSION_RASTER_SAGA)
            else:
                # cas GDAL (ou QGIS) : tiff
                # parametre insuffisant nom_raster_temp = QgsProcessingUtils.generateTempFilename("xx", EXTENSION_RASTER_SANS_POINT)
                nom_raster_temp = getTempFilename( EXTENSION_RASTER_SANS_POINT)                
        except:
            physiocap_log( self.tr( "Exception durant nommage temporaire {0} et chemin \n{1}").\
            format( "TMP_RASTER", nom_raster_temp), TRACE_INTRA)
            raise
      
        # Récuperer pour GDAL orientation et Passage
        orientation = 0
        ellipse_orientee = 0
        if choix_interpolation == "GDAL" and dialogue.checkBoxV3.isChecked():

            mon_expression = "\"{0}\" = '{1}'".format( CHAMP_NOM_ID, le_nom_entite_libere)                
            try:
                physiocap_log( self.tr( "avant Expression ==>{0}<===").\
                    format( mon_expression), TRACE_INTRA)
                for ma_moyenne in vignette_vector.getFeatures( QgsFeatureRequest( \
                    QgsExpression( mon_expression))):
                    # en D° horaire par rapport au N
                    orientation = ma_moyenne[ "ORIENT_A"]
                    # en d° antihoraire et perpenpendiculaire
                    ellipse_orientee = 90 + (180 - orientation)
                    # on suppose un seul retour
                    break
            except:
                physiocap_log( self.tr( "Exception durant recherche orientation & passage pour {0}").\
                format( le_nom_entite_libere), TRACE_INTRA)
                raise                

            # Cas sans orientation retrouvé
            if  ellipse_orientee == 0:
                deuxieme_rayon = rayonDoubleIntra            
            physiocap_log( self.tr( "=~= Orientation du rang soit ellipse == {0} soit= {1} == {2}*{3} == ").\
                format(  orientation, ellipse_orientee,  rayonDoubleIntra,  deuxieme_rayon), leModeDeTrace)     

        else: # cas GDAL forcé, on utilise pas l'ellipse
            deuxieme_rayon = rayonDoubleIntra
     
        # Initialisation avant Interpolation
        nom_raster_produit = ""
        nom_raster_clippe = ""
        nom_raster_final = ""
        nom_iso_final = ""        
        # Récuperer Extent du polygone en cours
        ex = vignette_vector.extent()
        xmin, xmax, ymin, ymax = ex.xMinimum(),ex.xMaximum(), ex.yMinimum(), ex.yMaximum()
        if choix_force_interpolation == "GDAL":
            info_extent = str(xmin) + "," + str(ymin) + "," + str(xmax) + "," + str(ymax)
        else: # SAGA !
            info_extent = str(xmin) + "," + str(xmax) + "," + str(ymin) + "," + str(ymax)
        info_extent_epsg = info_extent + " [EPSG:" + str( EPSG_NUMBER) + "]"
        
        if choix_force_interpolation in [ "SAGA", "SAGA7"]:
            # Appel SAGA : power à 2 fixe
            physiocap_log( self.tr( "=~= Interpolation SAGA dans {0}").\
                format(  nom_court_raster), leModeDeTrace)
            if choix_force_interpolation == "SAGA":
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
                    ### 'DW_BANDWIDTH' : 0, 
                    ### 'SEARCH_POINTS_MAX' : 20, 
                    # ????  ### 'TARGET_USER_SIZE' : 1.8, 
                IDW_SAGA = { 'SHAPES' : nom_point, 
                    'FIELD' : le_champ_choisi, 
                    'OUTPUT_EXTENT' : info_extent_epsg,
                    'DW_WEIGHTING' : 1,
                    'DW_IDW_POWER' : 2, 
                    'DW_IDW_OFFSET' : False, 
                    'DW_BANDWIDTH' : 1, 
                    'SEARCH_RANGE' : 0, 
                    'SEARCH_RADIUS' : rayonDoubleIntra, 
                    'SEARCH_POINTS_ALL' : 0, 
                    'SEARCH_POINTS_MIN' : 1, 
                    'SEARCH_POINTS_MAX' : 20, 
                    'SEARCH_DIRECTION' : 0, 
                    'TARGET_USER_SIZE' : pixelIntra, 
                    'TARGET_DEFINITION' : 0, 
                    'TARGET_USER_FITS' : 0,
                    'TARGET_TEMPLATE' : None,
                    'TARGET_OUT_GRID' : nom_raster_temp
                    }
                nom_raster_produit = self.appel_processing( nom_point, \
                    "IDW_SAGA", "saga:inversedistanceweightedinterpolation", \
                    IDW_SAGA, "TARGET_OUT_GRID")     
            elif choix_force_interpolation == "SAGA7":
                IDW_SAGA_7 = { 'POINTS' : nom_point, 
                    'FIELD' : le_champ_choisi, 
                    'CV_METHOD':0,'CV_SUMMARY':'TEMPORARY_OUTPUT',
                    'CV_RESIDUALS':'TEMPORARY_OUTPUT', 'CV_SAMPLES':10,
                    'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX' : info_extent_epsg, 
                    'TARGET_USER_SIZE' : pixelIntra, 
                    'TARGET_OUT_GRID' : nom_raster_temp, 
                    'SEARCH_RANGE' : 0, 
                    'SEARCH_RADIUS' : rayonDoubleIntra,
                    'SEARCH_POINTS_ALL' : 0, 'SEARCH_POINTS_MIN' : 1, 'SEARCH_POINTS_MAX' : 10, 
                    'DW_WEIGHTING' : 1, 'DW_IDW_POWER' : 2, 'DW_BANDWIDTH' : 1
                    }
                nom_raster_produit = self.appel_processing( nom_point, \
                    "IDW_SAGA7", "saga:inversedistanceweighted", \
                    IDW_SAGA_7, "TARGET_OUT_GRID")      
            #QgsMessageLog.logMessage( "PHYSIOCAP : Avant clip SAGA", "Processing", Qgis.Info)

            # Cas TIFF on garde le nom final du tiff pour le step suivant
            if dialogue.checkBoxSagaTIFF.isChecked():
                nom_clippe = nom_raster_temp_clip    
            else:
                nom_clippe = nom_raster
            # On passe ETAPE CLIP si nom_raster_produit existe
            if ( nom_raster_produit != ""):
                # KO 0 : nom_raster_produit
                # KO 1 : nom_raster_sgrd = nom_raster_produit[:-4] + "sgrd"
                # Passage du QgsRasterLayer
                le_raster_temp = QgsRasterLayer( nom_raster_produit, "Raster_SAGA_temporaire")                
                CLIP_SAGA = { 'INPUT' : le_raster_temp,
                    'POLYGONS' : nom_vignette,
                    'OUTPUT' : nom_clippe }
                
                nom_raster_clippe = self.appel_processing( nom_point, \
                "CLIP_SAGA", "saga:cliprasterwithpolygon", \
                CLIP_SAGA, "OUTPUT")                    
#####                raster_dans_poly = processing.runalg("saga:clipgridwithpolygon",
#####                nom_raster_produit,
#####                nom_vignette,
#####                nom_raster)

                le_raster_temp = None

            if ( nom_raster_clippe != ""):
                if dialogue.checkBoxSagaTIFF.isChecked():
                    # GDAL translate pour créer le TIFF
                    le_raster_translate = QgsRasterLayer( nom_raster_clippe, "Raster_Translate_temporaire")                
                    QgsMessageLog.logMessage( "PHYSIOCAP : Avant GDAL translate pour le TIFF", "Processing", Qgis.Warning)
                    #   'NODATA':0,
                    TRANSLATE_TIFF = { 'INPUT' : le_raster_translate,
                        'NODATA':-99999,
                        'COPY_SUBDATASETS':False,
                        'OPTIONS':'',
                        'DATA_TYPE':6,
                        'OUTPUT' : nom_raster}
                    nom_raster_final = self.appel_processing( nom_point, \
                        "TRANSLATE_TIFF", "gdal:translate", \
                        TRANSLATE_TIFF, "OUTPUT")
                    le_raster_translate = None
                else:
                    # Cas non tiff
                    nom_raster_final = nom_raster_clippe
            
            if dialogue.groupBoxIsolignes.isChecked():
                QgsMessageLog.logMessage( "PHYSIOCAP : Avant isolignes SAGA {0}".\
                    format( nom_raster_final), "Processing", Qgis.Warning)
                                                
                # On passe ISO si nom_raster_final existe
                if ( nom_raster_final != ""):
                    le_raster_final = QgsRasterLayer( nom_raster_final, nom_court_raster)                
                    if choix_force_interpolation == "SAGA":
                        ISO_SAGA = { 'GRID' : le_raster_final,
                            'VERTEX' : 1,
                            'ZMIN' : isoMin, 'ZMAX' : isoMax, 
                            'ZSTEP' : isoInterlignes, 
                            'CONTOUR' : nom_isoligne }
                            
                        nom_iso_final = self.appel_processing( nom_point, \
                            "ISO_SAGA", "saga:contourlines", \
                            ISO_SAGA, "CONTOUR")
                    elif choix_force_interpolation == "SAGA7":
                            #pour 2.18
# ("saga:contourlinesfromraster", {'GRID':'L93.tiff','CONTOUR':'TEMPORARY_OUTPUT',
#'POLYGONS':'TEMPORARY_OUTPUT',
#'VERTEX':0,'SCALE':1,'LINE_PARTS':True,
#'POLY_PARTS':False,'ZMIN':0,'ZMAX':10000,'ZSTEP':10})
                        ISO_SAGA7 = { 'GRID' : le_raster_final, 
                            'CONTOUR' : nom_isoligne, 'POLYGONS': nom_contour, 
                            'VERTEX' : 1, 'SCALE':1, 'LINE_PARTS':True, 'POLY_PARTS':False,
                            'ZMIN' : isoMin, 'ZMAX' : isoMax, 
                            'ZSTEP' : isoInterlignes}
                            
                        nom_iso_final = self.appel_processing( nom_point, \
                            "ISO_SAGA7", "saga:contourlinesfromraster", \
                            ISO_SAGA7, "CONTOUR")                        
                    
                    le_raster_final = None

                    physiocap_log( self.tr( "=~= Interpolation SAGA - Fin iso - {0}").\
                        format( nom_iso_final), TRACE_INTRA)   
            else:
                physiocap_log( self.tr( "=~= Interpolation SAGA - Fin raster sans iso - {0}").\
                    format( nom_raster_final), TRACE_INTRA)   
                
        elif choix_force_interpolation == "GDAL":
##            # Appel GDAL
##            # Paramètres apres le champ
##            # Power vaut 2 
##            # Lissage à 0 car ce lissage peut se faire dans les propriétés du raster
##            # Rayon identique 
##            # Max points à 20 (si non atteint, forcage à valeur 0    
##            # Min à 5 
##            # Angle à 0 (c'est l'angle de l'ellipse)
##            # KO dans IDW option_outsize = "-outsize {0} {0}".format( pixelIntra)
##            # KO pour idw et clip VOIR Avec \" ou ' et "
##            # KO pour idw et clip
##            # option_resolution = "-tr \"{0} {0}\"".format( pixelIntra)

            # IDW GDAL
            IDW_GDAL = {'INPUT':nom_point,  'Z_FIELD' : le_champ_choisi, 
                'POWER':2,'SMOOTHING':0,
                'RADIUS_1':rayonDoubleIntra,'RADIUS_2':deuxieme_rayon,
                'ANGLE':ellipse_orientee,
                'MAX_POINTS':20,'MIN_POINTS':1,'NODATA':0,
                'OPTIONS':'','DATA_TYPE':6, 'OUTPUT': nom_raster_temp}

            nom_raster_produit = self.appel_processing( nom_point, \
                "IDW_GDAL", "gdal:gridinversedistance", \
                IDW_GDAL, "OUTPUT")  
          
            QgsMessageLog.logMessage( "PHYSIOCAP : Avant clip GDAL", "Processing", Qgis.Warning)

            # On passe ETAPE CLIP si nom_raster_produit existe
            if ( nom_raster_produit != ""):
                CLIP_GDAL = {'INPUT':nom_raster_produit,
                    'MASK':nom_vignette,
                    'NODATA':-99999,
                    'ALPHA_BAND':False,
                    'CROP_TO_CUTLINE':True,
                    'KEEP_RESOLUTION':True,
                    'OPTIONS':'',
                    'DATA_TYPE':6,
                    'OUTPUT':nom_raster}
                    
                nom_raster_final = self.appel_processing( nom_point, \
                "CLIP_GDAL", "gdal:cliprasterbymasklayer", \
                CLIP_GDAL, "OUTPUT")
                         
            if dialogue.groupBoxIsolignes.isChecked():
                # On passe ETAPE ISO si nom_raster_final existe
                if ( nom_raster_final != ""):
                    # Isolignes
                    ISO_GDAL = {'INPUT':nom_raster,
                        'BAND' : 1,
                        'INTERVAL' : isoInterlignes,
                        'FIELD_NAME' : 'Z',
                        'CREATE_3D' : True, 'IGNORE_NODATA' : False, 'NODATA' : None, 'OFFSET' : 0,
                        'OUTPUT' : nom_isoligne }
                    # Bug iso gdal si NODATA=0

                    nom_iso_final = self.appel_processing( nom_point, \
                    "ISO_GDAL", "gdal:contour", \
                    ISO_GDAL, "OUTPUT")
                
        else:
            # Autres choix
            physiocap_error( self, self.tr( "=~= Pas d'autre méthode d'interpolation que GDAL et SAGA"))
           
        return "NOUVEAUX", nom_raster_final, nom_court_raster, nom_iso_final, nom_court_isoligne            

    def assert_processing( self):
        # Vérifier disponibilité de processing (on attend d'etre dans Intra)
        versionSAGA = None
        try :
            import processing
            try:
                from processing.core.Processing import Processing
                Processing.initialize()
            except:
                physiocap_log( self.tr( "{0} nécessite l'extension {1}").\
                    format( PHYSIOCAP_UNI, self.tr("Traitement")), TRACE_INTRA)
                raise physiocap_exception_no_processing( "Pas d'extension Traitement - initialize")               
            versionGDAL = processing.tools.raster.gdal.__version__
            try:
                import sagaprovider
                versionSAGA = sagaprovider.SagaUtils.getInstalledVersion() # version > 3.22
                physiocap_log( "OK sagaProvider {0}".format( versionSAGA), TRACE_JH)
            except ImportError:
                physiocap_log( "KO import sagaProvider", TRACE_JH)
                pass
            except AttributeError:
                physiocap_log( "KO version SAGA by sagaProvider", TRACE_JH)
                pass
            if versionSAGA == None:
                versionSAGA = processing.algs.saga.SagaUtils.getInstalledVersion() # version <= 3.16.15
                physiocap_log( "OK saga avant 3.22 {0}".format( versionSAGA), TRACE_JH)

        except ImportError:
            physiocap_log( self.tr( "{0} nécessite l'extension {1}").\
                format( PHYSIOCAP_UNI, self.tr("Traitement (Processing)")), TRACE_INTRA)
            raise physiocap_exception_no_processing( "Pas d'extension Traitement")
        except AttributeError:
            pass
                
#        if versionSAGA == None:
#            physiocap_log( self.tr( "{0} nécessite SAGA (attribute error)").\
#                format( PHYSIOCAP_UNI), self.tr("Traitement (Processing)"))
#            raise physiocap_exception_no_saga( "Pas de version SAGA")

        physiocap_log ( "= Version GDAL = {0}".format( versionGDAL), TRACE_INTRA)
        physiocap_log ( "= Version SAGA = {0}".format( versionSAGA), TRACE_INTRA)
        return versionGDAL, versionSAGA

    def quelle_librairie_interpolation( self, dialogue, versionSAGA):
        """
        Traite le choix et la version SAGA QGIS ou GDAL avant appel des Processing (Traitement) correspondants
        Attention ce choix peut être revu pour certains cas (SAGA n'accepte pas les caractere non ascii
        """        
        # Test version de SAGA, sinon annonce de l'utilisation de GDAL
        PROCESSING_INTERPOLATION = "INCONNU"
        if dialogue.radioButtonSAGA.isChecked():
            if versionSAGA == None:
                versionNum = -1
            else:
                unite, dixieme, centieme = versionSAGA.split( ".")
                versionNum = round( (float(unite) + float(dixieme)/10 + float(centieme)/100 ), 2)
                physiocap_log ( self.tr( "= Version SAGA = {0}".format( versionNum)), TRACE_INTRA)

            # ouverture SAGA Windows 7.82
            if ((( versionNum >= 2.31) and ( versionNum <= 2.32)) or versionNum == 7.82):
                physiocap_log ( self.tr( "= Version SAGA OK : {0}".format( versionSAGA)), TRACE_INTRA)
                if (( versionNum >= 2.31) and ( versionNum <= 2.32)):
                    PROCESSING_INTERPOLATION = "SAGA"
                elif versionNum == 7.82:
                    PROCESSING_INTERPOLATION = "SAGA7"
            else:
                physiocap_log ( self.tr( "= Version SAGA %s n'est pas parmi 2.3.1 ou 2.3.2 ou 7.8.2 " % ( str( versionSAGA))), \
                    TRACE_INTRA)
                physiocap_log ( self.tr( "= On force l'utilisation de Gdal : "), TRACE_INTRA)
                PROCESSING_INTERPOLATION = "GDAL"
                dialogue.radioButtonSAGA.setEnabled( False)
                dialogue.radioButtonGDAL.setChecked(  Qt.Checked)
                dialogue.radioButtonSAGA.setChecked(  Qt.Unchecked)
                dialogue.spinBoxPower.setEnabled( False)
                physiocap_message_box(dialogue,  self.tr( "= Saga a une version incompatible : on force l'utilisation de Gdal" ),
                    "information")
        
        else: # cas GDAL
            PROCESSING_INTERPOLATION = "GDAL"
        
        return PROCESSING_INTERPOLATION

    def appel_processing( self, nom_point, algo_court, algo, params_algo,  
        nom_produit_algo,  deuxieme_nom = None):
        """
        Traite les appels à processing avec gestion du nom_produit_algo attendu
        Emet exception si pas de retour 
        """
        import processing
        mon_feedback = QgsProcessingFeedback()
        
        lettre_algo = algo[0]

        physiocap_log( self.tr( "={0}= Parametres pour algo {1} de nom long {2}\n{3}".\
                        format( lettre_algo, algo_court, algo , params_algo )), TRACE_INTRA)       
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
            physiocap_log( erreur_processing, TRACE_INTRA)
            raise physiocap_exception_interpolation( nom_point)

        physiocap_log( "={0}= Produit en sortie de {1}\n{2}".\
                        format( lettre_algo, algo_court, produit_algo), TRACE_INTRA)
        return produit_algo
    
    def physiocap_interpolation_IntraParcelles( self, dialogue):
        """Interpolation des données de points intra parcellaires"""
        derniere_session = dialogue.lineEditDerniereSession.text()
        leModeDeTrace = dialogue.fieldComboModeTrace.currentText()     
        DATA_VERSION_3 = "NO"
        if dialogue.checkBoxV3.isChecked():
            DATA_VERSION_3 = "YES"

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
            
        # Trouver deux vecteurs
        nom_noeud_arbre, vecteur_point, origine_poly, vecteur_poly, _ = quel_sont_vecteurs_choisis( dialogue, "Intra")

        # Cas des INFO AGRO vignoble par fichier 
        if dialogue.groupBoxDetailVignoble.isChecked() and dialogue.checkBoxInfoVignoble.isChecked() and \
           dialogue.radioButtonContour.isChecked():
            dialogue.progressBarIntra.setValue( 1)
            champsVignobleOrdonnes, champs_agro_fichier, _, _, champs_vignoble_requis, champs_vignoble_requis_fichier, \
                dictEnteteVignoble, champExistants, les_parcelles_agro, modele_agro_retenu  = \
                assert_champs_agro_obligatoires( dialogue, vecteur_poly, origine_poly)       

        # Pour attribut en cours d'interpolation
        le_champ_contour = dialogue.fieldComboContours.currentText()
        champ_pb_gdal = dialogue.fieldPbGdal.currentText()
            
        versionGDAL, versionSAGA = self.assert_processing()
        physiocap_log( self.tr( "=~= {0} début de l'interpolation des points de {1}").\
            format( PHYSIOCAP_UNI, nom_noeud_arbre), leModeDeTrace)

        # Progress BAR 2%
        dialogue.progressBarIntra.setValue( 2)
        
        # Appel une seule fois des vérification Processing dispo et choix de Librairie 
        choix_interpolation = self.quelle_librairie_interpolation( dialogue, versionSAGA)
        physiocap_log ( self.tr( "=~= Choix de la librairie d'interpolation : {0}".\
            format( choix_interpolation)), leModeDeTrace)

        # Vérification de l'arbre
        mon_projet = QgsProject.instance()
        root = mon_projet.layerTreeRoot()        
        un_groupe = root.findGroup( nom_noeud_arbre)
        if ( not isinstance( un_groupe, QgsLayerTreeGroup)):
            aText = self.tr( "La session {0} n'existe pas dans l'onglet des couches. ").\
                format(  nom_noeud_arbre)
            aText = aText + self.tr( "Créer une nouvelle session Physiocap - bouton Filtrer les données brutes puis Inter - ")
            aText = aText + self.tr( "avant de faire votre interpolation Intra Parcellaire")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( dialogue, aText, "information" )            
        
        # Vérification 
        if ( vecteur_point == None) or ( not vecteur_point.isValid()):
            aText = self.tr( "Le jeu de points choisi n'est pas valide. ")
            aText = aText + self.tr( "Créer une nouvelle session Physiocap - bouton Filtrer les données brutes puis Inter - ")
            aText = aText + self.tr( "avant de faire votre interpolation Intra Parcellaire")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( dialogue, aText, "information" )  

        if ( vecteur_poly == None) or ( not vecteur_poly.isValid()):
            aText = self.tr( "Le contour choisi n'est pas valide. ")
            aText = aText + self.tr( "Créer une nouvelle session Physiocap - bouton Filtrer les données brutes puis Inter - ")
            aText = aText + self.tr( "avant de faire votre interpolation Intra Parcellaire")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( dialogue, aText, "information" ) 
        nom_vecteur_contour = vecteur_poly.name()
                   
        # Recuperer le CRS choisi, les extensions et le calculateur de distance
        distancearea, quel_vecteur_demande, EXTENSION_CRS_VECTEUR, DRIVER_VECTEUR, EXTENSION_RASTER_COMPLET, \
            transform_context, laProjectionCRS, laProjectionTXT, EPSG_NUMBER = quelle_projection_et_format_vecteur( dialogue)

        nom_point_en_cours = vecteur_point.dataProvider().dataSourceUri()
        pos_fin_layer = nom_point_en_cours.rfind( "|layerid=")
        if ( pos_fin_layer != -1):
            nom_point_exact = nom_point_en_cours[:pos_fin_layer]
        else:
            nom_point_exact  = nom_point_en_cours

        # TODO: ?V3.x GEOPACKAGE et autre type de vecteur
        if quel_vecteur_demande == GEOPACKAGE_NOM  and DATA_VERSION_3 == "YES":
            chemin_session = os.path.dirname( nom_point_exact)
            # Version 3.4.0 pas de geopackage en intra
            return physiocap_message_box( dialogue, 
            self.tr( "== Le format Géopackage n'est pas disponible pour les traitements intra-parcellaires"), "information")
        
        elif quel_vecteur_demande in [ SHAPEFILE_NOM, GEOJSON_NOM]:
            # Assert repertoire shapefile 
            chemin_shapes = os.path.dirname( nom_point_exact ) 
            chemin_session = os.path.dirname( chemin_shapes)
            shape_point_extension = os.path.basename( nom_point_exact)
            pos_extension = shape_point_extension.rfind(".")
            shape_point_sans_extension = shape_point_extension[:pos_extension]
            if ( not os.path.exists( chemin_shapes)):
                raise physiocap_exception_rep( chemin_shapes)
        
        else: # Assert type vecteur supporté
                raise physiocap_exception_vecteur_type_inconnu( quel_vecteur_demande)

        if ( not os.path.exists( chemin_session)):
            raise physiocap_exception_rep( chemin_session)
 
        consolidation = "NO"
        if dialogue.checkBoxConsolidation.isChecked():
            consolidation = "YES"
            
        # Test selon Consolidation
        if (consolidation == "YES"):
            # Rajout pour consolidation du nom du shape
            chemin_vecteur_nom_point = os.path.join( chemin_shapes, shape_point_sans_extension)
            if not (os.path.exists( chemin_vecteur_nom_point)):
                os.mkdir( chemin_vecteur_nom_point)                    
            chemin_vignettes = os.path.join( chemin_vecteur_nom_point, VIGNETTES_INTER)
        else:            
            if DATA_VERSION_3 == "NO":                
                chemin_vignettes = os.path.join( chemin_shapes, VIGNETTES_INTER)
            else:
                chemin_vignettes = os.path.join( chemin_session , REPERTOIRE_INTER_V3)
        # Assert repertoire vignette inter 
        if not (os.path.exists( chemin_vignettes)):
            raise physiocap_exception_rep( VIGNETTES_INTER)

       # QT Confiance 
        les_champs_INTRA_choisis = dialogue.fieldComboIntra.currentText().split( SEPARATEUR_NOEUD)
        physiocap_log( self.tr( "=~= Les champs à traiter {0}". \
            format( les_champs_INTRA_choisis)), TRACE_INTRA)
        arret_groupe_intra = "NO"
        if dialogue.checkBoxArret.isChecked():
            arret_groupe_intra = "YES"
            le_choix_INTRA_continue = 0
        else:
            le_choix_INTRA_continue = dialogue.fieldComboIntraContinue.currentIndex()
            
        # Création du REP RASTER et ISOLIGNES
        # Test selon Consolidation
        if (consolidation == "YES"):
            chemin_raster = os.path.join( chemin_vecteur_nom_point, REPERTOIRE_RASTERS)
            chemin_iso = chemin_raster
        else:
            if DATA_VERSION_3 == "NO":                
                chemin_raster = os.path.join( chemin_shapes, REPERTOIRE_RASTERS)
                chemin_iso = chemin_raster
            else:
                chemin_intra =  os.path.join( chemin_session , REPERTOIRE_INTRA_V3)
                chemin_raster =  os.path.join( chemin_intra, REPERTOIRE_RASTER_V3)
                chemin_iso =  os.path.join( chemin_intra, REPERTOIRE_ISO_V3)

        if DATA_VERSION_3 == "YES" and consolidation != "YES":
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
        nombre_calcul_max = i_forme_min * len( les_champs_INTRA_choisis) 
        id_bar = 0
        barre = 1
        if nombre_calcul_max > (85-20):
            progress_step = int( nombre_calcul_max / (85-20))
        else:
            progress_step = 0
        progress_bar = 20
        dialogue.progressBarIntra.setValue( 5)
        for idx, le_champ_choisi in enumerate( les_champs_INTRA_choisis):
            # Pour chaque attribut à interpoler
            physiocap_log( self.tr( "=~= {0} Champ choisi == {1} est le {2} parmi {3} ==").\
                format( PHYSIOCAP_UNI, le_champ_choisi, idx+1, len( les_champs_INTRA_choisis)), leModeDeTrace)
            # Copier la liste des parcelle agro
            if dialogue.groupBoxDetailVignoble.isChecked() and dialogue.checkBoxInfoVignoble.isChecked() and \
               dialogue.radioButtonContour.isChecked():
                les_parcelles_agro_suivi = les_parcelles_agro.copy()
            # Si plusieurs champs choisis : récupérer le parametres fixe présent Affichage
            if ((len( les_champs_INTRA_choisis) > 1) and ( dialogue.checkBoxIntraIsos.isChecked())):
                # Forcer pour éviter le calcul d'aide
                dialogue.fieldComboAideIso.setCurrentIndex( 2) 
                if idx == 0:
                    # récuperer les saisies nommées DIAM
                    # ASSERT : 
                    leChoixEncours = dialogue.fieldComboIntraDIAM.currentText()
                    if le_champ_choisi != leChoixEncours:
                        raise physiocap_exception_attribut_multiple_incoherent( leChoixEncours)
#                    physiocap_log( self.tr( "=~= {0} Synchro iso == {1} ==").\
#                        format( PHYSIOCAP_UNI, leChoixEncours), leModeDeTrace)                    
                    dialogue.spinBoxIsoMax.setValue( int( dialogue.spinBoxIsoMax_Fixe_DIAM.value()))
                    dialogue.spinBoxIsoMin.setValue( int( dialogue.spinBoxIsoMin_Fixe_DIAM.value()))
                    dialogue.spinBoxDistanceIso.setValue( int( dialogue.spinBoxIsoDistance_Fixe_DIAM.value()))                    
                elif idx == 1:
                    # récuperer les saisies nommées SARM
                    # ASSERT : 
                    leChoixEncours = dialogue.fieldComboIntraSARM.currentText()
                    if le_champ_choisi != leChoixEncours:
                        raise physiocap_exception_attribut_multiple_incoherent( leChoixEncours)
#                    physiocap_log( self.tr( "=~= {0} Synchro iso == {1} ==").\
#                        format( PHYSIOCAP_UNI, leChoixEncours), leModeDeTrace)                    
                    dialogue.spinBoxIsoMax.setValue( int( dialogue.spinBoxIsoMax_Fixe_SARM.value()))
                    dialogue.spinBoxIsoMin.setValue( int( dialogue.spinBoxIsoMin_Fixe_SARM.value()))
                    dialogue.spinBoxDistanceIso.setValue( int( dialogue.spinBoxIsoDistance_Fixe_SARM.value()))
                elif idx == 2:
                    # récuperer les saisies nommées BIOM
                    # ASSERT : 
                    leChoixEncours = dialogue.fieldComboIntraBIOM.currentText()
                    if le_champ_choisi != leChoixEncours:
                        raise physiocap_exception_attribut_multiple_incoherent( leChoixEncours)
#                    physiocap_log( self.tr( "=~= {0} Synchro iso == {1} ==").\
#                        format( PHYSIOCAP_UNI, leChoixEncours), leModeDeTrace)                    
                    dialogue.spinBoxIsoMax.setValue( int( dialogue.spinBoxIsoMax_Fixe_BIOM.value()))
                    dialogue.spinBoxIsoMin.setValue( int( dialogue.spinBoxIsoMin_Fixe_BIOM.value()))
                    dialogue.spinBoxDistanceIso.setValue( int( dialogue.spinBoxIsoDistance_Fixe_BIOM.value()))
                else:
                    raise physiocap_exception_attribut_multiple_incoherent( "Autre choix")

            # Récupérer des styles pour chaque shape
            # Pour les templates
            repertoire_template,  repertoire_secours = quel_chemin_templates( dialogue)
            le_template_raster = quel_qml_existe( \
                dialogue.lineEditThematiqueIntraImage.text().strip('"') + le_champ_choisi + EXTENSION_QML,  \
                repertoire_template,  repertoire_secours)    
            le_template_isolignes = quel_qml_existe( \
                dialogue.lineEditThematiqueIntraIso.text().strip('"') + le_champ_choisi + EXTENSION_QML,  \
                repertoire_template,  repertoire_secours)    
#            physiocap_log( self.tr( "=~= {0} Template raster == {1} ==").\
#                format( PHYSIOCAP_UNI, le_template_raster), leModeDeTrace)      
                
            # On passe sur le contour général
            contour_avec_point = 0
            contours_possibles = 0
           
            # #####################
            # Cas d'une image seule
            # #####################
            # Nom du Shape moyenne de toutes les vignettes
            nom_court_du_contour = os.path.basename( nom_vecteur_contour)
            pos_projection_layer = nom_court_du_contour.rfind( SEPARATEUR_ + laProjectionTXT)
            if pos_projection_layer > 0:
                nom_court_du_contour = nom_court_du_contour[:pos_projection_layer]
            nom_court_vignette_toutes = nom_noeud_arbre + NOM_MOYENNE + nom_court_du_contour + EXTENSION_CRS_VECTEUR
            nom_vignette_toutes = os.path.join( chemin_vignettes, nom_court_vignette_toutes)        
            vignette_toutes_vecteur = None
            if (os.path.exists( nom_vignette_toutes)):
                vignette_toutes_vecteur = QgsVectorLayer( nom_vignette_toutes, nom_court_vignette_toutes, 'ogr')
            else:
                physiocap_log( "=~=  Pas de vignette tout vecteur : {0}".format(nom_vignette_toutes),  TRACE_JH)
                
            # A_TESTER: Selon la taille, éviter ce calcul Intra et remplacer par un merge des tif et isolignes
            if ( dialogue.checkBoxIntraUnSeul.isChecked() and 
                choix_interpolation != "GDAL") :
                contours_possibles = contours_possibles + 1
                                                       
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
                    nom_court_point = derniere_session + NOM_POINTS + EXTENSION_SANS_ZERO + EXTENSION_CRS_VECTEUR   
                nom_point = os.path.join( chemin_shapes, nom_court_point)                    

                # Vérifier si le point et la vignette existent
                if not (os.path.exists( nom_vignette_toutes)):
                    physiocap_log( self.tr( "=~=  Pas d'interpolation, Vignette absente : {0}").\
                        format( nom_vignette_toutes), TRACE_INTRA)
                if not (os.path.exists( nom_point)):
                    physiocap_log( self.tr( "=~=  Pas d'interpolation, Points absents : {0}").\
                        format( nom_point), TRACE_INTRA)
                if (os.path.exists( nom_vignette_toutes)) and (os.path.exists( nom_point)):
                    dialogue.progressBarIntra.setValue( 20)
                    try:
                        # ###############
                        # Calcul raster et iso
                        # ###############
                        physiocap_log( self.tr( "=~=  Le contour : {0}").\
                            format( nom_vecteur_contour), TRACE_INTRA)
                        if ( champ_pb_gdal == "NO"):
                            le_nom_entite_libere = nom_vecteur_contour[:-4]
                        else:
                            # Prepare un nom sans cote (requete dans gdal et nommage dans gdal)
                            le_nom_entite_libere = physiocap_nom_entite_sans_pb_caractere( nom_vecteur_contour[:-4])
                        
                        nouveau = "NON"
                        nouveau, nom_raster_final, nom_court_raster, nom_iso_final, nom_court_isoligne = \
                            self.creer_raster_iso( dialogue, choix_interpolation, choix_interpolation, 
                            nom_noeud_arbre, chemin_raster, chemin_iso,  
                            nom_court_vignette_toutes, nom_vignette_toutes, nom_court_point, nom_point,
                            le_champ_choisi, le_choix_INTRA_continue, le_nom_entite_libere) 
                        contour_avec_point = contour_avec_point + 1
                    except physiocap_exception_windows_value_ascii as e:
                        aText = self.tr( "La valeur {0} a ").format( e)
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
                        if arret_groupe_intra == "YES":
                            # Si vignette preexiste, on ne recommence pas
                            raise physiocap_exception_vignette_exists( vignette_projet) 

                if ( contour_avec_point >  0 ):                                            
                    # Affichage dans panneau QGIS                           
                    if ( dialogue.checkBoxIntraUnSeul.isChecked()):
                        if nouveau == "NOUVEAUX":
                            self.afficher_raster_iso( dialogue, \
                                nom_raster_final, nom_court_raster, le_template_raster, "YES",
                                nom_iso_final, nom_court_isoligne, le_template_isolignes, "YES",
                                vignette_group_intra, mon_projet)

            # Eviter de tourner en Intra sur chaque parcelle
            if (( dialogue.checkBoxIntraIsos.isChecked()) or 
                        ( dialogue.checkBoxIntraImages.isChecked())):        
                # PAR CONTOUR : ne tourner que sur les contours qui ont été crée par Inter
                id_contour = 0
                for un_contour in vecteur_poly.getFeatures(): 
                    id_bar = id_bar + 1
                    # Progress BAR de 20 à 85 %
                    if nombre_calcul_max > (85-20) and ( id_bar > barre * progress_step):
                        progress_bar = progress_bar + 1
                        barre = barre + 1
                    else:
                        progress_bar = progress_bar + int( (85-20) / nombre_calcul_max) 
                        
                    if progress_bar % 5 == 0 or nombre_calcul_max < 10:
                        dialogue.progressBarIntra.setValue( progress_bar)  

                    id_contour = id_contour + 1
                    contours_possibles = contours_possibles + 1
                    
                    # LIMITATION AUX SEULES PARCELLE AGRO 
                    if dialogue.groupBoxDetailVignoble.isChecked() and dialogue.checkBoxInfoVignoble.isChecked() and \
                       dialogue.radioButtonContour.isChecked():
                        indice_dict_Entete = assert_quel_format_entete( self, origine_poly)
                        parcelle_attendue = assert_parcelle_attendue(self, un_contour, les_parcelles_agro, modele_agro_retenu, \
                            indice_dict_Entete, dictEnteteVignoble, champsVignobleOrdonnes)
                        if parcelle_attendue == None:
                            physiocap_log( "=== PARCELLE {} non attendue dans agro".format( un_contour), TRACE_JH)
                            continue
                        
                        # Attention seulement si le contour est agro 
                        # Eventuellement à la parcelle choisie    
                        if not dialogue.checkBoxToutes.isChecked():
                            physiocap_log( "=== CAS UNE PARCELLE {}".format( parcelle_attendue), TRACE_JH)
                            if parcelle_attendue != dialogue.fieldComboParcelleIntra.currentText():
                                physiocap_log( "Par d'Interpolation pour la parcelle {} - non demandée".format( parcelle_attendue), TRACE_JH)
                                continue
                            physiocap_log( "=== CAS la parcelle choisie {}".format( parcelle_attendue), TRACE_JH)

                        if parcelle_attendue in les_parcelles_agro_suivi:
                            les_parcelles_agro_suivi.remove( parcelle_attendue)
                        else:
                            physiocap_log( "Parcelle {} n'est pas attendue comme une parcelle AGRO".format( parcelle_attendue), "Attention")
                            
                        un_nom = parcelle_attendue
                    else:
                        try:
                            un_nom = un_contour[ le_champ_contour] 
                        except:
                            un_nom = NOM_CHAMP_ID + SEPARATEUR_ + str(id_contour)
                            pass

                    # Limitation si densité de points est inférieure au seuil
                    if vignette_toutes_vecteur != None:
                        le_seuil = dialogue.spinBoxDensiteMinimale.value()
                        une_densite = 0
                        for une_moyenne in vignette_toutes_vecteur.getFeatures():
                            if une_moyenne[ CHAMP_NOM_PHY] != un_nom:
                                continue
                            une_densite = une_moyenne[ "MESURE_HA"]
                            break
                        if une_densite < le_seuil:
                            physiocap_log( "On ignore parcelle {} : densité de points {} est inférieure au seuil {}".\
                                format( un_nom, une_densite, le_seuil), "Attention")
                            continue

                    # ###################
                    # Contournement du bug SAGA et caractères spéciaux ==> Interpolation GDAL
                    # ###################                    
                    # Ne tester que si SAGA
                    if choix_interpolation[0:4] == "SAGA" and not physiocap_is_only_ascii( un_nom):
                        aText =  self.tr("=~= {0} {1} ne peut pas dialoguer avec SAGA et des caractères non ascii.\n").\
                                format( PHYSIOCAP_WARNING, PHYSIOCAP_UNI)
                        aText = aText + self.tr( "L'interpolation de {0} doit être réalisée par GDAL").format( un_nom)
                        physiocap_log( aText, leModeDeTrace)
                        choix_definitif_interpolation = "GDAL" 
                    elif choix_interpolation[0:4] == "SAGA" and EXTENSION_CRS_VECTEUR.find( EXTENSION_GEOJSON) > 0:
                        aText =  self.tr("=~= {0} {1} SAGA ne permet pas créer des iso au format geojson.\n").\
                                format( PHYSIOCAP_WARNING, PHYSIOCAP_UNI)
                        aText = aText + self.tr( "L'interpolation de {0} doit être réalisée par GDAL").format( un_nom)
                        physiocap_log( aText, leModeDeTrace)
                        choix_definitif_interpolation = "GDAL" 
                    else:
####                        aText = self.tr( "\nUn nom {0} est ascii compatible : {1}").\
####                                format( un_nom,  physiocap_is_only_ascii( un_nom))
####                        physiocap_log( aText, leModeDeTrace)
                        choix_definitif_interpolation = choix_interpolation 

                    # ###################
                    # Préparation du nom de l'entité pour les cas GDAL si besoin (comme pour INTER)
                    # ###################        
                    if ( champ_pb_gdal == "YES"):
                        # Prepare un nom sans cote (requete dans gdal et nommage dans gdal)
                        le_nom_entite_libere = physiocap_nom_entite_sans_pb_caractere( un_nom) 
                    else:
                        le_nom_entite_libere = un_nom

                    if physiocap_nom_entite_avec_pb_caractere( le_nom_entite_libere,  choix_definitif_interpolation):
                        # ASSERT le_nom_entite_libere contient un caractère non supporté par GDAL
                        physiocap_log ( self.tr( "=~= {0} Pas d'interpolation de {1}").\
                        format( PHYSIOCAP_UNI, un_nom), leModeDeTrace)
                        raise physiocap_exception_probleme_caractere_librairie( le_nom_entite_libere)
                        
                    physiocap_log ( self.tr( "=~= {0} Début d'interpolation de {1} (index {2})").\
                        format( PHYSIOCAP_UNI, un_nom,  id_contour), leModeDeTrace)

                    # Nom du Shape moyenne 
                    nom_court_vignette = nom_noeud_arbre + NOM_MOYENNE + le_nom_entite_libere +  EXTENSION_CRS_VECTEUR     
                    # Attention j'ai enleve physiocap_rename_existing_file(
                    nom_vignette = os.path.join( chemin_vignettes, nom_court_vignette)        
                                
                    # Nom point 
                    nom_court_point = nom_noeud_arbre + NOM_POINTS + SEPARATEUR_ + le_nom_entite_libere + EXTENSION_CRS_VECTEUR     
                    nom_point = os.path.join( chemin_vignettes, nom_court_point)                    
                    #physiocap_log( "=~= Vignette court : " +  nom_court_vignette , TRACE_INTRA)  

                    # Verifier si le point et la vignette existent
                    if not (os.path.exists( nom_vignette)):
                        physiocap_log( self.tr( "=~= {0} Vignette {1} absente : pas d'interpolation").\
                            format( PHYSIOCAP_WARNING, le_nom_entite_libere ), leModeDeTrace)
                        continue
                    if not (os.path.exists( nom_point)):
                        physiocap_log( self.tr( "=~= {0} Points de {1} absents : pas d'interpolation").\
                            format( PHYSIOCAP_WARNING, le_nom_entite_libere ), leModeDeTrace)
                        continue
                    else:
                        contour_avec_point = contour_avec_point + 1
                        #physiocap_log( "=~= Points - nom court : " +  nom_court_point , TRACE_INTRA)
                        #physiocap_log( "=~= Points - nom  : " +  nom_point , TRACE_INTRA)

                    # ###################
                    # CRÉATION groupe INTRA
                    # ###################
                    physiocap_log( "=~= Contour numéro {0}".format( contour_avec_point), TRACE_INTRA)
                    if ( contour_avec_point == 1):
                        if un_groupe != None:
                            vignette_projet = nom_noeud_arbre + SEPARATEUR_ + le_champ_choisi + SEPARATEUR_ + VIGNETTES_INTRA 
                            vignette_existante = un_groupe.findGroup( vignette_projet)
                            if ( vignette_existante == None ):
                                vignette_group_intra = un_groupe.addGroup( vignette_projet)
                                #physiocap_log( "=~= in vignette {0}".format( contour_avec_point), TRACE_INTRA)
                            else:
                                vignette_group_intra = vignette_existante
                                if arret_groupe_intra == "YES":
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
                            self.creer_raster_iso( dialogue, choix_interpolation, choix_definitif_interpolation, 
                            nom_noeud_arbre, chemin_raster, chemin_iso,
                            nom_court_vignette, nom_vignette, nom_court_point, nom_point,
                            le_champ_choisi, le_choix_INTRA_continue, le_nom_entite_libere)
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
                    
                    physiocap_log( "=~= Contour numéro {0}".format( contour_avec_point), TRACE_INTRA)
                       
                    # Affichage dans panneau des couches QGIS                           
                    if ( id_contour >  0 ):                                            
                        if (( dialogue.checkBoxIntraIsos.isChecked()) or 
                            ( dialogue.checkBoxIntraImages.isChecked())):

                            if (consolidation == "YES"):
                                # modifier les noms courts raster et iso
                                longueur_nom_arbre = len(nom_noeud_arbre)
                                nom_court_raster_ori = nom_court_raster
                                nom_court_raster = shape_point_sans_extension + \
                                    nom_court_raster_ori[longueur_nom_arbre:]
                                nom_court_isoligne_ori = nom_court_isoligne
                                nom_court_isoligne = shape_point_sans_extension + \
                                    nom_court_isoligne_ori[longueur_nom_arbre:]

                            afficheIso = "NO"
                            if ( dialogue.checkBoxIntraIsos.isChecked()):
                                afficheIso = "YES"                
                            afficheRaster = "NO"
                            if ( dialogue.checkBoxIntraImages.isChecked()):
                                afficheRaster = "YES"
                            physiocap_log( "=~= Avant nouveaux numéro {0}".format( contour_avec_point), TRACE_INTRA)
                            if nouveau == "NOUVEAUX":
                                self.afficher_raster_iso( dialogue, \
                                    nom_raster_final, nom_court_raster, le_template_raster, afficheRaster,
                                    nom_iso_final, nom_court_isoligne, le_template_isolignes, afficheIso,
                                    vignette_group_intra, mon_projet)
                        physiocap_log ( self.tr( "=~= Fin Interpolation de {0}").\
                            format( un_nom), leModeDeTrace)
                        
                        # Impression PDF
                        if  dialogue.checkBoxIntraPDF.isChecked():
                            moyenne = 'Inconnue'
                            for un_contour in vignette_toutes_vecteur.getFeatures():
                                if un_contour[ CHAMP_NOM_PHY] != un_nom:
                                    continue
                                moyenne = un_contour[ le_champ_choisi]
                                break
                            self.imprimer_raster( dialogue, nom_raster_final, nom_court_raster, \
                                    un_nom, le_champ_choisi, moyenne)

            if ( contour_avec_point >  0 ):                                            
                physiocap_log( self.tr( "=~= Fin des {0}/{1} interpolation(s) intra parcellaire").\
                    format( str(contour_avec_point), str( contours_possibles)), leModeDeTrace)
            elif (contours_possibles == 0):
                aText = self.tr( "=~= Aucune interpolation(s) intra parcellaire à réaliser")
                aText = aText + self.tr( "=~= Vérifier dans l'onglet affichage vos choix.")
                physiocap_log( aText, leModeDeTrace)
                return physiocap_message_box( dialogue, aText, "information")
            else:
                if not dialogue.checkBoxToutes.isChecked():
                    aText = self.tr( "=~= Aucun point interpolé dans votre contour demandé dans {}\n".\
                        format(  dialogue.fieldComboParcelleIntra.currentText()))      
                    aText = aText + self.tr( "Pas d'interpolation intra parcellaire. ")       
                    aText = aText + self.tr( "\nVérifiez votre choix d'identifiant.")       
                else:
                    aText = self.tr( "=~= Aucun point interpolé dans vos {0} contours présents dans {1}\n".\
                        format(  contours_possibles, nom_vecteur_contour))      
                    aText = aText + self.tr( "\nNom point {0} \n".\
                        format( nom_point_exact))       
                    aText = aText + self.tr( "Pas d'interpolation intra parcellaire. ")       
                    aText = aText + self.tr( "\nUn changement a pu avoir lieu sur vos répertoires depuis votre calcul inter parcellaire ?")       
                    aText = aText + self.tr( "\nVérifiez votre choix de jeu de mesures.")       
                    aText = aText + self.tr( "\nVérifiez le champ identifiant votre contour.")       
                dialogue.ButtonInter.setEnabled( True)
                physiocap_log( aText, leModeDeTrace)
                return physiocap_message_box( dialogue, aText, "information")
            
        dialogue.progressBarIntra.setValue( 100)
        vecteur_poly = None
        vecteur_point = None
        dialogue.ButtonIntra.setEnabled( True)
        if  dialogue.checkBoxTroisActions.isChecked():                                            
            return physiocap_message_box( dialogue, 
                        self.tr( "Fin de l'enchainement pour la session {}".format( derniere_session)),
                        "information")
        else:
            return physiocap_message_box( dialogue, 
                        self.tr( "Fin de l'interpolation intra-parcellaire"),
                        "information")
                        
