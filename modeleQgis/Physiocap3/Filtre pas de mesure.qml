<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.0.3-Girona" labelsEnabled="0" simplifyAlgorithm="0" minScale="0" simplifyLocal="1" readOnly="0" maxScale="0" simplifyMaxScale="1" simplifyDrawingTol="1" simplifyDrawingHints="0" hasScaleBasedVisibilityFlag="0">
  <renderer-v2 type="graduatedSymbol" forceraster="0" enableorderby="0" attr="VITESSE" graduatedMethod="GraduatedColor" symbollevels="0">
    <ranges>
      <range label=" inf à 2 km/h" render="true" lower="0.000000000000000" symbol="0" upper="2.000000000000000"/>
      <range label=" sup à 2 km/h" render="true" lower="2.000000000000000" symbol="1" upper="1000.000000000000000"/>
    </ranges>
    <symbols>
      <symbol type="marker" name="0" alpha="1" clip_to_extent="1">
        <layer class="SimpleMarker" enabled="1" locked="0" pass="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="34,255,27,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="marker" name="1" alpha="1" clip_to_extent="1">
        <layer class="SimpleMarker" enabled="1" locked="0" pass="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol type="marker" name="0" alpha="1" clip_to_extent="1">
        <layer class="SimpleMarker" enabled="1" locked="0" pass="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="126,228,150,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <colorramp type="gradient" name="[source]">
      <prop k="color1" v="34,255,27,255"/>
      <prop k="color2" v="255,0,0,255"/>
      <prop k="discrete" v="0"/>
      <prop k="rampType" v="gradient"/>
    </colorramp>
    <mode name="jenks"/>
    <rotation/>
    <sizescale/>
    <labelformat decimalplaces="1" format=" %1 - %2 " trimtrailingzeroes="false"/>
  </renderer-v2>
  <customproperties>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory barWidth="5" rotationOffset="270" penColor="#000000" penAlpha="255" enabled="0" width="15" scaleBasedVisibility="0" lineSizeScale="3x:0,0,0,0,0,0" sizeType="MM" sizeScale="3x:0,0,0,0,0,0" opacity="1" lineSizeType="MM" scaleDependency="Area" diagramOrientation="Up" height="15" penWidth="0" minimumSize="0" minScaleDenominator="0" labelPlacementMethod="XHeight" backgroundColor="#ffffff" maxScaleDenominator="1e+8" backgroundAlpha="255">
      <fontProperties description="Ubuntu,11,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings priority="0" obstacle="0" showAll="1" placement="0" dist="0" zIndex="0" linePlacementFlags="18">
    <properties>
      <Option type="Map">
        <Option type="QString" name="name" value=""/>
        <Option name="properties"/>
        <Option type="QString" name="type" value="collection"/>
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
    <field name="AZIMUTH">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="NBSART">
      <editWidget type="TextEdit">
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
  </fieldConfiguration>
  <aliases>
    <alias name="" field="GID" index="0"/>
    <alias name="" field="DATE" index="1"/>
    <alias name="" field="VITESSE" index="2"/>
    <alias name="" field="ALTITUDE" index="3"/>
    <alias name="" field="PDOP" index="4"/>
    <alias name="" field="DISTANCE" index="5"/>
    <alias name="" field="DERIVE" index="6"/>
    <alias name="" field="AZIMUTH" index="7"/>
    <alias name="" field="NBSART" index="8"/>
    <alias name="" field="NBSARM" index="9"/>
    <alias name="" field="DIAM" index="10"/>
    <alias name="" field="BIOM" index="11"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" field="GID" applyOnUpdate="0"/>
    <default expression="" field="DATE" applyOnUpdate="0"/>
    <default expression="" field="VITESSE" applyOnUpdate="0"/>
    <default expression="" field="ALTITUDE" applyOnUpdate="0"/>
    <default expression="" field="PDOP" applyOnUpdate="0"/>
    <default expression="" field="DISTANCE" applyOnUpdate="0"/>
    <default expression="" field="DERIVE" applyOnUpdate="0"/>
    <default expression="" field="AZIMUTH" applyOnUpdate="0"/>
    <default expression="" field="NBSART" applyOnUpdate="0"/>
    <default expression="" field="NBSARM" applyOnUpdate="0"/>
    <default expression="" field="DIAM" applyOnUpdate="0"/>
    <default expression="" field="BIOM" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint constraints="0" exp_strength="0" unique_strength="0" field="GID" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" field="DATE" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" field="VITESSE" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" field="ALTITUDE" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" field="PDOP" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" field="DISTANCE" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" field="DERIVE" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" field="AZIMUTH" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" field="NBSART" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" field="NBSARM" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" field="DIAM" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" field="BIOM" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="GID"/>
    <constraint desc="" exp="" field="DATE"/>
    <constraint desc="" exp="" field="VITESSE"/>
    <constraint desc="" exp="" field="ALTITUDE"/>
    <constraint desc="" exp="" field="PDOP"/>
    <constraint desc="" exp="" field="DISTANCE"/>
    <constraint desc="" exp="" field="DERIVE"/>
    <constraint desc="" exp="" field="AZIMUTH"/>
    <constraint desc="" exp="" field="NBSART"/>
    <constraint desc="" exp="" field="NBSARM"/>
    <constraint desc="" exp="" field="DIAM"/>
    <constraint desc="" exp="" field="BIOM"/>
  </constraintExpressions>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column type="field" name="GID" hidden="0" width="-1"/>
      <column type="field" name="DATE" hidden="0" width="-1"/>
      <column type="field" name="VITESSE" hidden="0" width="-1"/>
      <column type="field" name="ALTITUDE" hidden="0" width="-1"/>
      <column type="field" name="DISTANCE" hidden="0" width="-1"/>
      <column type="field" name="DERIVE" hidden="0" width="-1"/>
      <column type="field" name="NBSARM" hidden="0" width="-1"/>
      <column type="field" name="DIAM" hidden="0" width="-1"/>
      <column type="field" name="BIOM" hidden="0" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
      <column type="field" name="PDOP" hidden="0" width="-1"/>
      <column type="field" name="AZIMUTH" hidden="0" width="-1"/>
      <column type="field" name="NBSART" hidden="0" width="-1"/>
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
    <field name="BIOM" editable="1"/>
    <field name="DATE" editable="1"/>
    <field name="DERIVE" editable="1"/>
    <field name="DIAM" editable="1"/>
    <field name="DISTANCE" editable="1"/>
    <field name="GID" editable="1"/>
    <field name="NBSARM" editable="1"/>
    <field name="NBSART" editable="1"/>
    <field name="PDOP" editable="1"/>
    <field name="VITESSE" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="ALTITUDE"/>
    <field labelOnTop="0" name="AZIMUTH"/>
    <field labelOnTop="0" name="BIOM"/>
    <field labelOnTop="0" name="DATE"/>
    <field labelOnTop="0" name="DERIVE"/>
    <field labelOnTop="0" name="DIAM"/>
    <field labelOnTop="0" name="DISTANCE"/>
    <field labelOnTop="0" name="GID"/>
    <field labelOnTop="0" name="NBSARM"/>
    <field labelOnTop="0" name="NBSART"/>
    <field labelOnTop="0" name="PDOP"/>
    <field labelOnTop="0" name="VITESSE"/>
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
