# -*- coding: utf-8 -*-
"""
/***************************************************************************
 __init__ de Physiocap3
                                 A QGIS 3 plugin
    Physiocap3 for QGIS 3
                             -------------------
        begin                : 2017-10-19
        copyright            : (C) 2017 by jhemmi.eu
        email                : jean@jhemmi.eu
        git sha              : $Format:%H$
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
 This script initializes the plugin, making it known to QGIS
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Physiocap3 class from file Physiocap3.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .Physiocap3 import Physiocap3
    return Physiocap3(iface)
