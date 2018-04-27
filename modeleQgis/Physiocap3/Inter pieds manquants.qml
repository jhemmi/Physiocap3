<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.1.0-Master" labelsEnabled="0" simplifyDrawingHints="0" simplifyMaxScale="1" simplifyLocal="1" simplifyAlgorithm="0" minScale="0" simplifyDrawingTol="1" readOnly="0" maxScale="0" hasScaleBasedVisibilityFlag="0">
  <renderer-v2 forceraster="0" enableorderby="0" type="singleSymbol" symbollevels="0">
    <symbols>
      <symbol alpha="1" type="marker" clip_to_extent="1" name="0">
        <layer class="SimpleMarker" enabled="1" pass="0" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,27,229,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="star"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="253,246,37,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="6"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>GID</value>
    </property>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory minScaleDenominator="0" sizeType="MM" sizeScale="3x:0,0,0,0,0,0" maxScaleDenominator="1e+8" labelPlacementMethod="XHeight" height="15" enabled="0" minimumSize="0" lineSizeType="MM" rotationOffset="270" scaleDependency="Area" penWidth="0" scaleBasedVisibility="0" opacity="1" lineSizeScale="3x:0,0,0,0,0,0" width="15" barWidth="5" diagramOrientation="Up" backgroundColor="#ffffff" backgroundAlpha="255" penColor="#000000" penAlpha="255">
      <fontProperties style="" description="Ubuntu,11,-1,5,50,0,0,0,0,0"/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings showAll="1" priority="0" zIndex="0" obstacle="0" placement="0" linePlacementFlags="18" dist="0">
    <properties>
      <Option type="Map">
        <Option type="QString" value="" name="name"/>
        <Option name="properties"/>
        <Option type="QString" value="collection" name="type"/>
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
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="AZIMUTH">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="orig_ogc_fid">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="GID" index="0" name=""/>
    <alias field="DATE" index="1" name=""/>
    <alias field="VITESSE" index="2" name=""/>
    <alias field="ALTITUDE" index="3" name=""/>
    <alias field="PDOP" index="4" name=""/>
    <alias field="AZIMUTH" index="5" name=""/>
    <alias field="orig_ogc_fid" index="6" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="GID"/>
    <default expression="" applyOnUpdate="0" field="DATE"/>
    <default expression="" applyOnUpdate="0" field="VITESSE"/>
    <default expression="" applyOnUpdate="0" field="ALTITUDE"/>
    <default expression="" applyOnUpdate="0" field="PDOP"/>
    <default expression="" applyOnUpdate="0" field="AZIMUTH"/>
    <default expression="" applyOnUpdate="0" field="orig_ogc_fid"/>
  </defaults>
  <constraints>
    <constraint constraints="0" notnull_strength="0" unique_strength="0" exp_strength="0" field="GID"/>
    <constraint constraints="0" notnull_strength="0" unique_strength="0" exp_strength="0" field="DATE"/>
    <constraint constraints="0" notnull_strength="0" unique_strength="0" exp_strength="0" field="VITESSE"/>
    <constraint constraints="0" notnull_strength="0" unique_strength="0" exp_strength="0" field="ALTITUDE"/>
    <constraint constraints="0" notnull_strength="0" unique_strength="0" exp_strength="0" field="PDOP"/>
    <constraint constraints="0" notnull_strength="0" unique_strength="0" exp_strength="0" field="AZIMUTH"/>
    <constraint constraints="0" notnull_strength="0" unique_strength="0" exp_strength="0" field="orig_ogc_fid"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="GID" desc=""/>
    <constraint exp="" field="DATE" desc=""/>
    <constraint exp="" field="VITESSE" desc=""/>
    <constraint exp="" field="ALTITUDE" desc=""/>
    <constraint exp="" field="PDOP" desc=""/>
    <constraint exp="" field="AZIMUTH" desc=""/>
    <constraint exp="" field="orig_ogc_fid" desc=""/>
  </constraintExpressions>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortExpression="&quot;AZIMUTH&quot;" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column type="field" hidden="0" name="GID" width="-1"/>
      <column type="field" hidden="0" name="DATE" width="-1"/>
      <column type="field" hidden="0" name="VITESSE" width="-1"/>
      <column type="field" hidden="0" name="ALTITUDE" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
      <column type="field" hidden="0" name="PDOP" width="-1"/>
      <column type="field" hidden="0" name="AZIMUTH" width="-1"/>
      <column type="field" hidden="0" name="orig_ogc_fid" width="-1"/>
    </columns>
  </attributetableconfig>
  <editform></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="ALTITUDE" editable="1"/>
    <field name="AZIMUTH" editable="1"/>
    <field name="DATE" editable="1"/>
    <field name="GID" editable="1"/>
    <field name="PDOP" editable="1"/>
    <field name="VITESSE" editable="1"/>
    <field name="orig_ogc_fid" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="ALTITUDE"/>
    <field labelOnTop="0" name="AZIMUTH"/>
    <field labelOnTop="0" name="DATE"/>
    <field labelOnTop="0" name="GID"/>
    <field labelOnTop="0" name="PDOP"/>
    <field labelOnTop="0" name="VITESSE"/>
    <field labelOnTop="0" name="orig_ogc_fid"/>
  </labelOnTop>
  <widgets/>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <expressionfields/>
  <previewExpression>GID</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
