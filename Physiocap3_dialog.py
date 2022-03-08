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

from .Physiocap_tools import (physiocap_message_box, \
        physiocap_log_for_error, physiocap_log, physiocap_error, \
        quel_chemin_templates, quel_poly_point_INTER, quelle_projection_et_lib_demandee, \
        quel_sont_vecteurs_choisis, assert_champs_agro_obligatoires, lister_parcelles_INTRA, \
        physiocap_nom_entite_avec_pb_caractere, physiocap_get_layer_by_name, physiocap_get_layer_by_ID)

from .Physiocap_creer_arbre import (PhysiocapFiltrer)
from .Physiocap_inter import (PhysiocapInter)
from .Physiocap_intra_interpolation import (PhysiocapIntra) 
from .Physiocap_var_exception import *

from PyQt5 import uic
from PyQt5.QtCore import (QSettings, Qt, QUrl)
from PyQt5.QtGui import (QPixmap,  QDesktopServices)
from PyQt5.QtWidgets import (QDialogButtonBox, QDialog, QFileDialog) 
from qgis.core import (Qgis, QgsVectorLayer)

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
        
        self.dans_Quel_Settings()
        # Remplissage du mode de traces
        self.fieldComboModeTrace.setCurrentIndex( 0)
        if len( MODE_TRACE) == 0:
            self.fieldComboModeTrace.clear( )
            physiocap_error( self, self.tr( "Pas de liste des modes de traces pré définie"))
        else:
            self.fieldComboModeTrace.clear( )
            self.fieldComboModeTrace.addItems( MODE_TRACE )
            # Retrouver le mode de trace dans  settings
            leModeDeTrace = self.settings.value("Expert/leModeDeTrace", TRACE_MINI)
            for idx, modeTrace in enumerate( MODE_TRACE):
                if ( modeTrace == leModeDeTrace):
                    self.fieldComboModeTrace.setCurrentIndex( idx)

        #physiocap_log( "Répertoire de QGIS : " +  self.gis_dir, leModeDeTrace)
        physiocap_log( "Répertoire des extensions (plugins) : " +  self.plugins_dir, leModeDeTrace)
       
        # Slot for boutons : ces deux sont déjà sont dans UI
        ##self.buttonBox.button( QDialogButtonBox.Ok ).pressed.connect(self.accept)
        ##self.buttonBox.button( QDialogButtonBox.Cancel ).pressed.connect(self.reject)
        self.buttonBox.button( QDialogButtonBox.Help ).pressed.connect(self.slot_AIDE_demander)
        self.ButtonFiltrer.pressed.connect(self.slot_accept)
        self.buttonContribuer.pressed.connect(self.slot_AIDE_demander_contribution)
        
        # Slot Profil & test PDF
        self.fieldComboProfilPHY.currentIndexChanged[int].connect( self.slot_PROFIL_change )  
        
        # Slot pour données brutes et pour données cibles
        self.toolButtonDirectoryPhysiocap.pressed.connect( self.slot_lecture_repertoire_donnees_brutes )  
        self.toolButtonDirectoryFiltre.pressed.connect( self.slot_lecture_repertoire_donnees_cibles)  
        # Slot pour le groupe vignoble
        self.groupBoxDetailVignoble.clicked.connect( self.slot_bascule_details_vignoble)
        self.radioButtonContour.toggled.connect( self.slot_bascule_onglet_contour)
        # Slot pour le groupe format V3
        self.checkBoxV3.stateChanged.connect( self.slot_bascule_V3)
        self.checkBoxInterPasMesure.stateChanged.connect( self.slot_bascule_pas_mesure)
        self.checkBoxInterSegment.stateChanged.connect( self.slot_bascule_segment)
        self.checkBoxInterSegmentBrise.stateChanged.connect( self.slot_bascule_segment_brise)
        
        # Inter
        self.checkBoxContourSolo.stateChanged.connect( self.slot_bascule_sans_contour)
        self.comboBoxPolygone.currentIndexChanged[int].connect( self.slot_PROFIL_INTER_maj_champ_poly_liste )
        self.fieldComboContours.currentIndexChanged[int].connect( self.slot_INTER_change_champ_choisi )
        self.ButtonInter.pressed.connect(self.slot_INTER_moyennes_parcelles)
        self.ButtonInterRefresh.pressed.connect(self.slot_INTER_liste_parcelles)
        #self.groupBoxInter.setEnabled( False)
        
        # Intra        
        self.fieldComboIntra.currentIndexChanged[int].connect( self.slot_INTRA_min_max_champ )
        self.spinBoxIsoMin_Fixe_DIAM.valueChanged.connect( self.slot_INTRA_DIAM_min_max_fixe )
        self.spinBoxIsoMax_Fixe_DIAM.valueChanged.connect( self.slot_INTRA_DIAM_min_max_fixe )
        self.spinBoxIsoMin_Fixe_SARM.valueChanged.connect( self.slot_INTRA_SARM_min_max_fixe )
        self.spinBoxIsoMax_Fixe_BIOM.valueChanged.connect( self.slot_INTRA_BIOM_min_max_fixe )
        self.spinBoxIsoMin_Fixe_SARM.valueChanged.connect( self.slot_INTRA_SARM_min_max_fixe )
        self.spinBoxIsoMax_Fixe_BIOM.valueChanged.connect( self.slot_INTRA_BIOM_min_max_fixe )
        # attention aux appels recursifs infinis : on a fait 2 maj_attributs ... 
        self.fieldComboIntraDIAM.currentIndexChanged[int].connect( self.slot_PROFIL_INTRA_maj_attributs_interpolables)
        self.fieldComboIntraSARM.currentIndexChanged[int].connect( self.slot_PROFIL_INTRA_maj_attributs_interpolables)
        self.fieldComboIntraBIOM.currentIndexChanged[int].connect( self.slot_PROFIL_INTRA_maj_attributs_interpolables)
        self.checkBoxToutes.stateChanged.connect( self.slot_bascule_intra_toutes)

        self.ButtonIntra.pressed.connect(self.slot_INTRA_interpolation_parcelles)
        self.groupBoxIntra.setEnabled( False)
        self.groupBoxMethode.setEnabled( True)
        self.ButtonIntra.setEnabled( False)
        
        # Affichage
        self.fieldComboAideIso.currentIndexChanged[int].connect( self.slot_INTRA_bascule_aide_iso )
               
        physiocap_log( self.tr( "Votre machine tourne sous QGIS {0} et {1} ").\
            format( Qgis.QGIS_VERSION, MACHINE), TRACE_TOOLS)        
##        physiocap_log( self.tr( "QGIS attend des couches de projection SRID {0} CRS_ID {1} ").\
##            format( GEOSRID, GEO_EPSG_CRS_ID ), TRACE_TOOLS)
    
        # Style sheet pour QProgressBar
        self.setStyleSheet( "QProgressBar {color:black; text-align:center; font-weight:bold; padding:2px;}"
           "QProgressBar:chunk {background-color:green; width: 10px; margin-left:1px;}")
        
        ###############
        # Récuperation dans les settings (derniers parametres saisies)
        ###############
        self.dans_Quel_Settings()
        # Initialisation des parametres à partir des settings
        nom_session = self.settings.value("Physiocap/session", NOM_PAR_DEFAUT)
        self.lineEditSession.setText( nom_session)
        
        if (self.settings.value("Physiocap/recursif") == "YES"):
            self.checkBoxRecursif.setChecked( Qt.Checked)
        else:
            self.checkBoxRecursif.setChecked( Qt.Unchecked)

        if (self.settings.value("Expert/version3") == "YES"):
            self.checkBoxV3.setChecked( Qt.Checked)
        else:
            self.checkBoxV3.setChecked( Qt.Unchecked)        
        self.slot_bascule_V3()    
 
        # Nom de la session et des répertoires
        repertoire_brut = self.settings.value("Physiocap/repertoire",
            REPERTOIRE_DONNEES_BRUTES)
        self.lineEditDirectoryPhysiocap.setText( repertoire_brut )
        self.lineEditDerniereSession.setText( self.settings.value("Physiocap/derniereSession",
            ""))    
        # Répertoire cibles apres filtre
        repertoire_cible = self.settings.value("Physiocap/cible_repertoire", "VIDE")
        if ( repertoire_cible == "VIDE"):
            repertoire_cible = repertoire_brut
        self.lineEditDirectoryFiltre.setText( repertoire_cible)
                
        # Consolidation
        if (self.settings.value("Expert/consolidation") == "YES"):
            self.checkBoxConsolidation.setChecked( Qt.Checked)
        else:
            self.checkBoxConsolidation.setChecked( Qt.Unchecked)

        # Remplissage des profils
        self.fieldComboProfilPHY.setCurrentIndex( 0) 
        if len( LISTE_PROFIL) == 0:
            self.fieldComboProfilPHY.clear( )
            physiocap_error( self, self.tr( "Pas de liste des profils pré définie"))
        else:
            self.fieldComboProfilPHY.clear( )
            self.fieldComboProfilPHY.addItems( LISTE_PROFIL)
             # Retrouver le profil de  settings
            self.fieldComboProfilPHY.setCurrentIndex( 0)
            leProfil = self.settings.value("Physiocap/leProfilPHY", "xx") 
            for idx, un in enumerate( LISTE_PROFIL):
                if ( un == leProfil):
                    self.fieldComboProfilPHY.setCurrentIndex( idx)
                    #physiocap_log( self.tr( "Profil retrouvé"), TRACE_PROFIL) 

        # Affichages
        self.lire_affichages()
        # Agro
        self.lire_agro()

        if ( self.settings.value("Intra/toutesParcelles") == "NO"):
            self.checkBoxToutes.setChecked( Qt.Unchecked)
        else:
            self.checkBoxToutes.setChecked( Qt.Checked)

        self.ButtonInter.setEnabled( False)
        self.ButtonIntra.setEnabled( False)            
        self.spinBoxDensiteMinimale.setValue( int( self.settings.value( "Intra/densiteMinimale", 500)))
        if (self.settings.value("Expert/library") == "SAGA"):
            self.radioButtonSAGA.setChecked(  Qt.Checked)
            self.spinBoxPower.setEnabled( False)
        else:
            self.radioButtonGDAL.setChecked(  Qt.Checked)

         # Saga to TIFF par defaut
        if (self.settings.value("Expert/SagaTIFF") == "NO"):
            self.checkBoxSagaTIFF.setChecked( Qt.Unchecked)
        else:
            self.checkBoxSagaTIFF.setChecked( Qt.Checked)
               
        # Choisir radioButtonL93 ou radioButtonGPS
        laProjectionCochee = self.settings.value("Expert/laProjection", PROJECTION_L93)
        if ( laProjectionCochee == PROJECTION_GPS ):
            self.radioButtonGPS.setChecked(  Qt.Checked)
        else:
            self.radioButtonL93.setChecked(  Qt.Checked)
            
        # Remettre vide le textEditSynthese
        self.textEditSynthese.clear()
        
        # Remplissage de la liste de FORMAT_VECTEUR 
        self.fieldComboFormats.setCurrentIndex( 0)         
        if self.checkBoxV3.isChecked():
            liste_formats = FORMAT_VECTEUR_V3
        else:
            liste_formats = FORMAT_VECTEUR

        if len( liste_formats) == 0:
            self.fieldComboFormats.clear( )
            physiocap_error( self, self.tr( "Pas de liste des formats de vecteurs pré définie"))
        else:
            self.fieldComboFormats.clear( )
#            #uri = physiocap_get_uri_by_layer( self)
#            uri = None
#            if uri != None:
            if (self.settings.value("Expert/version3") == "YES"):
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
        self.spinBoxInterrangs.setValue( int( self.settings.value("Agro/interrangs", 110 )))
        self.spinBoxInterceps.setValue( int( self.settings.value("Agro/interceps", 100 )))
        # Densité pied /ha
        self.slot_calcul_densite()
        self.spinBoxHauteur.setValue( int( self.settings.value("Agro/hauteur", 90 )))
        self.doubleSpinBoxDensite.setValue( float( self.settings.value("Agro/densite", 0.9 )))
      
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
            self.fieldComboShapeVitesse.setCurrentIndex( 1)                
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
               
        try :
            import matplotlib
            matplotlib.path
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
        self.spinBoxPower.setValue( float( self.settings.value("Intra/powerIntra", 2 )))
        self.spinBoxPixel.setValue( float( self.settings.value("Intra/pixelIntra", 0.5 )))
        self.spinBoxDoubleRayon.setValue( float( self.settings.value("Intra/rayonIntra", 12 )))
        self.slot_INTRA_rayon_selon_SCR_LIB()
        # Cas des 3 iso fixes qui ne sont pas sauvegardés dans memoriser_saisies_InterIntraParcelles
        self.spinBoxIsoMin_Fixe_DIAM.setValue( int( self.settings.value("Intra/isoMinFixe_1", 7 )))
        self.spinBoxIsoMax_Fixe_DIAM.setValue( int( self.settings.value("Intra/isoMaxFixe_1", 11 )))
        self.spinBoxIsoDistance_Fixe_DIAM.setValue( int( self.settings.value("Intra/isoDistanceFixe_1", 1 )))
        self.spinBoxIsoMin_Fixe_SARM.setValue( int( self.settings.value("Intra/isoMinFixe_2", 5 )))
        self.spinBoxIsoMax_Fixe_SARM.setValue( int( self.settings.value("Intra/isoMaxFixe_2", 13)))
        self.spinBoxIsoDistance_Fixe_SARM.setValue( int( self.settings.value("Intra/isoDistanceFixe_2", 2 )))
        self.spinBoxIsoMin_Fixe_BIOM.setValue( int( self.settings.value("Intra/isoMinFixe_3", 200 )))
        self.spinBoxIsoMax_Fixe_BIOM.setValue( int( self.settings.value("Intra/isoMaxFixe_3", 1000 )))
        self.spinBoxIsoDistance_Fixe_BIOM.setValue( int( self.settings.value("Intra/isoDistanceFixe_3", 200 )))
 
        # Cas des dernières valeurs iso
        self.spinBoxIsoMin.setValue( int( self.settings.value("Intra/isoMin", 1 )))
        self.spinBoxIsoMax.setValue( int( self.settings.value("Intra/isoMax", 1000 )))
        self.spinBoxNombreIso.setValue( int( self.settings.value("Intra/isoNombre", 5 )))
        self.spinBoxDistanceIso.setValue( int( self.settings.value("Intra/isoDistance", 1 )))
       
        # On initialise le nombre de distance Iso
        self.slot_INTRA_iso_distance()         

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
        self.slot_PROFIL_INTRA_maj_attributs_interpolables( "INIT")
        self.slot_PROFIL_INTRA_maj_triplet_interpolables()
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
        
        # En dernier la surcharge des cas de Profils
        self.slot_PROFIL_change()

        # Init fin 
        return
    
    # ################
    #  Différents SLOT
    # ################
    # PROFIL et mise en settings
    def slot_PROFIL_change( self, forcer_profil = None):
        """Paramétrage spécifique à chaque profil
            appel recursif pour forcer à 'standard' pour remettre toujours le profil standard avant de le modifier
        """
        self.dans_Quel_Settings()
        #leModeDeTrace = self.fieldComboModeTrace.currentText()
        if (forcer_profil == None or isinstance( forcer_profil, int)):
            Nom_Profil =  self.fieldComboProfilPHY.currentText()
            # On surcharge le contenu de la config sans la perdre 
            self.slot_PROFIL_change( 'Standard')
        else:
            Nom_Profil = forcer_profil
            #physiocap_log( "==> slot_PROFIL forcer à {}".format ( Nom_Profil), TRACE_PROFIL)
            
        # Cas des templates de champagne 
        _, _ = quel_chemin_templates( self)

        if  Nom_Profil == 'Champagne':
            # Fixer valeur de filtrer et bloquer filtre
            self.radioButtonNordPrecedent.setChecked( Qt.Checked)
            self.spinBoxMinDiametre.setValue( 4)
            self.spinBoxMaxDiametre.setValue( 18)
            self.spinBoxMaxSarmentsParMetre.setValue( 25)
            self.spinBoxHauteur.setValue( 90)
            self.doubleSpinBoxDensite.setValue( 0.9)
            self.groupBoxFiltrer.setEnabled( False)
            # Inter Intra
            self.groupBoxInter.setEnabled( True)
            self.groupBoxContourInter.setEnabled( True)
            self.groupBoxIntra.setEnabled( True)
            # Autoriser de continuer les cas d'intra
            self.checkBoxArret.setChecked( Qt.Unchecked)
            self.fieldComboIntraContinue.clear()
            self.fieldComboIntraContinue.addItems( ATTR_CONTINUE)        
            self.fieldComboIntraContinue.setCurrentIndex( 1)
            # Détail vignoble & agro et enchainer les 3 actions 
            self.checkBoxTroisActions.setChecked( Qt.Checked)
            self.groupBoxDetailVignoble.setChecked( Qt.Checked)
            self.checkBoxInfoVignoble.setChecked( Qt.Checked)
            self.radioButtonOnglet.setChecked(  Qt.Checked)  
            self.groupBoxVignoble.setEnabled( True)
            self.label_PH.setEnabled( False)            
            self.doubleSpinBoxPH.setEnabled( False)            
            # Saga par defaut et L93
            self.radioButtonSAGA.setChecked(  Qt.Checked)
            self.checkBoxSagaTIFF.setChecked( Qt.Checked)
            self.radioButtonL93.setChecked(  Qt.Checked)
            # Pas de choix de theme
            self.groupBoxThemaTrace.setEnabled( False)
            # initialisation sans sauvegarde dans profil
            self.spinBoxIsoMin_Fixe_DIAM.setValue( int( self.settings.value("Champagne/isoMinFixe_1", 7 )))
            self.spinBoxIsoMax_Fixe_DIAM.setValue( int( self.settings.value("Champagne/isoMaxFixe_1", 11 )))
            self.spinBoxIsoDistance_Fixe_DIAM.setValue( int( self.settings.value("Champagne/isoDistanceFixe_1", 1 )))
            self.spinBoxIsoMin_Fixe_SARM.setValue( int( self.settings.value("Champagne/isoMinFixe_2", 5 )))
            self.spinBoxIsoMax_Fixe_SARM.setValue( int( self.settings.value("Champagne/isoMaxFixe_2", 13)))
            self.spinBoxIsoDistance_Fixe_SARM.setValue( int( self.settings.value("Champagne/isoDistanceFixe_2", 2 )))
            self.spinBoxIsoMin_Fixe_BIOM.setValue( int( self.settings.value("Champagne/isoMinFixe_3", 200 )))
            self.spinBoxIsoMax_Fixe_BIOM.setValue( int( self.settings.value("Champagne/isoMaxFixe_3", 1000 )))
            self.spinBoxIsoDistance_Fixe_BIOM.setValue( int( self.settings.value("Champagne/isoDistanceFixe_3", 200 )))
            # un seul triplet pour intra DIAM BIOMGCEP NBSARCEP est code dans ce slot
            self.slot_PROFIL_INTRA_maj_attributs_interpolables( Nom_Profil)
            
            self.checkBoxIntraImages.setChecked( Qt.Checked)
            self.checkBoxIntraPDF.setChecked( Qt.Checked)
            # Afficher le contour généré
            self.checkBoxContour.setChecked( Qt.Checked)
            # Pas d'isoligne
            self.checkBoxIntraUnSeul.setChecked( Qt.Unchecked)
            self.checkBoxIntraIsos.setChecked( Qt.Unchecked)
            self.groupBoxIsolignes.setChecked( Qt.Unchecked)
            self.groupBoxIsolignes.setEnabled( False)
            self.groupBoxMethode.setEnabled( True)
            self.groupBoxExpertOuvert.setEnabled( False)
            self.groupBoxSegment.setEnabled( False)
        elif Nom_Profil == 'Fronton':
            self.radioButtonNordPrecedent.setChecked( Qt.Unchecked)
            self.spinBoxMinDiametre.setValue( 3)
            self.spinBoxMaxDiametre.setValue( 22)
            self.spinBoxMaxSarmentsParMetre.setValue( 25)
            self.groupBoxFiltrer.setEnabled( True)
            self.checkBoxContour.setChecked( Qt.Checked)
            self.groupBoxDetailVignoble.setEnabled( True)
            self.label_PH.setEnabled( True)            
            self.doubleSpinBoxPH.setEnabled( True)            
            self.groupBoxContourInter.setEnabled( True)
            self.checkBoxTroisActions.setChecked( Qt.Unchecked)
            self.groupBoxDetailVignoble.setChecked( Qt.Checked)
            self.checkBoxInfoVignoble.setChecked( Qt.Checked)
            self.groupBoxIntra.setEnabled( False)    # déclencher apres filtrer & inter
            self.groupBoxThemaTrace.setEnabled( False)
            self.groupBoxVignoble.setEnabled( True)
            self.groupBoxIsolignes.setChecked( Qt.Checked)
            self.groupBoxIsolignes.setEnabled( True)
            self.groupBoxMethode.setEnabled( True)
            self.groupBoxExpertOuvert.setEnabled( False)
            self.groupBoxSegment.setEnabled( True)
            self.checkBoxIntraImages.setChecked( Qt.Checked)
        elif Nom_Profil == 'Standard':
            self.radioButtonNordPrecedent.setChecked( Qt.Checked)
            self.spinBoxMinDiametre.setValue( 4)
            self.spinBoxMaxDiametre.setValue( 18)
            self.spinBoxMaxSarmentsParMetre.setValue( 25)
            self.groupBoxFiltrer.setEnabled( True)
            self.checkBoxContour.setChecked( Qt.Checked)
            self.groupBoxContourInter.setEnabled( True)   
            self.groupBoxIntra.setEnabled( False)     # déclencher apres filtrer & inter
            self.checkBoxTroisActions.setChecked( Qt.Unchecked)
            self.groupBoxDetailVignoble.setChecked( Qt.Checked)
            self.checkBoxInfoVignoble.setChecked( Qt.Checked)
            # Autoriser de continuer les cas d'intra
            self.checkBoxArret.setChecked( Qt.Checked)
            self.fieldComboIntraContinue.clear()
            self.fieldComboIntraContinue.addItems( ATTR_CONTINUE)        
            self.fieldComboIntraContinue.setCurrentIndex( 0)
            self.groupBoxVignoble.setEnabled( True)
            self.label_PH.setEnabled( True)            
            self.doubleSpinBoxPH.setEnabled( True)            
            self.groupBoxMethode.setEnabled( True)
            self.groupBoxExpertOuvert.setEnabled( True)
            self.groupBoxThemaTrace.setEnabled( True)
            self.groupBoxIsolignes.setChecked( Qt.Checked)
            self.groupBoxIsolignes.setEnabled( True)
            self.checkBoxIntraImages.setChecked( Qt.Checked)
        else:
            physiocap_error( "Dans slot_PROFIL {} est inconnu ".format ( Nom_Profil), TRACE_PROFIL)
        physiocap_log( "PROFIL {} est initialisé".format ( Nom_Profil), TRACE_PROFIL)

    def dans_Quel_Settings( self, nomSettings=PHYSIOCAP_NOM_3+".4"):
        self.settings= QSettings(PHYSIOCAP_NOM, nomSettings)
        
    def memoriser_tous_Settings( self):
        """ Utilisation des settings de QT
            Organisation des initialisation commence  dans Physiocap puis 
            pour affichage, style, agro, expert, inter & intra 
            TODO: ?V3.x ENVISAGEABLE avec plusieurs profils : "PROFIL" bascules
            Pour les profils, on memorise l'initialisation d'un profil (premier passage) 
                - dans Profil/nom_du_profil et le dernier profil actif pour les changements.
                - et dans nom_du_profil/ on conserve les valeurs particulières, les check box ou group box    
                - une bascule On permet de jouer ces initalisations
                  et pour la bascule profil Off  dans le profil standard on stocke la valeur ou check box ou group box stadard
        """
        self.dans_Quel_Settings()
        self.settings.setValue("Physiocap/leProfilPHY", self.fieldComboProfilPHY.currentText())
        self.settings.setValue("Physiocap/repertoire", self.lineEditDirectoryPhysiocap.text() )
        self.settings.setValue("Physiocap/cible_repertoire", self.lineEditDirectoryFiltre.text() )
        self.settings.setValue("Physiocap/session", self.lineEditSession.text() )
        # Cas recursif
        recursif = "YES" if self.checkBoxRecursif.isChecked() else "NO"
        self.settings.setValue("Physiocap/recursif", recursif )
        TRACE_HISTO = "YES" if self.checkBoxHistogramme.isChecked() else "NO"
        self.settings.setValue("Physiocap/histogrammes", TRACE_HISTO )
        # Cas détail vignoble
        details = "YES" if self.groupBoxDetailVignoble.isChecked() else "NO"
        self.settings.setValue("Physiocap/details", details)
        self.settings.setValue("Physiocap/mindiam", int( self.spinBoxMinDiametre.value()))
        self.settings.setValue("Physiocap/maxdiam", int( self.spinBoxMaxDiametre.value()))
        self.settings.setValue("Physiocap/max_sarments_metre", int( self.spinBoxMaxSarmentsParMetre.value()))
        pasContour = "YES" if self.checkBoxContourSolo.isChecked() else "NO"
        self.settings.setValue("Physiocap/pasContour", pasContour)

        self.memoriser_affichages_styles()
        version_3, consolidation, leModeDeTrace = self.memoriser_expert()
        self.memoriser_agro()
        self.memoriser_saisies_InterIntraParcelles()
        # Profil Champagne
        VALEUR_PROFIL_INITIALISE = 'Initialisé'
        existeChampagne = self.settings.value("Profil/Champagne", "inconnu")
        if ( existeChampagne ==  "inconnu"):
            self.settings.setValue("Champagne/attributIntraFixe_1", "DIAM")
            self.settings.setValue("Champagne/isoMinFixe_1",  self.spinBoxIsoMin_Fixe_DIAM.value())
            self.settings.setValue("Champagne/isoMaxFixe_1",  self.spinBoxIsoMax_Fixe_DIAM.value())
            self.settings.setValue("Champagne/isoDistanceFixe_1",  self.spinBoxIsoDistance_Fixe_DIAM.value())

            self.settings.setValue("Champagne/attributIntraFixe_2", "NBSARCEP")
            self.settings.setValue("Champagne/isoMinFixe_2",  self.spinBoxIsoMin_Fixe_SARM.value())
            self.settings.setValue("Champagne/isoMaxFixe_2",  self.spinBoxIsoMax_Fixe_SARM.value())
            self.settings.setValue("Champagne/isoDistanceFixe_2",  self.spinBoxIsoDistance_Fixe_SARM.value())

            self.settings.setValue("Champagne/attributIntraFixe_3", "BIOMGCEP")
            self.settings.setValue("Champagne/isoMinFixe_3",  self.spinBoxIsoMin_Fixe_BIOM.value())
            self.settings.setValue("Champagne/isoMaxFixe_3",  self.spinBoxIsoMax_Fixe_BIOM.value())
            self.settings.setValue("Champagne/isoDistanceFixe_3",  self.spinBoxIsoDistance_Fixe_BIOM.value())
            physiocap_log('Settings Champagne devient {}'.format(VALEUR_PROFIL_INITIALISE), TRACE_PROFIL)
            self.settings.setValue("Profil/Champagne", VALEUR_PROFIL_INITIALISE)
            
        physiocap_log('Tous les settings PROFIL sont sauvegardées', TRACE_PROFIL) 
        return version_3, consolidation, recursif,  details, TRACE_HISTO, pasContour 
        
    def memoriser_expert( self):
        """ Mémoriser les choix d'expert """        
        # THEMATIQUES text et index
        self.dans_Quel_Settings()
        leModeDeTrace = self.fieldComboModeTrace.currentText()
        self.settings.setValue("Expert/leModeDeTrace", leModeDeTrace)
        self.settings.setValue("Expert/leFormat", self.fieldComboFormats.currentText())
        # Cas détail segment
        self.settings.setValue("Expert/vitesse_mini_segment", float( self.doubleSpinBoxVitesseMiniSegment.value()))        
        self.settings.setValue("Expert/vitesse_maxi_segment", float( self.doubleSpinBoxVitesseMaxiSegment.value()))        
        self.settings.setValue("Expert/nombre_mini_points", int( self.spinBoxNombreMiniPointsConsecutifs.value()))
        self.settings.setValue("Expert/derive_max_segment", int( self.spinBoxDeriveMaxSegment.value()))
        self.settings.setValue("Expert/pas_de_la_derive", int( self.spinBoxPasDeDerive.value()))
        self.settings.setValue("Expert/pdop_max_segment", float( self.doubleSpinBoxPdopMaxSegment.value()))
        # Cas version 3
        version_3 = "NO"
        if self.checkBoxV3.isChecked():
            version_3 = "YES"
            physiocap_log( self.tr( "Les formats de la version V3 sont choisis"), TRACE_PROFIL) 
        self.settings.setValue("Expert/version3", version_3 )

        # Cas consolidation
        consolidation = "YES" if self.checkBoxConsolidation.isChecked() else "NO"
        self.settings.setValue("Expert/consolidation", consolidation )
        # Cas SagaTIFF
        sagaTIFF = "YES" if self.checkBoxSagaTIFF.isChecked() else "NO"
        self.settings.setValue("Expert/SagaTIFF", sagaTIFF )
        physiocap_log('Les informations expertes sont sauvegardées', TRACE_PROFIL) 
        return version_3, consolidation, leModeDeTrace
        
    def lire_agro( self):
        # Informations agronomiques (inspiré de ___Nadia___)
        self.dans_Quel_Settings()
        Nom_Profil =  self.fieldComboProfilPHY.currentText()
        #leModeDeTrace = self.fieldComboModeTrace.currentText()

        self.lineEditNomParcelle.setText( self.settings.value("Agro/nom_parcelle", "_"))
        self.spinBoxAnneePlant.setValue( int( self.settings.value("Agro/annee_plantation", 2000 )))
               
        # Remplissage des Region
        self.comboBoxRegion.setCurrentIndex( 0)
        if  Nom_Profil == 'Champagne':
            LISTE_REGION = REGIONS_CHAMPAGNE
        elif Nom_Profil == 'Fronton':
            LISTE_REGION = ['Vins du Sud Ouest']
        else:
            LISTE_REGION = ['_']
        if len( LISTE_REGION) == 0:
            self.comboBoxRegion.clear( )
            physiocap_error( self, self.tr( "Pas de liste des régions pré définie"), TRACE_PROFIL)
        else:
            self.comboBoxRegion.clear( )
            self.comboBoxRegion.addItems( LISTE_REGION)
             # Retrouver la commune de  settings
            self.comboBoxRegion.setCurrentIndex( 0)
            laRegion = self.settings.value("Agro/region", "xx") 
            for idx, une in enumerate( LISTE_REGION):
                if ( une == laRegion):
                    self.comboBoxRegion.setCurrentIndex( idx)

        self.spinBoxInterrangs.setValue( int( self.settings.value("Agro/interrangs", 110 )))
        self.spinBoxInterceps.setValue( int( self.settings.value("Agro/interceps", 100 )))
        self.spinBoxHauteur.setValue( int( self.settings.value("Agro/hauteur", 90 )))
        self.doubleSpinBoxDensite.setValue( float( self.settings.value("Agro/densite", 0.9 )))

        # Remplissage des communes
        self.comboBoxCommune.setCurrentIndex( 0)
        if  Nom_Profil in [ 'Champagne', 'Fronton']:
            if Nom_Profil == 'Champagne':
                LISTE_COMMUNES = sorted( CRUS_CHAMPAGNE)
            elif Nom_Profil == 'Fronton':
                LISTE_COMMUNES = COMMUNES_FRONTON
            else:
                LISTE_COMMUNES = ['_']
            if len( LISTE_COMMUNES) == 0:
                self.comboBoxCommune.clear( )
                physiocap_error( self, self.tr( "Pas de liste des communes pré définie"))
            else:
                self.comboBoxCommune.clear( )
                self.comboBoxCommune.addItems( ["_"] + LISTE_COMMUNES)
                 # Retrouver la commune de  settings
                self.comboBoxCommune.setCurrentIndex( 0)
                laCommune = self.settings.value("Agro/commune", "xx") 
                for idx, une in enumerate( LISTE_COMMUNES):
                    if ( une == laCommune):
                        self.comboBoxCommune.setCurrentIndex( idx + 1)  # car _
                        #physiocap_log( self.tr( "Commune retrouvée"), leModeDeTrace) 
        
        self.lineEditClone.setText( self.settings.value("Agro/clone", "inconnu"))
        self.lineEditPorteGreffe.setText( self.settings.value("Agro/porte_greffe", "inconnu"))

        # Remplissage des cépages
        self.comboBoxCepage.setCurrentIndex( 0) 
        if len( LISTE_CEPAGES) == 0:
            self.comboBoxCepage.clear( )
            physiocap_error( self, self.tr( "Pas de liste des cépages pré définie"))
        else:
            self.comboBoxCepage.clear( )
            self.comboBoxCepage.addItems( LISTE_CEPAGES)
             # Retrouver le profil de  settings
            self.comboBoxCepage.setCurrentIndex( 0)
            leCepage = self.settings.value("Agro/cepage", "xx") 
            for idx, un in enumerate( LISTE_CEPAGES):
                if ( un == leCepage):
                    self.comboBoxCepage.setCurrentIndex( idx)

        # Remplissage des tailles
        self.comboBoxTaille.setCurrentIndex( 0) 
        if len( LISTE_TAILLES) == 0:
            self.comboBoxTaille.clear( )
            physiocap_error( self, self.tr( "Pas de liste des tailles pré définie"))
        else:
            self.comboBoxTaille.clear( )
            self.comboBoxTaille.addItems( LISTE_TAILLES)
             # Retrouver le profil de  settings
            self.comboBoxTaille.setCurrentIndex( 0)
            laTaille = self.settings.value("Agro/taille", "xx") 
            for idx, un in enumerate( LISTE_TAILLES):
                if ( un == laTaille):
                    self.comboBoxTaille.setCurrentIndex( idx)

        self.spinBoxArgile.setValue( int( self.settings.value("Agro/sol_argile", 20 )))
        self.doubleSpinBoxMO.setValue( float( self.settings.value("Agro/sol_mo", 0.5 )))
        self.spinBoxCsurN.setValue( int( self.settings.value("Agro/sol_CsurN", 20 )))
        self.doubleSpinBoxPH.setValue( float( self.settings.value("Agro/sol_PH", 7 )))
        self.doubleSpinBoxRendement.setValue( float( self.settings.value("Agro/rendement", 50 )))
        self.spinBoxNbGrappes.setValue( int( self.settings.value("Agro/nb_grappes", 80 )))
        self.spinBoxPoidsMoyenGrappes.setValue( int( self.settings.value("Agro/poids_moy_grappes", 180 )))
        physiocap_log('Les informations agronomiques sont lues', TRACE_PROFIL) 

    def memoriser_agro( self):
        # Informations agronomiques (inspiré de ___Nadia___)
        self.dans_Quel_Settings()
        self.settings.setValue("Agro/nom_parcelle", self.lineEditNomParcelle.text())#___definir les valeurs des variables : nom de la parcelle 
        self.settings.setValue("Agro/region",  self.comboBoxRegion.currentText())
        self.settings.setValue("Agro/annee_plantation", int( self.spinBoxAnneePlant.value()))
        self.settings.setValue("Agro/commune",  self.comboBoxCommune.currentText())
        self.settings.setValue("Agro/interrangs", int( self.spinBoxInterrangs.value()))
        self.settings.setValue("Agro/interceps", int( self.spinBoxInterceps.value()))
        self.settings.setValue("Agro/hauteur", int( self.spinBoxHauteur.value()))
        self.settings.setValue("Agro/densite", float( self.doubleSpinBoxDensite.value()))
        self.settings.setValue("Agro/cepage", self.comboBoxCepage.currentText())
        self.settings.setValue("Agro/clone",self.lineEditClone.text())#___définir les valeurs des variables : clone
        self.settings.setValue("Agro/porte_greffe", self.lineEditPorteGreffe.text())#___definir les valeurs des variables : porte-greffe
        self.settings.setValue("Agro/taille", self.comboBoxTaille.currentText())
        self.settings.setValue("Agro/sol_argile", int( self.spinBoxArgile.value()))
        self.settings.setValue("Agro/sol_mo", float( self.doubleSpinBoxMO.value()))
        self.settings.setValue("Agro/sol_CsurN", int( self.spinBoxCsurN.value()))
        self.settings.setValue("Agro/sol_PH", float( self.doubleSpinBoxPH.value()))
        self.settings.setValue("Agro/rendement", float( self.doubleSpinBoxRendement.value()))
        self.settings.setValue("Agro/nb_grappes", int( self.spinBoxNbGrappes.value()))
        self.settings.setValue("Agro/poids_moy_grappes", int( self.spinBoxPoidsMoyenGrappes.value()))
        physiocap_log('Les informations agronomiques sont sauvegardées', TRACE_PROFIL) 

    def memoriser_affichages_styles(self):
        """ Mémoriser les choix d'affichage """        
        # Sauver les affichages cas généraux
        diametre = "YES" if self.checkBoxDiametre.isChecked() else "NO"
        self.settings.setValue("Affichage/FiltrerDiametre", diametre )
        sarment = "YES" if self.checkBoxSarment.isChecked() else "NO"
        self.settings.setValue("Affichage/FiltrerSarment", sarment )
        biomasse = "YES" if self.checkBoxBiomasse.isChecked() else "NO"
        self.settings.setValue("Affichage/FiltrerBiomasse", biomasse )
        vitesse = "YES" if self.checkBoxVitesse.isChecked() else "NO"  
        self.settings.setValue("Affichage/FiltrerVitesse", vitesse )
        pas_mesure = "YES" if self.checkBoxPasMesure.isChecked() else "NO"
        self.settings.setValue("Affichage/FiltrerPasMesure", pas_mesure )
        filtre_segment = "YES" if self.checkBoxSegment.isChecked() else "NO"
        self.settings.setValue("Affichage/FiltrerSegment", filtre_segment )
        filtre_segment_brise = "YES" if self.checkBoxSegmentBrise.isChecked() else "NO"            
        self.settings.setValue("Affichage/FiltrerSegmentBrise", filtre_segment_brise )
        genere_contour = "YES" if self.checkBoxContour.isChecked() else "NO"            
        self.settings.setValue("Affichage/GenererContour", genere_contour )

        # Sauver les affichages Inter
        diametre = "YES" if self.checkBoxInterDiametre.isChecked() else "NO"
        self.settings.setValue("Affichage/InterDiametre", diametre )
        sarment = "YES" if self.checkBoxInterSarment.isChecked() else "NO"
        self.settings.setValue("Affichage/InterSarment", sarment )
        biomasse = "YES" if self.checkBoxInterBiomasse.isChecked() else "NO"
        self.settings.setValue("Affichage/InterBiomasse", biomasse )
        altitude = "YES" if self.checkBoxInterAltitude.isChecked() else "NO"
        self.settings.setValue("Affichage/InterAltitude", altitude )
        libelle = "YES" if self.checkBoxInterLibelle.isChecked() else "NO"
        self.settings.setValue("Affichage/InterLibelle", libelle )
        moyennes = "YES" if self.checkBoxInterMoyennes.isChecked() else "NO"
        self.settings.setValue("Affichage/InterMoyennes", moyennes )
        points = "YES" if self.checkBoxInterPoints.isChecked() else "NO"
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
        unSeul = "YES" if self.checkBoxIntraUnSeul.isChecked() else "NO"
        self.settings.setValue("Affichage/IntraUnSeul", unSeul )
        isos = "YES" if self.checkBoxIntraIsos.isChecked() else "NO"
        self.settings.setValue("Affichage/IntraIsos", isos )
        images = "YES" if self.checkBoxIntraImages.isChecked() else "NO"
        self.settings.setValue("Affichage/IntraImages", images ) 
        
        # Trois parametre INTRA
        self.settings.setValue("Physiocap/leChoixShapeSarment", self.fieldComboShapeSarment.currentIndex())
        self.settings.setValue("Physiocap/leChoixShapeBiomasse", self.fieldComboShapeBiomasse.currentIndex())
        self.settings.setValue("Physiocap/leChoixShapeVitesse", self.fieldComboShapeVitesse.currentIndex())
        # et styles
        self.settings.setValue("Style/leDirThematiques", self.fieldComboThematiques.currentText())
        self.settings.setValue("Style/leChoixDeThematiques", self.fieldComboThematiques.currentIndex())
        # Filtrage
        self.settings.setValue("Style/themeDiametre", self.lineEditThematiqueDiametre.text())
        self.settings.setValue("Style/themeSarment", self.lineEditThematiqueSarment.text())
        self.settings.setValue("Style/themeBiomasse",self.lineEditThematiqueBiomasse.text())
        self.settings.setValue("Style/themeVitesse", self.lineEditThematiqueVitesse.text())
        self.settings.setValue("Style/themePasMesure", self.lineEditThematiquePasMesure.text())
        self.settings.setValue("Style/themeSegment", self.lineEditThematiqueSegment.text())
        self.settings.setValue("Style/themeSegmentBrise", self.lineEditThematiqueSegmentBrise.text())
        self.settings.setValue("Style/themeContour", self.lineEditThematiqueContour.text())
        # Inter
        self.settings.setValue("Style/themeInterDiametre", self.lineEditThematiqueInterDiametre.text())
        self.settings.setValue("Style/themeInterSarment", self.lineEditThematiqueInterSarment.text())
        self.settings.setValue("Style/themeInterBiomasse", self.lineEditThematiqueInterBiomasse.text())
        self.settings.setValue("Style/themeInterAltitude", self.lineEditThematiqueInterAltitude.text())
        # inter moyenne et points
        self.settings.setValue("Style/themeInterLibelle", self.lineEditThematiqueInterLibelle.text())
        self.settings.setValue("Style/themeInterMoyenne", self.lineEditThematiqueInterMoyenne.text())
        self.settings.setValue("Style/themeInterPoints", self.lineEditThematiqueInterPoints.text())
        self.settings.setValue("Style/themeInterPasMesure", self.lineEditThematiqueInterPasMesure.text())
        self.settings.setValue("Style/themeInterSegment", self.lineEditThematiqueInterSegment.text())
        self.settings.setValue("Style/themeInterSegmentBrise", self.lineEditThematiqueInterSegmentBrise.text())
        # intra
        self.settings.setValue("Style/themeIntraIso", self.lineEditThematiqueIntraIso.text())
        self.settings.setValue("Style/themeIntraImage", self.lineEditThematiqueIntraImage.text())
        self.settings.setValue("Style/themeIntraPDF", self.lineEditThematiqueIntraPDF.text())

    def lire_affichages( self):         
        self.dans_Quel_Settings()
        # Choix d'affichage généraux
        # TOUJOURS le diametre qui est necessaire à "Inter" comme points
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
        if (self.settings.value("Affichage/GenererContour", "NO") == "YES"):
            self.checkBoxContour.setChecked( Qt.Checked)
        else:
            self.checkBoxContour.setChecked( Qt.Unchecked)
            
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

    def memoriser_saisies_InterIntraParcelles(self):
        """ Mémorise les saisies inter et intra """

        self.dans_Quel_Settings()
        #self.settings.setValue("Inter/interPoint", self.comboBoxPoints.currentText() )
        self.settings.setValue("Inter/interPoly", self.comboBoxPolygone.currentText() )
        self.settings.setValue("Inter/attributPoly", self.fieldComboContours.currentText())
        self.settings.setValue("Inter/attributpbGDAL", self.fieldPbGdal.currentText())

        self.settings.setValue("Intra/attributIntra", self.fieldComboIntra.currentText())
        toutes_parcelles = "YES" if self.checkBoxToutes.isChecked() else "NO"
        self.settings.setValue("Intra/toutesParcelles", toutes_parcelles)
        if toutes_parcelles == "NO":
            self.settings.setValue("Intra/attributUneParcelle", self.fieldComboParcelleIntra.currentText())
        
        self.settings.setValue("Intra/continueIntra", self.fieldComboIntraContinue.currentIndex())
        self.settings.setValue("Intra/densiteMinimale", float( self.spinBoxDensiteMinimale.value()))
        self.settings.setValue("Intra/powerIntra", float( self.spinBoxPower.value()))
        self.settings.setValue("Intra/rayonIntra", float( self.spinBoxDoubleRayon.value()))
        self.settings.setValue("Intra/pixelIntra", float( self.spinBoxPixel.value()))
        self.settings.setValue("Intra/isoMin", float( self.spinBoxIsoMin.value()))
        self.settings.setValue("Intra/isoMax", float( self.spinBoxIsoMax.value()))
        self.settings.setValue("Intra/isoNombre", float( self.spinBoxNombreIso.value()))
        self.settings.setValue("Intra/isoDistance", float( self.spinBoxDistanceIso.value()))
        
        self.settings.setValue("Intra/leChoixAideIso", self.fieldComboAideIso.currentIndex())
    
        # Choix des isolignes
        iso_group = "YES" if self.groupBoxIsolignes.isChecked() else "NO"
        self.settings.setValue("Intra/groupIso", iso_group )         
        self.settings.setValue("Intra/attributIntraFixe_1", self.fieldComboIntraDIAM.currentText())
        self.settings.setValue("Intra/isoMinFixe_1",  self.spinBoxIsoMin_Fixe_DIAM.value())
        self.settings.setValue("Intra/isoMaxFixe_1",  self.spinBoxIsoMax_Fixe_DIAM.value())
        self.settings.setValue("Intra/isoDistanceFixe_1",  self.spinBoxIsoDistance_Fixe_DIAM.value())

        self.settings.setValue("Intra/attributIntraFixe_2", self.fieldComboIntraSARM.currentText())
        self.settings.setValue("Intra/isoMinFixe_2",  self.spinBoxIsoMin_Fixe_SARM.value())
        self.settings.setValue("Intra/isoMaxFixe_2",  self.spinBoxIsoMax_Fixe_SARM.value())
        self.settings.setValue("Intra/isoDistanceFixe_2",  self.spinBoxIsoDistance_Fixe_SARM.value())

        self.settings.setValue("Intra/attributIntraFixe_3", self.fieldComboIntraBIOM.currentText())
        self.settings.setValue("Intra/isoMinFixe_3",  self.spinBoxIsoMin_Fixe_BIOM.value())
        self.settings.setValue("Intra/isoMaxFixe_3",  self.spinBoxIsoMax_Fixe_BIOM.value())
        self.settings.setValue("Intra/isoDistanceFixe_3",  self.spinBoxIsoDistance_Fixe_BIOM.value())
            
        # Choix de continuer ou non
        continue_group = "YES" if self.checkBoxArret.isChecked() else "NO"
        self.settings.setValue("Intra/groupStop", continue_group )         
        self.settings.setValue("Intra/continueIntra", self.fieldComboIntraContinue.currentIndex())
        
        # Cas SagaTIFF
        sagaTIFF = "YES" if self.checkBoxSagaTIFF.isChecked() else "NO"
        self.settings.setValue("Expert/SagaTIFF", sagaTIFF )

        # Cas du choix SAGA / GDAL
        LIB = "DO NOT KNOW"
        if self.radioButtonSAGA.isChecked():
            LIB = "SAGA"
        else:
            LIB = "GDAL"
        self.settings.setValue("Expert/library", LIB)
        
    def slot_lecture_repertoire_donnees_brutes( self):
        """Quel répertoire pour données brutes"""
        # Récuperer dans setting le nom du dernier ou sinon REPERTOIRE_DONNEES_BRUTES
        self.dans_Quel_Settings()
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
        """Quel répertoire pour données filtrées"""
        # Récuperer dans setting le nom du dernier ou sinon REPERTOIRE_DONNEES_BRUTES
        self.dans_Quel_Settings()
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
 
    # VIGNOBLE
    def slot_VIGNOBLE_choix_type_apport( self ):
        # si le choix de type apports est 'autre(à préciser)' une zone de texte doit apparaitre pour permettre de saisir l'information ___Nadia___
        liste_apports_nb=len(TYPE_APPORTS)
        choix_user_ind=self.comboBoxTypeApportFert.currentIndex()
        if(choix_user_ind==liste_apports_nb-1):
            self.lineEditTypeApportFert_Autres.setText("")
            self.lineEditTypeApportFert_Autres.setEnabled(True)
        else :
            self.lineEditTypeApportFert_Autres.setText("à préciser")
            self.lineEditTypeApportFert_Autres.setEnabled(False)

    def slot_VIGNOBLE_choix_strategie_sol( self ):
        # si le choix de strategie de sol est 'autre(à préciser)' une zone de texte doit apparaitre pour permettre de saisir l'information ___Nadia___
        liste_strategies_nb=len(ENTRETIEN_SOL)
        choix_user_ind=self.comboBoxStrategieSol.currentIndex()
        if(choix_user_ind==liste_strategies_nb-1):
            self.lineEditStrategieSol_Autres.setText("")
            self.lineEditStrategieSol_Autres.setEnabled(True)
        else :
            self.lineEditStrategieSol_Autres.setText("à préciser")
            self.lineEditStrategieSol_Autres.setEnabled(False)
    
    # INTRA
    def slot_INTRA_DIAM_min_max_fixe( self ):
        """ Vérifie si min et max du choix fixe DIAM sont cohérents"""
        if not self.groupBoxIsolignes.isChecked():
            return
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
        if not self.groupBoxIsolignes.isChecked():
            return
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
        if not self.groupBoxIsolignes.isChecked():
            return
        mon_champ = self.fieldComboIntraBIOM.currentText()
        min_entier = round( float ( self.spinBoxIsoMin_Fixe_BIOM.value()))
        le_max = float ( self.spinBoxIsoMax_Fixe_BIOM.value())      
        max_entier = round( le_max)
        if (min_entier >= max_entier):
            aText = self.tr( "Votre minimum pour {0} ne doit pas être plus grand que votre maximum".\
                format( mon_champ))
            return physiocap_message_box( self, aText, "information")              
        return
        
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
            self.lab_MultiplieRayon.setEnabled( False)
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
            self.lab_MultiplieRayon.setEnabled( True)
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
        
        
    def slot_PROFIL_INTRA_maj_attributs_interpolables( self,  ORIGINE_TRIPLET):
        """ Créer la liste des attributs interpolable
        Cette liste provient de ATTRIBUTS_INTRA et si details ATTRIBUTS_INTRA_DETAILS et gere le cas V3"""
        #leModeDeTrace = self.fieldComboModeTrace.currentText()
        Nom_Profil =  self.fieldComboProfilPHY.currentText()
        ATTR_LISTE=[]

        if (len( ATTRIBUTS_INTRA) == 0):
            self.fieldComboIntra.clear()
            physiocap_error( self, self.tr( "Pas de liste des attributs pour Intra pré définie"))
            return
        if ORIGINE_TRIPLET == "INIT":
            # Récupérer les choix dans settings pour le cas initial
            leChoixDiam = self.settings.value("Intra/attributIntraFixe_1", "DIAM")
            leChoixSarm = self.settings.value("Intra/attributIntraFixe_2", "NBSARM")
            leChoixBiom = self.settings.value("Intra/attributIntraFixe_3", "BIOM")
            # Retrouver les choix intra précedent (dans intra ou dans préference)        
            leChoixIntra = self.settings.value("Intra/attributIntra", "xx") 
        elif ORIGINE_TRIPLET == "Champagne":
            leChoixDiam = self.settings.value("Champagne/attributIntraFixe_1", "DIAM")
            leChoixSarm = self.settings.value("Champagne/attributIntraFixe_2", "NBSARCEP")
            leChoixBiom = self.settings.value("Champagne/attributIntraFixe_3", "BIOMGCEP")
            # Retrouver les choix intra précedent (dans intra ou dans préference)        
            leChoixIntra = self.settings.value("Intra/attributIntra", "xx") 
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

        if self.checkBoxV3.isChecked():     
            # Ajout d'un nouvelle liste d'attribut interpolable
            ATTR_LISTE = ATTR_LISTE + ATTRIBUTS_V3_INTRA
        
        # Cas de details ATTRIBUTS_INTRA_DETAIL
        if self.groupBoxDetailVignoble.isChecked():
            if  Nom_Profil == 'Champagne':
                ATTR_LISTE = ATTR_LISTE + ATTRIBUTS_INTRA_DETAILS
            else:
                ATTR_LISTE = ATTR_LISTE + ATTRIBUTS_INTRA_DETAILS + ATTRIBUTS_INTRA_DETAILS_PLUS

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
            self.checkBoxArret.setChecked( Qt.Checked)
            self.settings.setValue("Physiocap/groupStop", "YES")
            self.fieldComboIntraContinue.clear()
            self.fieldComboIntraContinue.addItems( ATTR_CONTINUE)        
            self.fieldComboIntraContinue.setCurrentIndex( 0)
            self.settings.setValue("Physiocap/continueIntra", 0)

        return

        
    def slot_PROFIL_INTRA_maj_triplet_interpolables( self):
        """ Créer la liste du triplet d'attributs interpolable
        on cherche dans settings et la liste des attributs possible dans pour le choix du triplet
        qui se nomme DIAM puis SARM puis BIOM mais peut contenir n'importe quelle valeur
        """
        ATTR_LISTE_TRIPLET=[]

        if (len( ATTRIBUTS_INTRA) == 0):
            self.fieldComboIntraDIAM.clear()
            self.fieldComboIntraSARM.clear()
            self.fieldComboIntraBIOM.clear()
            physiocap_error( self, self.tr( "Pas de liste des attributs pour Intra pré définie"))
            return
        
        # Récupérer les choix dans settings 
        Nom_Profil =  self.fieldComboProfilPHY.currentText()
        if Nom_Profil == 'Champagne': # ce passage est impossible si GroupIso est false
            leChoixDiam = self.settings.value("Champagne/attributIntraFixe_1", "DIAM")
            leChoixSarm = self.settings.value("Champagne/attributIntraFixe_2", "NBSARCEP")
            leChoixBiom = self.settings.value("Champagne/attributIntraFixe_3", "BIOMGCEP")
        else:
            leChoixDiam = self.settings.value("Intra/attributIntraFixe_1", "x1")
            leChoixSarm = self.settings.value("Intra/attributIntraFixe_2", "x2")
            leChoixBiom = self.settings.value("Intra/attributIntraFixe_3", "x3")

        # Ajout des attributs standard 
        ATTR_LISTE_TRIPLET = ATTRIBUTS_INTRA

        if self.checkBoxV3.isChecked():     
            # Ajout d'un nouvelle liste d'attribut interpolable
            ATTR_LISTE_TRIPLET = ATTR_LISTE_TRIPLET + ATTRIBUTS_V3_INTRA
        
        # Cas de details ATTRIBUTS_INTRA_DETAIL
        if self.groupBoxDetailVignoble.isChecked():
            if Nom_Profil == 'Champagne':
                ATTR_LISTE_TRIPLET = ATTR_LISTE_TRIPLET + ATTRIBUTS_INTRA_DETAILS
            else:
                ATTR_LISTE_TRIPLET = ATTR_LISTE_TRIPLET + ATTRIBUTS_INTRA_DETAILS + ATTRIBUTS_INTRA_DETAILS_PLUS
            
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
        if not self.groupBoxIsolignes.isChecked():
            return
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
        
    def slot_INTRA_interpolation_parcelles(self):
        """ Slot qui fait appel au interpolation Intra Parcelles et traite exceptions """

        leModeDeTrace = self.fieldComboModeTrace.currentText()

        # TODO: ?V3.z Trouver le fichier de points à partie de la session
        nom_complet_point = self.comboBoxPoints.currentText().split( SEPARATEUR_NOEUD)
        if ( len( nom_complet_point) != 3):
            aText = self.tr( "Le shape de points n'est pas choisi. ")
            aText = aText + self.tr( "Créer une nouvelle session Physiocap - bouton Filtrer les données brutes - ")
            aText = aText + self.tr( "avant de faire votre calcul de Moyenne Inter puis Intra Parcellaire")   
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )

        # Memorisation des saisies et expert et les affichages
        version_3, consolidation, _, details, _,  _ = self.memoriser_tous_Settings()
            
        try:
            # Création des répertoires et des résultats de synthèse
            intra = PhysiocapIntra( self)
            intra.physiocap_interpolation_IntraParcelles( self)
            
        except physiocap_exception_rep as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Erreur bloquante lors de la création du répertoire : {0}").\
                format( e)
            aText = aText + self.tr( "Vous pouvez avoir un problème d'accès à vos répertoires (accès réseau ...). \n ")
            aText = aText + self.tr( "Peut-être avez-vous commencé vos calculs en V2 et continué en V3 (ou inversement). ")
            aText = aText + self.tr( "Restez dans la même version pour l'ensemble des traitements dans une même session.")
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
            aText = aText + self.tr( "\nVérifier si le nom de la session ne contient pas d'accents et relancer l'interpolation")
            aText = aText + self.tr( "\nSinon, vous pouvez contacter le support avec vos traces et données brutes")
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
            aText = self.tr( "Le nom du contour {0} contient un caratère (parmi ',blanc...) non supporté durant l'interpolation. "). \
            format( e)
            aText = aText + self.tr( "Modifiez ce nom en supprimant ce(s) caractère(s) dans vos contours et relancez les traitements inter et/ou intra.")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        except physiocap_exception_agro_no_pdf_modele as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Le modèle pour l'impression {0} est absent.").format( e)
            aText = aText + self.tr( "Contacter jhemmi.eu pour créer un modele pour les impressions PDF.")
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
        # RENDU quel iface ? self.iface.mapCanvas().setRenderFlag( True )
        physiocap_log( self.tr( "=~= {0} a terminé toutes les interpolations intra parcelaire.").\
            format( PHYSIOCAP_UNI), leModeDeTrace, "INTRA")

                   
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
        #leModeDeTrace = self.fieldComboModeTrace.currentText()
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
                physiocap_log( aText , TRACE_MIN_MAX)
        else:
            # Cas pour une seul interpolation
#            self.spinBoxIsoMin.setEnabled( True)
#            self.spinBoxIsoMax.setEnabled( True)
            self.slot_INTRA_bascule_aide_iso()

            max_attribut = -99999
            min_attribut = 99999
            #physiocap_log("Attribut pour Intra >{0}".format( nom_attribut) , TRACE_TOOLS)
            nom_complet_point = self.comboBoxPoints.currentText().split( SEPARATEUR_NOEUD)
            if (len( nom_complet_point) !=3):
                # TODO: ?V3.x ERREUR à tracer
                return
            idLayer   = nom_complet_point[2]
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

    # INTER
    def slot_INTER_liste_parcelles( self):
        """ Rafraichit les listes avant le calcul inter parcelles"""
        nombre_poly = 0
        nombre_point = 0
        nombre_poly, nombre_point = quel_poly_point_INTER( self)
        physiocap_log( "Dans slot_INTER_liste_parcelles : poly >> {}<< et points >> {}<<". \
           format ( nombre_poly,nombre_point), TRACE_JH)

        if ( nombre_poly > 0):
            # A_TESTER: si utile fin inter self.slot_min_max_champ_intra()
            self.slot_PROFIL_INTER_maj_champ_poly_liste()
        if (( nombre_poly > 0) and ( nombre_point > 0)):
            # Liberer le bouton "Inter"
            self.ButtonInter.setEnabled( True)
        else:
            self.ButtonInter.setEnabled( False)
        
        # Mise à jour du commentaire pour le rayon
        self.slot_INTRA_rayon_selon_SCR_LIB()

    def slot_INTER_change_champ_choisi( self ):
        """ Synchronise les 2 combox"""
        position_choix = self.fieldComboContours.currentIndex()
        self.fieldPbGdal.setCurrentIndex( position_choix)                              
   
    def slot_PROFIL_INTER_maj_champ_poly_liste( self ):
        """ Creer une liste de champs (fieldCombo Box) à valuer values pour le vecteur courant"""
        leProfil = self.fieldComboProfilPHY.currentText()
        #leModeDeTrace = self.fieldComboModeTrace.currentText()
        nom_complet_poly = self.comboBoxPolygone.currentText().split( SEPARATEUR_NOEUD)
        inputLayer = nom_complet_poly[0] 

        self.fieldComboContours.clear()
        self.fieldPbGdal.clear()
        physiocap_log( "Dans recherche de champ : layer >> {0}<<". \
           format ( inputLayer), TRACE_JH)

        layer = physiocap_get_layer_by_name( inputLayer)
        if layer is None and len(nom_complet_poly) == 3:
            layer = QgsVectorLayer( nom_complet_poly[2], nom_complet_poly[0], 'ogr')

        # Initialisation avec CHAMP_NOM_PHY = NOM_PHY
        self.fieldPbGdal.addItem( "NO" )                                
        self.fieldComboContours.addItem( CHAMP_NOM_PHY)
        self.fieldComboContours.setCurrentIndex( 0)
        if layer is not None:
            # On exclut les layers qui ne sont pas de type 0 (exemple 1 raster)
            if ( layer.type() == 0):
                position_combo = 1 # Demarre à 1 car NOM_PHY est dejà ajouté
                dernierAttribut = self.settings.value("Physiocap/attributPoly", "xx")
                mon_provider = layer.dataProvider()
                nombre_ligne = mon_provider.featureCount()
                map_champ = mon_provider.fieldNameMap()
                valeur_unique = "NO"
                if leProfil == 'Champagne':
                    # On garde le seul champ nommant les parcelles 
                    for mon_champ in mon_provider.fields():
                        nom_champ = mon_champ.name()
                        physiocap_log( "Champ {}".format( nom_champ),  TRACE_JH)
                        if nom_champ == "Nom_Parcel":
                            physiocap_log( "Champ nom parcel",  TRACE_JH)
                            liste_valeurs = mon_provider.uniqueValues( map_champ[ nom_champ])
                            valeur_unique = "YES" if nombre_ligne == len( liste_valeurs) else "NO"
                            physiocap_log( "Champ nom parcel est unique ? {} ".format(valeur_unique),  TRACE_JH)
                            physiocap_log( "nombre champ {} attendu et uniques {} ".\
                                format(nombre_ligne, len( liste_valeurs)),  TRACE_JH)
                            break
                
                if valeur_unique == "YES": # cas champagne et champ Nom_Parcel OK
                    self.fieldComboContours.clear()
                    self.fieldPbGdal.clear()
                    self.fieldPbGdal.addItem( "NO" )                                
                    self.fieldComboContours.addItem( "Nom_Parcel")
                    self.fieldComboContours.setCurrentIndex( 0)
                else:
                    for mon_champ in mon_provider.fields():
                        nom_champ = mon_champ.name()
                        if mon_champ.type() != 10:
                            physiocap_log( "type Exclu {} pour {}".format( mon_champ.type(), nom_champ), TRACE_JH)
                            continue
                        liste_valeurs = mon_provider.uniqueValues( map_champ[ nom_champ])
                        valeur_unique = "YES" if nombre_ligne == len( liste_valeurs) else "NO"

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
            physiocap_log( "Dans recherche des champs uniques : aucun layer", TRACE_JH)      
                                                  
    def slot_INTER_moyennes_parcelles(self):
        """ Slot qui fait appel au traitement Inter Parcelles et traite exceptions """
       
        leModeDeTrace = self.fieldComboModeTrace.currentText()
        nom_complet_point = self.comboBoxPoints.currentText().split( SEPARATEUR_NOEUD)
        if ( len( nom_complet_point) != 3):
            aText = self.tr( "Le shape de points n'est pas choisi. ")
            aText = aText + self.tr( "Créer une nouvelle session Physiocap - bouton Filtrer les données brutes - ")
            aText = aText + self.tr( "avant de faire votre calcul de Moyenne Inter Parcellaire")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        
        # Eviter les appels multiples
        self.ButtonInter.setEnabled( False)
        # Memorisation des saisies
        version_3, consolidation, _, details, _, _ = self.memoriser_tous_Settings()
           
        try:
            inter = PhysiocapInter( self)
            inter.physiocap_moyenne_InterParcelles( self)
    
        except physiocap_exception_rep as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Erreur bloquante lors de la création du répertoire : {0}").\
                format( e)
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        except physiocap_exception_vignette_exists as e:
            aText = self.tr( "Les moyennes InterParcellaires dans {0} existent déjà. ").\
                format( e)
            physiocap_log(aText, leModeDeTrace,  "information")
            aText = aText + self.tr( "Vous ne pouvez pas redemander ce calcul Inter : vous devez détruire le groupe ") 
            aText = aText + self.tr( "ou créer une nouvelle session Physiocap")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        except physiocap_exception_poly_invalid as e:
            physiocap_log_for_error( self)
            aText = self.tr( "La couche de contour de la session {0} n'existe pas. ").\
                format( e)
            aText = aText + self.tr( "Lancez le traitement initial - bouton Filtrer les données brutes - avant de faire votre ")
            aText = aText + self.tr( "calcul de Moyenne Inter Parcellaire" )
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
        
        # Nouveautés avec Geopackage
        except physiocap_exception_no_gpkg as e:
            aText = self.tr( "Erreur bloquante : problème lors de recherche du géopackage {0}").\
                format( e)
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        except physiocap_exception_vecteur_type_inconnu as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Erreur bloquante : le format de vecteur {0} n'est pas supporté par l'extension").\
                format( e)
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )

        except:
            raise
        finally:
            pass
        # Fin de capture des erreurs Physiocap        
        
        self.groupBoxIntra.setEnabled( True)
        self.groupBoxMethode.setEnabled( True)
        self.ButtonInter.setEnabled( True)
        self.ButtonIntra.setEnabled( True)
        physiocap_log( self.tr( "== {0} a terminé les moyennes inter parcelaire.").\
            format( PHYSIOCAP_UNI), leModeDeTrace)

        # Si OK : chercher à enchainer vers Intra
        if  self.checkBoxTroisActions.isChecked():
            self.slot_INTRA_interpolation_parcelles()

####        else:
####            # TODO: RENDU again self.iface.mapCanvas().setRenderFlag( True )

    def slot_bascule_intra_toutes(self):
        """ Changement de choix Intra toutes parcelle libère la liste de choix et la remplit
        """ 
        Nom_Profil = self.fieldComboProfilPHY.currentText()
        set_quoi = False
        les_parcelles_agro = None
        if self.checkBoxToutes.isChecked():
            set_quoi = False
        else:
            set_quoi = True
            _, _, origine_poly, vecteur_poly, chemin_vecteur = quel_sont_vecteurs_choisis( self, "Filtrer")
            # Assert vecteur dejà choisi
            if vecteur_poly != None:
                if Nom_Profil == 'Champagne':
                    # Assert vecteur poly champ obligatoire
                    try:
                        _, champs_agro_fichier, _, _, champs_vignoble_requis, champs_vignoble_requis_fichier, _, _, les_parcelles_agro, _ = \
                            assert_champs_agro_obligatoires( self, vecteur_poly, origine_poly)
                    except physiocap_exception_agro_obligatoire as e:
                        aText = "{}".format(e)
                        physiocap_message_box( self, aText, 'information')

                    if les_parcelles_agro != None and len( les_parcelles_agro) > 0:
                        # Remplir la liste des parcelles diponibles
                        lister_parcelles_INTRA( self, None,  les_parcelles_agro)
                else:
                    # Remplir la liste des parcelles diponibles dans poly
                    lister_parcelles_INTRA( self, vecteur_poly)            
        self.fieldComboParcelleIntra.setEnabled( set_quoi)
        vecteur_poly = None
        
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
        quoi = True if self.checkBoxInterSegment.isChecked() else False
        self.checkBoxInterSegmentDetails.setEnabled( quoi)

    def slot_bascule_segment_brise(self):
        """ Changement de choix Inter Segment Brise: 
        """ 
        quoi = True if self.checkBoxInterSegmentBrise.isChecked() else False
        self.checkBoxInterSegmentBriseDetails.setEnabled( quoi)

    def slot_bascule_V3(self):
        """ Changement de demande pour format V3 : 
        on grise le groupe Segment et les choix segment
        """ 
        set_quoi = True if self.checkBoxV3.isChecked() else False
                
        if set_quoi == True and self.radioButtonGDAL.isChecked():
            set_ellipse = True
        else:
            set_ellipse = False
        self.lineEditDoubleRayon.setEnabled( set_ellipse)
        self.lineEditDoubleRayon.setEnabled( set_ellipse)
        
        self.checkBoxSegment.setEnabled( set_quoi)
        self.checkBoxSegmentBrise.setEnabled( set_quoi)
        self.checkBoxInterAltitude.setEnabled( set_quoi)
        self.checkBoxInterPasMesure.setEnabled( set_quoi)
        self.checkBoxInterSegment.setEnabled( set_quoi)
        self.checkBoxInterSegmentBrise.setEnabled( set_quoi)

        self.groupBoxSegment.setEnabled( set_quoi)
        self.groupBoxThemaTrace.setEnabled( set_quoi)
        self.groupBoxInterIntraExpert.setEnabled( set_quoi)
            
        # appel des attributs INTRA qui sont Profil dépendant
        self.slot_PROFIL_INTRA_maj_attributs_interpolables( "DYNAMIQUE")
        self.slot_PROFIL_INTRA_maj_triplet_interpolables()

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

    def slot_bascule_sans_contour(self):
        """ Mode sans contour connu : pas de choix de la couche        """ 
        if self.checkBoxContourSolo.isChecked():
            if  self.radioButtonContour.isChecked():
                #Assert
                aText = "Il est impossible de demander de créer un coutour en déclarant que les informations"
                aText = aText + " agronomiques proviennent de contours... Les informations vignobles proviennent"
                aText = aText + " donc de l'Onglet Agronomie"
                physiocap_message_box( self, aText, "information" )
                self.radioButtonOnglet.setChecked(  Qt.Checked)
            self.groupBoxContourInter.setEnabled( False)
            self.checkBoxToutes.setChecked(  Qt.Checked)
        else:
            self.groupBoxContourInter.setEnabled( True)
            self.slot_INTER_liste_parcelles()         
    
    def slot_bascule_onglet_contour(self):
        """ Mode onglet ou contour      """ 
        if  self.radioButtonOnglet.isChecked():
            self.groupBoxVignoble.setEnabled( True)
        else:
            self.groupBoxVignoble.setEnabled( False)
            self.slot_INTER_liste_parcelles()         
            if self.checkBoxContourSolo.isChecked():
                #Assert
                aText = "Il est impossible de demander de créer un coutour en déclarant que les informations"
                aText = aText + " agronomiques proviennent de contours... Les informations vignobles proviennent"
                aText = aText + " donc de l'Onglet Agronomie"
                physiocap_message_box( self, aText, "information" )
                self.radioButtonOnglet.setChecked(  Qt.Checked)

    def slot_bascule_details_vignoble(self):
    # Calcul aide et sortie
        """ Changement de demande pour les details vignoble : 
        on dégrise le groupe Vignoble que si le choix est onglet
        """ 
        # appel des attributs INTRA
        self.slot_PROFIL_INTRA_maj_attributs_interpolables( "DYNAMIQUE")
        self.slot_PROFIL_INTRA_maj_triplet_interpolables()
        if  self.radioButtonOnglet.isChecked():
            self.groupBoxVignoble.setEnabled( True)
        else:
            self.groupBoxVignoble.setEnabled( False)    
            self.slot_INTER_liste_parcelles()
            
    def slot_calcul_densite( self):
        # Densité pied /ha
        interrang  = int( self.spinBoxInterrangs.value())
        intercep   = int( self.spinBoxInterceps.value())
        densite = 0
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

    def slot_AIDE_contrib_alert( self):
        """ Toutes les x utilisations, rappeler à l'utilisateur qu'il est bien de contribuer """
        # Vérifier si le nombre d'utilisation est atteint
        self.dans_Quel_Settings()
        niveau_utilisation = int( self.settings.value("Affichage/Contrib_alert", 0))
        if ( niveau_utilisation <  1000):
            self.settings.setValue("Affichage/Contrib_alert", niveau_utilisation + 1)
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
        """ Quand GPS est choisi, on monte une alerte """
        # Vérifier si le message a déjà été donné
        self.dans_Quel_Settings()
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
            
    def reject( self ):
        """Close when bouton is Cancel"""
        # Todo : V3 prefixe Slot et nommage SLOT_Bouton_Cancel      
        # On sauve les saisies
        self.memoriser_tous_Settings()
        QDialog.reject( self)
                
    def slot_accept( self ):
        """Vérifier les valeurs saisies
         QT confiance et initialisation par Qsettings sert d'assert sur la
         cohérence des variables saisies"""
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
        if self.lineEditSession.text() == "":
            aText = self.tr( "Pas de nom de session Physiocap choisi")
            physiocap_error( self, aText)
            return physiocap_message_box( self, aText)                 
        # Remettre vide le textEditSynthese
        self.textEditSynthese.clear()

        distancearea, EXT_CRS_SHP, EXT_CRS_RASTER, \
        laProjectionCRS, laProjectionTXT, EPSG_NUMBER = quelle_projection_et_lib_demandee( self)
        self.settings.setValue("Expert/laProjection", laProjectionTXT)
        
        # On sauve les affichages et rend les bascules pour traitement
        version_3, consolidation, recursif, details, TRACE_HISTO, pasContour = self.memoriser_tous_Settings()

        if recursif == "YES":
            physiocap_log( self.tr( "La recherche des MID fouille l'arbre de données"), leModeDeTrace)
        if details == "YES":
            physiocap_log( self.tr( "Les détails du vignoble sont précisées"), leModeDeTrace)
        # Onglet Histogramme
        if TRACE_HISTO == "YES":
            self.settings.setValue("Physiocap/histogrammes", TRACE_HISTO)
                   
        # ########################################
        # Gestion de capture des erreurs et du filtre des données brutes Physiocap
        # ########################################
        try:
            filtreur = PhysiocapFiltrer( self)
            # Création des répertoires et des résultats de synthèse
            retour = filtreur.physiocap_creer_donnees_resultats( self, 
                laProjectionCRS,  laProjectionTXT, EXT_CRS_SHP, 
                details, TRACE_HISTO, recursif, version_3)

        except physiocap_exception_rep as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Erreur bloquante lors de la création du répertoire : {0}").\
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
        except physiocap_exception_err_csv as e:
            physiocap_log_for_error( self)
            aText = self.tr( "{0}").format( e)
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        except physiocap_exception_trop_err_csv as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Trop d'erreurs {0} dans les données brutes").\
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
        except physiocap_exception_no_transform as e:
            aText = "{0} Erreur bloquante durant tranformation du SCR : pour la ligne brute numéro {1}". \
                    format ( PHYSIOCAP_STOP,  e)
            physiocap_error( self, aText, "CRITICAL" )
            return physiocap_message_box( self, aText, "information" )
        except physiocap_exception_no_gpkg as e:
            aText = self.tr( "Erreur bloquante : problème lors de recherche du géopackage {0}").\
                format( e)
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        except physiocap_exception_vecteur_type_inconnu as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Erreur bloquante : le format de vecteur {0} n'est pas supporté par l'extension").\
                format( e)
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        except physiocap_exception_calcul_segment_invalid as e:
            physiocap_log_for_error( self)
            aText = self.tr( "Erreur bloquante durant création des segments : {0}").\
                format( e)
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "information" )
        except physiocap_exception_agro_profil as e:
            aText = "Seul le profil {} permet de préciser vos données agronomiques dans un contour. ".format( e)
            aText = aText + "\n" + "Si vous êtes intéressé par cette fonctionnalité, merci de contacter jean@jhemmi.eu. "
            aText = aText + "Sinon, précisez vos informations vignobles dans l'onglet Agronomie et cochez ""{}".\
                format( "Onglet Agronomie détaille mon information du vignoble")
            return physiocap_message_box( self, aText, "information" )        
        except physiocap_exception_agro_obligatoire as e:
            physiocap_log_for_error( self)
            aText = self.tr( "INFORMATIONS AGRO KO : la couche vecteur de votre session ne contient pas un attribut {0}. ").\
                format( e)
            aText = aText +  "\n" + self.tr( "Vérifier le vecteur choisi pour décrire vos contours et vos données AGRO ")
            aText = aText +  "\n" + self.tr( "Une information AGRO n'a pas le nommage attendu ")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "CRITICAL" )
        except physiocap_exception_agro_type_champ as e:
            physiocap_log_for_error( self)
            aText = self.tr( "INFORMATIONS AGRO inconsistentes : l'attribut {0}. ").format( e)
            aText = aText + "\n" + self.tr( "Vérifier si des lignes de données ne sont pas manquantes : vides ou nulles dans votre vecteur AGRO ")
            aText = aText + "\n" + self.tr( "Identifier le vecteur choisi pour décrire vos contours et vos données AGRO ")
            aText = aText + "\n" + self.tr( "Le nom du vecteur AGRO est dans Onglet Calcul" )
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( self, aText, "CRITICAL" )

        except physiocap_exception_stop_user:
            return physiocap_log( \
                self.tr( "Arrêt de {0} à la demande de l'utilisateur").format( PHYSIOCAP_UNI), 
                leModeDeTrace, "Attention")
         # On remonte les autres exceptions
        except:
            raise
        finally:
            pass
        # Fin de capture des erreurs Physiocap
        if ( retour == 0 ):
            self.ButtonInter.setEnabled( True)
            self.ButtonIntra.setEnabled( False)
            physiocap_log( self.tr( "** {0} est prêt pour calcul Inter parcellaire - Onglet Parcelles").\
                format( PHYSIOCAP_UNI), leModeDeTrace)

            # Si OK : chercher à enchainer vers Intra
            if  self.checkBoxTroisActions.isChecked():
                self.slot_INTER_moyennes_parcelles()

        return retour

