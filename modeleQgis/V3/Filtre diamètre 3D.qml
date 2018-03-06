<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.1.0-Master" minScale="0" maxScale="0" simplifyDrawingHints="0" readOnly="0" hasScaleBasedVisibilityFlag="0" simplifyDrawingTol="1" simplifyAlgorithm="0" labelsEnabled="0" simplifyLocal="1" simplifyMaxScale="1">
  <renderer-3d type="vector" layer="DIAMETRE_mm_10a864c8_42a8_44ce_8b88_a533b58510ab">
    <symbol type="point" shape="cylinder">
      <data alt-clamping="absolute"/>
      <material ambient="255,127,0,255" shininess="2" diffuse="255,255,255,255" specular="251,207,207,255"/>
      <shape-properties>
        <Option type="Map">
          <Option value="0" name="length" type="double"/>
          <Option value="" name="model" type="QString"/>
          <Option value="0.4" name="radius" type="double"/>
        </Option>
      </shape-properties>
      <transform matrix="5 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>
    </symbol>
  </renderer-3d>
  <renderer-v2 type="nullSymbol"/>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>DATE</value>
    </property>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory scaleBasedVisibility="0" rotationOffset="270" penColor="#000000" width="15" enabled="0" penAlpha="255" barWidth="5" scaleDependency="Area" opacity="1" height="15" minScaleDenominator="0" sizeType="MM" maxScaleDenominator="1e+8" lineSizeScale="3x:0,0,0,0,0,0" labelPlacementMethod="XHeight" minimumSize="0" backgroundColor="#ffffff" backgroundAlpha="255" penWidth="0" sizeScale="3x:0,0,0,0,0,0" diagramOrientation="Up" lineSizeType="MM">
      <fontProperties style="" description="Ubuntu,11,-1,5,50,0,0,0,0,0"/>
      <attribute field="" color="#000000" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" showAll="1" placement="0" linePlacementFlags="18" zIndex="0" priority="0" obstacle="0">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <fieldConfiguration>
    <field name="GID">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="DATE">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="VITESSE">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ALTITUDE">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="PDOP">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="DISTANCE">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="DERIVE">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="NBSARM">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="DIAM">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="BIOM">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="NBSARMM2">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="NBSARCEP">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="BIOMM2">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="BIOMGM2">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="BIOMGCEP">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="GID" name="" index="0"/>
    <alias field="DATE" name="" index="1"/>
    <alias field="VITESSE" name="" index="2"/>
    <alias field="ALTITUDE" name="" index="3"/>
    <alias field="PDOP" name="" index="4"/>
    <alias field="DISTANCE" name="" index="5"/>
    <alias field="DERIVE" name="" index="6"/>
    <alias field="NBSARM" name="" index="7"/>
    <alias field="DIAM" name="" index="8"/>
    <alias field="BIOM" name="" index="9"/>
    <alias field="NBSARMM2" name="" index="10"/>
    <alias field="NBSARCEP" name="" index="11"/>
    <alias field="BIOMM2" name="" index="12"/>
    <alias field="BIOMGM2" name="" index="13"/>
    <alias field="BIOMGCEP" name="" index="14"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="GID" applyOnUpdate="0" expression=""/>
    <default field="DATE" applyOnUpdate="0" expression=""/>
    <default field="VITESSE" applyOnUpdate="0" expression=""/>
    <default field="ALTITUDE" applyOnUpdate="0" expression=""/>
    <default field="PDOP" applyOnUpdate="0" expression=""/>
    <default field="DISTANCE" applyOnUpdate="0" expression=""/>
    <default field="DERIVE" applyOnUpdate="0" expression=""/>
    <default field="NBSARM" applyOnUpdate="0" expression=""/>
    <default field="DIAM" applyOnUpdate="0" expression=""/>
    <default field="BIOM" applyOnUpdate="0" expression=""/>
    <default field="NBSARMM2" applyOnUpdate="0" expression=""/>
    <default field="NBSARCEP" applyOnUpdate="0" expression=""/>
    <default field="BIOMM2" applyOnUpdate="0" expression=""/>
    <default field="BIOMGM2" applyOnUpdate="0" expression=""/>
    <default field="BIOMGCEP" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint field="GID" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="DATE" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="VITESSE" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="ALTITUDE" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="PDOP" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="DISTANCE" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="DERIVE" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="NBSARM" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="DIAM" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="BIOM" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="NBSARMM2" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="NBSARCEP" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="BIOMM2" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="BIOMGM2" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="BIOMGCEP" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="GID" exp="" desc=""/>
    <constraint field="DATE" exp="" desc=""/>
    <constraint field="VITESSE" exp="" desc=""/>
    <constraint field="ALTITUDE" exp="" desc=""/>
    <constraint field="PDOP" exp="" desc=""/>
    <constraint field="DISTANCE" exp="" desc=""/>
    <constraint field="DERIVE" exp="" desc=""/>
    <constraint field="NBSARM" exp="" desc=""/>
    <constraint field="DIAM" exp="" desc=""/>
    <constraint field="BIOM" exp="" desc=""/>
    <constraint field="NBSARMM2" exp="" desc=""/>
    <constraint field="NBSARCEP" exp="" desc=""/>
    <constraint field="BIOMM2" exp="" desc=""/>
    <constraint field="BIOMGM2" exp="" desc=""/>
    <constraint field="BIOMGCEP" exp="" desc=""/>
  </constraintExpressions>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortExpression="&quot;DIAM&quot;" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column name="GID" width="-1" hidden="0" type="field"/>
      <column name="DATE" width="-1" hidden="0" type="field"/>
      <column name="VITESSE" width="-1" hidden="0" type="field"/>
      <column name="ALTITUDE" width="-1" hidden="0" type="field"/>
      <column name="PDOP" width="-1" hidden="0" type="field"/>
      <column name="DISTANCE" width="-1" hidden="0" type="field"/>
      <column name="DERIVE" width="-1" hidden="0" type="field"/>
      <column name="NBSARM" width="-1" hidden="0" type="field"/>
      <column name="DIAM" width="-1" hidden="0" type="field"/>
      <column name="BIOM" width="-1" hidden="0" type="field"/>
      <column width="-1" hidden="1" type="actions"/>
      <column name="NBSARMM2" width="-1" hidden="0" type="field"/>
      <column name="NBSARCEP" width="-1" hidden="0" type="field"/>
      <column name="BIOMM2" width="-1" hidden="0" type="field"/>
      <column name="BIOMGM2" width="-1" hidden="0" type="field"/>
      <column name="BIOMGCEP" width="-1" hidden="0" type="field"/>
    </columns>
  </attributetableconfig>
  <editform>.</editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath>.</editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
Les formulaires QGIS peuvent avoir une fonction Python qui sera appelée à l'ouverture du formulaire.

Utilisez cette fonction pour ajouter plus de fonctionnalités à vos formulaires.

Entrez le nom de la fonction dans le champ
"Fonction d'initialisation Python"
Voici un exemple à suivre:
"""
from PyQt4.QtGui import QWidget

def my_form_open(dialog, layer, feature):
⇥geom = feature.geometry()
⇥control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="ALTITUDE" editable="1"/>
    <field name="BIOM" editable="1"/>
    <field name="BIOMGCEP" editable="1"/>
    <field name="BIOMGM2" editable="1"/>
    <field name="BIOMM2" editable="1"/>
    <field name="DATE" editable="1"/>
    <field name="DERIVE" editable="1"/>
    <field name="DIAM" editable="1"/>
    <field name="DISTANCE" editable="1"/>
    <field name="GID" editable="1"/>
    <field name="NBSARCEP" editable="1"/>
    <field name="NBSARM" editable="1"/>
    <field name="NBSARMM2" editable="1"/>
    <field name="PDOP" editable="1"/>
    <field name="VITESSE" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="ALTITUDE" labelOnTop="0"/>
    <field name="BIOM" labelOnTop="0"/>
    <field name="BIOMGCEP" labelOnTop="0"/>
    <field name="BIOMGM2" labelOnTop="0"/>
    <field name="BIOMM2" labelOnTop="0"/>
    <field name="DATE" labelOnTop="0"/>
    <field name="DERIVE" labelOnTop="0"/>
    <field name="DIAM" labelOnTop="0"/>
    <field name="DISTANCE" labelOnTop="0"/>
    <field name="GID" labelOnTop="0"/>
    <field name="NBSARCEP" labelOnTop="0"/>
    <field name="NBSARM" labelOnTop="0"/>
    <field name="NBSARMM2" labelOnTop="0"/>
    <field name="PDOP" labelOnTop="0"/>
    <field name="VITESSE" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <expressionfields/>
  <previewExpression>DATE</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
