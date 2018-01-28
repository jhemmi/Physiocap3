# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Physiocap_inter
                                 A QGIS 3 plugin
 Physiocap3 plugin helps analyse raw data from Physiocap in QGIS 3 and 
 creates a synthesis of Physiocap measures' campaign
 Physiocap3 plugin permet l'analyse les données brutes de Physiocap dans QGIS 3 et
 crée une synthese d'une campagne de mesures Physiocap
 
 Le module Inter gère la création des moyennes inter parcellaire
 à partir d'un shapefile de contour de parcelles et l'extration des points de
 chaque parcelle 

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
        physiocap_rename_existing_file,  \
        physiocap_quelle_projection_demandee, \
        physiocap_create_projection_file, \
        physiocap_get_layer_by_URI,  physiocap_get_layer_by_ID

from .Physiocap_var_exception import *

from PyQt5 import QtWidgets
from PyQt5.QtCore import QVariant
from qgis.core import (QgsProject, QgsDistanceArea, QgsVectorLayer, \
    QgsLayerTreeGroup, QgsLayerTreeLayer,\
    QgsFeatureRequest, QgsFields, QgsField, QgsVectorFileWriter, QgsFeature,\
    QgsPointXY, QgsGeometry, QgsWkbTypes, QgsMessageLog)
try :
    import numpy as np
except ImportError:
    aText ="Erreur bloquante : module numpy n'est pas accessible" 
    QgsMessageLog.logMessage( aText, "\u03D5 Erreurs", QgsMessageLog.WARNING)
    QgsMessageLog.logMessage( aText, PHYSIOCAP_LOG_ERREUR, QgsMessageLog.WARNING)


def physiocap_vector_type( self, vector):
    """Vérifie le type de forme du vector : on simplifie au cas multiple pour Wbk et """

    try:
        # A_TESTER: V3 ? vérifier multiType couvre plus de cas
        # et cas vecteur non shape
        geomWkbType = vector.wkbType()
        geomWkbMultiType = QgsWkbTypes.multiType( geomWkbType) # multiple sous processing
        geomType = QgsWkbTypes.geometryType( geomWkbType) 
        geomTypeText = QgsWkbTypes.geometryDisplayString( geomType)
        geomWkbTypeText = QgsWkbTypes.displayString( geomWkbType)
        
        # physiocap_log( "-- Vector Text {0} type geom {1} et WkbType {2}".\
        #    format( geomTypeText, geomType,  geomWkbType), TRACE_TOOLS)
        return geomTypeText, geomWkbTypeText, geomWkbType,  geomWkbMultiType  
    except:
        physiocap_error( self, self.tr("Warning : couche (layer) {0} n'est ni (is nor) point, ni (nor) polygone").\
            format( vector.id()))
        pass
        # On evite les cas imprévus
        return "Inconnu", "WkbInconnu",  None,  None
                    

 
def physiocap_fill_combo_poly_or_point( self, isRoot = None, node = None ):
    """ Recherche dans l'arbre Physiocap (recursif)
    les Polygones,
    les Points de nom DIAMETRE qui correspondent au données filtreés
    Remplit deux listes pour le comboxBox des vecteurs "inter Parcellaire"
    Rend aussi le nombre de poly et point retrouvé
    """
    leModeDeTrace = self.fieldComboModeTrace.currentText() 
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

    #physiocap_log( "- noeud en cours {0}".format( noeud_en_cours), TRACE_TOOLS))        

    # On descend de l'arbre par la racine
    for child in noeud.children():
        #physiocap_log( "-- in noeud : comment connaitre le type ?", TRACE_TOOLS))        
        if isinstance( child, QgsLayerTreeGroup):
            #physiocap_log( "--Group: " + child.name(), TRACE_TOOLS))
            noeud_en_cours = child.name()
            groupe_inter = noeud_en_cours + SEPARATEUR_ + VIGNETTES_INTER
            #physiocap_log( "--Group inter : " + groupe_inter, TRACE_TOOLS))
            if ( noeud_en_cours != groupe_inter ):
                # On exclut les vignettes INTER : sinon on descend dans le groupe
                un_nombre_poly, un_nombre_point = physiocap_fill_combo_poly_or_point( self, noeud, child)
                nombre_point = nombre_point + un_nombre_point
                nombre_poly = nombre_poly + un_nombre_poly
        elif isinstance( child, QgsLayerTreeLayer):
#            physiocap_log( "--Layer >> {0}  ID>> {1} ". \
#                format( child.name(),  child.layerId()), TRACE_TOOLS)) 
#           physiocap_log( "--Layer parent le groupe >> " + child.parent().name() , TRACE_TOOLS)) 
            # Tester si poly ou point
            type_layer,  type_Wkb_layer,  numero_Wkb_layer,  numero_Multi_Wkb = \
                physiocap_vector_type( self, child.layer())
#            physiocap_log( "--Layer a pour type >> {0} WkbType  >> {1} et numero_Wkb  >> {2} ".\
#            format( type_layer,  type_Wkb_layer,  numero_Wkb_layer), TRACE_TOOLS))
            if ( type_layer == "Point"):
                if (((not self.checkBoxConsolidation.isChecked()) and \
                    ( child.name() == "DIAMETRE mm")) \
                    or \
                    ((self.checkBoxConsolidation.isChecked()) and \
                    ( child.parent().name() == CONSOLIDATION))):
                    #physiocap_log( "- layer: " + child.name() + "  ID: " + child.layerId(), TRACE_TOOLS)) 
                    node_layer = noeud_en_cours + SEPARATEUR_NOEUD + child.layerId()
                    # A_TESTER : physiocap_log( "- group: type node_layer " + str( type( node_layer)), TRACE_TOOLS))
                    self.comboBoxPoints.addItem( node_layer)
                    nombre_point = nombre_point + 1
            elif ( type_layer == "Polygon"):
                node_layer = child.name() + SEPARATEUR_NOEUD + child.layerId()        
                self.comboBoxPolygone.addItem( node_layer)
                nombre_poly = nombre_poly + 1
            elif ( type_layer == "Line"):
                pass # cas de segments
            else:
                physiocap_log( "- Layer de type {0} rejeté : {1} ID: ".\
                    format( type_layer, child.name(),  child.layerId()), leModeDeTrace) 
    return nombre_poly, nombre_point

              
def physiocap_moyenne_un_contour( laProjectionCRS, EPSG_NUMBER, nom_vignette, nom_prj,
        geom_poly, la_surface, un_nom, un_autre_ID, date_debut, date_fin,
        nombre_points, le_taux_de_sans_mesure, le_nombre_segment, longueur_moyenne_segment, 

        moyennes_point, ecarts_point, medianes_point, 
        version_3 = "NO", details = "NO"):
    """ Creation d'une vignette nommé un_nom avec les moyennes
        qui se trouvent dans le dic "moyenne_point" :
        moyenne_vitesse, moyenne_sar, moyenne_dia 
        moyennes des nombres de sarments / Metre
        moyennes du diametre
        et depuis 1.8 les ecarts dans dic "ecarts_point" et medianes "medianes_point"
        Il s'agit d'un seul polygone
    """
    # Prépare les attributs
    les_champs = QgsFields()
    les_champs.append( QgsField( "GID", QVariant.Int, "integer", 10))
    les_champs.append( QgsField( "NOM_PHY", QVariant.String, "string", 25))
    les_champs.append( QgsField( "ID_PHY", QVariant.String, "string", 15))
    les_champs.append( QgsField( "MESURE_HA", QVariant.Double, "double", 10,1))           
    if version_3 == "YES":
        les_champs.append( QgsField( "0_MESURE", QVariant.Double, "double", 10,1))           
        les_champs.append( QgsField( "NB_SEG", QVariant.Double, "double", 10,1))           
        les_champs.append( QgsField( "LEN_SEG", QVariant.Double, "double", 10,1))           

    les_champs.append( QgsField( "NBSARM",  QVariant.Double, "double", 10,2))
    les_champs.append( QgsField( "M_NBSARM",  QVariant.Double, "double", 10,2))
    les_champs.append( QgsField( "E_NBSARM",  QVariant.Double, "double", 10,2))
    les_champs.append( QgsField( "DIAM",  QVariant.Double, "double", 10,2))
    les_champs.append( QgsField( "M_DIAM",  QVariant.Double, "double", 10,2))
    les_champs.append( QgsField( "E_DIAM",  QVariant.Double, "double", 10,2))
    les_champs.append( QgsField( "BIOM", QVariant.Double,"double", 10,2))
    les_champs.append( QgsField( "M_BIOM", QVariant.Double,"double", 10,2))
    les_champs.append( QgsField( "E_BIOM", QVariant.Double,"double", 10,2))
    if version_3 == "YES":
        les_champs.append( QgsField("ALTITUDE", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("M_ALTI", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("E_ALTI", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("PDOP", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("M_PDOP", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("E_PDOP", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("DISTANCE", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("M_DIST", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("E_DIST", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("DERIVE", QVariant.Double, "double", 10,1))
        les_champs.append( QgsField("M_DERIVE", QVariant.Double, "double", 10,1))
        les_champs.append( QgsField("E_DERIVE", QVariant.Double, "double", 10,1))
    if details == "YES":
        # Niveau de detail demandé
        les_champs.append( QgsField( "BIOMGM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "M_BIOMGM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "E_BIOMGM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "BIOMGCEP", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "M_BIOMGCEP", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "E_BIOMGCEP", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "BIOMM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "M_BIOMM2", QVariant.Double,"double", 10,2))        
        les_champs.append( QgsField( "E_BIOMM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "NBSARMM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "M_NBSARMM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "E_NBSARMM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "NBSARCEP", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "M_NBSARCEP", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "E_NBSARCEP", QVariant.Double,"double", 10,2))
        
    les_champs.append( QgsField( "VITESSE", QVariant.Double, "double", 10,2))
    les_champs.append( QgsField( "M_VITESSE", QVariant.Double, "double", 10,2))
    les_champs.append( QgsField( "E_VITESSE", QVariant.Double, "double", 10,2))
    les_champs.append( QgsField( "DEBUT", QVariant.String, "string", 25))
    les_champs.append( QgsField( "FIN", QVariant.String, "string", 25))    
    les_champs.append( QgsField( "SURF_HA", QVariant.Double, "double", 10,4))
    les_champs.append( QgsField( "NOMBRE", QVariant.Int, "int", 10))           

    # Creation du Shape
    writer = QgsVectorFileWriter( nom_vignette, "utf-8", les_champs, 
        QgsWkbTypes.MultiPolygon, laProjectionCRS , "ESRI Shapefile")

    feat = QgsFeature()
    feat.setGeometry( QgsGeometry.fromMultiPolygonXY(geom_poly.asMultiPolygon())) #écrit la géométrie tel que lu dans shape contour

    if details == "YES":
        if version_3 == "YES":
            # Ecrit tous les attributs avec V3
            feat.setAttributes( [ 1, un_nom, un_autre_ID, nombre_points/la_surface,
                le_taux_de_sans_mesure, le_nombre_segment, longueur_moyenne_segment, 
                moyennes_point.get( 'sarm'),    medianes_point.get( 'sarm'),    ecarts_point.get( 'sarm'), 
                moyennes_point.get( 'diam'),    medianes_point.get( 'diam'),    ecarts_point.get( 'diam'),
                moyennes_point.get( 'biom'),    medianes_point.get( 'biom'),    ecarts_point.get( 'biom'),
                
                moyennes_point.get( 'altitude'),medianes_point.get( 'altitude'),ecarts_point.get( 'altitude'),
                moyennes_point.get( 'pdop'),medianes_point.get( 'pdop'),ecarts_point.get( 'pdop'),
                moyennes_point.get( 'distance'),medianes_point.get( 'distance'),ecarts_point.get( 'distance'),
                moyennes_point.get( 'derive'),  medianes_point.get( 'derive'),  ecarts_point.get( 'derive'),
                
                moyennes_point.get( 'biomgm2'), medianes_point.get( 'biomgm2'),    ecarts_point.get( 'biomgm2'),
                moyennes_point.get( 'biomgcep'),medianes_point.get( 'biomgcep'),   ecarts_point.get( 'biomgcep'),  
                moyennes_point.get( 'biomm2'),  medianes_point.get( 'biomm2'),     ecarts_point.get( 'biomm2'),
                moyennes_point.get( 'nbsarmm2'),medianes_point.get( 'nbsarmm2'),   ecarts_point.get( 'nbsarmm2'), 
                moyennes_point.get( 'nbsarcep'),medianes_point.get( 'nbsarcep'),   ecarts_point.get( 'nbsarcep'),
      
                moyennes_point.get( 'vitesse'), medianes_point.get( 'vitesse'), ecarts_point.get( 'vitesse'),
                date_debut, date_fin, la_surface, nombre_points
                ])
        else:
            # Ecrit tous les attributs de V2
            feat.setAttributes( [ 1, un_nom, un_autre_ID, int( nombre_points/la_surface),
                moyennes_point.get( 'sarm'),    medianes_point.get( 'sarm'),    ecarts_point.get( 'sarm'), 
                moyennes_point.get( 'diam'),    medianes_point.get( 'diam'),    ecarts_point.get( 'diam'),
                moyennes_point.get( 'biom'),    medianes_point.get( 'biom'),    ecarts_point.get( 'biom'),
                moyennes_point.get( 'biomgm2'), medianes_point.get( 'biomgm2'),    ecarts_point.get( 'biomgm2'),
                moyennes_point.get( 'biomgcep'),medianes_point.get( 'biomgcep'),   ecarts_point.get( 'biomgcep'),  
                moyennes_point.get( 'biomm2'),  medianes_point.get( 'biomm2'),     ecarts_point.get( 'biomm2'),
                moyennes_point.get( 'nbsarmm2'),medianes_point.get( 'nbsarmm2'),   ecarts_point.get( 'nbsarmm2'), 
                moyennes_point.get( 'nbsarcep'),medianes_point.get( 'nbsarcep'),   ecarts_point.get( 'nbsarcep'),
      
                moyennes_point.get( 'vitesse'), medianes_point.get( 'vitesse'), ecarts_point.get( 'vitesse'),
                date_debut, date_fin, la_surface, nombre_points
                ])
    else:
        if version_3 == "YES":
            # Ecrit tous les attributs avec V3
            feat.setAttributes( [ 1, un_nom, un_autre_ID, nombre_points/la_surface,
                le_taux_de_sans_mesure, le_nombre_segment, longueur_moyenne_segment, 
                moyennes_point.get( 'sarm'),    medianes_point.get( 'sarm'), ecarts_point.get( 'sarm'), 
                moyennes_point.get( 'diam'),    medianes_point.get( 'diam'), ecarts_point.get( 'diam'),
                moyennes_point.get( 'biom'),    medianes_point.get( 'biom'), ecarts_point.get( 'biom'),

                moyennes_point.get( 'altitude'),medianes_point.get( 'altitude'),ecarts_point.get( 'altitude'),
                moyennes_point.get( 'pdop'),medianes_point.get( 'pdop'),ecarts_point.get( 'pdop'),
                moyennes_point.get( 'distance'),medianes_point.get( 'distance'),ecarts_point.get( 'distance'),
                moyennes_point.get( 'derive'),  medianes_point.get( 'derive'),  ecarts_point.get( 'derive'),
                
                moyennes_point.get( 'vitesse'), medianes_point.get( 'vitesse'), ecarts_point.get( 'vitesse'),
                date_debut, date_fin, la_surface, nombre_points
                ])

        else:
            # Ecrit les premiers attributs
            feat.setAttributes( [ 1, un_nom, un_autre_ID, int( nombre_points/la_surface),
                moyennes_point.get( 'sarm'),    medianes_point.get( 'sarm'), ecarts_point.get( 'sarm'), 
                moyennes_point.get( 'diam'),    medianes_point.get( 'diam'), ecarts_point.get( 'diam'),
                moyennes_point.get( 'biom'),    medianes_point.get( 'biom'), ecarts_point.get( 'biom'),
                 
                moyennes_point.get( 'vitesse'), medianes_point.get( 'vitesse'), ecarts_point.get( 'vitesse'),
                date_debut, date_fin, la_surface, nombre_points
                ])
   # Ecrit le feature
    writer.addFeature( feat)
    
    # PRJ file
    physiocap_create_projection_file( nom_prj, EPSG_NUMBER)  
    return 0
    
    

def physiocap_segment_tous_contours( laProjectionCRS, EPSG_NUMBER, 
                nom_segment, nom_prj,
                toutes_les_geoms_segment, les_infos_segment, 
                segment_simplifie="YES"):

    """ Creation d'un shape de points sans mesure se trouvant dans tous les contours
    """
    # Prepare les attributs
    les_champs = QgsFields()
    les_champs.append( QgsField("GID", QVariant.Int, "integer", 10))
    les_champs.append( QgsField("GID_10", QVariant.Int, "integer", 10))
    les_champs.append( QgsField("NB_PTS_INI", QVariant.Int, "integer", 10))
    les_champs.append( QgsField("NB_POINTS", QVariant.Int, "integer", 10))
    les_champs.append( QgsField("DATE_DEB", QVariant.String, "string", 25))
    les_champs.append( QgsField("DATE_FIN", QVariant.String, "string", 25))

    # Creation du Shape
    writer = QgsVectorFileWriter( nom_segment, "utf-8", les_champs, 
        QgsWkbTypes.MultiLineString, laProjectionCRS , "ESRI Shapefile")

    for i in range( 0, len( toutes_les_geoms_segment)):
        for j in range( 0, len( toutes_les_geoms_segment[i])): 
            gid_modulo_10 = les_infos_segment[i]["GID"][j] % 10
            nombre = les_infos_segment[i]["NB_PTS_INI"][j]
            nombre_points = les_infos_segment[i]["NB_POINTS"][j]
            feat = QgsFeature()
            if (segment_simplifie == "YES"):   # Premier et dernier 
                feat.setGeometry( QgsGeometry.fromPolylineXY( [ 
                    toutes_les_geoms_segment[ i][ j][0], 
                    toutes_les_geoms_segment[ i][ j][nombre_points-1]
                    ] )) #écrit la géométrie
            else:  # Tous les poins
                feat.setGeometry( QgsGeometry.fromPolylineXY( toutes_les_geoms_segment[ i][ j] )) #écrit la géométrie            
            feat.setAttributes([ les_infos_segment[i]["GID"][j], gid_modulo_10, 
                                nombre, nombre_points,  les_infos_segment[i]["DATE_DEB"][j], 
                                les_infos_segment[i]["DATE_FIN"][j]
                                ])
            # Ecrit le feature
            writer.addFeature( feat)

    # PRJ file
    physiocap_create_projection_file( nom_prj, EPSG_NUMBER)  
    
    return 0

def physiocap_segments_un_contour( laProjectionCRS, EPSG_NUMBER, nom_segment, nom_segment_prj, 
                        les_geoms_segment, les_dates_debut_segment, les_dates_fin_segment, 
                        les_GID, les_nombres_points_segment, les_nombres_points_restant, 
                        segment_simplifie="YES"):

    """ Creation d'un shape des segments se trouvant dans le contour
    """
    # Prepare les attributs
    les_champs = QgsFields()
    les_champs.append( QgsField("GID", QVariant.Int, "integer", 10))
    les_champs.append( QgsField("GID_10", QVariant.Int, "integer", 10))
    # C'est le NB_POINTS du segment filtre qui devient NB_PTS_INI
    les_champs.append( QgsField("NB_PTS_INI", QVariant.Int, "integer", 10))
    les_champs.append( QgsField("NB_POINTS", QVariant.Int, "integer", 10))
    les_champs.append( QgsField("DATE_DEB", QVariant.String, "string", 25))
    les_champs.append( QgsField("DATE_FIN", QVariant.String, "string", 25))

    # Creation du Shape
    writer = QgsVectorFileWriter( nom_segment, "utf-8", les_champs, 
        QgsWkbTypes.MultiLineString, laProjectionCRS , "ESRI Shapefile")

    # Ecriture du shp
    numero_ligne = 0
    for un_segment  in les_geoms_segment:
        feat = QgsFeature()
        
        le_gid = les_GID[numero_ligne]
        gid_modulo_10 = le_gid % 10
        nombre_inter = les_nombres_points_restant[numero_ligne]
        nombre_points_initiaux = les_nombres_points_segment[numero_ligne]
        # ASSERT sur nombre de points intérieurs et longuur du segment
        if len( un_segment) != nombre_inter:
            message = " - ASSERT GID {0} longueur segment {1} différent du nombre points {2} interieurs au contour  - ". \
                format( le_gid, len( un_segment), nombre_inter )
            raise physiocap_exception_segment_invalid( message)
        physiocap_log( "INTER un contour : segment {0} Nombre de points dans le segment >> {1}  et nb de points restant >> {2} ". \
                format( le_gid,  nombre_points_initiaux,   nombre_inter),  TRACE_SEGMENT) 
        if (segment_simplifie == "YES"):   # Premier et dernier 
            feat.setGeometry( QgsGeometry.fromPolylineXY( [ un_segment[0], un_segment[nombre_inter-1]] )) #écrit la géométrie
        else:  # Tous les poins
            feat.setGeometry( QgsGeometry.fromPolylineXY( un_segment )) #écrit la géométrie            
        feat.setAttributes([ le_gid, gid_modulo_10, 
                                nombre_points_initiaux, nombre_inter, 
                                les_dates_debut_segment[numero_ligne], 
                                les_dates_fin_segment[numero_ligne]
                                ])
        numero_ligne = numero_ligne + 1
        # Ecrit le feature
        writer.addFeature( feat)

    # PRJ file
    physiocap_create_projection_file( nom_segment_prj, EPSG_NUMBER)  
    
    return 0

 
def physiocap_sans_mesure_tous_contours( laProjectionCRS, EPSG_NUMBER, nom_sans_mesure, nom_prj,
                toutes_les_geoms_sans_mesure, les_infos_sans_mesure):
    """ Creation d'un shape de points sans mesure se trouvant dans tous les contours
    """
    # Prepare les attributs
    les_champs = QgsFields()
    les_champs.append( QgsField( "GID", QVariant.Int, "integer", 10))
    les_champs.append( QgsField( "DATE", QVariant.String, "string", 25))
    les_champs.append( QgsField("VITESSE", QVariant.Double, "double", 10,2))
    les_champs.append(QgsField("ALTITUDE", QVariant.Double,"double", 10,2)) 
    les_champs.append(QgsField("PDOP", QVariant.Double,"double", 10,2)) 

    # Creation du Shape
    writer = QgsVectorFileWriter( nom_sans_mesure, "utf-8", les_champs, 
        QgsWkbTypes.Point, laProjectionCRS , "ESRI Shapefile")


    for i in range( 0, len( toutes_les_geoms_sans_mesure)):
        for j in range( 0, len( toutes_les_geoms_sans_mesure[i])): 
            feat = QgsFeature()
                                
            feat.setGeometry( QgsGeometry.fromPointXY( toutes_les_geoms_sans_mesure[ i][ j])) #écrit la géométrie tel que lu dans shape contour
            feat.setAttributes( [ les_infos_sans_mesure[ i]["GID"][ j],
                les_infos_sans_mesure[ i]["DATE"][ j], les_infos_sans_mesure[ i]["VITESSE"][ j],
                les_infos_sans_mesure[ i]["ALTITUDE"][ j], les_infos_sans_mesure[ i]["PDOP"][ j] 
                            ])
            # Ecrit le feature
            writer.addFeature( feat)

    # PRJ file
    physiocap_create_projection_file( nom_prj, EPSG_NUMBER)  
    
    return 0
 
def physiocap_sans_mesure_un_contour( laProjectionCRS, EPSG_NUMBER, nom_sans_mesure, nom_prj,
                    les_geoms_des_points, les_GID, les_dates, 
                    les_vitesses, les_altitudes,  les_pdop):
    """ Creation d'un shape de points sans mesure se trouvant dans le contour
    """
    # Prepare les attributs
    les_champs = QgsFields()
    les_champs.append( QgsField( "GID", QVariant.Int, "integer", 10))
    les_champs.append( QgsField( "DATE", QVariant.String, "string", 25))
    les_champs.append( QgsField("VITESSE", QVariant.Double, "double", 10,2))
    les_champs.append(QgsField("ALTITUDE", QVariant.Double,"double", 10,2)) 
    les_champs.append(QgsField("PDOP", QVariant.Double,"double", 10,2)) 

    # Creation du Shape
    writer = QgsVectorFileWriter( nom_sans_mesure, "utf-8", les_champs, 
        QgsWkbTypes.Point, laProjectionCRS , "ESRI Shapefile")

    i = -1
    for gid in les_GID:   
        i = i+1
        feat = QgsFeature()
        feat.setGeometry( QgsGeometry.fromPointXY( les_geoms_des_points[ i])) #écrit la géométrie tel que lu dans shape contour
        feat.setAttributes( [ les_GID[ i], les_dates[ i], les_vitesses[ i], les_altitudes[ i], les_pdop[ i] ])
       # Ecrit le feature
        writer.addFeature( feat)

    # PRJ file
    physiocap_create_projection_file( nom_prj, EPSG_NUMBER)  
    
    return 0

def physiocap_point_un_contour( laProjectionCRS, EPSG_NUMBER, nom_point, nom_prj,
                    les_geoms_des_points, les_GID, les_dates, 
                    les_vitesses, les_sarments, les_diametres, les_biom, 
                    les_altitudes, les_pdop, les_distances, les_derives, 
                    les_biomgm2, les_biomgcep, les_biomm2, les_nbsarmm2, les_nbsarcep,
                    version_3 = "NO", details = "NO"):
    """ Creation d'un shape de points se trouvant dans le contour
    """
    # Prepare les attributs
    les_champs = QgsFields()
    les_champs.append( QgsField( "GID", QVariant.Int, "integer", 10))
    les_champs.append( QgsField( "DATE", QVariant.String, "string", 25))
    les_champs.append( QgsField("VITESSE", QVariant.Double, "double", 10,2))
    les_champs.append(QgsField( "NBSARM",  QVariant.Double, "double", 10,2))
    les_champs.append(QgsField( "DIAM",  QVariant.Double, "double", 10,2))
    les_champs.append(QgsField("BIOM", QVariant.Double,"double", 10,2)) 
    if version_3 == "YES":
        les_champs.append(QgsField("ALTITUDE", QVariant.Double,"double", 10,2)) 
        les_champs.append(QgsField("PDOP", QVariant.Double,"double", 10,2)) 
        les_champs.append(QgsField("DISTANCE", QVariant.Double,"double", 10,2)) 
        les_champs.append(QgsField("DERIVE", QVariant.Double,"double", 10.1)) 
    if details == "YES":
        # Niveau de detail demandé
        les_champs.append(QgsField("BIOMGM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "BIOMGCEP", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "BIOMM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "NBSARMM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "NBSARCEP", QVariant.Double,"double", 10,2))
    # Creation du Shape
    writer = QgsVectorFileWriter( nom_point, "utf-8", les_champs, 
        QgsWkbTypes.Point, laProjectionCRS , "ESRI Shapefile")

    i = -1
    for gid in les_GID:   
        i = i+1
        feat = QgsFeature()
        feat.setGeometry( QgsGeometry.fromPointXY( les_geoms_des_points[ i])) #écrit la géométrie tel que lu dans shape contour
        if details == "YES":
            if version_3 == "YES":
                # Ecrit tous les attributs avec V3
                feat.setAttributes( [ les_GID[ i], les_dates[ i], les_vitesses[ i], 
                les_sarments[ i], les_diametres[ i], les_biom[ i], 
                les_altitudes[ i], les_pdop[ i], les_distances[ i], les_derives[ i], 
                les_biomgm2[ i], les_biomgcep[ i], les_biomm2[ i], les_nbsarmm2[ i], les_nbsarcep[ i] ])
            else:
                # Ecrit tous les attributs pour V2
                feat.setAttributes( [ les_GID[ i], les_dates[ i], les_vitesses[ i], 
                les_sarments[ i], les_diametres[ i], les_biom[ i], 
                les_biomgm2[ i], les_biomgcep[ i], les_biomm2[ i], les_nbsarmm2[ i], les_nbsarcep[ i] ])                
        else:
            if version_3 == "YES":
                # Ecrit tous les attributs avec V3
                # Ecrit les premiers attributs
                feat.setAttributes( [ les_GID[ i], les_dates[ i], les_vitesses[ i], 
                    les_sarments[ i], les_diametres[ i], les_biom[ i],  
                    les_altitudes[ i], les_pdop[ i], les_distances[ i], les_derives[ i]
                 ])
            else:
                # Ecrit les premiers attributs
                feat.setAttributes( [ les_GID[ i], les_dates[ i], les_vitesses[ i], 
                 les_sarments[ i], les_diametres[ i], les_biom[ i] ])
       # Ecrit le feature
        writer.addFeature( feat)

    # PRJ file
    physiocap_create_projection_file( nom_prj, EPSG_NUMBER)  
    
    return 0

def physiocap_moyennes_tous_contours( laProjectionCRS, EPSG_NUMBER, 
    nom_contour_moyenne, nom_contour_moyenne_prj,
    les_geoms_poly, les_surfaces, les_parcelles, les_parcelles_ID, 
    dates_debut_parcelle, dates_fin_parcelle,
    les_nombres, les_taux_sans_mesure, 
    les_moyennes_par_contour, les_ecarts_par_contour, les_medianes_par_contour, 
    version_3 = "NO", details = "NO"):
    """ Creation d'un contour avec les moyennes, ecart et mediane dans un tableau de dict
       Il s'agit de tous les polygones du contour avec des moyennes 
    """
    
    # Prepare les attributs
    les_champs = QgsFields()
    les_champs.append( QgsField( "GID", QVariant.Int, "integer", 10))
    les_champs.append( QgsField( "NOM_PHY", QVariant.String, "string", 25))
    les_champs.append( QgsField( "ID_PHY", QVariant.String, "string", 15))
    les_champs.append( QgsField( "MESURE_HA", QVariant.Double, "double", 10,1))
    if version_3 == "YES":
        les_champs.append( QgsField( "0_MESURE", QVariant.Double, "double", 10,1))                   

    les_champs.append( QgsField( "NBSARM",  QVariant.Double, "double", 10,2))
    les_champs.append( QgsField( "M_NBSARM",  QVariant.Double, "double", 10,2))
    les_champs.append( QgsField( "E_NBSARM",  QVariant.Double, "double", 10,2))
    les_champs.append( QgsField( "DIAM",  QVariant.Double, "double", 10,2))
    les_champs.append( QgsField( "M_DIAM",  QVariant.Double, "double", 10,2))
    les_champs.append( QgsField( "E_DIAM",  QVariant.Double, "double", 10,2))
    les_champs.append( QgsField( "BIOM", QVariant.Double,"double", 10,2))
    les_champs.append( QgsField( "M_BIOM", QVariant.Double,"double", 10,2))
    les_champs.append( QgsField( "E_BIOM", QVariant.Double,"double", 10,2))
    
    if version_3 == "YES":
        les_champs.append( QgsField("ALTITUDE", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("M_ALTI", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("E_ALTI", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("PDOP", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("M_PDOP", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("E_PDOP", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("DISTANCE", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("M_DIST", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("E_DIST", QVariant.Double, "double", 10,2))
        les_champs.append( QgsField("DERIVE", QVariant.Double, "double", 10,1))
        les_champs.append( QgsField("M_DERIVE", QVariant.Double, "double", 10,1))
        les_champs.append( QgsField("E_DERIVE", QVariant.Double, "double", 10,1))
    
    if details == "YES":
        # Niveau de detail demandé
        les_champs.append( QgsField( "BIOMGM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "M_BIOMGM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "E_BIOMGM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "BIOMGCEP", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "M_BIOMGCEP", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "E_BIOMGCEP", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "BIOMM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "M_BIOMM2", QVariant.Double,"double", 10,2))        
        les_champs.append( QgsField( "E_BIOMM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "NBSARMM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "M_NBSARMM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "E_NBSARMM2", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "NBSARCEP", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "M_NBSARCEP", QVariant.Double,"double", 10,2))
        les_champs.append( QgsField( "E_NBSARCEP", QVariant.Double,"double", 10,2))

    les_champs.append( QgsField( "VITESSE", QVariant.Double, "double", 10,2))
    les_champs.append( QgsField( "M_VITESSE", QVariant.Double, "double", 10,2))
    les_champs.append( QgsField( "E_VITESSE", QVariant.Double, "double", 10,2))
    les_champs.append( QgsField( "DEBUT", QVariant.String, "string", 25))
    les_champs.append( QgsField( "FIN", QVariant.String, "string", 25))
    les_champs.append( QgsField( "SURF_HA", QVariant.Double, "double", 10,4))
    les_champs.append( QgsField( "NOMBRE", QVariant.Int, "int", 10))

    # Creation du Shape
    writer = QgsVectorFileWriter( nom_contour_moyenne, "utf-8", les_champs, 
        QgsWkbTypes.MultiPolygon, laProjectionCRS , "ESRI Shapefile")
    
    for i in range( 0, len( les_parcelles)) :
        
        feat = QgsFeature()
        la_geom = QgsGeometry.fromMultiPolygonXY( les_geoms_poly[ i])
        feat.setGeometry( la_geom) #écrit la géométrie tel que lu dans shape contour
        
        if details == "YES":
            if version_3 == "YES":
                # Ecrit tous les attributs pour V3
                feat.setAttributes( [ i, les_parcelles[ i], les_parcelles_ID[ i], les_nombres[ i] / les_surfaces[ i],
                les_taux_sans_mesure[i], 
                les_moyennes_par_contour[ i].get( 'sarm'),    les_medianes_par_contour[ i].get( 'sarm'),    les_ecarts_par_contour[ i].get( 'sarm'), 
                les_moyennes_par_contour[ i].get( 'diam'),    les_medianes_par_contour[ i].get( 'diam'),    les_ecarts_par_contour[ i].get( 'diam'),
                les_moyennes_par_contour[ i].get( 'biom'),    les_medianes_par_contour[ i].get( 'biom'),    les_ecarts_par_contour[ i].get( 'biom'),

                les_moyennes_par_contour[ i].get( 'altitude'),les_medianes_par_contour[ i].get( 'altitude'),les_ecarts_par_contour[ i].get( 'altitude'),
                les_moyennes_par_contour[ i].get( 'pdop'),les_medianes_par_contour[ i].get( 'pdop'),les_ecarts_par_contour[ i].get( 'pdop'),
                les_moyennes_par_contour[ i].get( 'distance'),les_medianes_par_contour[ i].get( 'distance'),les_ecarts_par_contour[ i].get( 'distance'),
                les_moyennes_par_contour[ i].get( 'derive'),les_medianes_par_contour[ i].get( 'derive'),les_ecarts_par_contour[ i].get( 'derive'),
                    
                les_moyennes_par_contour[ i].get( 'biomgm2'), les_medianes_par_contour[ i].get( 'biomgm2'), les_ecarts_par_contour[ i].get( 'biomgm2'),
                les_moyennes_par_contour[ i].get( 'biomgcep'),les_medianes_par_contour[ i].get( 'biomgcep'),les_ecarts_par_contour[ i].get( 'biomgcep'),   
                les_moyennes_par_contour[ i].get( 'biomm2'),  les_medianes_par_contour[ i].get( 'biomm2'),  les_ecarts_par_contour[ i].get( 'biomm2'),
                les_moyennes_par_contour[ i].get( 'nbsarmm2'),les_medianes_par_contour[ i].get( 'nbsarmm2'),les_ecarts_par_contour[ i].get( 'nbsarmm2'),
                les_moyennes_par_contour[ i].get( 'nbsarcep'),les_medianes_par_contour[ i].get( 'nbsarcep'),les_ecarts_par_contour[ i].get( 'nbsarcep'),

                les_moyennes_par_contour[ i].get( 'vitesse'), les_medianes_par_contour[ i].get( 'vitesse'), les_ecarts_par_contour[ i].get( 'vitesse'),
                dates_debut_parcelle[ i],  dates_fin_parcelle[ i], les_surfaces[ i],  les_nombres[ i]
                    ])
            else:
                feat.setAttributes( [ i, les_parcelles[ i], les_parcelles_ID[ i], les_nombres[ i] / les_surfaces[ i],
                les_moyennes_par_contour[ i].get( 'sarm'),    les_medianes_par_contour[ i].get( 'sarm'),    les_ecarts_par_contour[ i].get( 'sarm'), 
                les_moyennes_par_contour[ i].get( 'diam'),    les_medianes_par_contour[ i].get( 'diam'),    les_ecarts_par_contour[ i].get( 'diam'),
                les_moyennes_par_contour[ i].get( 'biom'),    les_medianes_par_contour[ i].get( 'biom'),    les_ecarts_par_contour[ i].get( 'biom'),
                    
                les_moyennes_par_contour[ i].get( 'biomgm2'), les_medianes_par_contour[ i].get( 'biomgm2'), les_ecarts_par_contour[ i].get( 'biomgm2'),
                les_moyennes_par_contour[ i].get( 'biomgcep'),les_medianes_par_contour[ i].get( 'biomgcep'),les_ecarts_par_contour[ i].get( 'biomgcep'),   
                les_moyennes_par_contour[ i].get( 'biomm2'),  les_medianes_par_contour[ i].get( 'biomm2'),  les_ecarts_par_contour[ i].get( 'biomm2'),
                les_moyennes_par_contour[ i].get( 'nbsarmm2'),les_medianes_par_contour[ i].get( 'nbsarmm2'),les_ecarts_par_contour[ i].get( 'nbsarmm2'),
                les_moyennes_par_contour[ i].get( 'nbsarcep'),les_medianes_par_contour[ i].get( 'nbsarcep'),les_ecarts_par_contour[ i].get( 'nbsarcep'),

                les_moyennes_par_contour[ i].get( 'vitesse'), les_medianes_par_contour[ i].get( 'vitesse'), les_ecarts_par_contour[ i].get( 'vitesse'),
                dates_debut_parcelle[ i],  dates_fin_parcelle[ i], les_surfaces[ i],  les_nombres[ i]
                    ])
        else:
            if version_3 == "YES":
                # Ecrit tous les attributs pour V3
                feat.setAttributes( [ i, les_parcelles[ i], les_parcelles_ID[ i],les_nombres[ i] / les_surfaces[ i],
                les_taux_sans_mesure[i], 
                les_moyennes_par_contour[ i].get( 'sarm'),    les_medianes_par_contour[ i].get( 'sarm'),    les_ecarts_par_contour[ i].get( 'sarm'), 
                les_moyennes_par_contour[ i].get( 'diam'),    les_medianes_par_contour[ i].get( 'diam'),    les_ecarts_par_contour[ i].get( 'diam'),
                les_moyennes_par_contour[ i].get( 'biom'),    les_medianes_par_contour[ i].get( 'biom'),    les_ecarts_par_contour[ i].get( 'biom'),

                les_moyennes_par_contour[ i].get( 'altitude'),les_medianes_par_contour[ i].get( 'altitude'),les_ecarts_par_contour[ i].get( 'altitude'),
                les_moyennes_par_contour[ i].get( 'pdop'),les_medianes_par_contour[ i].get( 'pdop'),les_ecarts_par_contour[ i].get( 'pdop'),
                les_moyennes_par_contour[ i].get( 'distance'),les_medianes_par_contour[ i].get( 'distance'),les_ecarts_par_contour[ i].get( 'distance'),
                les_moyennes_par_contour[ i].get( 'derive'),les_medianes_par_contour[ i].get( 'derive'),les_ecarts_par_contour[ i].get( 'derive'),
                
                les_moyennes_par_contour[ i].get( 'vitesse'), les_medianes_par_contour[ i].get( 'vitesse'), les_ecarts_par_contour[ i].get( 'vitesse'),
                dates_debut_parcelle[ i],  dates_fin_parcelle[ i], les_surfaces[ i],  les_nombres[ i]
                    ])
            else:
                # Ecrit tous les attributs pour V2
                feat.setAttributes( [ i, les_parcelles[ i], les_parcelles_ID[ i], les_nombres[ i] / les_surfaces[ i],
                les_moyennes_par_contour[ i].get( 'sarm'),    les_medianes_par_contour[ i].get( 'sarm'),    les_ecarts_par_contour[ i].get( 'sarm'), 
                les_moyennes_par_contour[ i].get( 'diam'),    les_medianes_par_contour[ i].get( 'diam'),    les_ecarts_par_contour[ i].get( 'diam'),
                les_moyennes_par_contour[ i].get( 'biom'),    les_medianes_par_contour[ i].get( 'biom'),    les_ecarts_par_contour[ i].get( 'biom'),
                
                les_moyennes_par_contour[ i].get( 'vitesse'), les_medianes_par_contour[ i].get( 'vitesse'), les_ecarts_par_contour[ i].get( 'vitesse'),
                dates_debut_parcelle[ i],  dates_fin_parcelle[ i], les_surfaces[ i], les_nombres[ i]
                    ])                
        # Ecrit le feature
        writer.addFeature( feat)
    
    # PRJ file
    physiocap_create_projection_file( nom_contour_moyenne_prj, EPSG_NUMBER)

    return 0     

                            
class PhysiocapInter( QtWidgets.QDialog):
    """QGIS Pour voir les messages traduits."""

    def __init__(self, parent=None):
        """Class constructor."""
        super( PhysiocapInter, self).__init__()
    

    
    def physiocap_moyenne_InterParcelles( self, dialogue):
        """Vérification et requete spatiale"""
        
        leModeDeTrace = dialogue.fieldComboModeTrace.currentText() 
        physiocap_log( self.tr( "{0} {1} Début du calcul des moyennes à partir de vos contours").\
            format( PHYSIOCAP_2_EGALS, PHYSIOCAP_UNI), 
            leModeDeTrace)

        # QT Confiance
        repertoire_data = dialogue.lineEditDirectoryPhysiocap.text()
        # Attention peut être non renseigné repertoire_projet = dialogue.lineEditDernierProjet.text()
        if ((repertoire_data == "") or ( not os.path.exists( repertoire_data))):
            aText = self.tr( "Pas de répertoire de données brutes spécifié" )
            physiocap_error( self, aText)
            return physiocap_message_box( dialogue, aText, "information")
        repertoire_cible = dialogue.lineEditDirectoryFiltre.text()
        # Attention peut être non renseigné repertoire_projet = dialogue.lineEditDernierProjet.text()
        if ((repertoire_cible == "") or ( not os.path.exists( repertoire_cible))):
            aText = self.tr( "Pas de répertoire de données cibles spécifié" )
            physiocap_error( self, aText)
            return physiocap_message_box( dialogue, aText, "information")
                
        details = "NO"
        if dialogue.checkBoxInfoVignoble.isChecked():
            details = "YES"
        consolidation = "NO"
        if dialogue.checkBoxConsolidation.isChecked():
            consolidation = "YES"
        version_3 = "NO"
        if dialogue.checkBoxV3.isChecked():
            version_3 = "YES"
                    
        # Récupérer des styles pour chaque shape dans Affichage
        #dir_template = os.path.join( os.path.dirname(__file__), 'modeleQgis')       
        dir_template = dialogue.fieldComboThematiques.currentText()
        qml_is = dialogue.lineEditThematiqueInterMoyenne.text().strip('"') + EXTENSION_QML
        le_template_moyenne = os.path.join( dir_template, qml_is)
        qml_is = dialogue.lineEditThematiqueInterPoints.text().strip('"') + EXTENSION_QML
        le_template_point = os.path.join( dir_template, qml_is)
        if version_3 == "YES":
            qml_is = dialogue.lineEditThematiqueInterPasMesure.text().strip('"') + EXTENSION_QML
            le_template_sans_mesure = os.path.join( dir_template, qml_is)
            qml_is = dialogue.lineEditThematiqueInterSegment.text().strip('"') + EXTENSION_QML
            le_template_segment = os.path.join( dir_template, qml_is)
            qml_is = dialogue.lineEditThematiqueInterSegmentBrise.text().strip('"') + EXTENSION_QML
            le_template_segment_brise = os.path.join( dir_template, qml_is)
        
        # Pour polygone de contour   
        nom_complet_poly = dialogue.comboBoxPolygone.currentText().split( SEPARATEUR_NOEUD)
        if ( len( nom_complet_poly) != 2):
            aText = self.tr( "Le polygone de contour n'est pas choisi.")
            physiocap_error( self, aText)
            aText = aText + "\n" + self.tr( "Avez-vous créer votre shapefile de contour ?")
            return physiocap_message_box( dialogue, aText)           
        id_poly = nom_complet_poly[ 1] 
        vecteur_poly = physiocap_get_layer_by_ID( id_poly)

        leChampPoly = dialogue.fieldComboContours.currentText()
            
        # Pour les points
        nom_complet_point = dialogue.comboBoxPoints.currentText().split( SEPARATEUR_NOEUD)
        if ( len( nom_complet_point) != 2):
            aText = self.tr( "Le shape de points n'est pas choisi. ")
            aText = aText + self.tr( "Créer une nouvelle instance de projet - bouton Filtrer les données brutes - ")
            aText = aText + self.tr( "avant de faire votre calcul de Moyenne Inter Parcellaire")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( dialogue, aText, "information" )
        nom_noeud_arbre = nom_complet_point[ 0] 
        id_point = nom_complet_point[ 1] 
        vecteur_point = physiocap_get_layer_by_ID( id_point)

        # Verification de l'arbre
        mon_projet = QgsProject.instance()
        root = mon_projet.layerTreeRoot()
        un_groupe = root.findGroup( nom_noeud_arbre)
        if ( not isinstance( un_groupe, QgsLayerTreeGroup)):
            aText = self.tr( "Le projet {0} n'existe pas. ").\
                format( nom_noeud_arbre)
            aText = aText + self.tr( "Créer une nouvelle instance de projet - bouton Filtrer les données brutes - ")
            aText = aText + self.tr( "avant de faire votre calcul de Moyenne Inter Parcellaire")
            if (consolidation == "YES"):
                aText = aText + self.tr( "Cas de consolidation : le groupe {0} doit exister. ").\
                    format( nom_noeud_arbre)
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( dialogue, aText, "information" )            

        # Vérification 
        if ( vecteur_point == None) or ( not vecteur_point.isValid()):
            aText = self.tr( "Le jeu de points choisi n'est pas valide. ")
            aText = aText + self.tr( "Créer une nouvelle instance de projet - bouton Filtrer les données brutes - ")
            aText = aText + self.tr( "avant de faire votre calcul de Moyenne Inter Parcellaire")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( dialogue, aText, "information" )  

        if ( vecteur_poly == None) or ( not vecteur_poly.isValid()):
            aText = self.tr( "Le contour choisi n'est pas valide. ")
            aText = aText + self.tr( "Créer une nouvelle instance de projet - bouton Filtrer les données brutes - ")
            aText = aText + self.tr( "avant de faire votre calcul de Moyenne Inter Parcellaire")
            physiocap_error( self, aText, "CRITICAL")
            return physiocap_message_box( dialogue, aText, "information" ) 

        # Verifier SRCs sont les même
        crs_poly = vecteur_poly.crs().authid()
        crs_point = vecteur_point.crs().authid()
        if ( crs_poly != crs_point):
            mes = self.tr( "Les projections (CRS) des contours ({0}) et mesures brutes ({1}) sont différentes !").\
                format( crs_poly, crs_point)
            physiocap_error( self, mes)
            return physiocap_message_box( dialogue, mes,"information")
                    
        laProjectionCRS, laProjectionTXT, EXT_CRS_SHP, EXT_CRS_PRJ, EXT_CRS_RASTER, EPSG_NUMBER = \
            physiocap_quelle_projection_demandee(dialogue)

        if (version_3 == "NO"):
            rep_vecteur = REPERTOIRE_SHAPEFILE
        else:
            rep_vecteur = REPERTOIRE_SHAPEFILE_V3
            

        # Verification du repertoire shape
        pro = vecteur_point.dataProvider() 
        if ( pro.name() == POSTGRES_NOM):
            # On construit le chemin depuis data/projet...
            # Todo: WT PG : test non passé : repertoire_data = > repertoire_cible
            chemin_projet = os.path.join( repertoire_cible, nom_noeud_arbre)
            chemin_shapes = os.path.join( chemin_projet, rep_vecteur)
        else:
            # Assert repertoire shapefile : c'est le repertoire qui contient le vecteur point
            # Ca fonctionne pour consolidation
            # A_TESTER: WINDOWS apres suppression des  deux : unicode( vecteur 
            nom_vecteur_point = vecteur_point.dataProvider().dataSourceUri()
            chemin_shapes = os.path.dirname( nom_vecteur_point)
            shape_point_extension = os.path.basename( nom_vecteur_point)
            pos_extension = shape_point_extension.rfind(".")
            shape_point_sans_extension = shape_point_extension[:pos_extension]
        if ( not os.path.exists( chemin_shapes)):
            raise physiocap_exception_rep( chemin_shapes)
                    
        # TODO: si on n'est pas en consolidation 
        if  version_3 == "YES":
            # On remplace la chaine finale du vecteur point par segment
            pos_diametre = nom_vecteur_point.rfind( NOM_POINTS + EXTENSION_SANS_ZERO + EXT_CRS_SHP)
            physiocap_log( "{0} retrouve le 'sans zero' à position {1}". \
                format(PHYSIOCAP_UNI, pos_diametre), leModeDeTrace)
            nom_base_point = nom_vecteur_point[:pos_diametre]
            if ( dialogue.checkBoxInterPasMesure.isChecked()):
                nom_vecteur_pas_mesure = nom_base_point + NOM_POINTS + EXTENSION_ZERO_SEUL + EXT_CRS_SHP
                vecteur_pas_mesure = physiocap_get_layer_by_URI( nom_vecteur_pas_mesure)
                if ( vecteur_pas_mesure == None) or ( not vecteur_pas_mesure.isValid()):
                    aText = self.tr( "La couche des points sans mesure n'est pas disponible ou valide. ")
                    aText = aText + self.tr( "Créer une nouvelle instance de projet - bouton Filtrer les données brutes - ")
                    aText = aText + self.tr( "en cochant le Format version 3 ")
                    aText = aText + self.tr( "avant de faire votre calcul de Moyenne Inter Parcellaire")
                    physiocap_error( self, aText, "CRITICAL")
                    return physiocap_message_box( dialogue, aText, "information" ) 
            if ( dialogue.checkBoxInterSegment.isChecked() or \
                dialogue.checkBoxInterSegmentBrise.isChecked() ):
                nom_vecteur_segment = nom_base_point + NOM_SEGMENTS_DETAILS + EXT_CRS_SHP
                vecteur_segment = physiocap_get_layer_by_URI( nom_vecteur_segment)
                if ( vecteur_segment == None) or ( not vecteur_segment.isValid()):
                    aText = self.tr( "La couche des segments brisés n'est pas disponible ou valide. ")
                    aText = aText + self.tr( "Créer une nouvelle instance de projet - bouton Filtrer les données brutes - ")
                    aText = aText + self.tr( "en cochant le Format version 3 ")
                    aText = aText + self.tr( "avant de faire votre calcul de Moyenne Inter Parcellaire")
                    physiocap_error( self, aText, "CRITICAL")
                    return physiocap_message_box( dialogue, aText, "information" )  

        # On passe sur les differents contours
        id = 0
        contour_avec_point = 0
        les_geoms_poly = []
        les_surfaces = []
        les_parcelles = []
        les_parcelles_ID = []
        dates_debut_parcelle = []
        dates_fin_parcelle = []
        les_nombres = []
        les_taux_sans_mesure = []  
        les_moyennes_par_contour = []
        les_ecarts_par_contour = []
        les_medianes_par_contour = []
        
        toutes_les_geoms_sans_mesure = []
        les_infos_sans_mesure = []
        info_en_cours = {}

        toutes_les_geoms_segment = []
        les_infos_segment = []
        info_segment_en_cours = {}

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
            
        if MACHINE == "Linux":
            distancearea.setSourceCrs( laProjectionCRS)
        else:
            distancearea.setSourceCrs( laProjectionCRS, QgsProject.instance().transformContext())
            
        distancearea.setEllipsoid( spheroid)
        physiocap_log( "Calcul de distance sous ellipsoide {0}".\
            format( distancearea.ellipsoid()), TRACE_TOOLS)

        for un_contour in vecteur_poly.getFeatures(): #iterate poly features
            id = id + 1
            try:
                # A_TESTER : OK avec avec et ? sans str
                un_nom = str( un_contour[ leChampPoly]) #get attribute of poly layer
            except:
                un_nom = "PHY_ID_" + str(id)
                pass
            
            physiocap_log ( self.tr( "{0} {1} Début Inter pour {2} >>>> ").\
                format( PHYSIOCAP_2_EGALS, PHYSIOCAP_UNI, un_nom), leModeDeTrace)
            
            un_autre_ID = "PHY_ID" + str(id)
            geom_poly = un_contour.geometry() #get geometry of poly layer
            geomWkbType = geom_poly.wkbType()
            geomWkbMultiType = QgsWkbTypes.multiType( geomWkbType) # multiple sous processing
            geomType = QgsWkbTypes.geometryType( geomWkbType) 
           
            if geomType == QgsWkbTypes.Polygon:
                physiocap_log ( self.tr( "Layer (Polygone) simple : {0} ".\
                    format( un_nom)), leModeDeTrace)
            elif geomWkbMultiType == QgsWkbTypes.MultiPolygon:
                physiocap_log ( self.tr("Layer (Polygone) multiple : {0} ".\
                    format( un_nom)), leModeDeTrace)
            else:
                aText = self.tr( "Cette forme n'est pas un polygone : {0}".\
                    format( un_nom))
                physiocap_log( aText, leModeDeTrace,  QgsMessageLog.WARNING)
                physiocap_error( self, aText)
                physiocap_message_box( dialogue, aText, "information")
                continue

            la_surface = distancearea.measureArea( geom_poly) /10000
            #physiocap_log( "Distancearea surface {0}".format( la_surface), leModeDeTrace)

            if  version_3 == "YES" and dialogue.checkBoxInterPasMesure.isChecked():
                # on initialise pour ce contour
                les_geoms_sans_mesure = []
                les_dates_sans_mesure = []
                les_GID_sans_mesure = []
                les_vitesses_sans_mesure = []
                les_altitudes_sans_mesure = []
                les_pdop_sans_mesure = []
                i_sans_mesure = 0
                # Préfiltre dans un rectangle
                # Récupération des POINT SANS MESURE qui concernent ce contour
                for un_sans_mesure in vecteur_pas_mesure.getFeatures(QgsFeatureRequest().
                                setFilterRect(geom_poly.boundingBox())):
                    # un_point est un feature !                          
                    if un_sans_mesure.geometry().within(geom_poly):            
                        i_sans_mesure = i_sans_mesure + 1
                        try:
                            les_geoms_sans_mesure.append( un_sans_mesure.geometry().asPoint())
                            les_dates_sans_mesure.append( un_sans_mesure["DATE"])
                            try:
                                les_GID_sans_mesure.append( un_sans_mesure["GID"])
                            except KeyError:
                                les_GID_sans_mesure.append( i_sans_mesure)
                            les_vitesses_sans_mesure.append( un_sans_mesure["VITESSE"])
                            les_altitudes_sans_mesure.append( un_sans_mesure["ALTITUDE"])
                            les_pdop_sans_mesure.append( un_sans_mesure["PDOP"])
                        except KeyError:
                            message = un_nom + " - " + str( i_sans_mesure) + " - "
                            raise physiocap_exception_points_invalid( message)    
                
                # Mémoriser ces sans mesures
                toutes_les_geoms_sans_mesure.append( les_geoms_sans_mesure)
                info_en_cours[ "DATE"] = les_dates_sans_mesure
                info_en_cours[ "GID"] = les_GID_sans_mesure
                info_en_cours[ "VITESSE"] = les_vitesses_sans_mesure
                info_en_cours[ "ALTITUDE"] = les_altitudes_sans_mesure
                info_en_cours[ "PDOP"] = les_pdop_sans_mesure
                les_infos_sans_mesure.append( info_en_cours)
                info_en_cours = {}
                
            if  version_3 == "YES" and ( dialogue.checkBoxInterSegment.isChecked() or \
                dialogue.checkBoxInterSegmentBrise.isChecked() ):
                # on initialise pour ce contour
                les_geoms_segment = []
                les_dates_debut_segment = []
                les_dates_fin_segment = []
                les_GID_segment = []
                les_nombres_points_segment = []
                les_nombres_points_restant = []
                i_segment = 0
                # Préfiltre dans un rectangle
                # Récupération des SEGMENTS qui concernent ce contour
                for un_segment in vecteur_segment.getFeatures():
#                    physiocap_log( "La geom du segment {1} est de type {0}". \
#                        format( un_segment.geometry().wkbType(), i_segment ), leModeDeTrace)
                    # un_segment est un feature et une ligne 
                    les_geoms_du_segment = []
                    j_points = 0
                    i_segment = i_segment + 1
                    # extraire les points
                    les_multi_points = un_segment.geometry().asMultiPolyline()
                    # TODO: chercher à eviter cet ASSERT KO si on a plusieurs lignes
                    if len( les_multi_points) != 1:
                        message = un_nom + " - PB multi segment" + str( i_segment) + " - "
                        raise physiocap_exception_segment_invalid( message)
                    les_points = les_multi_points[0]
                    nb_points = len( les_points)
#                    physiocap_log( "== Pour le segment {0} le nombre de points {1}". \
#                        format( i_segment, nb_points), TRACE_SEGMENT)
                    # On doit garder les points inter de ce segment 
                    for x_point,  y_point in les_points:
                        le_point = QgsPointXY(x_point, y_point)
                        if  geom_poly.contains( le_point):            
                            j_points = j_points + 1
                            try:
                                les_geoms_du_segment.append(  le_point)
                            except:
                                message = un_nom + " - PB_GEOM " + str( j_points) + " - "
                                raise physiocap_exception_segment_invalid( message)                                     
                    if ( j_points > 2):
                        physiocap_log( "Présence finale {0} points sur {2} dans segment {1}". \
                                format( j_points, i_segment,  nb_points), leModeDeTrace)
                        try:
                            les_geoms_segment.append( les_geoms_du_segment)
                            les_dates_debut_segment.append( un_segment["DATE_DEB"])
                            les_dates_fin_segment.append( un_segment["DATE_FIN"])
                            les_nombres_points_segment.append( un_segment["NB_POINTS"])
                            les_nombres_points_restant.append( j_points)
                            try:
                                les_GID_segment.append( un_segment["GID"])
                            except KeyError:
                                les_GID_segment.append( i_segment)

                        except KeyError:
                            message = un_nom + " - PB segment " + str( i_segment) + " - "
                            raise physiocap_exception_segment_invalid( message)    

                # Mémoriser ces sans mesures
                toutes_les_geoms_segment.append( les_geoms_segment)
                info_segment_en_cours[ "GID"] = les_GID_segment
                info_segment_en_cours[ "DATE_DEB"] = les_dates_debut_segment
                info_segment_en_cours[ "DATE_FIN"] = les_dates_fin_segment
                # Nb de points devient NB_PTS_INI
                info_segment_en_cours[ "NB_PTS_INI"] = les_nombres_points_segment
                # Nb de points restant est le nouveau NB_POINTS "inter"
                info_segment_en_cours[ "NB_POINTS"] = les_nombres_points_restant
                les_infos_segment.append( info_segment_en_cours)
                info_segment_en_cours = {}
      


       
            # on initialise pour ce contour
            les_geoms_des_points = []
            les_dates = []
            les_GID = []
            les_vitesses = []
            les_sarments = []
            les_diametres = []
            nb_dia = 0
            nb_sar = 0
            les_biom = []
            les_altitudes = []
            les_pdop = []
            les_distances = []
            les_derives = []
            les_biomgm2 = []
            les_biomgcep = []
            les_biomm2 = []
            les_nbsarmm2 = []
            les_nbsarcep= []
            i_point = 0
            date_debut = ""
            date_fin = ""
            
            # Récupération des entites POINTS qui concernent ce contour
            for un_point in vecteur_point.getFeatures(QgsFeatureRequest().
                            setFilterRect(geom_poly.boundingBox())):
                # un_point est un feature ! 
                if un_point.geometry().within(geom_poly):
                    # Cas du premier point d'un contour 
                    if i_point == 0:
                        contour_avec_point = contour_avec_point + 1
                    i_point = i_point + 1
                    try:
                        if i_point == 2:
                            # Attraper date début
                            date_debut = un_point["DATE"]
                        les_geoms_des_points.append( un_point.geometry().asPoint())
                        les_dates.append( un_point["DATE"])
                        # Bug 38 : si pas de GID (cf Python V8)
                        try:
                            les_GID.append( un_point["GID"])
                        except KeyError:
                            les_GID.append( i_point)
                        les_vitesses.append( un_point["VITESSE"])
                        les_sarments.append( un_point["NBSARM"])
                        les_diametres.append( un_point["DIAM"])
                        les_biom.append( un_point["BIOM"])
                        if version_3 == "YES":
                            les_altitudes.append( un_point["ALTITUDE"])
                            les_pdop.append( un_point["PDOP"])
                            les_distances.append( un_point["DISTANCE"])
                            les_derives.append( un_point["DERIVE"])

                        if ( details == "YES"):
                            try:
                                les_biomgm2.append( un_point["BIOMGM2"])
                                les_biomgcep.append( un_point["BIOMGCEP"])
                                les_biomm2.append( un_point["BIOMM2"])
                                les_nbsarmm2.append( un_point["NBSARMM2"])
                                les_nbsarcep.append( un_point["NBSARCEP"])
                            except KeyError:
                                # Se remettre en détails non
                                details = "NO"
                    except KeyError:
                        raise physiocap_exception_points_invalid( un_nom) 
                            
            # en sortie de boucle on attrape la derniere date
            if i_point > 10:
                date_fin = un_point["DATE"]
                
            # On a memorisé pour chaque parcelle les attributs de chaque points
            # On fait les calculs des moyenne, médiane et ecart type
            nb_dia = len( les_diametres)
            nb_sar = len( les_sarments)
            le_taux_de_sans_mesure = -1
            le_nombre_segment = 0
            longueur_moyenne_segment = 0

            if version_3 == "YES" and nb_dia > 0:
                le_taux_de_sans_mesure = i_sans_mesure / nb_dia * 100
            if version_3 == "YES":
                le_nombre_segment = len (les_nombres_points_restant)
                longueur_moyenne_segment =float(  np.mean( les_nombres_points_restant)) 
            moyennes_point = {}
            ecarts_point = {}
            medianes_point = {}
            if ( (nb_dia > 0) and ( nb_dia == nb_sar )):
                # Appel np pour mean et std
                # Ranger toutes les moyennes dans un dict Moyenne et un dict Ecart
                moyennes_point['vitesse'] = float(  np.mean( les_vitesses))
                ecarts_point['vitesse'] = float(    np.std( les_vitesses))
                medianes_point['vitesse'] = float(  np.median( les_vitesses))
                moyennes_point['sarm'] = float(     np.mean( les_sarments))
                ecarts_point['sarm'] = float(       np.std( les_sarments))
                medianes_point['sarm'] = float(     np.median( les_sarments))
                moyennes_point['diam'] = float(     np.mean( les_diametres))
                ecarts_point['diam'] = float(       np.std( les_diametres))
                medianes_point['diam'] = float(     np.median( les_diametres))
                moyennes_point['biom'] = float(     np.mean( les_biom))
                ecarts_point['biom'] = float(       np.std( les_biom))
                medianes_point['biom'] = float(     np.median( les_biom))
                if version_3 == "YES":
                    moyennes_point['altitude'] = float(     np.mean( les_altitudes))
                    ecarts_point['altitude'] = float(       np.std( les_altitudes))
                    medianes_point['altitude'] = float(     np.median( les_altitudes))
                    moyennes_point['pdop'] = float(     np.mean( les_pdop))
                    ecarts_point['pdop'] = float(       np.std( les_pdop))
                    medianes_point['pdop'] = float(     np.median( les_pdop))
                    moyennes_point['distance'] = float(     np.mean( les_distances))
                    ecarts_point['distance'] = float(       np.std( les_distances))
                    medianes_point['distance'] = float(     np.median( les_distances))
                    moyennes_point['derive'] = float(     np.mean( les_derives))
                    ecarts_point['derive'] = float(       np.std( les_derives))
                    medianes_point['derive'] = float(     np.median( les_derives))
                if ( details == "YES"):
                    moyennes_point['biomgm2'] = float(  np.mean( les_biomgm2))
                    ecarts_point['biomgm2'] = float(    np.std( les_biomgm2))
                    medianes_point['biomgm2'] = float(  np.median( les_biomgm2))
                    moyennes_point['biomgcep'] = float( np.mean( les_biomgcep))
                    ecarts_point['biomgcep'] = float(   np.std( les_biomgcep))
                    medianes_point['biomgcep'] = float( np.median( les_biomgcep))
                    moyennes_point['biomm2'] = float(   np.mean( les_biomm2))
                    ecarts_point['biomm2'] = float(     np.std( les_biomm2)) 
                    medianes_point['biomm2'] = float(   np.median( les_biomm2)) 
                    moyennes_point['nbsarmm2'] = float( np.mean( les_nbsarmm2))
                    ecarts_point['nbsarmm2'] = float(   np.std( les_nbsarmm2))
                    medianes_point['nbsarmm2'] = float( np.median( les_nbsarmm2))
                    moyennes_point['nbsarcep'] = float( np.mean( les_nbsarcep))
                    ecarts_point['nbsarcep'] = float(   np.std( les_nbsarcep))
                    medianes_point['nbsarcep'] = float( np.median( les_nbsarcep))
                
                physiocap_log ( self.tr( "Date : {0}").\
                    format( date_debut), leModeDeTrace) 
                if version_3 == "YES":                
                    physiocap_log ( self.tr( "Moyenne des altitudes : {0:6.1f} - Ecarts : {1:6.1f} en m").\
                        format( moyennes_point.get('altitude'), ecarts_point.get('altitude') ), leModeDeTrace)
                    physiocap_log ( self.tr( "Moyenne des dérives entre points : {0:6.1f} - Ecarts : {1:6.1f} en %").\
                        format( moyennes_point.get('derive'), ecarts_point.get('derive') ), leModeDeTrace)
                physiocap_log ( self.tr( "Moyenne du nombre de sarments : {0:6.1f} - Ecarts : {1:6.1f}").\
                    format( moyennes_point.get('sarm'), ecarts_point.get('sarm')  ), leModeDeTrace) 
                physiocap_log ( self.tr( "Moyenne des diamètres : {0:5.1f} - Ecarts : {1:5.1f} en mm").\
                    format( moyennes_point.get('diam'),  ecarts_point.get('diam')), leModeDeTrace)
                physiocap_log ( self.tr( "{0} {1} Fin Inter pour {2} <<<< ").\
                    format( PHYSIOCAP_2_EGALS, PHYSIOCAP_UNI, un_nom), leModeDeTrace)

                # ###################
                # CRÉATION groupe INTER _ PROJET
                # ##################
                if ( contour_avec_point == 1):
                    if un_groupe != None:
                        # Rajout pour consolidation du nom du shape
                        if (consolidation == "YES"):
                            vignette_projet = nom_noeud_arbre + SEPARATEUR_ + shape_point_sans_extension + \
                             SEPARATEUR_ + VIGNETTES_INTER  
                        else:
                            vignette_projet = nom_noeud_arbre + SEPARATEUR_ + VIGNETTES_INTER  
                        vignette_existante = un_groupe.findGroup( vignette_projet)
                        if ( vignette_existante == None ):
                            vignette_group_inter = un_groupe.addGroup( vignette_projet)
                        else:
                            # Si vignette preexiste, on ne recommence pas
                            raise physiocap_exception_vignette_exists( nom_noeud_arbre) 
                        
                    if (consolidation == "YES"):
                        # Rajout pour consolidation du nom du shape
                        chemin_shape_nom_point = os.path.join( chemin_shapes, shape_point_sans_extension)
                        if not (os.path.exists( chemin_shape_nom_point)):
                            os.mkdir( chemin_shape_nom_point)                    
                        chemin_vignettes = os.path.join( chemin_shape_nom_point, VIGNETTES_INTER)
                    else:
                        chemin_vignettes = os.path.join( chemin_shapes, VIGNETTES_INTER)
                    if not (os.path.exists( chemin_vignettes)):
                        try:
                            os.mkdir( chemin_vignettes)
                        except:
                            raise physiocap_exception_rep( VIGNETTES_INTER)

                
                # ###################
                # CRÉATION moyenne
                # ################### 
                nom_court_vignette = nom_noeud_arbre + NOM_MOYENNE + un_nom +  EXT_CRS_SHP     
                nom_court_prj = nom_noeud_arbre + NOM_MOYENNE + un_nom  + EXT_CRS_PRJ     
                #physiocap_log( "Vignette court : " + nom_court_vignette , leModeDeTrace)       
                nom_vignette = physiocap_rename_existing_file( os.path.join( chemin_vignettes, nom_court_vignette))        
                nom_prj = physiocap_rename_existing_file( os.path.join( chemin_vignettes, nom_court_prj))        
                physiocap_moyenne_un_contour( laProjectionCRS, EPSG_NUMBER, nom_vignette, nom_prj, 
                    geom_poly, la_surface,  un_nom, un_autre_ID, date_debut, date_fin,
                    nb_dia, le_taux_de_sans_mesure, le_nombre_segment, longueur_moyenne_segment, 
                    moyennes_point, ecarts_point, medianes_point, version_3, details)
                                     
                # Memorisation de la parcelle du contour et des moyennes
                les_geoms_poly.append( geom_poly.asMultiPolygon())
                les_surfaces.append( la_surface)
                les_parcelles.append( un_nom)
                les_parcelles_ID.append( un_autre_ID)
                dates_debut_parcelle.append( date_debut)
                dates_fin_parcelle.append( date_fin)

                les_nombres.append( nb_dia)
                les_taux_sans_mesure.append( le_taux_de_sans_mesure) 
                les_moyennes_par_contour.append( moyennes_point)
                les_ecarts_par_contour.append( ecarts_point)
                les_medianes_par_contour.append( medianes_point)
                
                # ###################
                # CRÉATION point
                # ###################
                nom_court_point = nom_noeud_arbre + NOM_POINTS + SEPARATEUR_ + un_nom + EXT_CRS_SHP     
                nom_court_point_prj = nom_noeud_arbre + NOM_POINTS + SEPARATEUR_ + un_nom + EXT_CRS_PRJ     
                nom_point = physiocap_rename_existing_file( os.path.join( chemin_vignettes, nom_court_point))        
                nom_point_prj = physiocap_rename_existing_file( os.path.join( chemin_vignettes, nom_court_point_prj))        
                
                physiocap_point_un_contour( laProjectionCRS, EPSG_NUMBER, nom_point, nom_point_prj, 
                    les_geoms_des_points, les_GID, les_dates, 
                    les_vitesses, les_sarments, les_diametres, les_biom,
                    les_altitudes,  les_pdop, les_distances, les_derives, 
                    les_biomgm2, les_biomgcep, les_biomm2, les_nbsarmm2, les_nbsarcep,
                    version_3, details)
                
                if  version_3 == "YES" and dialogue.checkBoxInterPasMesureDetails.isChecked():
                    # ###################
                    # CRÉATION point sans mesure
                    # ###################
                    nom_court_sans_mesure = nom_noeud_arbre + NOM_POINTS + EXTENSION_ZERO_SEUL + SEPARATEUR_ + un_nom + EXT_CRS_SHP     
                    nom_court_sans_mesure_prj = nom_noeud_arbre + NOM_POINTS + EXTENSION_ZERO_SEUL + SEPARATEUR_ + un_nom + EXT_CRS_PRJ     
                    nom_sans_mesure = physiocap_rename_existing_file( os.path.join( chemin_vignettes, nom_court_sans_mesure))        
                    nom_sans_mesure_prj = physiocap_rename_existing_file( os.path.join( chemin_vignettes, nom_court_sans_mesure_prj))        
                    
                    physiocap_sans_mesure_un_contour( laProjectionCRS, EPSG_NUMBER, 
                        nom_sans_mesure, nom_sans_mesure_prj, 
                        les_geoms_sans_mesure, les_GID_sans_mesure, les_dates_sans_mesure, 
                        les_vitesses_sans_mesure, les_altitudes_sans_mesure, les_pdop_sans_mesure)

                if  version_3 == "YES" and dialogue.checkBoxInterSegmentDetails.isChecked():
                    # ###################
                    # CRÉATION segment droit dans contour
                    # ###################
                    nom_court_segment = nom_noeud_arbre + NOM_SEGMENTS + SEPARATEUR_ + un_nom + EXT_CRS_SHP     
                    nnom_court_segment_prj = nom_noeud_arbre + NOM_SEGMENTS + SEPARATEUR_ + un_nom + EXT_CRS_PRJ     
                    nom_segment = physiocap_rename_existing_file( os.path.join( chemin_vignettes, nom_court_segment))        
                    nom_segment_prj = physiocap_rename_existing_file( os.path.join( chemin_vignettes, nnom_court_segment_prj))        
                    
                    physiocap_segments_un_contour( laProjectionCRS, EPSG_NUMBER, nom_segment, nom_segment_prj, 
                        les_geoms_segment, les_dates_debut_segment, les_dates_fin_segment, 
                        les_GID_segment, les_nombres_points_segment, les_nombres_points_restant)

                if  version_3 == "YES" and dialogue.checkBoxInterSegmentBriseDetails.isChecked():
                    # ###################
                    # CRÉATION segment  brisé dans contour
                    # ###################

                    nom_court_segment_brise = nom_noeud_arbre + NOM_SEGMENTS_DETAILS + SEPARATEUR_ + un_nom + EXT_CRS_SHP     
                    nnom_court_segment_brise_prj = nom_noeud_arbre + NOM_SEGMENTS_DETAILS + SEPARATEUR_ + un_nom + EXT_CRS_PRJ     
                    nom_segment_brise = physiocap_rename_existing_file( os.path.join( chemin_vignettes, nom_court_segment_brise))        
                    nom_segment_brise_prj = physiocap_rename_existing_file( os.path.join( chemin_vignettes, nnom_court_segment_brise_prj))        
                    
                    physiocap_segments_un_contour( laProjectionCRS, EPSG_NUMBER, nom_segment_brise, nom_segment_brise_prj, 
                        les_geoms_segment, les_dates_debut_segment, les_dates_fin_segment, 
                        les_GID_segment, les_nombres_points_segment, les_nombres_points_restant, 
                        "BRISE")
                         
                # Affichage dans arbre "vignettes" selon les choix dans onglet Affichage
                SHAPE_MOYENNE_PAR_CONTOUR = "NO"
                if dialogue.checkBoxInterMoyennes.isChecked():
                    SHAPE_MOYENNE_PAR_CONTOUR = "YES"
                SHAPE_POINTS_PAR_CONTOUR = "NO"
                if dialogue.checkBoxInterPoints.isChecked():
                    SHAPE_POINTS_PAR_CONTOUR = "YES"
                SHAPE_SANS_MESURE_PAR_CONTOUR = "NO"
                if  version_3 == "YES" and dialogue.checkBoxInterPasMesureDetails.isChecked():
                    SHAPE_SANS_MESURE_PAR_CONTOUR = "YES"
                    points_sans_mesure = QgsVectorLayer( nom_sans_mesure, nom_court_sans_mesure, 'ogr')
                SHAPE_SEGMENT_PAR_CONTOUR = "NO"
                if  version_3 == "YES" and dialogue.checkBoxInterSegmentDetails.isChecked():
                    SHAPE_SEGMENT_PAR_CONTOUR = "YES"
                    ligne_segment = QgsVectorLayer( nom_segment, nom_court_segment, 'ogr')
                SHAPE_SEGMENT_BRISE_PAR_CONTOUR = "NO"
                if  version_3 == "YES" and dialogue.checkBoxInterSegmentBriseDetails.isChecked():
                    SHAPE_SEGMENT_BRISE_PAR_CONTOUR = "YES"
                    ligne_segment_brise = QgsVectorLayer( nom_segment_brise, nom_court_segment_brise, 'ogr')
                    
                # TODO: Vérifier le besoin de recuperer ces deux vecteurs
                points_vector = QgsVectorLayer( nom_point, nom_court_point, 'ogr')
                vignette_vector = QgsVectorLayer( nom_vignette, nom_court_vignette, 'ogr')
          
                
                if vignette_group_inter != None:
                    if  SHAPE_MOYENNE_PAR_CONTOUR == "YES" or \
                        SHAPE_POINTS_PAR_CONTOUR == "YES"  or \
                        SHAPE_SANS_MESURE_PAR_CONTOUR == "YES" or \
                        SHAPE_SEGMENT_BRISE_PAR_CONTOUR == "YES" or \
                        SHAPE_SEGMENT_PAR_CONTOUR == "YES":
                        # Création d'un groupe par parcelle
                        groupe_parcelle_existante = vignette_group_inter.findGroup( un_nom)
                        if ( groupe_parcelle_existante != None ):                            
                            # Si vignette preexiste, on arrete
                            raise physiocap_exception_vignette_exists( un_nom)
                        else:
                            groupe_parcelle = vignette_group_inter.addGroup( un_nom)
                       
                    # Ajouter le vecteur dans un groupe
                    if SHAPE_MOYENNE_PAR_CONTOUR == "YES":
                        mon_projet.addMapLayer( vignette_vector, False)
                        groupe_parcelle.addLayer( vignette_vector)
                    if SHAPE_POINTS_PAR_CONTOUR == "YES":
                        mon_projet.addMapLayer( points_vector, False)
                        groupe_parcelle.addLayer( points_vector)
                    if  version_3 == "YES" and SHAPE_SANS_MESURE_PAR_CONTOUR == "YES":
                        mon_projet.addMapLayer( points_sans_mesure, False)
                        groupe_parcelle.addLayer( points_sans_mesure)
                    if  version_3 == "YES" and SHAPE_SEGMENT_BRISE_PAR_CONTOUR == "YES":
                        mon_projet.addMapLayer( ligne_segment_brise, False)
                        groupe_parcelle.addLayer( ligne_segment_brise)
                    if  version_3 == "YES" and SHAPE_SEGMENT_PAR_CONTOUR == "YES":
                        mon_projet.addMapLayer( ligne_segment, False)
                        groupe_parcelle.addLayer( ligne_segment)

                else:
                    # Pas de vignette pour le groupe_inter ... ce code est mort ? ou utile à quel cas
                    if SHAPE_MOYENNE_PAR_CONTOUR == "YES":
                        mon_projet.addMapLayer( vignette_vector)
                    if SHAPE_POINTS_PAR_CONTOUR == "YES":
                        mon_projet.addMapLayer( points_vector)
                    if  version_3 == "YES" and SHAPE_SANS_MESURE_PAR_CONTOUR == "YES":
                        mon_projet.addMapLayer( points_sans_mesure, False)
                    if  version_3 == "YES" and SHAPE_SEGMENT_BRISE_PAR_CONTOUR == "YES":
                        mon_projet.addMapLayer( ligne_segment_brise, False)
                    if  version_3 == "YES" and SHAPE_SEGMENT_PAR_CONTOUR == "YES":
                        mon_projet.addMapLayer( ligne_segment, False)

                        
                # Mise en action du template
                if SHAPE_MOYENNE_PAR_CONTOUR == "YES":
                    if ( os.path.exists( le_template_moyenne)):
                        vignette_vector.loadNamedStyle( le_template_moyenne)                                
                if SHAPE_POINTS_PAR_CONTOUR == "YES":
                    if ( os.path.exists( le_template_point)):
                        points_vector.loadNamedStyle( le_template_point)
                if  version_3 == "YES" and SHAPE_SANS_MESURE_PAR_CONTOUR == "YES":                   
                    if ( os.path.exists( le_template_sans_mesure)):
                        points_sans_mesure.loadNamedStyle( le_template_sans_mesure)
                if  version_3 == "YES" and SHAPE_SEGMENT_BRISE_PAR_CONTOUR == "YES":                   
                    if ( os.path.exists( le_template_segment_brise)):
                        ligne_segment_brise.loadNamedStyle( le_template_segment_brise)
                if  version_3 == "YES" and SHAPE_SEGMENT_PAR_CONTOUR == "YES":                   
                    if ( os.path.exists( le_template_segment)):
                        ligne_segment.loadNamedStyle( le_template_segment)

            else:
                physiocap_log( self.tr( "== Aucune point dans {0}. Pas de comparaison inter parcellaire").\
                    format( un_nom), leModeDeTrace)       
        
        if ( contour_avec_point == 0):
            return physiocap_message_box( dialogue, 
                    self.tr( "== Aucune point dans {0}. Pas de comparaison inter parcellaire").\
                    format( self.tr( "vos contours")),
                    "information")
        else:
            
            # On a des parcelles dans le contour avec des moyennes
            nom_court_du_contour = os.path.basename( vecteur_poly.name() + EXTENSION_SHP)
            # Inserer "MOYENNES"
            nom_court_du_contour_moyenne = nom_noeud_arbre + NOM_MOYENNE + nom_court_du_contour
            nom_court_du_contour_moyenne_prj = nom_court_du_contour_moyenne [:-4] + EXT_CRS_PRJ[ -4:]     
            nom_contour_moyenne = physiocap_rename_existing_file( 
            os.path.join( chemin_vignettes, nom_court_du_contour_moyenne))        
            nom_contour_moyenne_prj = physiocap_rename_existing_file( 
            os.path.join( chemin_vignettes, nom_court_du_contour_moyenne_prj)) 
            
            physiocap_moyennes_tous_contours( laProjectionCRS, EPSG_NUMBER, nom_contour_moyenne, nom_contour_moyenne_prj,
                les_geoms_poly, les_surfaces, les_parcelles, les_parcelles_ID, 
                dates_debut_parcelle,  dates_fin_parcelle,
                les_nombres, les_taux_sans_mesure, 
                les_moyennes_par_contour, les_ecarts_par_contour, les_medianes_par_contour, 
                version_3, details)

            # Inserer les PAS DE MESURE de tous les contours
            if  version_3 == "YES" and dialogue.checkBoxInterPasMesure.isChecked():
                # ###################
                # CRÉATION point sans mesure
                # ###################
                nom_court_sans_mesure_moyenne = nom_noeud_arbre + NOM_POINTS + EXTENSION_ZERO_SEUL + SEPARATEUR_ + nom_court_du_contour
                nom_court_sans_mesure_moyenne_prj = nom_court_sans_mesure_moyenne [:-4] + EXT_CRS_PRJ[ -4:]
                nom_sans_mesure_moyenne = physiocap_rename_existing_file( os.path.join( chemin_vignettes, nom_court_sans_mesure_moyenne))        
                nom_sans_mesure_moyenne_prj = physiocap_rename_existing_file( os.path.join( chemin_vignettes, nom_court_sans_mesure_moyenne_prj))        
                physiocap_sans_mesure_tous_contours( laProjectionCRS, EPSG_NUMBER, 
                    nom_sans_mesure_moyenne, nom_sans_mesure_moyenne_prj, 
                    toutes_les_geoms_sans_mesure, les_infos_sans_mesure)
                    
            if  version_3 == "YES" and dialogue.checkBoxInterSegmentBrise.isChecked():
                nom_court_segment_brise_moyenne = nom_noeud_arbre + NOM_SEGMENTS + SEPARATEUR_ + nom_court_du_contour
                nom_court_segment_brise_moyenne_prj = nom_court_segment_brise_moyenne [:-4] + EXT_CRS_PRJ[ -4:]
                nom_segment_brise_moyenne = physiocap_rename_existing_file( os.path.join( chemin_vignettes, nom_court_segment_brise_moyenne))        
                nom_segment_brise_moyenne_prj = physiocap_rename_existing_file( os.path.join( chemin_vignettes, nom_court_segment_brise_moyenne_prj))        

                physiocap_segment_tous_contours( laProjectionCRS, EPSG_NUMBER, 
                    nom_segment_brise_moyenne, nom_segment_brise_moyenne_prj,
                    toutes_les_geoms_segment, les_infos_segment, 
                    "BRISE")

            # Inserer les SEGMENTS de tous les contours
            if  version_3 == "YES" and dialogue.checkBoxInterSegment.isChecked() :
                nom_court_segment_moyenne = nom_noeud_arbre + NOM_SEGMENTS + SEPARATEUR_ + nom_court_du_contour
                nom_court_segment_moyenne_prj = nom_court_segment_moyenne [:-4] + EXT_CRS_PRJ[ -4:]
                nom_segment_moyenne = physiocap_rename_existing_file( os.path.join( chemin_vignettes, nom_court_segment_moyenne))        
                nom_segment_moyenne_prj = physiocap_rename_existing_file( os.path.join( chemin_vignettes, nom_court_segment_moyenne_prj))        

                physiocap_segment_tous_contours( laProjectionCRS, EPSG_NUMBER, 
                    nom_segment_moyenne, nom_segment_moyenne_prj,
                    toutes_les_geoms_segment, les_infos_segment)
                
            # Affichage du resultat
            if (consolidation == "YES"):
                # Cas de consolidation on précise le nom du shaoe de point
                nom_court_affichage = shape_point_sans_extension + \
                    SEPARATEUR_
            else:
                nom_court_affichage = nom_noeud_arbre + SEPARATEUR_
            SHAPE_A_AFFICHER = []
            if dialogue.checkBoxInterDiametre.isChecked():
                nom_affichage = nom_court_affichage + 'MOY_DIAMETRE' + SEPARATEUR_ + nom_court_du_contour
                qml_is = dialogue.lineEditThematiqueInterDiametre.text().strip('"') + EXTENSION_QML
                SHAPE_A_AFFICHER.append( (nom_affichage, qml_is, nom_contour_moyenne ))
            if dialogue.checkBoxInterSarment.isChecked():
                nom_affichage = nom_court_affichage + 'MOY_SARMENT' + SEPARATEUR_ + nom_court_du_contour
                qml_is = dialogue.lineEditThematiqueInterSarment.text().strip('"') + EXTENSION_QML
                SHAPE_A_AFFICHER.append( (nom_affichage, qml_is, nom_contour_moyenne))
            if dialogue.checkBoxInterBiomasse.isChecked():
                nom_affichage = nom_court_affichage + 'MOY_BIOMASSE' + SEPARATEUR_ + nom_court_du_contour
                qml_is = dialogue.lineEditThematiqueInterBiomasse.text().strip('"') + EXTENSION_QML
                SHAPE_A_AFFICHER.append( (nom_affichage, qml_is, nom_contour_moyenne))
            if dialogue.checkBoxInterAltitude.isChecked():
                nom_affichage = nom_court_affichage + 'MOY_ALTITUDE' + SEPARATEUR_ + nom_court_du_contour
                qml_is = dialogue.lineEditThematiqueInterAltitude.text().strip('"') + EXTENSION_QML
                SHAPE_A_AFFICHER.append( (nom_affichage, qml_is, nom_contour_moyenne))
            if dialogue.checkBoxInterLibelle.isChecked():
                nom_affichage = nom_court_affichage + 'LIBELLE' + SEPARATEUR_ + nom_court_du_contour
                qml_is = dialogue.lineEditThematiqueInterLibelle.text().strip('"') + EXTENSION_QML
                SHAPE_A_AFFICHER.append( (nom_affichage, qml_is, nom_contour_moyenne))
            if version_3 == "YES" and dialogue.checkBoxInterPasMesure.isChecked():
                nom_affichage = nom_court_affichage + 'PAS DE MESURE' + SEPARATEUR_ + nom_court_du_contour
                qml_is = dialogue.lineEditThematiqueInterPasMesure.text().strip('"') + EXTENSION_QML
                SHAPE_A_AFFICHER.append( (nom_affichage, qml_is, nom_sans_mesure_moyenne))
            if version_3 == "YES" and dialogue.checkBoxInterSegmentBrise.isChecked():
                nom_affichage = nom_court_affichage + 'SEGMENT BRISE' + SEPARATEUR_ + nom_court_du_contour
                qml_is = dialogue.lineEditThematiqueInterSegmentBrise.text().strip('"') + EXTENSION_QML
                SHAPE_A_AFFICHER.append( (nom_affichage, qml_is,  nom_segment_brise_moyenne))
            if version_3 == "YES" and dialogue.checkBoxInterSegment.isChecked():
                nom_affichage = nom_court_affichage + 'SEGMENT' + SEPARATEUR_ + nom_court_du_contour
                qml_is = dialogue.lineEditThematiqueInterSegment.text().strip('"') + EXTENSION_QML
                SHAPE_A_AFFICHER.append( (nom_affichage, qml_is, nom_segment_moyenne))

            # Afficher le contour_moyennes et/ou pas de mesure et segments dans arbre "projet"
            for titre, unTemplate, un_nom in SHAPE_A_AFFICHER:
                vector = QgsVectorLayer( un_nom, titre, 'ogr')

                # On se positionne dans l'arbre
                if vignette_group_inter != None:
                    mon_projet.addMapLayer( vector, False)
                    vignette_group_inter.addLayer( vector)
                else:
                    mon_projet.addMapLayer( vector)
                    
                le_template = os.path.join( dir_template, unTemplate)
                if ( os.path.exists( le_template)):
                    #physiocap_log ( "Physiocap le template : " + os.path.basename( leTemplate) , leModeDeTrace)
                    vector.loadNamedStyle( le_template)  

        return physiocap_message_box( dialogue, 
                        self.tr( "== Fin des traitements inter-parcellaires"),
                        "information")
          
