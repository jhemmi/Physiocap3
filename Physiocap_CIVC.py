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

from .Physiocap_tools import ( physiocap_log, physiocap_error, 
    physiocap_quelles_informations_vignoble_agro, \
    physiocap_quelle_projection_et_lib_demandee, physiocap_segment_vers_vecteur ) 
from .Physiocap_var_exception import *

#from PyQt5.QtCore import QVariant
from qgis.core import ( Qgis, QgsCoordinateReferenceSystem, QgsCoordinateTransform,  \
        QgsPointXY, QgsMessageLog, QgsProcessingFeedback, QgsProject, QgsVectorLayer)

try :
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.use('Qt4Agg')

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

def generer_contour_depuis_points(self, nom_fichier_shape_sans_0):
    """ Générer un Contour à partir des points sans Zéro"""
    # Vérifier disponibilité de processing (on attend d'etre dans Intra)
    try :
        import processing
    except ImportError:
        physiocap_log( self.tr( "{0} nécessite l'extension {1}").\
                format( PHYSIOCAP_UNI, self.tr("Traitement")), leModeDeTrace)
        raise physiocap_exception_no_processing( "Pas d'extension Traitement")
    
    # Assert points existent bien
    if ( os.path.exists( nom_fichier_shape_sans_0)):
        infoVignobleAgro = physiocap_quelles_informations_vignoble_agro( self)
        physiocap_log( "Information vignoble et agro == Nom de parcelle {}".\
            format( infoVignobleAgro[ "nom_parcelle"]))
#        type_apports = self.settings.value("Physiocap/type_apports","xx")  # ___recuperer les valeurs des variables : type apports fertilisation
#        produit = self.settings.value("Physiocap/produit", "xx")  # ___recuperer les valeurs des variables : produit
#        dose = self.settings.value("Physiocap/dose", "xx")  # ___recuperer les valeurs des variables : dose(t/ha)
#        strategie_entretien_sol = self.settings.value("Physiocap/strategie_entretien_sol", "xx")  # ___recuperer les valeurs des variables : strategie entretien de sol
#        etat_sanitaire = self.settings.value("Physiocap/etat_sanitaire","xx")  # ___recuperer les valeurs des variables : etat sanitaire intensité*frequance
#        cepage = self.settings.value("Physiocap/leCepage2","xx")  # ___recuperer les valeurs des variables : etat sanitaire intensité*frequance
#        hauteur_rognage = self.settings.value("Physiocap/hauteur", "xx")  # ___recuperer les valeurs des variables : etat sanitaire intensité*frequance
#        densite_plantation = self.settings.value("Physiocap/densite", "xx")  # ___recuperer les valeurs des variables : etat sanitaire intensité*frequance
#        type_taille = self.settings.value("Physiocap/laTaille", "xx")  # ___recuperer les valeurs des variables : etat sanitaire intensité*frequance
#        diamshp_moy = self.settings.value("Physiocap/diamshp_moy","xx")  # ___recuperer les valeurs des variables : diametre moyen
#        nbsarmshp_moy = self.settings.value("Physiocap/nbsarmshp_moy","xx")  # ___recuperer les valeurs des variables : nbsarmshp moyen
#        biomshp_moy = self.settings.value("Physiocap/biomshp_moy", "xx")  # ___recuperer les valeurs des variables : biomshp moyen
#        vitesseshp_moy = self.settings.value("Physiocap/vitesseshp","xx")  # ___recuperer les valeurs des varoables : vitesse moyenne
#        generer_contour = self.settings.value("Physiocap/generer_contour","xx")  # ___recuperer les valeurs des varoables : vitesse moyenne
        chemin_acces = os.path.dirname( nom_fichier_shape_sans_0)
        chemin_fichier_convex = os.path.join( chemin_acces,  FICHIER_CONTOUR_GENERE + EXTENSION_SHP)
        mon_feedback = QgsProcessingFeedback()
        params_algo = { 'FIELD' : None, 
         'INPUT' : nom_fichier_shape_sans_0, 
         'OUTPUT' : chemin_fichier_convex, 
         'TYPE' : 3 } # Enveloppe convexe
        textes_sortie_algo={}
        algo = "qgis:minimumboundinggeometry"
        textes_sortie_algo = processing.run( algo, params_algo, feedback=mon_feedback)        
        physiocap_log( "Sortie algo {} contient {}".\
            format( algo, textes_sortie_algo))
        
        self.settings.setValue("Physiocap/chemin_contour_genere", chemin_fichier_convex)
    else:
        msg = "Erreur durant génération automatique de contour : fichier de point {} n'existe pas\n".\
            format( nom_fichier_shape_sans_0)
        physiocap_error( self, msg )
        err.write( str( msg) ) # on écrit la ligne dans le fichier ERREUR
    return chemin_fichier_convex


def inclure_vignoble_sur_contour(self, chemin_fichier_convex, ss_groupe=None):

    if ( os.path.exists( chemin_fichier_convex)):

    ###    geom_wkt = ""

        # delete fields and leave just the geometry
    ###    fields = convexhull_layer.dataProvider().fields()
        count = 0
        fieldsList = list()
        for field in convexhull_layer.pendingFields():
            fieldsList.append(count)
            count += 1
        convexhull_layer.dataProvider().deleteAttributes(fieldsList)
        convexhull_layer.updateFields()
        # add the layer to the legend
        convexhull_layer.setLayerTransparency(60)
        QgsMapLayerRegistry.instance().addMapLayer(convexhull_layer, False)
        ss_groupe.addLayer(convexhull_layer)
        # iface.addVectorLayer(chemin_fichier_convex, 'contour_genere', 'ogr')
        # get the geometry from the layer and paste it in the csv file
        for feature in convexhull_layer.getFeatures():
            buff = feature.geometry().buffer(0.5, 1)
            convexhull_layer.dataProvider().changeGeometryValues({feature.id(): buff})
###        geom_wkt = str(feature.geometry().exportToWkt())

###            # add attributes filled by the user
###            convexhull_layer.startEditing()
###
###            convexhull_layer.dataProvider().addAttributes([QgsField("Nom_Parcel", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Commune", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Region", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Cepage", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Clone", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Porte_gref", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Annee_plan", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Haut_rogn", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Dens_plan", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Type_tail", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Sol_argile", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Sol_MO", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Sol_CaCo3", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Rendement", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Poi_m_grap", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Nb_grap", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Rend_an-1", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Poi_m_gra1", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Nbgrap-1", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("type_appor", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Fert_prod", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Fert_dose", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("entr_sol", QVariant.String)])
###            convexhull_layer.dataProvider().addAttributes([QgsField("Etat_sanit", QVariant.String)])
###
###            convexhull_layer.updateFields()
###
###            for feat in convexhull_layer.getFeatures():
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Nom_Parcel'),
###                                                      nom_parcelle.encode("Utf-8"))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Commune'),
###                                                      comuune.encode("Utf-8"))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Region'),
###                                                      region.encode("Utf-8"))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Cepage'),
###                                                      cepage.encode("Utf-8"))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Clone'),
###                                                      clone.encode("Utf-8"))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Porte_gref'),
###                                                      str(porte_greffe.encode("Utf-8")))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Annee_plan'),
###                                                      str(annee_plant))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Haut_rogn'),
###                                                      str(hauteur_rognage))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Dens_plan'),
###                                                      str(densite_plantation))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Type_tail'),
###                                                      type_taille.encode("Utf-8"))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Sol_argile'),
###                                                      str(sol_argile))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Sol_MO'),
###                                                      str(sol_mo))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Sol_CaCo3'),
###                                                      str(sol_caco3))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Rendement'),
###                                                      str(rendement))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Poi_m_grap'),
###                                                      str(poids_moy_grappes))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Nb_grap'),
###                                                      str(nb_grappes))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Rend_an-1'),
###                                                      str(rendement_1))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Poi_m_gra1'),
###                                                      str(poids_moy_grappes_1))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Nbgrap-1'),
###                                                      str(nb_grappes_1))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('type_appor'),
###                                                      str(type_apports.encode("Utf-8")))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Fert_prod'),
###                                                      str(produit.encode("Utf-8")))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Fert_dose'),
###                                                      str(dose))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('entr_sol'),
###                                                      str(strategie_entretien_sol.encode("Utf-8")))
###                convexhull_layer.changeAttributeValue(feat.id(), convexhull_layer.fieldNameIndex('Etat_sanit'),
###                                                      str(etat_sanitaire.encode("Utf-8")))
###
###            convexhull_layer.commitChanges()
        # get the feature geometry and copy the WKT
        # ecriture de l'entête
        # fichier_synthese_CSV.write("Nom_Parcelle; Commune ; Region ; Cepage; Clone; Porte_greffe; Annee_plantation; Hauteur_rognage; Densite_plantation; Type_taille; Sol_argile; Sol_MO; Sol_CaCo3; Rendement; Poids_moyen_grappes; Nombre_grappes; Rendemenr_annee-1; Poids_moyen_grappes-1; Nombre_grappes-1; Fert_type_apports; Fert_produit; Fert_dose; Strategie_entretien_sol; Etat_sanitaire; Nb_sarments_moy; Section_moy; Biomasse_moy "+"\n")
    else:
        msg = "Erreur durant génération automatique de contour : fichier de point {} n'existe pas\n".\
            format( nom_fichier_shape_sans_0)
        physiocap_error( self, msg )
        err.write( str( msg) ) # on écrit la ligne dans le fichier ERREUR
    return chemin_fichier_convex

# Fonction pour créer les fichiers histogrammes    
def physiocap_fichier_histo( self, src, histo_diametre, histo_nbsarment, histo_vitesse,  err):
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
                    histo_vitesse.write("%f%s" %(XY[7],";"))                
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
    return

def physiocap_tracer_histo(src, name, min=0, max =28, labelx = "Lab X", labely = "Lab Y", titre = "Titre"):
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
    #physiocap_log( "Histo liste {0} ".format( XY), TRACE_TOOLS)
    #plt.hist( XY, bins=classes, normed=1, facecolor='green', alpha=0.75) 
    plt.hist( XY, bins=classes, density=1, facecolor='green', alpha=0.75) 
    plt.xlabel(labelx)
    plt.ylabel(labely)
    plt.title(titre)
    plt.xlim((min, max))
    plt.grid(True)
    plt.savefig(name)
    #print("avant show Histo")
    #plt.ion()
    plt.show( block = 'false')
    #print("apres show Histo")
    plt.close()
    return

def physiocap_ferme_csv( csv_sans_0, csv_avec_0, csv_0_seul, diametre_filtre, erreur, csv_concat):
    """ Fermeture des fichiers de filtration """
    csv_sans_0.close()
    csv_avec_0.close()
    csv_0_seul.close()
    diametre_filtre.close()
    erreur.close()
    # Fermerture du fichier source
    csv_concat.close()   
    return

# Fonction de filtrage et traitement des données
def physiocap_filtrer(self,  src, csv_sans_0, csv_avec_0, csv_0_seul,
    nom_dir_segment, nom_session, chemin_session, 
    diametre_filtre, nom_fichier_synthese, err, 
    mindiam, maxdiam, max_sarments_metre, 
    segment_mini_vitesse,  segment_maxi_vitesse,  segment_mini_point, segment_max_pdop, 
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

    # Récuperer le CRS choisi, les extensions et le calculateur de distance
    distancearea, EXT_CRS_SHP, EXT_CRS_PRJ, EXT_CRS_RASTER, \
    laProjectionCRS, laProjectionTXT, EPSG_NUMBER = \
            physiocap_quelle_projection_et_lib_demandee( self)

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

            # Puis on transforme les WGS84 (du capteur) en L93 (probablement utile)
            # TODO: ?V3.x autres EPSG ? et eviter cet appel dans la boucle
            crsDest = QgsCoordinateReferenceSystem.fromEpsgId( EPSG_NUMBER_L93)   # Lambert 93
            crsSrc = QgsCoordinateReferenceSystem.fromEpsgId( EPSG_NUMBER_GPS)  # WGS 84
            transformer = QgsCoordinateTransform()
            transformer.setSourceCrs( crsSrc)
            transformer.setDestinationCrs( crsDest)
            if not transformer.isValid():
                raise physiocap_exception_no_transform( numero_point)

            # On assure la tranformation par compatibilité du CVS en GPS et L93
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
            aMsg = "{0} Erreur bloquante durant tranformation SCR : pour la ligne brute numéro {1}". \
                format ( PHYSIOCAP_STOP,  numero_point)
            physiocap_error( self, aMsg )
            err.write( aMsg) # on écrit la ligne dans le fichier ERREUR
            # monter directemenr exception
            raise

        # TODO: ?V3.x marquer les points à conserver (non filtré et dans un segment)
        # pour creer un 4eme csv POINTS_VALIDES
        # ce qui reste compliqué pour les segments courts que je ne connais pas encore

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
                # TODO: ?V3.y passage en 3D mettre en Z la dérive
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

                # Quand vitesse plus de 2.5 et moins de 8 et pdop reste cohérent segment_max_pdop
                if XY[7] >= segment_mini_vitesse and XY[7] < segment_maxi_vitesse and XY[5] < segment_max_pdop:
                    # on est en vitesse de croisière                        
                    # Calcul de la distance théorique par rapport au precedent
                    # Introduire un calcul de distance length et l'azimuth
                    le_point_precedent = QgsPointXY( precedent[0] ,  precedent[1])
                    ma_distance = distancearea.measureLine( le_point_projete, le_point_precedent)
                    mon_azimuth = le_point_projete.azimuth( le_point_precedent)
                    # TODO: ?V3.y Traiter l'azimuth depuis le début du segment

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
                            physiocap_log("{0} DECOUPAGE point {1} : vitesse {2:.1f} alors que min est {3:.1f}! ".\
                            format(PHYSIOCAP_WARNING, numero_point, XY[7],  segment_mini_vitesse), \
                            TRACE_SEGMENT_DECOUPES)                           
                    if XY[7] > segment_maxi_vitesse:
                        if  len(segment_en_cours) > 0:
                            physiocap_log("{0} DECOUPAGE point {1} : vitesse {2:.1f} que max est {3:.1f}! ".\
                            format(PHYSIOCAP_WARNING, numero_point, XY[7],  segment_maxi_vitesse), \
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
                        # Vérifier les gid_sans_mesure
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
            raise physiocap_exception_err_csv( nom_court_csv_concat)

    if version_3 == "NO":
        vecteur_segment = None
        vecteur_segment_brise = None
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
        vecteur_segment = physiocap_segment_vers_vecteur( self, chemin_session, nom_dir_segment,  nom_session, 
            mes_lignes_sans_coupure,  info_lignes_sans_coupure, version_3)
        vecteur_segment_brise = physiocap_segment_vers_vecteur( self, chemin_session, nom_dir_segment,  nom_session,
            mes_lignes_sans_coupure,  info_lignes_sans_coupure, version_3,  "BRISE")

    physiocap_log( "{0} {1} Fin du filtrage OK des {2} lignes.". \
        format( PHYSIOCAP_INFO, PHYSIOCAP_UNI, str(numero_point - 1)), leModeDeTrace)

    return vecteur_segment, vecteur_segment_brise
