#/***************************************************************************
# Physiocap3
#
# Physiocap3 plugin helps analysing raw data from Physiocap in QGIS 3
#							 -------------------
#		begin				: 2015-07-31
#		git sha				: $Format:%H$
#		copyright			: (C) 2015 by jhemmi.eu
#		email				: jean@jhemmi.eu
# ***************************************************************************/
#
#/***************************************************************************
# *																		 *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or	 *
# *   (at your option) any later version.								   *
# *																		 *
# ***************************************************************************/

#################################################
# Edit the following to match your sources lists
#################################################


#Add iso code for any locales you want to support here (space separated)
# default is no locales
LOCALES = Physiocap3_it Physiocap3_en 

# If locales are enabled, set the name of the lrelease binary on your system. If
# you have trouble compiling the translations, you may have to specify the full path to
# lrelease
LRELEASE = lrelease

# translation
SOURCES = \
    __init__.py \
    Physiocap3.py \
    Physiocap_tools.py \
    Physiocap_var_exception.py \
    Physiocap_CIVC.py \
    Physiocap_creer_arbre.py \
    Physiocap_inter.py \
    Physiocap_intra_interpolation.py \
    Physiocap3_dialog.py

PLUGINNAME = Physiocap3

PY_FILES = \
    Physiocap3.py \
    Physiocap3_dialog.py \
    Physiocap_var_exception.py \
    Physiocap_tools.py \
    Physiocap_creer_arbre.py \
    Physiocap_CIVC.py \
    Physiocap_inter.py \
    Physiocap_intra_interpolation.py \
    __init__.py

UI_FILES = Physiocap3_dialog_base.ui

DATA = data
DATA_FILES = $(DATA)/01021103.MID $(DATA)/01021103.ERC  \
	$(DATA)/Agro.shp $(DATA)/Agro.shx $(DATA)/Agro.cpg \
	$(DATA)/Agro.dbf $(DATA)/Agro.prj \
	$(DATA)/contour.geojson $(DATA)/Contour_L93.shp $(DATA)/Contour_L93.shx \
	$(DATA)/Contour_L93.dbf $(DATA)/Contour_L93.prj $(DATA)/Contour_L93.cpg\
	$(DATA)/exemple_vide_contour_vignoble.csv $(DATA)/exemple_contour_vignoble.csv \
	$(DATA)/exemple_contour_vignoble.csvt $(DATA)/exemple_contour_vignoble.prj
	
EXTRAS = icon.png metadata.txt LICENSE README.md

COMPILED_RESOURCE_FILES = resources_rc.py

PEP8EXCLUDE=pydev,resources_rc.py,conf.py,third_party,ui


#################################################
# Normally you would not need to edit below here
#################################################

HELP = help
HELP_FILES = $(HELP)/index.html $(HELP)/Histo_non_calcule.png \
    $(HELP)/jhemmi.eu.png $(HELP)/CIVC.jpg $(HELP)/Logo_IFV.png \
    $(HELP)/Logo_MHCS.png $(HELP)/Logo_VCP.png $(HELP)/Logo_TAITTINGER.png
    
CONF_TARGET = $(HOME)/.config/Physiocap/Physiocap3.22.conf
CONF_MODEL = test/Physiocap3.22.conf
CONF_SAVE = $(CONF_TARGET).sauve

TEMPLATE = modeleQGIS
LAYOUT = Mise_en_page
PROJECTION = Projection
VERSION_STANDARD= Standard
VERSION_CHAMPAGNE= Champagne
GPKG = modeleGPKG

PLUGIN_UPLOAD = $(c)/plugin_upload.py

RESOURCE_SRC=$(shell grep '^ *<file' resources.qrc | sed 's@</file>@@g;s/.*>//g' | tr '\n' ' ')
QGISDIR=.local/share/QGIS/QGIS3/profiles/default
#QGISDIR=.local/share/QGIS/QGIS3/profiles/jhemmi

NOW =$(shell date +"%y_%m_%d-%H:%M")

default: compile

compile: $(COMPILED_RESOURCE_FILES)

%_rc.py : %.qrc $(RESOURCES_SRC)
	pyrcc5 -o $*_rc.py  $<

%.qm : %.ts
	$(LRELEASE) $<

test: compile transcompile
	@echo
	@echo "----------------------"
	@echo "Regression Test Suite"
	@echo "Python path"
	@echo $(PYTHONPATH)
	@echo "----------------------"
	@cp $(CONF_TARGET) $(CONF_SAVE)
	@cp $(CONF_MODEL) $(CONF_TARGET)  
	@echo "------- Début test  ----- --with-nocoverage -------"
	
	@# Preceding dash means that make will continue in case of errors
	@-export PYTHONPATH=`pwd`:"$(HOME)/apps/qgis/share/qgis/python":$(PYTHONPATH); \
		export QGIS_DEBUG=0; \
		export QGIS_LOG_FILE=/dev/null; \
		nosetests -v --with-id  --cover-package=. \
		3>&1 1>&2 2>&3 3>&- || true
	
	@echo "-- FIN --------------------"
	#@echo "If you get a 'no module named qgis.core error, try sourcing"
	#@echo "the helper script we have provided first then run make test."
	#@echo "e.g. source run-env-linux.sh <path to qgis install>; make test"
	#@echo "----------------------"
	@cp $(CONF_SAVE) $(CONF_TARGET) 


deploy: compile doc transcompile
	@echo
	@echo "------------------------------------------"
	@echo "Deploying plugin to your QGIS3 directory."
	@echo "------------------------------------------"
	# The deploy  target only works on unix like operating system where
	# the Python plugin directory is located at:
	# $(HOME)/$(QGISDIR)/python/plugins
	mkdir -p $(HOME)/$(QGISDIR)/project_templates/$(PLUGINNAME)
	mkdir -p $(HOME)/$(QGISDIR)/project_templates/$(PLUGINNAME)/$(VERSION_STANDARD)
	mkdir -p $(HOME)/$(QGISDIR)/project_templates/$(PLUGINNAME)/$(VERSION_CHAMPAGNE)
	mkdir -p $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	mkdir -p $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)/$(DATA)
	mkdir -p $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)/$(HELP)
	mkdir -p $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)/$(TEMPLATE)
	mkdir -p $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)/$(TEMPLATE)/$(LAYOUT)
	mkdir -p $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)/$(TEMPLATE)/$(PROJECTION)
	mkdir -p $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)/$(TEMPLATE)/$(VERSION_STANDARD)
	mkdir -p $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)/$(TEMPLATE)/$(VERSION_CHAMPAGNE)
	mkdir -p $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)/$(GPKG)
	cp -vf $(PY_FILES) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	@cp -vf $(UI_FILES) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	@cp -vf $(COMPILED_RESOURCE_FILES) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vf $(EXTRAS) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	@cp -vfr i18n $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	@cp -vf $(HELP_FILES)  $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)/$(HELP)
	@cp -vf $(DATA_FILES) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)/$(DATA)
	@cp -vf $(TEMPLATE)/$(LAYOUT)/*.qpt $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)/$(TEMPLATE)/$(LAYOUT)
	@cp -vf $(TEMPLATE)/$(PROJECTION)/*.prj $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)/$(TEMPLATE)/$(PROJECTION)
	@cp -vf $(TEMPLATE)/$(PROJECTION)/*.qpj $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)/$(TEMPLATE)/$(PROJECTION)
	@cp -vf $(TEMPLATE)/$(VERSION_STANDARD)/*.qml $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)/$(TEMPLATE)/$(VERSION_STANDARD)
	@cp -vf $(TEMPLATE)/$(VERSION_CHAMPAGNE)/*.qml $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)/$(TEMPLATE)/$(VERSION_CHAMPAGNE)
	@cp -vf $(TEMPLATE)/$(VERSION_STANDARD)/*.qml $(HOME)/$(QGISDIR)/project_templates/$(PLUGINNAME)/$(VERSION_STANDARD)
	@cp -vf $(TEMPLATE)/$(VERSION_CHAMPAGNE)/*.qml $(HOME)/$(QGISDIR)/project_templates/$(PLUGINNAME)/$(VERSION_CHAMPAGNE)
	@cp -vf $(GPKG)/*.gpkg $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)/$(GPKG)
	# Fin de la copie du plugin Physiocap3

# The dclean target removes compiled python files from plugin directory
# also deletes any .git entry
dclean:
	@echo
	@echo "-----------------------------------"
	@echo "Removing any compiled python files & .git ? TODO"
	@echo "-----------------------------------"
	find $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME) -iname "*.pyc" -delete
	find $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME) -iname ".git" -prune -exec rm -Rf {} \;


derase:
	@echo
	@echo "-------------------------"
	@echo "Removing deployed plugin."
	@echo "-------------------------"
	rm -Rf $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)


zip: deploy dclean
	@echo
	@echo "---------------------------"
	@echo "Creating plugin zip bundle."
	@echo "---------------------------"
	# The zip target deploys the plugin and creates a zip file with the deployed
	# content. You can then upload the zip file on http://plugins.qgis.org
	rm -f $(PLUGINNAME).zip
	cd $(HOME)/$(QGISDIR)/python/plugins; zip -9r $(CURDIR)/$(PLUGINNAME)_$(NOW).zip $(PLUGINNAME)

package: compile
	# Create a zip package of the plugin named $(PLUGINNAME).zip.
	# This requires use of git (your plugin development directory must be a
	# git repository).
	# To use, pass a valid commit or tag as follows:
	#   make package VERSION=Version_0.3.2
	@echo
	@echo "------------------------------------"
	@echo "Exporting plugin to zip package.	"
	@echo "------------------------------------"
	rm -f $(PLUGINNAME).zip
	git archive --prefix=$(PLUGINNAME)/ -o $(PLUGINNAME).zip $(VERSION)
	echo "Created package: $(PLUGINNAME).zip"

upload: zip
	@echo
	@echo "-------------------------------------"
	@echo "Uploading plugin to QGIS Plugin repo."
	@echo "-------------------------------------"
	$(PLUGIN_UPLOAD) $(PLUGINNAME).zip

transupKO:
	@echo
	@echo "------------------------------------------------"
	@echo "Updating translation files with any new strings."
	@echo "------------------------------------------------"
	@chmod +x scripts/update-strings.sh
	@scripts/update-strings.sh $(LOCALES)

transcompile:
	@echo
	@echo "----------------------------------------"
	@echo "Compiled translation files to .qm files."
	@echo "----------------------------------------"
	@chmod +x scripts/compile-strings.sh
	#echo "Trancompile == $(LOCALES) =="
	@scripts/compile-strings.sh $(LRELEASE) "$(LOCALES)"

transclean:
	@echo
	@echo "------------------------------------"
	@echo "Removing compiled translation files."
	@echo "------------------------------------"
	rm -f i18n/*.qm

clean:
	@echo
	@echo "------------------------------------"
	@echo "Removing uic and rcc generated files"
	@echo "------------------------------------"
	rm $(COMPILED_UI_FILES) $(COMPILED_RESOURCE_FILES)

doc:
	@echo
	@echo "------------------------------------"
	@echo "Building documentation using sphinx."
	@echo "------------------------------------"
	# no sphinx 
	#cd help; make html

pylint:
	@echo
	@echo "-----------------"
	@echo "Pylint violations"
	@echo "-----------------"
	@pylint --reports=n --rcfile=pylintrc . || true
	@echo
	@echo "----------------------"
	@echo "If you get a 'no module named qgis.core' error, try sourcing"
	@echo "the helper script we have provided first then run make pylint."
	@echo "e.g. source run-env-linux.sh <path to qgis install>; make pylint"
	@echo "----------------------"


# Run pep8 style checking
#http://pypi.python.org/pypi/pep8
pep8:
	@echo
	@echo "-----------"
	@echo "PEP8 issues"
	@echo "-----------"
	@pep8 --repeat --ignore=E203,E121,E122,E123,E124,E125,E126,E127,E128 --exclude $(PEP8EXCLUDE) . || true
	@echo "-----------"
	@echo "Ignored in PEP8 check:"
	@echo $(PEP8EXCLUDE)
