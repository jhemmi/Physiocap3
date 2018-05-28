# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Physiocap3_dialog
                                 A QGIS 3 plugin
 Physiocap3 plugin helps analyse raw data from Physiocap in QGIS 3 and 
 creates a synthesis of Physiocap measures' campaign
 Physiocap3 plugin permet l'analyse les données brutes de Physiocap dans QGIS 3 et
 crée une synthese d'une campagne de mesures Physiocap
 
 Le module dialog gère la dynamique des dialogues, initialisation 
 et récupération des variables, sauvegarde des parametres.
 Les slots sont définis et activés.
 La gestion des assert avant traitement et des retours d'exception se trouve 
 dans ce module 

 Les variables et fonctions sont nommées en Francais
 
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

from .Physiocap_tools import physiocap_message_box, \
        physiocap_log_for_error, physiocap_log, physiocap_error, \
        physiocap_quelle_projection_et_lib_demandee, physiocap_nom_entite_avec_pb_caractere, \
        physiocap_get_layer_by_name,  physiocap_get_layer_by_ID

from .Physiocap_creer_arbre import PhysiocapFiltrer
from .Physiocap_inter import (PhysiocapInter, physiocap_fill_combo_poly_or_point)
from .Physiocap_intra_interpolation import PhysiocapIntra 
from .Physiocap_var_exception import *

from PyQt5 import uic
from PyQt5.QtCore import (QSettings, Qt, QUrl)
from PyQt5.QtGui import (QPixmap,  QDesktopServices)
from PyQt5.QtWidgets import (QDialogButtonBox, QDialog, QFileDialog) 
from qgis.core import (Qgis) # QgsMessageLog) #, QgsProject, QgsMapLayer)   

FORM_CLASS, _ = uic.loadUiType(os.path.join( os.path.dirname(__file__), 'Physiocap3_dialog_base.ui'))

class Physiocap3Dialog( QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructeur du dialogue Physiocap 
        Initialisation et recupération des variables, sauvegarde des parametres.
        Les slots sont définis et activés.
        """
        super(Physiocap3Dialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.plugin_dir = os.path.dirname(__file__)  
        self.plugins_dir = os.path.dirname( self.plugin_dir)
        self.python_dir = os.path.dirname( self.plugins_dir)
        self.gis_dir = os.path.dirname( self.python_dir)

#        version_3 = "NO"
#        if self.checkBoxV3.isChecked():
#            version_3 = "YES"

        self.settings= QSettings(PHYSIOCAP_NOM, PHYSIOCAP_NOM_3)
        # Remplissage du mode de traces
        self.fieldComboModeTrace.setCurrentIndex( 0)
        if len( MODE_TRACE) == 0:
            self.fieldComboModeTrace.clear( )
            physiocap_error( self, self.tr( "Pas de liste des modes de traces pré défini"))
        else:
            self.fieldComboModeTrace.clear( )
            self.fieldComboModeTrace.addItems( MODE_TRACE )
            # Retrouver le mode de trace dans  settings
            leModeDeTrace = self.settings.value("Physiocap/leModeTrace", TRACE_TOUT)
            for idx, modeTrace in enumerate( MODE_TRACE):
                if ( modeTrace == leModeDeTrace):
                    self.fieldComboModeTrace.setCurrentIndex( idx)

       
        #physiocap_log( "Répertoire de QGIS : " +  self.gis_dir, leModeDeTrace)
        physiocap_log( "Répertoire des plugins ou extensions : " +  self.plugins_dir, leModeDeTrace)
       
        # Slot for boutons : ces deux sont déjà sont dans UI
        ##self.buttonBox.button( QDialogButtonBox.Ok ).pressed.connect(self.accept)
        ##self.buttonBox.button( QDialogButtonBox.Cancel ).pressed.connect(self.reject)
        self.buttonBox.button( QDialogButtonBox.Help ).pressed.connect(self.slot_AIDE_demander)
        self.ButtonFiltrer.pressed.connect(self.slot_accept)
        self.buttonContribuer.pressed.connect(self.slot_AIDE_demander_contribution)
        
        # Slot pour données brutes et pour données cibles
        self.toolButtonDirectoryPhysiocap.pressed.connect( self.slot_lecture_repertoire_donnees_brutes )  
        self.toolButtonDirectoryFiltre.pressed.connect( self.slot_lecture_repertoire_donnees_cibles)  
        # Slot pour le groupe vignoble
        self.checkBoxInfoVignoble.stateChanged.connect( self.slot_bascule_details_vignoble)
        # Slot pour le groupe format V3
        self.checkBoxV3.stateChanged.connect( self.slot_bascule_V3)
        self.checkBoxInterPasMesure.stateChanged.connect( self.slot_bascule_pas_mesure)
        self.checkBoxInterSegment.stateChanged.connect( self.slot_bascule_segment)
        self.checkBoxInterSegmentBrise.stateChanged.connect( self.slot_bascule_segment_brise)

        onglet_params = self.tr("{0} Params").format( PHYSIOCAP_UNI)
        self.tabWidgetPhysiocap.setTabText(0, onglet_params)
       
        # Inter
        self.comboBoxPolygone.currentIndexChanged[int].connect( self.slot_INTER_maj_champ_poly_liste )
        self.fieldComboContours.currentIndexChanged[int].connect( self.slot_INTER_change_champ_choisi )
        self.ButtonInter.pressed.connect(self.slot_INTER_moyennes_parcelles)
        self.ButtonInterRefresh.pressed.connect(self.slot_INTER_liste_parcelles)
        self.groupBoxInter.setEnabled( False)
        
        # Intra        
        self.comboBoxPoints.currentIndexChanged[int].connect( self.slot_INTER_INTRA_maj_points_choix )
        self.fieldComboIntra.currentIndexChanged[int].connect( self.slot_INTRA_min_max_champ )
        self.spinBoxIsoMin_Fixe_DIAM.valueChanged.connect( self.slot_INTRA_DIAM_min_max_fixe )
        self.spinBoxIsoMax_Fixe_DIAM.valueChanged.connect( self.slot_INTRA_DIAM_min_max_fixe )
        self.spinBoxIsoMin_Fixe_SARM.valueChanged.connect( self.slot_INTRA_SARM_min_max_fixe )
        self.spinBoxIsoMax_Fixe_BIOM.valueChanged.connect( self.slot_INTRA_BIOM_min_max_fixe )
        self.spinBoxIsoMin_Fixe_SARM.valueChanged.connect( self.slot_INTRA_SARM_min_max_fixe )
        self.spinBoxIsoMax_Fixe_BIOM.valueChanged.connect( self.slot_INTRA_BIOM_min_max_fixe )
        # attention aux appel recursif infini : on a fait 2 maj_attributs ... 
        self.fieldComboIntraDIAM.currentIndexChanged[int].connect( self.slot_INTRA_maj_attributs_interpolables)
        self.fieldComboIntraSARM.currentIndexChanged[int].connect( self.slot_INTRA_maj_attributs_interpolables)
        self.fieldComboIntraBIOM.currentIndexChanged[int].connect( self.slot_INTRA_maj_attributs_interpolables)

        self.ButtonIntra.pressed.connect(self.slot_INTRA_interpolation_parcelles)
        self.groupBoxIntra.setEnabled( False)
        self.groupBoxArret.setEnabled( False)
        self.groupBoxMethode.setEnabled( False)
        self.ButtonIntra.setEnabled( False)
        
        # Affichage
        self.fieldComboAideIso.currentIndexChanged[int].connect( self.slot_INTRA_bascule_aide_iso )
               
        physiocap_log( self.tr( "Votre machine tourne sous QGIS {0} et {1} ").\
            format( Qgis.QGIS_VERSION, MACHINE), TRACE_TOOLS)        
##        physiocap_log( self.tr( "Test 1 et 2 : {0} <===> {1} ").\
##            format( PHYSIOCAP_TEST1, PHYSIOCAP_TEST2), TRACE_TOOLS)
##        physiocap_log( self.tr( "Test 3 et 4 : {0} <===> {1} ").\
##            format( PHYSIOCAP_TEST3, PHYSIOCAP_TEST4), TRACE_TOOLS)
##        physiocap_log( self.tr( "QGIS attend des couches de projection SRID {0} CRS_ID {1} ").\
##            format( GEOSRID, GEO_EPSG_CRS_ID ), TRACE_TOOLS)
        
        
        # Style sheet pour QProgressBar
        self.setStyleSheet( "QProgressBar {color:black; text-align:center; font-weight:bold; padding:2px;}"
           "QProgressBar:chunk {background-color:green; width: 10px; margin-left:1px;}")
        
        ###############
        # Récuperation dans les settings (derniers parametres saisies)
        ###############
        self.settings= QSettings(PHYSIOCAP_NOM, PHYSIOCAP_NOM_3)
        # Initialisation des parametres à partir des settings
        nom_projet = self.settings.value("Physiocap/projet", NOM_PROJET)
        self.lineEditProjet.setText( nom_projet)
        
        if (self.settings.value("Physiocap/recursif") == "YES"):
            self.checkBoxRecursif.setChecked( Qt.Checked)
        else:
            self.checkBoxRecursif.setChecked( Qt.Unchecked)

        if (self.settings.value("Physiocap/version3") == "YES"):
            self.checkBoxV3.setChecked( Qt.Checked)
        else:
            self.checkBoxV3.setChecked( Qt.Unchecked)        
        self.slot_bascule_V3()    
 
        mode_expert = self.settings.value("Physiocap/expert", "As-tu contribué ?")
        self.lineEditExpert.setText( mode_expert)
        self.groupBoxSegment.setEnabled( mode_expert == MODE_EXPERT)
        self.groupBoxThemaTrace.setEnabled( mode_expert == MODE_EXPERT)
        self.groupBoxInterIntraExpert.setEnabled( mode_expert == MODE_EXPERT)

        # Nom de la session et des répertoires
        repertoire_brut = self.settings.value("Physiocap/repertoire",
            REPERTOIRE_DONNEES_BRUTES)
        self.lineEditDirectoryPhysiocap.setText( repertoire_brut )
        self.lineEditDernierProjet.setText( self.settings.value("Physiocap/dernier_repertoire",
            ""))    
        # Répertoire cibles apres filtre
        repertoire_cible = self.settings.value("Physiocap/cible_repertoire", "VIDE")
        if ( repertoire_cible == "VIDE"):
            repertoire_cible = repertoire_brut
        self.lineEditDirectoryFiltre.setText( repertoire_cible)
                
        # Consolidation
        if (self.settings.value("Physiocap/consolidation") == "YES"):
            self.checkBoxConsolidation.setChecked( Qt.Checked)
        else:
            self.checkBoxConsolidation.setChecked( Qt.Unchecked)
    
        # Saga to TIFF par defaut
        if (self.settings.value("Physiocap/SagaTIFF") == "NO"):
            self.checkBoxSagaTIFF.setChecked( Qt.Unchecked)
        else:
            self.checkBoxSagaTIFF.setChecked( Qt.Checked)
        
            
        # Choisir radioButtonL93 ou radioButtonGPS
        laProjectionCochee = self.settings.value("Physiocap/laProjection", PROJECTION_L93)
        #physiocap_log( "Projection récupérée " + laProjectionCochee, leModeDeTrace)
        if ( laProjectionCochee == PROJECTION_GPS ):
            self.radioButtonGPS.setChecked(  Qt.Checked)
        else:
            #physiocap_log( "Projection allumé L93 ==? " + laProjectionCochee, leModeDeTrace)
            self.radioButtonL93.setChecked(  Qt.Checked)
            
        # Remettre vide le textEditSynthese
        self.textEditSynthese.clear()
        
        # Remplissage de la liste de FORMAT_VECTEUR 
        self.fieldComboFormats.setCurrentIndex( 0) 
        
        if ( self.settings.value("Physiocap/expert", "As-tu contribué ?") == MODE_EXPERT):
            liste_formats = FORMAT_VECTEUR_V3
        else:
            liste_formats = FORMAT_VECTEUR
            


        if len( liste_formats) == 0:
            self.fieldComboFormats.clear( )
            physiocap_error( self, self.tr( "Pas de liste des formats de vecteurs pré défini"))
        else:
            self.fieldComboFormats.clear( )
#            #uri = physiocap_get_uri_by_layer( self)
#            uri = None
#            if uri != None:
            if (self.settings.value("Physiocap/version3") == "YES"):
                self.fieldComboFormats.addItems( liste_formats)
            else:
                self.fieldComboFormats.addItem( liste_formats[ 0])
                self.fieldComboFormats.setEnabled( False)
             # Retrouver le format de  settings
            self.fieldComboFormats.setCurrentIndex( 0)
            leFormat = self.settings.value("Physiocap/leFormat", "xx") 
            for idx, unFormat in enumerate( liste_formats):
                if ( unFormat == leFormat):
                    self.fieldComboFormats.setCurrentIndex( idx)
                    #physiocap_log( self.tr( "Format retrouvé"), leModeDeTrace) 


        # Remplissage des parametres segment à partir des settings
        self.doubleSpinBoxVitesseMiniSegment.setValue( 
            float( self.settings.value("Physiocap/vitesse_mini_segment", 2.5 )))
        self.doubleSpinBoxVitesseMaxiSegment.setValue( 
            float( self.settings.value("Physiocap/vitesse_maxi_segment", 8.0 )))
        self.spinBoxNombreMiniPointsConsecutifs.setValue( 
            int( self.settings.value("Physiocap/nombre_mini_points", 5 )))
        self.spinBoxDeriveMaxSegment.setValue( int( self.settings.value("Physiocap/derive_max_segment", 35 )))
        self.spinBoxPasDeDerive.setValue( int( self.settings.value("Physiocap/pas_de_la_derive", 30 )))
        self.doubleSpinBoxPdopMaxSegment.setValue( 
            float( self.settings.value("Physiocap/pdop_max_segment", 2.0 )))        
        
        # Remplissage des parametres vignobles à partir des settings
        self.spinBoxMinDiametre.setValue( int( self.settings.value("Physiocap/mindiam", 2 )))
        self.spinBoxMaxDiametre.setValue( int( self.settings.value("Physiocap/maxdiam", 28 )))
        self.spinBoxMaxSarmentsParMetre.setValue( int( self.settings.value("Physiocap/max_sarments_metre", 25 )))
        if (self.settings.value("Physiocap/details") == "YES"):
            self.checkBoxInfoVignoble.setChecked( Qt.Checked)
            self.Vignoble.setEnabled( True)
        else:
            self.checkBoxInfoVignoble.setChecked( Qt.Unchecked)
            self.Vignoble.setEnabled( False)
        
        self.spinBoxInterrangs.setValue( int( self.settings.value("Physiocap/interrangs", 110 )))
        self.spinBoxInterceps.setValue( int( self.settings.value("Physiocap/interceps", 100 )))
        # Densité pied /ha
        self.slot_calcul_densite()
        self.spinBoxHauteur.setValue( int( self.settings.value("Physiocap/hauteur", 90 )))
        self.doubleSpinBoxDensite.setValue( float( self.settings.value("Physiocap/densite", 0.9 )))

        # Remplissage de la liste de SHAPE Filtre
        # DIAMETRE : Cas unique
        self.fieldComboShapeDiametre.clear( )
        self.fieldComboShapeDiametre.addItem( PHYSIOCAP_WARNING + " " + self.tr("Sarments filtrés"))
        self.fieldComboShapeDiametre.setCurrentIndex( 0)                
 
        # SARMENT
        self.fieldComboShapeSarment.setCurrentIndex( 0)   
        leChoixDeShape = int( self.settings.value("Physiocap/leChoixShapeSarment", -1)) 
        # Cas initial
        self.fieldComboShapeSarment.clear( )
        self.fieldComboShapeSarment.addItem( self.tr("Sarments filtrés") )
        self.fieldComboShapeSarment.addItem( self.tr("Points sans sarment") )
        if ( leChoixDeShape == -1):
            self.fieldComboShapeSarment.setCurrentIndex( 0)                
        else:
            # Le combo a déjà été rempli, on retrouve le choix
            self.fieldComboShapeSarment.setCurrentIndex( leChoixDeShape)
        # Vitesse
        self.fieldComboShapeVitesse.setCurrentIndex( 0)   
        leChoixDeShape = int( self.settings.value("Physiocap/leChoixShapeVitesse", -1)) 
        # Cas initial
        self.fieldComboShapeVitesse.clear( )
        self.fieldComboShapeVitesse.addItem( self.tr("Sarments filtrés") )
        self.fieldComboShapeVitesse.addItem( self.tr("Points sans sarment") )
        if ( leChoixDeShape == -1):
            self.fieldComboShapeVitesse.setCurrentIndex( 0)                
        else:
            # Le combo a déjà été rempli, on retrouve le choix
            self.fieldComboShapeVitesse.setCurrentIndex( leChoixDeShape)
        # BIOMASSE
        self.fieldComboShapeBiomasse.setCurrentIndex( 0)   
        leChoixDeShape = int( self.settings.value("Physiocap/leChoixShapeBiomasse", -1)) 
        # Cas initial
        self.fieldComboShapeBiomasse.clear( )
        self.fieldComboShapeBiomasse.addItem( self.tr("Sarments filtrés") )
        self.fieldComboShapeBiomasse.addItem( self.tr("Points sans sarment") )
        if ( leChoixDeShape == -1):
            self.fieldComboShapeBiomasse.setCurrentIndex( 0)                
        else:
            # Le combo a déjà été rempli, on retrouve le choix
            self.fieldComboShapeBiomasse.setCurrentIndex( leChoixDeShape)

        # PAS DE MESURE : Cas unique
        self.fieldComboShapePasMesure.clear( )
        self.fieldComboShapePasMesure.addItem( self.tr("Points sans mesure"))
        self.fieldComboShapeDiametre.setCurrentIndex( 0)                

        # Remplissage du choix d'aide au calcul isoligne
        self.fieldComboAideIso.setCurrentIndex( 0)   
        leChoixAideIso = int( self.settings.value("Physiocap/leChoixAideIso", 0)) 
        # Cas inital
        self.fieldComboAideIso.clear( )
        self.fieldComboAideIso.addItem( \
            self.tr("Nombre d'isolignes permet le calcul de l'écartement des isolignes"))
        self.fieldComboAideIso.addItem( \
            self.tr("Ecartement des isolignes permet le calcul du nombre d'isolignes"))
        self.fieldComboAideIso.addItem( \
            self.tr("Utilisation des paramètres fixes (min, nombre des isolignes et max) pour chaque attribut"))
        # Le combo a déjà été rempli, on retrouve le choix
        self.fieldComboAideIso.setCurrentIndex( leChoixAideIso) 
                
        # Selon le choix on rend modifiable 
        self.slot_INTRA_bascule_aide_iso()
               
        # Remplissage de la liste de CHEMIN_TEMPLATES
        self.fieldComboThematiques.setCurrentIndex( 0)   
        if len( CHEMIN_TEMPLATES) == 0:
            self.fieldComboThematiques.clear( )
            aText = self.tr( "Pas de répertoire de thématiques pré défini")
            physiocap_log( aText, leModeDeTrace)
            physiocap_error( self, aText)
        else:
            leChoixDeThematiques = int( self.settings.value("Physiocap/leChoixDeThematiques", 0)) 
            # Cas inital
            CHEMIN_TEMPLATES_USER = []
            self.fieldComboThematiques.clear( )
            CHEMIN_TEMPLATES_USER.append( os.path.join( self.plugin_dir, CHEMIN_TEMPLATES[0]))
            # On donne le chemin QGIS ou celui présent dans les preferences
            if leChoixDeThematiques == 1:
                chemin_preference = self.settings.value("Physiocap/leDirThematiques", \
                    os.path.join( self.gis_dir, CHEMIN_TEMPLATES[1]))
            else:
                # cas QGIS pour le premier cas
                chemin_preference = os.path.join( self.gis_dir, CHEMIN_TEMPLATES[1])                
            CHEMIN_TEMPLATES_USER.append( chemin_preference)
            self.fieldComboThematiques.addItems( CHEMIN_TEMPLATES_USER )

            # Le combo a déjà été rempli, on retrouve le choix
            self.fieldComboThematiques.setCurrentIndex( leChoixDeThematiques)
            if ( leChoixDeThematiques == 1): 
                # On est dans le cas où l'utilisateur a pris la main sur ces qml
                # autorisation de modifier les nom de qml
                self.groupBoxThematiques.setEnabled( True)
                # Renommage V3
                themeDiametre = self.settings.value("Physiocap/themeDiametre", "Filtre diamètre")
                self.lineEditThematiqueDiametre.setText( themeDiametre )
                themeSarment = self.settings.value("Physiocap/themeSarment", "Filtre sarment")
                self.lineEditThematiqueSarment.setText( themeSarment )
                themeBiomasse = self.settings.value("Physiocap/themeBiomasse", "Filtre biomasse")
                self.lineEditThematiqueBiomasse.setText( themeBiomasse )
                themeVitesse = self.settings.value("Physiocap/themeVitesse", "Filtre vitesse")
                self.lineEditThematiqueVitesse.setText( themeVitesse )
                themePasMesure = self.settings.value("Physiocap/themePasMesure", "Filtre pas de mesure")
                self.lineEditThematiquePasMesure.setText( themePasMesure )
                themeSegment = self.settings.value("Physiocap/themeSegment", "Filtre segment")
                self.lineEditThematiqueSegment.setText( themeSegment )
                themeSegmentBrise = self.settings.value("Physiocap/themeSegmentBrise", "Filtre segment brisé")
                self.lineEditThematiqueSegmentBrise.setText( themeSegmentBrise )
                # Inter
                themeDiametre = self.settings.value("Physiocap/themeInterDiametre", "Inter diamètre")
                self.lineEditThematiqueInterDiametre.setText( themeDiametre )
                themeSarment = self.settings.value("Physiocap/themeInterSarment", "Inter sarment")
                self.lineEditThematiqueInterSarment.setText( themeSarment )
                themeBiomasse = self.settings.value("Physiocap/themeInterBiomasse", "Inter biomasse")
                self.lineEditThematiqueInterBiomasse.setText( themeBiomasse )

                themeAltitude = self.settings.value("Physiocap/themeInterAltitude", "Inter altitude")
                self.lineEditThematiqueInterAltitude.setText( themeAltitude )
                # inter Libelle
                themeLibelle = self.settings.value("Physiocap/themeInterLibelle", "Inter parcelles")
                self.lineEditThematiqueInterLibelle.setText( themeLibelle )
                # inter moyenne et points
                themeMoyenne = self.settings.value("Physiocap/themeInterMoyenne", "Inter parcelle")
                self.lineEditThematiqueInterMoyenne.setText( themeMoyenne )
                themePoints = self.settings.value("Physiocap/themeInterPoints", "Filtre diamètre 3D")
                self.lineEditThematiqueInterPoints.setText( themePoints )
                themeInterPasMesure = self.settings.value("Physiocap/themeInterPasMesure", "Inter pieds manquants")
                self.lineEditThematiqueInterPasMesure.setText( themeInterPasMesure )
                themeSegment = self.settings.value("Physiocap/themeInterSegment", "Inter Segment")
                self.lineEditThematiqueInterSegment.setText( themeSegment )
                themeSegmentBrise = self.settings.value("Physiocap/themeInterSegmentBrise", "Inter Segment Brise")
                self.lineEditThematiqueInterSegmentBrise.setText( themeSegmentBrise )
                # intra
                themeIso = self.settings.value("Physiocap/themeIntraIso", "Isolignes")
                self.lineEditThematiqueIntraIso.setText( themeIso )
                themeImage = self.settings.value("Physiocap/themeIntraImage", "Intra")
                self.lineEditThematiqueIntraImage.setText( themeImage )
            else:
                # Cas repertoire du plugin
                self.groupBoxThematiques.setEnabled( False)
                # Remettre les nom de thematiques par defaut 
                self.lineEditThematiqueDiametre.setText("Filtre diamètre")
                self.settings.setValue("Physiocap/themeDiametre", "Filtre diamètre")
                self.lineEditThematiqueSarment.setText("Filtre sarment")
                self.settings.setValue("Physiocap/themeSarment", "Filtre sarment")
                self.lineEditThematiqueBiomasse.setText("Filtre biomasse")
                self.settings.setValue("Physiocap/themeBiomasse", "Filtre biomasse")
                self.lineEditThematiqueVitesse.setText("Filtre vitesse")
                self.settings.setValue("Physiocap/themeVitesse", "Filtre vitesse")
                self.lineEditThematiquePasMesure.setText("Filtre pas de mesure")
                self.settings.setValue("Physiocap/themePasMesure", "Filtre pas de mesure")
                self.lineEditThematiqueSegment.setText("Filtre segment")
                self.settings.setValue("Physiocap/themeSegment","Filtre segment")
                self.lineEditThematiqueSegmentBrise.setText("Filtre segment brisé")
                self.settings.setValue("Physiocap/themeSegmentBrise","Filtre segment brisé")
                # Inter
                self.lineEditThematiqueInterDiametre.setText("Inter diamètre")
                self.settings.setValue("Physiocap/themeInterDiametre", "Inter diamètre")
                self.lineEditThematiqueInterSarment.setText("Inter sarment")
                self.settings.setValue("Physiocap/themeInterSarment", "Inter sarment")
                self.lineEditThematiqueInterBiomasse.setText("Inter biomasse")
                self.settings.setValue("Physiocap/themeInterBiomasse", "Inter biomasse")

                self.lineEditThematiqueInterAltitude.setText("Inter altitude")
                self.settings.setValue("Physiocap/themeInterAltitude", "Inter altitude")
                
                self.lineEditThematiqueInterLibelle.setText("Inter parcelles")
                self.settings.setValue("Physiocap/themeInterLibelle", "Inter parcelles")
                # inter moyenne et points
                self.lineEditThematiqueInterMoyenne.setText("Inter parcelle")
                self.settings.setValue("Physiocap/themeInterMoyenne", "Inter parcelle")
                self.lineEditThematiqueInterPoints.setText("Filtre diamètre 3D")
                self.settings.setValue("Physiocap/themeInterPoints", "Filtre diamètre 3D")     
                self.lineEditThematiqueInterPasMesure.setText("Inter pieds manquants")
                self.settings.setValue("Physiocap/themePasMesure", "Inter pieds manquants")
                self.lineEditThematiqueInterSegment.setText("Inter segment")
                self.settings.setValue("Physiocap/themeInterSegment", "Inter segment")
                self.lineEditThematiqueInterSegmentBrise.setText("Inter segment brisé")
                self.settings.setValue("Physiocap/themeInterSegmentBrise", "Inter segment brisé")
                # Intra
                self.lineEditThematiqueIntraIso.setText("Isolignes")
                self.settings.setValue("Physiocap/themeIntraIso", "Isolignes")
                self.lineEditThematiqueIntraImage.setText("Intra")
                self.settings.setValue("Physiocap/themeIntraImage", "Intra")
                

        try :
            import matplotlib
        except ImportError:
            aText = self.tr( "Le module matplotlib n'est pas accessible. ")
            aText = aText + self.tr( "Vous ne pouvez pas visualiser les histogrammes ")
            physiocap_log( aText, leModeDeTrace)
            physiocap_error( self, aText)
            self.settings.setValue("Physiocap/histogrammes", "NO")
            self.checkBoxHistogramme.setChecked( Qt.Unchecked)
            self.checkBoxHistogramme.setEnabled( False)
            aText = self.tr( 'Physiocap : Votre installation QGIS ne permet pas du visualisation des histogrammes')
            physiocap_log( aText, leModeDeTrace)
            physiocap_message_box( self, aText, "information")

        if (self.settings.value("Physiocap/histogrammes") == "YES"):
            self.checkBoxHistogramme.setChecked( Qt.Checked)
        else:
            self.checkBoxHistogramme.setChecked( Qt.Unchecked)
        # Pas d'histo avant calcul
        self.label_histo_sarment.setPixmap( QPixmap( FICHIER_HISTO_NON_CALCULE))
        self.label_histo_vitesse.setPixmap( QPixmap( FICHIER_HISTO_NON_CALCULE))
        self.label_histo_diametre_avant.setPixmap( QPixmap( FICHIER_HISTO_NON_CALCULE))
        self.label_histo_diametre_apres.setPixmap( QPixmap( FICHIER_HISTO_NON_CALCULE))
        
        # Les parametres Intra  
        self.spinBoxPower.setValue( float( self.settings.value("Physiocap/powerIntra", 2 )))
        self.spinBoxPixel.setValue( float( self.settings.value("Physiocap/pixelIntra", 0.5 )))
        self.spinBoxDoubleRayon.setValue( float( self.settings.value("Physiocap/rayonIntra", 12 )))
        self.slot_INTRA_rayon_selon_SCR_LIB()
        # Cas des 3 iso fixes
        self.spinBoxIsoMin_Fixe_DIAM.setValue( int( self.settings.value("Physiocap/isoMinFixe_1", 7 )))
        self.spinBoxIsoMax_Fixe_DIAM.setValue( int( self.settings.value("Physiocap/isoMaxFixe_1", 11 )))
        self.spinBoxIsoDistance_Fixe_DIAM.setValue( int( self.settings.value("Physiocap/isoDistanceFixe_1", 1 )))
        self.spinBoxIsoMin_Fixe_SARM.setValue( int( self.settings.value("Physiocap/isoMinFixe_2", 5 )))
        self.spinBoxIsoMax_Fixe_SARM.setValue( int( self.settings.value("Physiocap/isoMaxFixe_2", 13)))
        self.spinBoxIsoDistance_Fixe_SARM.setValue( int( self.settings.value("Physiocap/isoDistanceFixe_2", 2 )))
        self.spinBoxIsoMin_Fixe_BIOM.setValue( int( self.settings.value("Physiocap/isoMinFixe_3", 200 )))
        self.spinBoxIsoMax_Fixe_BIOM.setValue( int( self.settings.value("Physiocap/isoMaxFixe_3", 1000 )))
        self.spinBoxIsoDistance_Fixe_BIOM.setValue( int( self.settings.value("Physiocap/isoDistanceFixe_3", 200 )))
 
        # Cas des dernières valeurs iso
        self.spinBoxIsoMin.setValue( int( self.settings.value("Physiocap/isoMin", 1 )))
        self.spinBoxIsoMax.setValue( int( self.settings.value("Physiocap/isoMax", 1000 )))
        self.spinBoxNombreIso.setValue( int( self.settings.value("Physiocap/isoNombre", 5 )))
        self.spinBoxDistanceIso.setValue( int( self.settings.value("Physiocap/isoDistance", 1 )))

        # Cas de continuation traitement intra
        self.groupBoxArret.setChecked( Qt.Unchecked)
        if (self.settings.value("Physiocap/groupStop") == "YES"):
            self.groupBoxArret.setChecked( Qt.Checked)    
        self.fieldComboIntraContinue.setCurrentIndex( int(self.settings.value("Physiocap/continueIntra", 0)))
        
        
        # On initialise le nombre de distance Iso
        self.slot_INTRA_iso_distance()
         
        if (self.settings.value("Physiocap/library") == "SAGA"):
            self.radioButtonSAGA.setChecked(  Qt.Checked)
            self.spinBoxPower.setEnabled( False)
        else:
            self.radioButtonGDAL.setChecked(  Qt.Checked)
        
#       # On ne vérifie pas la version SAGA ici mais dans Intra
###        # Cas Windows : on force SAGA
###        if ( MACHINE == "Windows"):
###            self.radioButtonSAGA.setChecked(  Qt.Checked)
###            # On bloque Gdal
###            self.radioButtonGDAL.setEnabled( False)
###            self.spinBoxPower.setEnabled( False)
###            self.spinBoxPixel.setEnabled( True)

        # Choix d'affichage généraux
        # Toujour le diametre qui est necessaire à "Inter"
        self.checkBoxDiametre.setChecked( Qt.Checked)
        # Tous les autres on peut les choisir 
        if (self.settings.value("Affichage/FiltrerSarment", "NO") == "YES"):
            self.checkBoxSarment.setChecked( Qt.Checked)
        else:
            self.checkBoxSarment.setChecked( Qt.Unchecked)
        if (self.settings.value("Affichage/FiltrerBiomasse", "NO") == "YES"):
            self.checkBoxBiomasse.setChecked( Qt.Checked)
        else:
            self.checkBoxBiomasse.setChecked( Qt.Unchecked)
        if (self.settings.value("Affichage/FiltrerVitesse", "NO") == "YES"):
            self.checkBoxVitesse.setChecked( Qt.Checked)
        else:
            self.checkBoxVitesse.setChecked( Qt.Unchecked)        
        # Toujours pas_mesure qui est necessaire à "Inter"
        self.checkBoxPasMesure.setChecked( Qt.Checked)
        self.checkBoxSegmentBrise.setChecked( Qt.Checked)
        if (self.settings.value("Affichage/FiltrerSegment", "NO") == "YES"):
            self.checkBoxSegment.setChecked( Qt.Checked)
        else:
            self.checkBoxSegment.setChecked( Qt.Unchecked)
            
        # Choix d'affichage Inter
        if (self.settings.value("Affichage/InterDiametre", "YES") == "YES"):
            self.checkBoxInterDiametre.setChecked( Qt.Checked)
        else:
            self.checkBoxInterDiametre.setChecked( Qt.Unchecked)
        if (self.settings.value("Affichage/InterSarment", "NO") == "YES"):
            self.checkBoxInterSarment.setChecked( Qt.Checked)
        else:
            self.checkBoxInterSarment.setChecked( Qt.Unchecked)
        if (self.settings.value("Affichage/InterBiomasse", "YES") == "YES"):
            self.checkBoxInterBiomasse.setChecked( Qt.Checked)
        else:
            self.checkBoxInterBiomasse.setChecked( Qt.Unchecked)
        if (self.settings.value("Affichage/InterAltitude", "NO") == "YES"):
            self.checkBoxInterAltitude.setChecked( Qt.Checked)
        else:
            self.checkBoxInterAltitude.setChecked( Qt.Unchecked)
        # Toujours interpoint qui est necessaire à "Inter"
        self.checkBoxInterLibelle.setChecked( Qt.Checked)     
        if (self.settings.value("Affichage/InterPoints", "NO") == "YES"):
            self.checkBoxInterPoints.setChecked( Qt.Checked)
        else:
            self.checkBoxInterPoints.setChecked( Qt.Unchecked)        
        if (self.settings.value("Affichage/InterMoyennes", "NO") == "YES"):
            self.checkBoxInterMoyennes.setChecked( Qt.Checked)
        else:
            self.checkBoxInterMoyennes.setChecked( Qt.Unchecked)        
        if (self.settings.value("Affichage/InterPasMesure", "YES") == "YES"):
            self.checkBoxInterPasMesure.setChecked( Qt.Checked)
            self.checkBoxInterPasMesureDetails.setEnabled( True)
            if (self.settings.value("Affichage/InterPasMesureDetails", "NO") == "YES"):
                self.checkBoxInterPasMesureDetails.setChecked( Qt.Checked)
        else:
            self.checkBoxInterPasMesure.setChecked( Qt.Unchecked)
            self.checkBoxInterPasMesureDetails.setChecked( Qt.Unchecked)
            self.checkBoxInterPasMesureDetails.setEnabled( False)

        if (self.settings.value("Affichage/InterSegment", "YES") == "YES"):
            self.checkBoxInterSegment.setChecked( Qt.Checked)
            self.checkBoxInterSegmentDetails.setEnabled( True)
            if (self.settings.value("Affichage/InterSegmentDetails", "NO") == "YES"):
                self.checkBoxInterSegmentDetails.setChecked( Qt.Checked)
        else:
            self.checkBoxInterSegment.setChecked( Qt.Unchecked)
            self.checkBoxInterSegmentDetails.setChecked( Qt.Unchecked)
            self.checkBoxInterSegmentDetails.setEnabled( False)

        if (self.settings.value("Affichage/InterSegmentBrise", "YES") == "YES"):
            self.checkBoxInterSegmentBrise.setChecked( Qt.Checked)
            self.checkBoxInterSegmentBriseDetails.setEnabled( True)
            if (self.settings.value("Affichage/InterSegmentBriseDetails", "NO") == "YES"):
                self.checkBoxInterSegmentBriseDetails.setChecked( Qt.Checked)
        else:
            self.checkBoxInterSegmentBrise.setChecked( Qt.Unchecked)        
            self.checkBoxInterSegmentBriseDetails.setChecked( Qt.Unchecked)
            self.checkBoxInterSegmentBriseDetails.setEnabled( False)

        # Choix d'affichage Intra 
        if (self.settings.value("Affichage/IntraUnSeul", "YES") == "YES"):
            self.checkBoxIntraUnSeul.setChecked( Qt.Checked)
        else:
            self.checkBoxIntraUnSeul.setChecked( Qt.Unchecked)
        if (self.settings.value("Affichage/IntraIsos", "NO") == "YES"):
            self.checkBoxIntraIsos.setChecked( Qt.Checked)
        else:
            self.checkBoxIntraIsos.setChecked( Qt.Unchecked)
        if (self.settings.value("Affichage/IntraImages", "NO") == "YES"):
            self.checkBoxIntraImages.setChecked( Qt.Checked)
        else:
            self.checkBoxIntraImages.setChecked( Qt.Unchecked)

        # Calcul dynamique de la densité
        self.spinBoxInterrangs.valueChanged.connect( self.slot_calcul_densite)
        self.spinBoxInterceps.valueChanged.connect( self.slot_calcul_densite)
 
        # Calcul du commentaire sur pixel et rayon en unite de carte
        self.radioButtonSAGA.toggled.connect( self.slot_INTRA_rayon_selon_SCR_LIB)
        #self.radioButtonGDAL.toggled.connect( self.slot_INTRA_rayon_selon_SCR_LIB)
        self.radioButtonGPS.toggled.connect( self.slot_INTRA_rayon_selon_SCR_LIB)
        #self.radioButtonL93.toggled.connect( self.slot_INTRA_rayon_selon_SCR_LIB)
      
        # Calcul dynamique des intervale Isolignes
        self.spinBoxIsoMin.valueChanged.connect( self.slot_INTRA_iso_distance)
        self.spinBoxIsoMax.valueChanged.connect( self.slot_INTRA_iso_distance)
        self.spinBoxNombreIso.valueChanged.connect( self.slot_INTRA_iso_distance)
        self.spinBoxDistanceIso.valueChanged.connect( self.slot_INTRA_iso_distance)
        
        # Alerte GPS
        self.radioButtonGPS.toggled.connect( self.slot_GPS_alert)
 
        # Remplissage de la liste de ATTRIBUTS_INTRA 
        self.slot_INTRA_maj_attributs_interpolables( "INIT")
        self.slot_INTRA_maj_triplet_interpolables()
        # la box arret-continue
        self.slot_INTRA_box_arret()

        # Auteurs : Icone
        self.label_jhemmi.setPixmap( QPixmap( os.path.join( REPERTOIRE_HELP, 
            "jhemmi.eu.png")))
        self.label_CIVC.setPixmap( QPixmap( os.path.join( REPERTOIRE_HELP, 
            "CIVC.jpg")))
        
        # Appel à contrib
        self.slot_AIDE_contrib_alert()
        # Contributeurs : Icone
        self.label_IFVV.setPixmap( QPixmap( os.path.join( REPERTOIRE_HELP, 
            "Logo_IFV.png"))) 
        self.label_MHCS.setPixmap( QPixmap( os.path.join( REPERTOIRE_HELP, 
            "Logo_MHCS.png"))) 
        self.label_VCP.setPixmap( QPixmap( os.path.join( REPERTOIRE_HELP, 
            "Logo_VCP.png"))) 
        self.label_TAITTINGER.setPixmap( QPixmap( os.path.join( REPERTOIRE_HELP, 
            "Logo_TAITTINGER.png"))) 
        
        # Init fin 
        return
    
    # ################
    #  Différents SLOT
    # ################

    # FIELDS
    def slot_INTRA_DIAM_min_max_fixe( self ):
        """ Vérifie si min et max du choix fixe DIAM sont cohérents"""
        mon_champ = self.fieldComboIntraDIAM.currentText()
        min_entier = round( float ( self.spinBoxIsoMin_Fixe_DIAM.value()))
        le_max = float ( self.spinBoxIsoMax_Fixe_DIAM.value())      
        max_entier = round( le_max)
        if (min_entier >= max_entier):
            aText = self.tr( "Votre minimum pour {0} ne doit pas être plus grand que votre maximum".\
                format( mon_champ))
            return physiocap_message_box( self, aText, "information")              
        return
    def slot_INTRA_SARM_min_max_fixe( self ):
        """ Vérifie si min et max du choix fixe SARM sont cohérents"""
        mon_champ = self.fieldComboIntraSARM.currentText()
        min_entier = round( float ( self.spinBoxIsoMin_Fixe_SARM.value()))
        le_max = float ( self.spinBoxIsoMax_Fixe_SARM.value())      
        max_entier = round( le_max)
        if (min_entier >= max_entier):
            aText = self.tr( "Votre minimum pour {0} ne doit pas être plus grand que votre maximum".\
                format( mon_champ))
            return physiocap_message_box( self, aText, "information")              
        return
    def slot_INTRA_BIOM_min_max_fixe( self ):
        """ Vérifie si min et max du choix fixe BIOM sont cohérents"""
        mon_champ = self.fieldComboIntraBIOM.currentText()
        min_entier = round( float ( self.spinBoxIsoMin_Fixe_BIOM.value()))
        le_max = float ( self.spinBoxIsoMax_Fixe_BIOM.value())      
        max_entier = round( le_max)
        if (min_entier >= max_entier):
            aText = self.tr( "Votre minimum pour {0} ne doit pas être plus grand que votre maximum".\
                format( mon_champ))
            return physiocap_message_box( self, aText, "information")              
        return
        
    def slot_INTRA_min_max_champ( self ):
        """ Recherche et mise à jour min max de l'attribut ComboIntra dans le vecteur comboPoints"""
        nom_attribut = self.fieldComboIntra.currentText()
        premier_attribut = self.fieldComboIntraDIAM.currentText()
        deuxieme_attribut = self.fieldComboIntraSARM.currentText()
        troisieme_attribut = self.fieldComboIntraBIOM.currentText()
        if nom_attribut == None or premier_attribut == None or deuxieme_attribut == None or \
            troisieme_attribut == None:
            # Evitons les cas initiaux
            return
        if nom_attribut == "" or premier_attribut == "" or deuxieme_attribut == "" or \
            troisieme_attribut == "":
            # Evitons les cas initiaux
            return        

        choix_aide_calcul = self.fieldComboAideIso.currentIndex()
        leModeDeTrace = self.fieldComboModeTrace.currentText()
        # Remettre le bouton intra à enable
        self.ButtonIntra.setEnabled( True)
        
        # Si plusieurs champs à interpoler, pas de calcul de min max 
        # Prendre les min spinBoxIsoMin_Fixe_DIAM et max spinBoxIsoMAX_Fixe_DIAM et 
        # Griser les choix min max
#        nombre_attribut = 0
#        nombre_attribut = nom_attribut.find( SEPARATEUR_NOEUD)
        decoupage = nom_attribut.split( SEPARATEUR_NOEUD)
#        physiocap_log("Attribut pour Intra à découper {0}. longueur {1} . Nombre {2} ".\
#                    format( decoupage,  len( decoupage), nombre_attribut ) , leModeDeTrace)
#        physiocap_log("Choix de calcul indice {0}. fixe  {1} , {2} , {3} ".\
#                    format( choix_aide_calcul,  premier_attribut, deuxieme_attribut,  troisieme_attribut) , leModeDeTrace)
                    
        if len( decoupage) > 2:
            # Cas pour plusieurs interpolations
            if ( choix_aide_calcul != 2):
                physiocap_log("{0} Attribut pour Intra à enchainer {1}. {2} force le choix le la méthode de calcul des isolignes ".\
                    format( PHYSIOCAP_WARNING, decoupage,  PHYSIOCAP_UNI) , TRACE_MIN_MAX)
                self.fieldComboAideIso.setCurrentIndex( 2)   
            else:
                physiocap_log("{0} Trois attributs pour Intra à enchainer {1}.".\
                    format( PHYSIOCAP_INFO, decoupage) , TRACE_MIN_MAX)                
            self.spinBoxIsoMin.setValue( -999999)
            self.spinBoxIsoMax.setValue( int( self.spinBoxIsoMax_Fixe_DIAM.value()))
            self.spinBoxIsoMin.setValue( int( self.spinBoxIsoMin_Fixe_DIAM.value()))
            self.spinBoxDistanceIso.setValue( int( self.spinBoxIsoDistance_Fixe_DIAM.value()))
            self.spinBoxIsoMin.setEnabled( False)
            self.spinBoxIsoMax.setEnabled( False)
            self.spinBoxDistanceIso.setEnabled( False)
            self.spinBoxNombreIso.setEnabled( False)
            self.slot_INTRA_bascule_aide_iso()
            return
        elif ( choix_aide_calcul == 2):
            if nom_attribut == premier_attribut:
                self.spinBoxIsoMin.setValue( -999999)
                self.spinBoxIsoMax.setValue( int( self.spinBoxIsoMax_Fixe_DIAM.value()))
                self.spinBoxIsoMin.setValue( int( self.spinBoxIsoMin_Fixe_DIAM.value()))
                self.spinBoxDistanceIso.setValue( int( self.spinBoxIsoDistance_Fixe_DIAM.value()))
                self.slot_INTRA_bascule_aide_iso()
                return
            elif nom_attribut == deuxieme_attribut:
                self.spinBoxIsoMin.setValue( -999999)
                self.spinBoxIsoMax.setValue( int( self.spinBoxIsoMax_Fixe_SARM.value()))
                self.spinBoxIsoMin.setValue( int( self.spinBoxIsoMin_Fixe_SARM.value()))
                self.spinBoxDistanceIso.setValue( int( self.spinBoxIsoDistance_Fixe_SARM.value()))
                self.slot_INTRA_bascule_aide_iso()
                return
            elif nom_attribut == troisieme_attribut:
                self.spinBoxIsoMin.setValue( -999999)
                self.spinBoxIsoMax.setValue( int( self.spinBoxIsoMax_Fixe_BIOM.value()))
                self.spinBoxIsoMin.setValue( int( self.spinBoxIsoMin_Fixe_BIOM.value()))
                self.spinBoxDistanceIso.setValue( int( self.spinBoxIsoDistance_Fixe_BIOM.value()))
                self.slot_INTRA_bascule_aide_iso()
                return
            else:
                aText = self.tr( "{0} L'attribut {1} n'est pas l'un des trois champs à interpoler dont les choix sont fixés dans l'onglet Affichage. ").\
                format( PHYSIOCAP_WARNING, nom_attribut)
                aText = aText + self.tr( "La méthode d'aide au calcul des isolignes est forcée à \n")
                aText = aText + "\"Nombre d'isolignes permet le calcul de l'écartement des isolignes\""
                self.fieldComboAideIso.setCurrentIndex( 0)   
                physiocap_log( aText , leModeDeTrace)
        else:
            # Cas pour une seul interpolation
#            self.spinBoxIsoMin.setEnabled( True)
#            self.spinBoxIsoMax.setEnabled( True)
            self.slot_INTRA_bascule_aide_iso()

            max_attribut = -99999
            min_attribut = 99999
            #physiocap_log("Attribut pour Intra >{0}".format( nom_attribut) , TRACE_TOOLS)
            nom_complet_point = self.comboBoxPoints.currentText().split( SEPARATEUR_NOEUD)
            if (len( nom_complet_point) !=2):
                return
            #nomProjet = nom_complet_point[0] 
            idLayer   = nom_complet_point[1]
            layer = physiocap_get_layer_by_ID( idLayer)
            if layer is not None:
                try:
                    monProvider = layer.dataProvider()
                    map_champ = monProvider.fieldNameMap()
                    index_attribut =  map_champ[ nom_attribut]
                    # Utilisation du dataProvider maximumValue() et minimumValue()
                    max_attribut = monProvider.maximumValue( index_attribut)
                    min_attribut = monProvider.minimumValue( index_attribut)
                except:
                    physiocap_log_for_error( self)
                    aText = self.tr( "L'attribut {0} n'existe pas dans les données à disposition.").\
                    format( nom_attribut)
                    aText = aText + \
                        self.tr( "Cette interpolation n'est pas possible. Recréer une nouvelle session Physiocap.")
                    physiocap_error( self, aText, "CRITICAL")
                    return physiocap_message_box( self, aText, "information")
                
                monProvider = None
                physiocap_log("Min et max de > {0} < sont {1} =~= {2}". \
                    format( nom_attribut, min_attribut,  max_attribut) , TRACE_MIN_MAX)
                self.spinBoxIsoMin.setValue( -9999999)
                self.spinBoxIsoMax.setValue( int( max_attribut ))
                self.spinBoxIsoMin.setValue( int( min_attribut ))

    def slot_INTER_change_champ_choisi( self ):
        """ Synchronise les 2 combox"""
        position_choix = self.fieldComboContours.currentIndex()
        self.fieldPbGdal.setCurrentIndex( position_choix)                              
   
    def slot_INTER_maj_champ_poly_liste( self ):
        """ Create a list of fields having unique values for the current vector in fieldCombo Box"""
        leModeDeTrace = self.fieldComboModeTrace.currentText()
        nom_complet_poly = self.comboBoxPolygone.currentText().split( SEPARATEUR_NOEUD)
        inputLayer = nom_complet_poly[0] 

        self.fieldComboContours.clear()
        self.fieldPbGdal.clear()
        #physiocap_log( "Dans recherche de champ : layer >> {0}<<". \
        #   format ( inputLayer), leModeDeTrace)

        layer = physiocap_get_layer_by_name( inputLayer)
        # Initialisation avec CHAMP_NOM_PHY = NOM_PHY
        self.fieldPbGdal.addItem( "NO" )                                
        self.fieldComboContours.addItem( CHAMP_NOM_PHY)
        self.fieldComboContours.setCurrentIndex( 0)
        if layer is not None:
            # On exclut les layer qui ne sont pas de type 0 (exemple 1 raster)
            if ( layer.type() == 0):
                position_combo = 1 # Demarre à 1 car NOM_PHY est dejà ajouté
                dernierAttribut = self.settings.value("Physiocap/attributPoly", "xx")
                mon_provider = layer.dataProvider()
                nombre_ligne = mon_provider.featureCount()
                map_champ = mon_provider.fieldNameMap()
                for mon_champ in mon_provider.fields():
                    nom_champ = mon_champ.name()
                    liste_valeurs = mon_provider.uniqueValues( map_champ[ nom_champ])

                    if leModeDeTrace == TRACE_PAS:
                        # Raccourci si aucun trace, on suppose toutes les valeurs sont uniques
                        valeur_unique = "YES" 
                    else:
                        # Vérifier si les valeurs du field name sont toutes uniques
    #                    physiocap_log( "Unique : field >> {0} \n {1}<<". \
    #                        format ( nom_champ,  liste_valeurs), leModeDeTrace)
                        if nombre_ligne == len( liste_valeurs):
                            valeur_unique = "YES" 
                        else:
#                            physiocap_log( "Dans recherche de champ : field >> {0} nombre {1} mais possible {2}". \
#                            format ( nom_champ,  len( liste_valeurs),  nombre_ligne), leModeDeTrace)
                            valeur_unique = "NO" 
                            
                    # ne pas remettre NOM_PHY une deuxieme fois
                    if valeur_unique == "YES" and nom_champ != CHAMP_NOM_PHY:
                        valeur_pb_GDAL = "NO"
                        for val in liste_valeurs:
                            if physiocap_nom_entite_avec_pb_caractere( val):
                                valeur_pb_GDAL = "YES"
                                break                        
                        self.fieldPbGdal.addItem( valeur_pb_GDAL )                                
                        self.fieldComboContours.addItem( nom_champ )
                        if ( nom_champ == dernierAttribut):
                            self.fieldComboContours.setCurrentIndex( position_combo)
                            self.fieldPbGdal.setCurrentIndex( position_combo)                              
                        position_combo = position_combo + 1
  
                liste_valeurs={}
                mon_provider = None
        else:
            physiocap_log( "Dans recherche des champs uniques : aucun layer", leModeDeTrace)            
                    
    def slot_INTER_INTRA_maj_points_choix( self ):
        """ Verify whether the value autorize Inter or Intra"""
        nom_complet_point = self.comboBoxPoints.currentText().split( SEPARATEUR_NOEUD)
        if ( len( nom_complet_point) != 2):
            return
            
        version_3 = "NO"
        if self.checkBoxV3.isChecked():
            version_3 = "YES"
        
        #projet = nom_complet_point[0]
        # Chercher dans arbre si la session Inter existe
        diametre = nom_complet_point[1] 
        layer = physiocap_get_layer_by_ID( diametre)
        if layer is not None:
            # Avec le diametre, on trouve le repertoire
            pro = layer.dataProvider()
            chemin_shapes = "chemin vers shapeFile"
            if pro.name() != POSTGRES_NOM:
                chemin_shapes = os.path.dirname( pro.dataSourceUri())  ;
                chemin_projet = os.path.dirname(chemin_shapes)  ;
                nom_shape = os.path.basename( pro.dataSourceUri())  ;
                if ( not os.path.exists( chemin_shapes)):
                    raise physiocap_exception_rep( "chemin vers shapeFile")

                consolidation = "NO"
                if self.checkBoxConsolidation.isChecked():
                    consolidation = "YES"                
                if (consolidation == "YES"):
                    pos_extension = nom_shape.rfind(".")
                    nom_shape_sans_ext = nom_shape[:pos_extension]
                    chemin_shape_et_nom = os.path.join( chemin_shapes, nom_shape_sans_ext)            
                    chemin_inter = os.path.join( chemin_shape_et_nom, VIGNETTES_INTER)
                else:
                    if version_3 == "NO":
                        chemin_inter = os.path.join( chemin_shapes, VIGNETTES_INTER)
                    else:
                        chemin_inter = os.path.join( chemin_projet, REPERTOIRE_INTER_V3)
                if (os.path.exists( chemin_inter)):
                    # On aiguille vers Intra
                    self.groupBoxIntra.setEnabled( True)
                    self.groupBoxArret.setEnabled( True)
                    self.groupBoxMethode.setEnabled( True)
                    self.ButtonIntra.setEnabled( True)
                    self.ButtonInter.setEnabled( False)

                else:
                    # On aiguille vers Inter
                    self.groupBoxIntra.setEnabled( False)
                    self.groupBoxArret.setEnabled( False)
                    self.groupBoxMethode.setEnabled( False)
                    self.ButtonIntra.setEnabled( False)
                    self.ButtonInter.setEnabled( True)
                              
    # Repertoire données brutes :
    def slot_lecture_repertoire_donnees_brutes( self):
        """Catch directory for raw data"""
        # Récuperer dans setting le nom du dernier ou sinon REPERTOIRE_DONNEES_BRUTES
        self.settings= QSettings(PHYSIOCAP_NOM, PHYSIOCAP_NOM_3)
        exampleDirName =  self.settings.value("Physiocap/repertoire", REPERTOIRE_DONNEES_BRUTES)
        
        dirName = QFileDialog.getExistingDirectory( self, self.tr("Choisir le répertoire de vos données Physiocap brutes (MID)"),
                                                 exampleDirName,
                                                 QFileDialog.ShowDirsOnly
                                                 | QFileDialog.DontResolveSymlinks);
        if len( dirName) == 0:
          return
        self.lineEditDirectoryPhysiocap.setText( dirName )
        
     # Repertoire données brutes :
    def slot_lecture_repertoire_donnees_cibles( self):
        """Catch directory for new filtered data"""
        # Récuperer dans setting le nom du dernier ou sinon REPERTOIRE_DONNEES_BRUTES
        self.settings= QSettings(PHYSIOCAP_NOM, PHYSIOCAP_NOM_3)
        exampleDirName =  self.settings.value("Physiocap/cible_repertoire", "Vide")
        # Cas vraiment inital
        if exampleDirName == "Vide":
            exampleDirName =  self.settings.value("Physiocap/repertoire", REPERTOIRE_DONNEES_BRUTES)
            
        dirName = QFileDialog.getExistingDirectory( self, self.tr("Choisir le répertoire qui contiendra les résultats les données filtrées par Physiocap"),
                                                 exampleDirName,
                                                 QFileDialog.ShowDirsOnly
                                                 | QFileDialog.DontResolveSymlinks);
        if len( dirName) == 0:
          return
        self.lineEditDirectoryFiltre.setText( dirName )
 
    def slot_INTER_liste_parcelles( self):
        """ Rafraichit les listes avant le calcul inter parcelles"""
        nombre_poly = 0
        nombre_point = 0
        nombre_poly, nombre_point = physiocap_fill_combo_poly_or_point( self)

        if ( nombre_poly > 0):
            # A_TESTER: si utile fin inter self.slot_min_max_champ_intra()
            self.slot_INTER_maj_champ_poly_liste()
        if (( nombre_poly > 0) and ( nombre_point > 0)):
            # Liberer le bouton "moyenne"
            self.groupBoxInter.setEnabled( True)
        else:
            self.groupBoxInter.setEnabled( False)
        
        # Mise à jour du commentaire pour le rayon
        self.slot_INTRA_rayon_selon_SCR_LIB()
        
#    def slot_INTRA_maj_interpolable( self):
#        """ Recherche à chaud à mattre à jour le triplet"""
#        #aText = self.tr( "{0} vous demande de fermer l'extension et quitter QGIS pour prendre en compte le changement").\
#        aText = self.tr( "{0} changement box interpolation").\
#            format( PHYSIOCAP_UNI)
#        aText = aText + self.tr( " d'attibut fixe")
#        physiocap_message_box( self, aText, "information")
#        self.slot_INTRA_maj_attributs_interpolables( "DYNAMIQUE")
#        
    def slot_AIDE_contrib_alert( self):
        """ 
        Toute les x utilisations, rappeler à l'utilisateur qu'il est bien de contribuer
        """
        # Vérifier si le nombre d'utilisation est atteint
        self.settings= QSettings( PHYSIOCAP_NOM, PHYSIOCAP_NOM_3)
        niveau_utilisation = int( self.settings.value("Affichage/Contrib_alert", 0))
        if ( niveau_utilisation <  500):
            self.settings.setValue("Affichage/Contrib_alert", \
                niveau_utilisation + 1)
            return 
        
        aText = self.tr( "{0} vous rapelle que ce logiciel ouvert et libre n'est pas exempt de besoins. ").\
                    format( PHYSIOCAP_UNI)
        aText = aText + self.tr( "L'extension est diffusée gratuitement par le biais de la distribution ")
        aText = aText + self.tr( "QGIS pour vous faciliter son utilisation. Ce choix est lié à la grande importance ")
        aText = aText + self.tr( "de rester maître de ses données. L'extension a besoin de votre aide. ")
        aText = aText + self.tr( "Contribuez simplement à la hauteur du service rendu. ")
        aText = aText + self.tr( 'Trois clics : Onglet "A Propos" puis bouton "Contribuer" et passez par votre navigateur')
        # Mémoriser que le message a été donné
        self.settings.setValue("Affichage/Contrib_alert", 0)
        return physiocap_message_box( self, aText, "information")
    
    def slot_GPS_alert( self):
        """ 
        Quand GPS est choisi, on monte une alerte
        """
        # Vérifier si le message a déjà été donné
        self.settings= QSettings( PHYSIOCAP_NOM, PHYSIOCAP_NOM_3)
        if (self.settings.value("Affichage/GPSalertIntra", "NO") == "YES"):
            return
            
        #physiocap_message_box( self, "Dans slot_GPS_alert", "information")   
        aText = self.tr( "{0} ne conseille le choix GPS si vous souhaitez réaliser").\
                    format( PHYSIOCAP_UNI)
        aText = aText + self.tr( "une interpolatioin INTRA parcellaire. ")
        aText = aText + self.tr( "Il n'est pas conseillé d'interpoler dans un systeme non plan. ")
        aText = aText + self.tr( "En effet, selon votre lattitude, l'unite des coordonnées X et Y ")
        aText = aText + self.tr( "peuvent varier. L'interpolation basée sur l'inverse des distances ")
        aText = aText + self.tr( "pourra donc être déformée par rapport à un calcul dans un systeme ")
        aText = aText + self.tr( "plan (comme L93).")
        # Mémoriser que le message a été donné
        self.settings.setValue("Affichage/GPSalertIntra", "YES")
        
        return physiocap_message_box( self, aText, "information")
            
    def slot_INTRA_rayon_selon_SCR_LIB( self):
        """ 
        Selon GPS ou L93 et SAGA ou GDAL mise en place du commentaire pour le
        rayon en unite de carte
        """
        # retrouve sans QT
        #physiocap_message_box( self, "Dans slot Rayon", "information")   
        self.lineEditDoubleRayon.setText( "Etrange et bizarre")
                
        self.spinBoxDoubleRayon.setEnabled( True)
        
        if self.radioButtonSAGA.isChecked():
            self.spinBoxPixel.setEnabled( True)
            self.spinBoxMultiplieRayon.setEnabled( False)
            if self.radioButtonL93.isChecked():
                aText = self.tr( "{0} conseille un rayon d'interpolation entre 5 et 15").\
                    format( PHYSIOCAP_UNI)
                self.lineEditDoubleRayon.setText( aText)
            if self.radioButtonGPS.isChecked():
                aText = self.tr( "{0} conseille un rayon d'interpolation proche de 0.000085 (8.85E-5)").\
                    format( PHYSIOCAP_UNI)
                self.lineEditDoubleRayon.setText( aText)
                
        if self.radioButtonGDAL.isChecked():
            self.spinBoxPixel.setEnabled( False)
            self.spinBoxMultiplieRayon.setEnabled( True)
            if self.radioButtonL93.isChecked():
                # Proposer un texte
                aText = self.tr( "{0} conseille un rayon d'interpolation proche de 5").\
                    format( PHYSIOCAP_UNI)
                self.lineEditDoubleRayon.setText( aText)
            if self.radioButtonGPS.isChecked():
                # Proposer un texte
                aText = self.tr( "{0} conseille un rayon d'interpolation proche de 0.00015 (1.5E-4)").\
                    format( PHYSIOCAP_UNI)
                self.lineEditDoubleRayon.setText( aText)

        return 0
    
    def slot_INTRA_bascule_aide_iso( self):
        """ 
        Bascule le mode d'aide du calcul iso 
        """
        if ( self.fieldComboAideIso.currentIndex() == 0):
            self.spinBoxIsoMin.setEnabled( True)
            self.spinBoxIsoMax.setEnabled( True)
            self.spinBoxDistanceIso.setEnabled( False)
            self.spinBoxNombreIso.setEnabled( True)
            self.slot_INTRA_iso_distance()
        if ( self.fieldComboAideIso.currentIndex() == 1):
            self.spinBoxIsoMin.setEnabled( True)
            self.spinBoxIsoMax.setEnabled( True)
            self.spinBoxDistanceIso.setEnabled( True)
            self.spinBoxNombreIso.setEnabled( False)        
            self.slot_INTRA_iso_distance()
        if ( self.fieldComboAideIso.currentIndex() == 2):
            self.spinBoxIsoMin.setEnabled( False)
            self.spinBoxIsoMax.setEnabled( False)
            self.spinBoxDistanceIso.setEnabled( False)
            self.spinBoxNombreIso.setEnabled( False)
        return
        
#    def OLD_INTRA_maj_attributs_interpolables( self, MAJ_TRIPLET = "NO"):
#        """ Créer la liste des attributs interpolable
#        Cette liste provient de ATTRIBUTS_INTRA et si details ATTRIBUTS_INTRA_DETAILS
#        mais aussi du choix dans préférence affichage (le triplet d'interpolation fixé)
#        SI MAJ_TRIPLET est à YES, on crée en même temps la liste des attributs possible dans pour le choix du triplet
#        qui se nomme DIAM puis SARM puis BIOM mais peut contenir n'importe quelle valeur
#        """
#        ATTR_LISTE=[]
#        ATTR_LISTE_TRIPLET=[]
#
#        if (len( ATTRIBUTS_INTRA) == 0) and  MAJ_TRIPLET == "YES":
#            self.fieldComboIntra.clear()
#            self.fieldComboIntraDIAM.clear()
#            self.fieldComboIntraSARM.clear()
#            self.fieldComboIntraBIOM.clear()
#            physiocap_error( self, self.tr( "Pas de liste des attributs pour Intra pré défini"))
#            return
#        
#        if MAJ_TRIPLET == "DYNAMIQUE":
#            leChoixDiam = self.fieldComboIntraDIAM.currentText()
#            leChoixSarm = self.fieldComboIntraSARM.currentText()
#            leChoixBiom = self.fieldComboIntraBIOM.currentText()
#            leChoixIntra = self.fieldComboIntra.currentText()
#        else:
#            # Récupérer les choix dans settings 
#            leChoixDiam = self.settings.value("Physiocap/attributIntraFixe_1", "x1")
#            leChoixSarm = self.settings.value("Physiocap/attributIntraFixe_2", "x2")
#            leChoixBiom = self.settings.value("Physiocap/attributIntraFixe_3", "x3")
#            # Retrouver les choix intra précedent (dans intra ou dans préference)
#            leChoixIntra = self.settings.value("Physiocap/attributIntra", "xx") 
#        # Ajout des trois entités choisies dans affichage intra
#        if ( leChoixDiam != "x1" or leChoixSarm != "x2" or leChoixBiom != "x3"):
#            attribut_triple = leChoixDiam + SEPARATEUR_NOEUD + leChoixSarm + \
#                    SEPARATEUR_NOEUD + leChoixBiom
#            ATTR_LISTE.append( attribut_triple)
#
#        # Ajout des attributs standard 
#        ATTR_LISTE = ATTR_LISTE + ATTRIBUTS_INTRA
#        ATTR_LISTE_TRIPLET = ATTRIBUTS_INTRA
#
#        if self.checkBoxV3.isChecked() and ( self.settings.value("Physiocap/expert", "As-tu contribué ?") == MODE_EXPERT):     
#            # Ajout d'un nouvelle liste d'attribut interpolable
#            ATTR_LISTE = ATTR_LISTE + ATTRIBUTS_V3_INTRA
#            ATTR_LISTE_TRIPLET = ATTR_LISTE_TRIPLET + ATTRIBUTS_V3_INTRA
#        
#        # Cas de details ATTRIBUTS_INTRA_DETAIL
#        if (self.settings.value("Physiocap/details") == "YES"):
#            ATTR_LISTE = ATTR_LISTE + ATTRIBUTS_INTRA_DETAILS
#            ATTR_LISTE_TRIPLET = ATTR_LISTE_TRIPLET + ATTRIBUTS_INTRA_DETAILS
#
#        
#        physiocap_log( self.tr( "Liste des attributs pour Intra {0}".format( ATTR_LISTE)))
#            
#        self.fieldComboIntra.clear()
#        self.fieldComboIntra.addItems( ATTR_LISTE)
#        physiocap_log( self.tr( "apres de liste des attributs pour Intra {0}".format( ATTR_LISTE_TRIPLET)))
#        if MAJ_TRIPLET == "YES":
#            self.fieldComboIntraDIAM.clear()
#            self.fieldComboIntraDIAM.addItems( ATTR_LISTE_TRIPLET)
#            self.fieldComboIntraSARM.clear()
#            self.fieldComboIntraSARM.addItems( ATTR_LISTE_TRIPLET)
#            self.fieldComboIntraBIOM.clear()
#            self.fieldComboIntraBIOM.addItems( ATTR_LISTE_TRIPLET)
#            self.fieldComboIntraDIAM.setCurrentIndex( 0)   
#            self.fieldComboIntraSARM.setCurrentIndex( 1)   
#            self.fieldComboIntraBIOM.setCurrentIndex( 2) 
#
#        # Ne pas rester à 0 dans le premier cas
#        if len( ATTR_LISTE) > 1:
#            self.fieldComboIntra.setCurrentIndex( 1)
#        # Se souvenir du choix inital
#        j=0
#        for monAttribut in ATTR_LISTE:
#            if ( monAttribut == leChoixIntra):
#                self.fieldComboIntra.setCurrentIndex( j)
#            j = j+1
#            
#        if MAJ_TRIPLET == "YES":
#            i=0
#            for monAttribut in ATTR_LISTE_TRIPLET:        
#                if ( monAttribut == leChoixDiam):
#                    self.fieldComboIntraDIAM.setCurrentIndex( i)
#                if ( monAttribut == leChoixSarm):
#                    self.fieldComboIntraSARM.setCurrentIndex( i)
#                if ( monAttribut == leChoixBiom):
#                    self.fieldComboIntraBIOM.setCurrentIndex( i)
#                i=i+1
#            
#        if self.checkBoxV3.isChecked():
#            self.groupBoxArret.setEnabled( True)
#            if (self.settings.value("Physiocap/groupStop", "YES") == "YES"):
#                self.checkBoxArret.setChecked( Qt.Checked)
#            else:
#                self.checkBoxArret.setChecked( Qt.Unchecked)
#            self.fieldComboIntraContinue.clear()
#            self.fieldComboIntraContinue.addItems( ATTR_CONTINUE)        
#            k=0
#            idx = 0
#            LeChoixContinue = self.fieldComboIntraContinue.currentText()
#            for monChoix in ATTR_CONTINUE:        
#                if ( monChoix == LeChoixContinue):
#                    self.fieldComboIntraContinue.setCurrentIndex( k)
#                    idx = k
#                k = k+1
#            self.settings.setValue("Physiocap/continueIntra", idx)
#        else:
#            self.groupBoxArret.setEnabled( False)
#            self.checkBoxArret.setChecked( Qt.Checked)
#            self.settings.setValue("Physiocap/groupStop", "YES")
#            self.fieldComboIntraContinue.clear()
#            self.fieldComboIntraContinue.addItems( ATTR_CONTINUE)        
#            self.fieldComboIntraContinue.setCurrentIndex( 0)
#            self.settings.setValue("Physiocap/continueIntra", 0)
#
#        return

    def slot_INTRA_maj_attributs_interpolables( self,  ORIGINE_TRIPLET):
        """ Créer la liste des attributs interpolable
        Cette liste provient de ATTRIBUTS_INTRA et si details ATTRIBUTS_INTRA_DETAILS et gere le cas V3"""
        leModeDeTrace = self.fieldComboModeTrace.currentText()
        ATTR_LISTE=[]

        if (len( ATTRIBUTS_INTRA) == 0):
            self.fieldComboIntra.clear()
            physiocap_error( self, self.tr( "Pas de liste des attributs pour Intra pré défini"))
            return
        
        if ORIGINE_TRIPLET == "INIT":
            # Récupérer les choix dans settings pour le cas initalial
            leChoixDiam = self.settings.value("Physiocap/attributIntraFixe_1", "x1")
            leChoixSarm = self.settings.value("Physiocap/attributIntraFixe_2", "x2")
            leChoixBiom = self.settings.value("Physiocap/attributIntraFixe_3", "x3")
            # Retrouver les choix intra précedent (dans intra ou dans préference)        
            leChoixIntra = self.settings.value("Physiocap/attributIntra", "xx") 
        else:    # pour les autres cas dont le slot lors d'un changement dans le triplet
            leChoixDiam = self.fieldComboIntraDIAM.currentText()
            leChoixSarm = self.fieldComboIntraSARM.currentText()
            leChoixBiom = self.fieldComboIntraBIOM.currentText()
            leChoixIntra = self.fieldComboIntra.currentText()
        # Ajout des trois entités choisies dans affichage intra
        if ( leChoixDiam != "x1" or leChoixSarm != "x2" or leChoixBiom != "x3"):
            attribut_triple = leChoixDiam + SEPARATEUR_NOEUD + leChoixSarm + \
                    SEPARATEUR_NOEUD + leChoixBiom
            ATTR_LISTE.append( attribut_triple)

        # Ajout des attributs standard 
        ATTR_LISTE = ATTR_LISTE + ATTRIBUTS_INTRA

        if self.checkBoxV3.isChecked() and ( self.settings.value("Physiocap/expert", "As-tu contribué ?") == MODE_EXPERT):     
            # Ajout d'un nouvelle liste d'attribut interpolable
            ATTR_LISTE = ATTR_LISTE + ATTRIBUTS_V3_INTRA
        
        # Cas de details ATTRIBUTS_INTRA_DETAIL
        if self.checkBoxInfoVignoble.isChecked():
            ATTR_LISTE = ATTR_LISTE + ATTRIBUTS_INTRA_DETAILS

        self.fieldComboIntra.clear()
        self.fieldComboIntra.addItems( ATTR_LISTE)

        # Ne pas rester à 0 dans le premier cas
        if len( ATTR_LISTE) > 1:
            self.fieldComboIntra.setCurrentIndex( 1)
        # Se souvenir du choix inital
        j=0
        for monAttribut in ATTR_LISTE:
            if ( monAttribut == leChoixIntra):
                self.fieldComboIntra.setCurrentIndex( j)
            j = j+1
        
        self.fieldPbGdal.setEnabled( False)
        return
        
    def slot_INTRA_box_arret( self):
        """ Initialise la box arret / continue"""

        if self.checkBoxV3.isChecked():
            self.groupBoxArret.setEnabled( True)
            if (self.settings.value("Physiocap/groupStop", "YES") == "YES"):
                self.checkBoxArret.setChecked( Qt.Checked)
            else:
                self.checkBoxArret.setChecked( Qt.Unchecked)
            self.fieldComboIntraContinue.clear()
            self.fieldComboIntraContinue.addItems( ATTR_CONTINUE)        
            k=0
            idx = 0
            LeChoixContinue = self.fieldComboIntraContinue.currentText()
            for monChoix in ATTR_CONTINUE:        
                if ( monChoix == LeChoixContinue):
                    self.fieldComboIntraContinue.setCurrentIndex( k)
                    idx = k
                k = k+1
            self.settings.setValue("Physiocap/continueIntra", idx)
        else:
            self.groupBoxArret.setEnabled( False)
            self.checkBoxArret.setChecked( Qt.Checked)
            self.settings.setValue("Physiocap/groupStop", "YES")
            self.fieldComboIntraContinue.clear()
            self.fieldComboIntraContinue.addItems( ATTR_CONTINUE)        
            self.fieldComboIntraContinue.setCurrentIndex( 0)
            self.settings.setValue("Physiocap/continueIntra", 0)

        return

        
    def slot_INTRA_maj_triplet_interpolables( self):
        """ Créer la liste du triplet d'attributs interpolable
        on cherche dans settings et la liste des attributs possible dans pour le choix du triplet
        qui se nomme DIAM puis SARM puis BIOM mais peut contenir n'importe quelle valeur
        """
        ATTR_LISTE_TRIPLET=[]

        if (len( ATTRIBUTS_INTRA) == 0):
            self.fieldComboIntraDIAM.clear()
            self.fieldComboIntraSARM.clear()
            self.fieldComboIntraBIOM.clear()
            physiocap_error( self, self.tr( "Pas de liste des attributs pour Intra pré défini"))
            return
        
        # Récupérer les choix dans settings 
        leChoixDiam = self.settings.value("Physiocap/attributIntraFixe_1", "x1")
        leChoixSarm = self.settings.value("Physiocap/attributIntraFixe_2", "x2")
        leChoixBiom = self.settings.value("Physiocap/attributIntraFixe_3", "x3")

        # Ajout des attributs standard 
        ATTR_LISTE_TRIPLET = ATTRIBUTS_INTRA

        if self.checkBoxV3.isChecked() and ( self.settings.value("Physiocap/expert", "As-tu contribué ?") == MODE_EXPERT):     
            # Ajout d'un nouvelle liste d'attribut interpolable
            ATTR_LISTE_TRIPLET = ATTR_LISTE_TRIPLET + ATTRIBUTS_V3_INTRA
        
        # Cas de details ATTRIBUTS_INTRA_DETAIL
        if self.checkBoxInfoVignoble.isChecked():
            ATTR_LISTE_TRIPLET = ATTR_LISTE_TRIPLET + ATTRIBUTS_INTRA_DETAILS
            
        self.fieldComboIntraDIAM.clear()
        self.fieldComboIntraDIAM.addItems( ATTR_LISTE_TRIPLET)
        self.fieldComboIntraSARM.clear()
        self.fieldComboIntraSARM.addItems( ATTR_LISTE_TRIPLET)
        self.fieldComboIntraBIOM.clear()
        self.fieldComboIntraBIOM.addItems( ATTR_LISTE_TRIPLET)
        self.fieldComboIntraDIAM.setCurrentIndex( 0)   
        self.fieldComboIntraSARM.setCurrentIndex( 1)   
        self.fieldComboIntraBIOM.setCurrentIndex( 2) 

        i=0
        for monAttribut in ATTR_LISTE_TRIPLET:        
            if ( monAttribut == leChoixDiam):
                self.fieldComboIntraDIAM.setCurrentIndex( i)
            if ( monAttribut == leChoixSarm):
                self.fieldComboIntraSARM.setCurrentIndex( i)
            if ( monAttribut == leChoixBiom):
                self.fieldComboIntraBIOM.setCurrentIndex( i)
            i=i+1
            
        return

    def slot_INTRA_iso_distance( self):
        """ 
        Recherche du la distance optimale tenant compte de min et max et du nombre d'intervalle
        """
        # retrouve sans QT
        #leModeDeTrace = self.fieldComboModeTrace.currentText()
        min_entier = round( float ( self.spinBoxIsoMin.value()))
        le_max = float ( self.spinBoxIsoMax.value())      
        max_entier = round( le_max)

        if (min_entier >= max_entier):
            aText = self.tr( "Votre minimum ne doit pas être plus grand que votre maximum")
            return physiocap_message_box( self, aText, "information")              
        
        if (max_entier < le_max):
            max_entier = max_entier +1

        if (min_entier >= max_entier):
            # forcer le nombre d'intervalle à 1
            self.spinBoxDistanceIso.setValue( 1)
            return 
        
        choix_aide_calcul = self.fieldComboAideIso.currentIndex()
            
#        physiocap_log( "CAS aide ISO : {0} ".format( choix_aide_calcul), leModeDeTrace)
# 
        if ( choix_aide_calcul == 0):
            # du nombre d'iso on déduit l'écart
            nombre_iso = round( float ( self.spinBoxNombreIso.value())) 
            distance = max_entier - min_entier
            ecart_intervalle = int( distance / ( nombre_iso + 1))
            if ecart_intervalle < 1:
                ecart_intervalle = 1
            if ecart_intervalle >max_entier:
                ecart_intervalle = max_entier
                
##            physiocap_log( "CAS nb ISO : Ecart d'un intervalle : " + str(ecart_intervalle) + " min =" + \
##                str( min_entier) + " max =" + str( max_entier) + " nombre iso =" + str( nombre_iso), leModeDeTrace)
            self.spinBoxDistanceIso.setValue( ecart_intervalle)
            return
        if ( choix_aide_calcul == 1) or ( choix_aide_calcul == 2):
            # de l'écart entre iso on deduit nombre d'iso
            ecart_intervalle = round( float ( self.spinBoxDistanceIso.value()))
            distance = max_entier - min_entier
            if ecart_intervalle > distance:
                ecart_intervalle = distance
                self.spinBoxDistanceIso.setValue( ecart_intervalle)
            nombre_iso = int( distance /  ecart_intervalle)
            if nombre_iso < 1:
                nombre_iso = 1
                
#            physiocap_log( "CAS ECART : Ecart d'un intervalle : " + str(ecart_intervalle) + " min =" + \
#                str( min_entier) + " max =" + str( max_entier) + " nombre iso =" + str( nombre_iso), leModeDeTrace)
            self.spinBoxNombreIso.setValue( nombre_iso)                    
            return
               
        return
        
    def memoriser_expert(self):
        """ Mémoriser les choix d'expert """        
        # THEMATIQUES
        self.settings.setValue("Physiocap/leDirThematiques", self.fieldComboThematiques.currentText())
        self.settings.setValue("Physiocap/leChoixDeThematiques", self.fieldComboThematiques.currentIndex())

        self.settings.setValue("Physiocap/leModeTrace", self.fieldComboModeTrace.currentText())
        
        # Cas détail segment
        self.settings.setValue("Physiocap/vitesse_mini_segment", float( self.doubleSpinBoxVitesseMiniSegment.value()))        
        self.settings.setValue("Physiocap/vitesse_maxi_segment", float( self.doubleSpinBoxVitesseMaxiSegment.value()))        
        self.settings.setValue("Physiocap/nombre_mini_points", int( self.spinBoxNombreMiniPointsConsecutifs.value()))
        self.settings.setValue("Physiocap/derive_max_segment", int( self.spinBoxDeriveMaxSegment.value()))
        self.settings.setValue("Physiocap/pas_de_la_derive", int( self.spinBoxPasDeDerive.value()))
        self.settings.setValue("Physiocap/pdop_max_segment", float( self.doubleSpinBoxPdopMaxSegment.value()))

    
    def memoriser_affichages(self):
        """ Mémoriser les choix d'affichage """        
        # Sauver les affichages cas généraux
        diametre = "NO"
        if self.checkBoxDiametre.isChecked():
            diametre = "YES"
        self.settings.setValue("Affichage/FiltrerDiametre", diametre )
        sarment = "NO"
        if self.checkBoxSarment.isChecked():
            sarment = "YES"
        self.settings.setValue("Affichage/FiltrerSarment", sarment )
        biomasse = "NO"
        if self.checkBoxBiomasse.isChecked():
            biomasse = "YES"
        self.settings.setValue("Affichage/FiltrerBiomasse", biomasse )
        vitesse = "NO"
        if self.checkBoxVitesse.isChecked():
            vitesse = "YES"
        self.settings.setValue("Affichage/FiltrerVitesse", vitesse )
        pas_mesure = "NO"
        if self.checkBoxPasMesure.isChecked():
            pas_mesure = "YES"
        self.settings.setValue("Affichage/FiltrerPasMesure", pas_mesure )
        filtre_segment = "NO"
        if self.checkBoxSegment.isChecked():
            filtre_segment = "YES"
        self.settings.setValue("Affichage/FiltrerSegment", filtre_segment )
        filtre_segment_brise = "NO"
        if self.checkBoxSegmentBrise.isChecked():
            filtre_segment_brise = "YES"
        self.settings.setValue("Affichage/FiltrerSegmentBrise", filtre_segment_brise )
        
        self.settings.setValue("Physiocap/leFormat", self.fieldComboFormats.currentText())
        #self.settings.setValue("Physiocap/leChoixShapeDiametre", self.fieldComboShapeDiametre.currentIndex())
        self.settings.setValue("Physiocap/leChoixShapeSarment", self.fieldComboShapeSarment.currentIndex())
        self.settings.setValue("Physiocap/leChoixShapeBiomasse", self.fieldComboShapeBiomasse.currentIndex())
        self.settings.setValue("Physiocap/leChoixShapeVitesse", self.fieldComboShapeVitesse.currentIndex())
        

        # Filtrage
        self.settings.setValue("Physiocap/themeDiametre", self.lineEditThematiqueDiametre.text())
        self.settings.setValue("Physiocap/themeSarment", self.lineEditThematiqueSarment.text())
        self.settings.setValue("Physiocap/themeBiomasse",self.lineEditThematiqueBiomasse.text())
        self.settings.setValue("Physiocap/themeVitesse", self.lineEditThematiqueVitesse.text())
        self.settings.setValue("Physiocap/themePasMesure", self.lineEditThematiquePasMesure.text())
        self.settings.setValue("Physiocap/themeSegment", self.lineEditThematiqueSegment.text())
        self.settings.setValue("Physiocap/themeSegmentBrise", self.lineEditThematiqueSegmentBrise.text())
        # Inter
        self.settings.setValue("Physiocap/themeInterDiametre", self.lineEditThematiqueInterDiametre.text())
        self.settings.setValue("Physiocap/themeInterSarment", self.lineEditThematiqueInterSarment.text())
        self.settings.setValue("Physiocap/themeInterBiomasse", self.lineEditThematiqueInterBiomasse.text())
        self.settings.setValue("Physiocap/themeInterAltitude", self.lineEditThematiqueInterAltitude.text())
        # inter moyenne et points
        self.settings.setValue("Physiocap/themeInterLibelle", self.lineEditThematiqueInterLibelle.text())
        self.settings.setValue("Physiocap/themeInterMoyenne", self.lineEditThematiqueInterMoyenne.text())
        self.settings.setValue("Physiocap/themeInterPoints", self.lineEditThematiqueInterPoints.text())
        self.settings.setValue("Physiocap/themeInterPasMesure", self.lineEditThematiqueInterPasMesure.text())
        self.settings.setValue("Physiocap/themeInterSegment", self.lineEditThematiqueInterSegment.text())
        self.settings.setValue("Physiocap/themeInterSegmentBrise", self.lineEditThematiqueInterSegmentBrise.text())
        # intra
        self.settings.setValue("Physiocap/themeIntraIso", self.lineEditThematiqueIntraIso.text())
        self.settings.setValue("Physiocap/themeIntraImage", self.lineEditThematiqueIntraImage.text())

    def memoriser_saisies_inter_intra_parcelles(self):
        """ Mémorise les saisies inter et intra """

        # Memorisation des saisies
        self.settings= QSettings( PHYSIOCAP_NOM, PHYSIOCAP_NOM_3)
        self.settings.setValue("Physiocap/interPoint", self.comboBoxPoints.currentText() )
        self.settings.setValue("Physiocap/interPoly", self.comboBoxPolygone.currentText() )
        self.settings.setValue("Physiocap/attributPoly", self.fieldComboContours.currentText())
        self.settings.setValue("Physiocap/attributpbGDAL", self.fieldPbGdal.currentText())

        self.settings.setValue("Physiocap/attributIntra", self.fieldComboIntra.currentText())
        self.settings.setValue("Physiocap/continueIntra", self.fieldComboIntraContinue.currentIndex())
        self.settings.setValue("Physiocap/powerIntra", float( self.spinBoxPower.value()))
        self.settings.setValue("Physiocap/rayonIntra", float( self.spinBoxDoubleRayon.value()))
        self.settings.setValue("Physiocap/pixelIntra", float( self.spinBoxPixel.value()))
        self.settings.setValue("Physiocap/isoMin", float( self.spinBoxIsoMin.value()))
        self.settings.setValue("Physiocap/isoMax", float( self.spinBoxIsoMax.value()))
        self.settings.setValue("Physiocap/isoNombre", float( self.spinBoxNombreIso.value()))
        self.settings.setValue("Physiocap/isoDistance", float( self.spinBoxDistanceIso.value()))

        self.settings.setValue("Physiocap/leChoixAideIso", self.fieldComboAideIso.currentIndex())
        
        self.settings.setValue("Physiocap/leDirThematiques", self.fieldComboThematiques.currentText())
        self.settings.setValue("Physiocap/leChoixDeThematiques", self.fieldComboThematiques.currentIndex())
        
        # Sauver les affichages Inter
        diametre = "NO"
        if self.checkBoxInterDiametre.isChecked():
            diametre = "YES"
        self.settings.setValue("Affichage/InterDiametre", diametre )
        sarment = "NO"
        if self.checkBoxInterSarment.isChecked():
            sarment = "YES"
        self.settings.setValue("Affichage/InterSarment", sarment )
        biomasse = "NO"
        if self.checkBoxInterBiomasse.isChecked():
            biomasse = "YES"
        self.settings.setValue("Affichage/InterBiomasse", biomasse )
        altitude = "NO"
        if self.checkBoxInterAltitude.isChecked():
            altitude = "YES"
        self.settings.setValue("Affichage/InterAltitude", altitude )
        libelle = "NO"
        if self.checkBoxInterLibelle.isChecked():
            libelle = "YES"
        self.settings.setValue("Affichage/InterLibelle", libelle )
        moyennes = "NO"
        if self.checkBoxInterMoyennes.isChecked():
            moyennes = "YES"
        self.settings.setValue("Affichage/InterMoyennes", moyennes )
        points = "NO"
        if self.checkBoxInterPoints.isChecked():
            points = "YES"
        self.settings.setValue("Affichage/InterPoints", points )
        pas_mesure = "NO"
        pas_mesure_details = "NO"
        if self.checkBoxInterPasMesure.isChecked():
            pas_mesure = "YES"
            if self.checkBoxInterPasMesureDetails.isChecked():
                pas_mesure_details = "YES"
        self.settings.setValue("Affichage/InterPasMesure", pas_mesure )
        self.settings.setValue("Affichage/InterPasMesureDetails", pas_mesure_details )
        segment = "NO"
        segment_details = "NO"
        if self.checkBoxInterSegment.isChecked():
            segment = "YES"
            if self.checkBoxInterSegmentDetails.isChecked():
                segment_details = "YES"
        self.settings.setValue("Affichage/InterSegment", segment )
        self.settings.setValue("Affichage/InterSegmentDetails", segment_details )
        segment_brise = "NO"
        segment_brise_details = "NO"
        if self.checkBoxInterSegmentBrise.isChecked():
            segment_brise = "YES"
            if self.checkBoxInterSegmentBriseDetails.isChecked():
                segment_brise_details = "YES"
        self.settings.setValue("Affichage/InterSegmentBrise", segment_brise )
        self.settings.setValue("Affichage/InterSegmentBriseDetails", segment_brise_details )

        
        # Sauver les affichages Intra
        unSeul = "NO"
        if self.checkBoxIntraUnSeul.isChecked():
            unSeul = "YES"
        self.settings.setValue("Affichage/IntraUnSeul", unSeul )
        isos = "NO"
        if self.checkBoxIntraIsos.isChecked():
            isos = "YES"
        self.settings.setValue("Affichage/IntraIsos", isos )
        images = "NO"
        if self.checkBoxIntraImages.isChecked():
            images = "YES"
        self.settings.setValue("Affichage/IntraImages", images ) 

        self.settings.setValue("Physiocap/attributIntraFixe_1", self.fieldComboIntraDIAM.currentText())
        self.settings.setValue("Physiocap/isoMinFixe_1",  self.spinBoxIsoMin_Fixe_DIAM.value())
        self.settings.setValue("Physiocap/isoMaxFixe_1",  self.spinBoxIsoMax_Fixe_DIAM.value())
        self.settings.setValue("Physiocap/isoDistanceFixe_1",  self.spinBoxIsoDistance_Fixe_DIAM.value())

        self.settings.setValue("Physiocap/attributIntraFixe_2", self.fieldComboIntraSARM.currentText())
        self.settings.setValue("Physiocap/isoMinFixe_2",  self.spinBoxIsoMin_Fixe_SARM.value())
        self.settings.setValue("Physiocap/isoMaxFixe_2",  self.spinBoxIsoMax_Fixe_SARM.value())
        self.settings.setValue("Physiocap/isoDistanceFixe_2",  self.spinBoxIsoDistance_Fixe_SARM.value())

        self.settings.setValue("Physiocap/attributIntraFixe_3", self.fieldComboIntraBIOM.currentText())
        self.settings.setValue("Physiocap/isoMinFixe_3",  self.spinBoxIsoMin_Fixe_BIOM.value())
        self.settings.setValue("Physiocap/isoMaxFixe_3",  self.spinBoxIsoMax_Fixe_BIOM.value())
        self.settings.setValue("Physiocap/isoDistanceFixe_3",  self.spinBoxIsoDistance_Fixe_BIOM.value())
        
        # Choix choix de continuer ou non
        continue_group = "NO"
        if self.checkBoxArret.isChecked():
            continue_group = "YES"
        self.settings.setValue("Physiocap/groupStop", continue_group )         
        self.settings.setValue("Physiocap/continueIntra", self.fieldComboIntraContinue.currentIndex())
        
        # Cas consolidation
        consolidation = "NO"
        if self.checkBoxConsolidation.isChecked():
            consolidation = "YES"
        self.settings.setValue("Physiocap/consolidation", consolidation )
        # Cas SagaTIFF
        sagaTIFF = "NO"
        if self.checkBoxSagaTIFF.isChecked():
            sagaTIFF = "YES"
        self.settings.setValue("Physiocap/SagaTIFF", sagaTIFF )

        # Cas du choix SAGA / GDAL
        LIB = "DO NOT KNOW"
        if self.radioButtonSAGA.isChecked():
            LIB = "SAGA"
        else:
            LIB = "GDAL"
        self.settings.setValue("Physiocap/library", LIB)
        
    def slot_INTRA_interpolation_parcelles(self):
        """ Slot qui fait appel au interpolation Intra Parcelles et traite exceptions """

        leModeDeTrace = self.fieldComboModeTrace.currentText()

        nom_complet_point = self.comboBoxPoints.currentText().split( SEPARATEUR_NOEUD)
        if ( len( nom_complet_point) != 2):
            aText = self.tr( "Le shape de points n'est pas choisi. ")
            aText = aText + self.tr( "Créer une nouvelle session Physiocap - bouton Filtrer les données brutes - ")
            aText = aText + self.tr( "avant de faire votre calcul de Moyenne Inter puis Intra Parcellaire")   
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )

        # Memorisation des saisies et expert et les affichages
        self.memoriser_affichages()
        self.memoriser_expert()
        self.memoriser_saisies_inter_intra_parcelles()
            
        try:
            # Création des répertoires et des résultats de synthèse
            intra = PhysiocapIntra( self)
            intra.physiocap_interpolation_IntraParcelles( self)
            
        except physiocap_exception_rep as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Erreur bloquante lors de la création du répertoire : {0}").\
                format( e)
            aText = aText + self.tr( "Vous pouvez avoir un problème d'accès à vos répertoires (accès reseau ...). \n ")
            aText = aText + self.tr( "Vous avez peut être commencé vos calculs en V2 et continuer en V3 (ou inversement). ")
            aText = aText + self.tr( "Restez dans la même version pour l'ensemble des traitemetns dans un même projet.")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        except physiocap_exception_vignette_exists as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Les interpolations dans {0} existent déjà. ").\
                format( e)
            aText = aText + self.tr( "Vous ne pouvez pas redemander ce calcul d'interpolation :\n")
            aText = aText + self.tr( "- Vous pouvez détruire le groupe dans le panneau des couches\n- ou ") 
            aText = aText + self.tr( 'décocher le choix "Arrêt si groupe existe"  \n- ou ') 
            aText = aText + self.tr( "créer une nouvelle session Physiocap.")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        except physiocap_exception_iso_manquant as e:
            physiocap_log_for_error( self)
            aText = self.tr( "L'interpolation n'a pas créé d'isoligne pour {0}. ").\
                format( e)
            aText = aText + self.tr( "Vérifiez vos paramètres min, max, écartement d'isoligne")
            aText = aText + self.tr( "\nVous pouvez contacter le support avec vos traces et données brutes")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        except physiocap_exception_raster_manquant as e:
            physiocap_log_for_error( self)
            aText = self.tr( "L'interpolation n'a pas créé d'image raster pour {0}. ").\
                format( e)
            aText = aText + self.tr( "\nVous pouvez contacter le support avec vos traces et données brutes")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )                
        except physiocap_exception_raster_ou_iso_existe_deja as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Les interpolations {0} existent déjà. ").\
                format( e)
            aText = aText + self.tr( "Vous ne pouvez pas redemander ce calcul d'interpolation :\n")
            aText = aText + self.tr( "- Vous pouvez détruire le groupe dans le panneau des couches\n- et ") 
            aText = aText + self.tr( "détruire les raster et isolignes de {0}\n- ou ").\
                format( e) 
            aText = aText + self.tr( 'modifier le choix "Arrêt si une interpolation existe" \n- ou ') 
            aText = aText + self.tr( "créer une nouvelle session Physiocap.")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        except physiocap_exception_points_invalid as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Le fichier de points ne contient pas les attributs attendus (champ{0})").\
                format( e)
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        except physiocap_exception_interpolation as e:
            physiocap_log_for_error( self)
            allFile = str(e)   # avec str(e) on edite du garbage
            finFile = '"...' + allFile[-60:-1] + '"'            
            aText = self.tr( "L'interpolation de : {0} n'a pu s'exécuter entièrement. ").\
                format( finFile)
            aText = aText + self.tr( "\n - Si la librairie d'interpolation (SAGA ou GDAL) ")
            aText = aText + self.tr( "est bien installée et activée dans {0}. ").\
                format( self.tr( "Traitement"))
            aText = aText + self.tr( "\n - Si vous n'avez pas des contours bizarres.")
            aText = aText + self.tr( "\n - Si vous n'avez pas détruit de couches récemment...")
            aText = aText + self.tr( "\n - Si vous n'avez pas modifié de contexte L93/GPS.")
            aText = aText + self.tr( "\nAlors vous pouvez contacter le support avec vos traces et données brutes")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        except physiocap_exception_no_processing:
            physiocap_log_for_error( self)
            aText = self.tr( "L'extension {0} n'est pas accessible. ").\
                format( self.tr( "Traitement"))
            aText = aText + self.tr( "Pour réaliser l'interpolation intra parcellaire, vous devez")
            aText = aText + self.tr( " installer l'extension {0} (menu Extension => Installer une extension)").\
                format( self.tr( "Traitement"))
            physiocap_error( self, aText)
            return physiocap_message_box( self, aText, "information")
        except physiocap_exception_no_saga:
            physiocap_log_for_error( self)
            aText = self.tr( "SAGA n'est pas accessible. ")
            aText = aText + self.tr( "Pour réaliser l'interpolation intra parcellaire, vous devez")
            aText = aText + self.tr( " installer SAGA")
            physiocap_error( self, aText)
            return physiocap_message_box( self, aText, "information")
        except physiocap_exception_project_contour_incoherence as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Le polygone de contour {0} n'est pas retrouvé. ").\
                format( e)
            aText = aText + self.tr( "Une incohérence entre la session Physiocap et ses données vous oblige à ")
            aText = aText + self.tr( "créer une nouvelle session Physiocap")
            physiocap_error( self, aText)
            return physiocap_message_box( self, aText, "information") 
        except physiocap_exception_project_point_incoherence as e:
            physiocap_log_for_error( self)
            aText = self.tr( "La couche de point {0} n'est pas retrouvé. ").\
                format( e)
            aText = aText + self.tr( "Une incohérence entre la session Physiocap et ses données vous oblige à ")
            aText = aText + self.tr( "créer une nouvelle session Physiocap ")
            physiocap_error( self, aText)
            return physiocap_message_box( self, aText, "information")  
        except physiocap_exception_windows_saga_ascii as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Le projet, le champ ou une valeur de champ {0} ont ").\
                format( e)
            aText = aText + self.tr( "des caractères (non ascii) incompatibles avec l'interpolation SAGA.")
            aText = aText + self.tr( "\nErreur bloquante sous Windows qui nécessite de créer une nouvelle session Physiocap")
            aText = aText + self.tr( " et du contour avec seulement des caractères ascii (non accentuées).")
            physiocap_error( self, aText, "CRITICAL")        
        except physiocap_exception_attribut_multiple_incoherent as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Les attributs fixes pour les isolignes de {0} sont incohérents.").\
                format( e)
            aText = aText + self.tr( "des caractères (non ascii) incompatibles avec l'interpolation SAGA.")
            aText = aText + self.tr( "\nErreur bloquante sous Windows qui nécessite de créer une nouvelle session Physiocap")
            aText = aText + self.tr( " et du contour avec seulement des caractères ascii (non accentuées).")
            physiocap_error( self, aText, "CRITICAL")        
        except physiocap_exception_raster_sans_iso as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Le raster {0} existe sans isoligne correspondante (ou inversement). La situation n'est pas prévu et ").\
                format( e)
            aText = aText + self.tr( "nécessite de créer une nouvelle session Physiocap ")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )    
        except physiocap_exception_no_choix_raster_iso as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Le choix de continuation du traitement intra n'est pas prévu.")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" ) 
        except physiocap_exception_probleme_caractere_librairie as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Le nom du contour {0} contient un caratère (parmi ',...) non supporté durant l'interpolation. "). \
            format( e)
            aText = aText + self.tr( "Modifiez ce nom en supprimant ce(s) caractère(s) dans vos contours et relancez les traitements inter et/ou intra.")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )

##        except x as e:
##            physiocap_log_for_error( self)
##            aText = self.tr( "Physiocap")
##            aText = aText + self.tr( "Intra")
##            physiocap_error( self, aText)
##            return physiocap_message_box( self, aText, "information")

        except:
            raise
        finally:
            pass
        # Fin de capture des erreurs Physiocap        
        physiocap_log( self.tr( "=~= {0} a terminé toutes les interpolations intra parcelaire.").\
            format( PHYSIOCAP_UNI), leModeDeTrace, "INTRA")

                   
    def slot_INTER_moyennes_parcelles(self):
        """ Slot qui fait appel au traitement Inter Parcelles et traite exceptions """
       
        leModeDeTrace = self.fieldComboModeTrace.currentText()
        nom_complet_point = self.comboBoxPoints.currentText().split( SEPARATEUR_NOEUD)
        if ( len( nom_complet_point) != 2):
            aText = self.tr( "Le shape de points n'est pas choisi. ")
            aText = aText + self.tr( "Créer une nouvelle session Physiocap - bouton Filtrer les données brutes - ")
            aText = aText + self.tr( "avant de faire votre calcul de Moyenne Inter Parcellaire")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        
        # Eviter les appels multiples
        self.ButtonInter.setEnabled( False)
        # Memorisation des saisies
        self.memoriser_affichages()
        self.memoriser_expert()
        self.memoriser_saisies_inter_intra_parcelles()
            
        try:
            #physiocap_moyenne_InterParcelles(self)
            inter = PhysiocapInter( self)
            # not used retour = 
            inter.physiocap_moyenne_InterParcelles( self)        
        except physiocap_exception_rep as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Erreur bloquante lors de la création du répertoire : {0}").\
                format( e)
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        except physiocap_exception_vignette_exists as e:
            aText1 = self.tr( "Les moyennes InterParcellaires dans {0} existent déjà. ").\
                format( e)
            physiocap_log(aText1, leModeDeTrace,  "information")
            physiocap_log_for_error( self)
            aText = aText1 + self.tr( "Vous ne pouvez pas redemander ce calcul Inter : vous devez détruire le groupe ") 
            aText = aText + self.tr( "ou créer une nouvelle session Physiocap")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        except physiocap_exception_points_invalid as e:
            physiocap_log_for_error( self)
            aText = self.tr( "La couche de points de la session {0} ne contient pas les attributs attendus. ").\
                format( e)
            aText = aText + self.tr( "Lancez le traitement initial - bouton Filtrer les données brutes - avant de faire votre ")
            aText = aText + self.tr( "calcul de Moyenne Inter Parcellaire" )
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        except physiocap_exception_segment_invalid as e:
            physiocap_log_for_error( self)
            aText = self.tr( "La couche de segment brisé de la session {0} ne contient pas les attributs attendus. ").\
                format( e)
            aText = aText + self.tr( "Lancez le traitement initial - bouton Filtrer les données brutes - avant de faire votre ")
            aText = aText + self.tr( "calcul de Moyenne Inter Parcellaire" )
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        except:
            raise
        finally:
            pass
        # Fin de capture des erreurs Physiocap        
        
        self.groupBoxIntra.setEnabled( True)
        self.groupBoxArret.setEnabled( True)
        self.groupBoxMethode.setEnabled( True)
        self.ButtonIntra.setEnabled( True)
        physiocap_log( self.tr( "== {0} a terminé les moyennes inter parcelaire.").\
            format( PHYSIOCAP_UNI), leModeDeTrace)

    def slot_bascule_pas_mesure(self):
        """ Changement de choix Inter PasMesure : 
        """ 
        set_quoi = False
        if self.checkBoxInterPasMesure.isChecked():
            set_quoi = True
        else:
            set_quoi = False            
        self.checkBoxInterPasMesureDetails.setEnabled( set_quoi)
    
    def slot_bascule_segment(self):
        """ Changement de choix Inter Segment : 
        """ 
        set_quoi = False
        if self.checkBoxInterSegment.isChecked():
            set_quoi = True
        else:
            set_quoi = False            
        self.checkBoxInterSegmentDetails.setEnabled( set_quoi)

    def slot_bascule_segment_brise(self):
        """ Changement de choix Inter Segment Brise: 
        """ 
        set_quoi = False
        if self.checkBoxInterSegmentBrise.isChecked():
            set_quoi = True
        else:
            set_quoi = False            
        self.checkBoxInterSegmentBriseDetails.setEnabled( set_quoi)

    def slot_bascule_V3(self):
        """ Changement de demande pour format V3 : 
        on grise le groupe Segment et les choix segment
        """ 
        set_quoi = False
        if self.checkBoxV3.isChecked():
            set_quoi = True
        else:
            set_quoi = False
                
        self.checkBoxSegment.setEnabled( set_quoi)
        self.checkBoxSegmentBrise.setEnabled( set_quoi)
        self.checkBoxInterAltitude.setEnabled( set_quoi)
        self.checkBoxInterPasMesure.setEnabled( set_quoi)
        self.checkBoxInterSegment.setEnabled( set_quoi)
        self.checkBoxInterSegmentBrise.setEnabled( set_quoi)
        
        if self.lineEditExpert.text() == MODE_EXPERT:
            self.groupBoxSegment.setEnabled( set_quoi)
            self.groupBoxThemaTrace.setEnabled( set_quoi)
            self.groupBoxInterIntraExpert.setEnabled( set_quoi)
        else:
            self.groupBoxSegment.setEnabled( False)
            self.groupBoxThemaTrace.setEnabled( False)
            self.groupBoxInterIntraExpert.setEnabled( False)
            
        # appel des attributs INTRA
        self.slot_INTRA_maj_attributs_interpolables( "DYNAMIQUE")
        self.slot_INTRA_maj_triplet_interpolables()

        if set_quoi == True:            # Forcer LE CHOIX DU SEGMENT BRISÉ
            physiocap_log( self.tr( "{0} passe en Format V3 et force le choix du segment brisé.").\
                format( PHYSIOCAP_UNI), TRACE_TOOLS)
            self.checkBoxSegmentBrise.setEnabled( set_quoi)
            self.checkBoxSegmentBrise.setChecked( Qt.Checked)
            self.settings.setValue("Affichage/FiltrerSegmentBrise", "YES" )
            self.checkBoxSegmentBrise.setEnabled( False)
        else:
            physiocap_log( self.tr( "{0} sort du Format V3 et force le choix du segment brisé.").\
                format( PHYSIOCAP_UNI), TRACE_TOOLS)
            self.checkBoxSegmentBrise.setChecked( Qt.Unchecked)
            self.settings.setValue("Affichage/FiltrerSegmentBrise", "N0" )            

    def slot_bascule_details_vignoble(self):
        """ Changement de demande pour les details vignoble : 
        on grise le groupe Vignoble
        """ 
        # appel des attributs INTRA
        self.slot_INTRA_maj_attributs_interpolables( "DYNAMIQUE")
        self.slot_INTRA_maj_triplet_interpolables()
        if self.checkBoxInfoVignoble.isChecked():
            self.Vignoble.setEnabled( True)
        else:
            self.Vignoble.setEnabled( False)    
            
    def slot_calcul_densite( self):
        # Densité pied /ha

        interrang  = int( self.spinBoxInterrangs.value())
        intercep   = int( self.spinBoxInterceps.value())
        densite = ""
        if (interrang !=0) and ( intercep != 0):
            densite = int (10000 / ((interrang/100) * (intercep/100)))
        self.lineEditDensite.setText( str( densite))
        
    def slot_AIDE_demander_contribution( self):
        """ Pointer vers page de paiement en ligne """ 
        help_url = QUrl("https://sites.google.com/a/jhemmi.eu/objectifs/tarifs")
        QDesktopServices.openUrl(help_url)
    
    def slot_AIDE_demander(self):
        """ Help html qui pointe vers gitHub""" 
        help_url = QUrl("https://github.com/jhemmi/Physiocap3/wiki")
        QDesktopServices.openUrl(help_url)


    def reject( self ):
        """Close when bouton is Cancel"""
        # Todo : V3 prefixe Slot et nommage SLOT_Bouton_Cancel      
        # On sauve les saisies
        self.memoriser_affichages()
        self.memoriser_expert()
        self.memoriser_saisies_inter_intra_parcelles()
        QDialog.reject( self)
                
    def slot_accept( self ):
        """Verify when bouton is Filtrer """
        # Vérifier les valeurs saisies
        # QT confiance et initialisation par Qsettings sert d'assert sur la
        # cohérence des variables saisies
        
        leModeDeTrace = self.fieldComboModeTrace.currentText()
        repertoire_data = self.lineEditDirectoryPhysiocap.text()
        if ((repertoire_data == "") or ( not os.path.exists( repertoire_data))):
            aText = self.tr( "Pas de répertoire de données brutes choisi")
            physiocap_error( self, aText)
            return physiocap_message_box( self, aText)
        repertoire_cible = self.lineEditDirectoryFiltre.text()
        if ((repertoire_cible == "") or ( not os.path.exists( repertoire_cible))):
            aText = self.tr( "Pas de répertoire de données cibles choisi")
            physiocap_error( self, aText)
            return physiocap_message_box( self, aText)
        if self.lineEditProjet.text() == "":
            aText = self.tr( "Pas de nom de session Physiocap choisi")
            physiocap_error( self, aText)
            return physiocap_message_box( self, aText)                 
        # Remettre vide le textEditSynthese
        self.textEditSynthese.clear()

        # Sauvergarde des saisies dans les settings
        self.settings= QSettings( PHYSIOCAP_NOM, PHYSIOCAP_NOM_3)
        self.settings.setValue("Physiocap/projet", self.lineEditProjet.text() )
        self.settings.setValue("Physiocap/expert", self.lineEditExpert.text() )
        self.settings.setValue("Physiocap/repertoire", self.lineEditDirectoryPhysiocap.text() )
        self.settings.setValue("Physiocap/cible_repertoire", self.lineEditDirectoryFiltre.text() )
        #self.settings.setValue("Physiocap/contours", self.lineEditContours.text() )

        # Cas recursif
        recursif = "NO"
        if self.checkBoxRecursif.isChecked():
            recursif = "YES"
            physiocap_log( self.tr( "La recherche des MID fouille l'arbre de données"), leModeDeTrace)
        self.settings.setValue("Physiocap/recursif", recursif )

        # Cas version 3
        version_3 = "NO"
        if self.checkBoxV3.isChecked():
            version_3 = "YES"
            physiocap_log( self.tr( "Les formats de la version V3 sont choisis"), leModeDeTrace)
        self.settings.setValue("Physiocap/version3", version_3 )

        # Cas consolidation
        consolidation = "NO"
        if self.checkBoxConsolidation.isChecked():
            consolidation = "YES"
        self.settings.setValue("Physiocap/consolidation", consolidation )
        # Cas SagaTIFF
        sagaTIFF = "NO"
        if self.checkBoxSagaTIFF.isChecked():
            sagaTIFF = "YES"
        self.settings.setValue("Physiocap/SagaTIFF", sagaTIFF )
            
        # Recuperer le CRS choisi, les extensions et le calculateur de distance
        distancearea, EXT_CRS_SHP, EXT_CRS_PRJ, EXT_CRS_RASTER, \
        laProjectionCRS, laProjectionTXT, EPSG_NUMBER = \
            physiocap_quelle_projection_et_lib_demandee( self)
        self.settings.setValue("Physiocap/laProjection", laProjectionTXT)
        
        # Trop tot self.settings.setValue("Physiocap/dernier_repertoire", self.lineEditDernierProjet.text() )
        self.settings.setValue("Physiocap/mindiam", int( self.spinBoxMinDiametre.value()))
        self.settings.setValue("Physiocap/maxdiam", int( self.spinBoxMaxDiametre.value()))

  
        # Cas détail vignoble
        details = "NO"
        if self.checkBoxInfoVignoble.isChecked():
            details = "YES"
            physiocap_log( self.tr( "Les détails du vignoble sont précisées"), leModeDeTrace)
        self.settings.setValue("Physiocap/details", details)
        self.settings.setValue("Physiocap/max_sarments_metre", int( self.spinBoxMaxSarmentsParMetre.value()))
        self.settings.setValue("Physiocap/interrangs", int( self.spinBoxInterrangs.value()))
        self.settings.setValue("Physiocap/interceps", int( self.spinBoxInterceps.value()))
        self.settings.setValue("Physiocap/hauteur", int( self.spinBoxHauteur.value()))
        self.settings.setValue("Physiocap/densite", float( self.doubleSpinBoxDensite.value()))
#        self.settings.setValue("Physiocap/leCepage", self.fieldComboCepage.currentText())
#        self.settings.setValue("Physiocap/laTaille", self.fieldComboTaille.currentText())

        # Onglet Histogramme
        TRACE_HISTO = "NO"
        if self.checkBoxHistogramme.isChecked():
            TRACE_HISTO = "YES"
            physiocap_log( self.tr( "Les histogrammes sont attendus"), leModeDeTrace)
        self.settings.setValue("Physiocap/histogrammes", TRACE_HISTO)

        # On sauve les affichages
        self.memoriser_affichages()
        self.memoriser_expert()
        self.memoriser_saisies_inter_intra_parcelles()

                    
        # ########################################
        # Gestion de capture des erreurs Physiocap
        # ########################################
        try:
            filtreur = PhysiocapFiltrer( self)
            # Création des répertoires et des résultats de synthèse
            retour = filtreur.physiocap_creer_donnees_resultats( self, 
                laProjectionCRS,  laProjectionTXT, 
                EXT_CRS_SHP, EXT_CRS_PRJ,
                details, TRACE_HISTO, recursif, version_3)
        except physiocap_exception_rep as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Erreur bloquante lors de la création du répertoire : {0}").\
                format( e)
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        
        except physiocap_exception_err_csv as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Erreurs dans les données brutes {0}").\
                format( e)
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )

        except physiocap_exception_trop_err_csv as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Trop d'erreurs {0} dans les données brutes").\
                format( e)
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        
        except physiocap_exception_fic as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Erreur bloquante lors de la création du fichier : {0}").\
                format( e)
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )

        except physiocap_exception_csv as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Erreur bloquante lors de la création du fichier csv : {0}").\
                format( e)
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )

        except physiocap_exception_mid as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Erreur bloquante lors de la copie du fichier MID : {0}").\
                format( e)
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )

        except physiocap_exception_no_mid:
            physiocap_log_for_error( self)
            aText = self.tr( "Erreur bloquante : aucun fichier MID à traiter")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )

        except physiocap_exception_calcul_segment_invalid as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Erreur bloquante durant création des segments : {0}").\
                format( e)
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )

        except physiocap_exception_stop_user:
            return physiocap_log( \
                self.tr( "Arrêt de {0} à la demande de l'utilisateur").format( PHYSIOCAP_UNI), 
                leModeDeTrace, "WARNING")
         # On remonte les autres exceptions
        except:
            raise
        finally:
            pass
        # Fin de capture des erreurs Physiocap
        if ( retour == 0 ):
            physiocap_log( self.tr( "** {0} est prêt pour calcul Inter parcellaire - Onglet Parcelles").\
                format( PHYSIOCAP_UNI), leModeDeTrace)
        return retour

