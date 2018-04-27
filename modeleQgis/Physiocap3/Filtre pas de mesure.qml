<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyAlgorithm="0" simplifyMaxScale="1" readOnly="0" maxScale="0" hasScaleBasedVisibilityFlag="0" version="2.99.0-Master" simplifyDrawingTol="1" simplifyLocal="1" mincale="1e+8" simplifyDrawingHints="0">
  <renderer-v2 enableorderby="0" attr="VITESSE" graduatedMethod="GraduatedColor" forceraster="0" symbollevels="0" type="graduatedSymbol">
    <ranges>
      <range symbol="0" upper="2.000000000000000" render="true" label=" inf à 2 km/h" lower="0.000000000000000"/>
      <range symbol="1" upper="1000.000000000000000" render="true" label=" inf à 2 km/h" lower="2.000000000000000"/>
    </ranges>
    <symbols>
      <symbol name="0" alpha="1" type="marker" clip_to_extent="1">
        <layer enabled="1" locked="0" pass="0" class="SimpleMarker">
          <prop v="0" k="angle"/>
          <prop v="34,255,27,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="2" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="1" alpha="1" type="marker" clip_to_extent="1">
        <layer enabled="1" locked="0" pass="0" class="SimpleMarker">
          <prop v="0" k="angle"/>
          <prop v="255,0,0,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="2" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol name="0" alpha="1" type="marker" clip_to_extent="1">
        <layer enabled="1" locked="0" pass="0" class="SimpleMarker">
          <prop v="0" k="angle"/>
          <prop v="126,228,150,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="2" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <colorramp name="[source]" type="gradient">
      <prop v="34,255,27,255" k="color1"/>
      <prop v="255,0,0,255" k="color2"/>
      <prop v="0" k="discrete"/>
      <prop v="gradient" k="rampType"/>
    </colorramp>
    <mode name="jenks"/>
    <rotation/>
    <sizescale/>
    <labelformat format=" %1 - %2 " decimalplaces="1" trimtrailingzeroes="false"/>
  </renderer-v2>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory height="15" enabled="0" sizeType="MM" rotationOffset="270" labelPlacementMethod="XHeight" sizeScale="3x:0,0,0,0,0,0" penWidth="0" opacity="1" minimumSize="0" lineSizeScale="3x:0,0,0,0,0,0" scaleDependency="Area" scaleBasedVisibility="0" lineSizeType="MM" penColor="#000000" penAlpha="255" minScaleDenominator="0" width="15" diagramOrientation="Up" maxScaleDenominator="1e+8" barWidth="5" backgroundColor="#ffffff" backgroundAlpha="255">
      <fontProperties description="Ubuntu,11,-1,5,50,0,0,0,0,0" style=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="0" priority="0" obstacle="0" zIndex="0" linePlacementFlags="18" showAll="1" dist="0">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
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
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="NBSARCEP">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="BIOMM2">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="BIOMGM2">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="BIOMGCEP">
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
    <alias name="" field="DISTANCE" index="4"/>
    <alias name="" field="DERIVE" index="5"/>
    <alias name="" field="NBSARM" index="6"/>
    <alias name="" field="DIAM" index="7"/>
    <alias name="" field="BIOM" index="8"/>
    <alias name="" field="NBSARMM2" index="9"/>
    <alias name="" field="NBSARCEP" index="10"/>
    <alias name="" field="BIOMM2" index="11"/>
    <alias name="" field="BIOMGM2" index="12"/>
    <alias name="" field="BIOMGCEP" index="13"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="GID" expression=""/>
    <default applyOnUpdate="0" field="DATE" expression=""/>
    <default applyOnUpdate="0" field="VITESSE" expression=""/>
    <default applyOnUpdate="0" field="ALTITUDE" expression=""/>
    <default applyOnUpdate="0" field="DISTANCE" expression=""/>
    <default applyOnUpdate="0" field="DERIVE" expression=""/>
    <default applyOnUpdate="0" field="NBSARM" expression=""/>
    <default applyOnUpdate="0" field="DIAM" expression=""/>
    <default applyOnUpdate="0" field="BIOM" expression=""/>
    <default applyOnUpdate="0" field="NBSARMM2" expression=""/>
    <default applyOnUpdate="0" field="NBSARCEP" expression=""/>
    <default applyOnUpdate="0" field="BIOMM2" expression=""/>
    <default applyOnUpdate="0" field="BIOMGM2" expression=""/>
    <default applyOnUpdate="0" field="BIOMGCEP" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" notnull_strength="0" field="GID" exp_strength="0" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="DATE" exp_strength="0" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="VITESSE" exp_strength="0" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="ALTITUDE" exp_strength="0" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="DISTANCE" exp_strength="0" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="DERIVE" exp_strength="0" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="NBSARM" exp_strength="0" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="DIAM" exp_strength="0" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="BIOM" exp_strength="0" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="NBSARMM2" exp_strength="0" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="NBSARCEP" exp_strength="0" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="BIOMM2" exp_strength="0" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="BIOMGM2" exp_strength="0" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="BIOMGCEP" exp_strength="0" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="GID" exp="" desc=""/>
    <constraint field="DATE" exp="" desc=""/>
    <constraint field="VITESSE" exp="" desc=""/>
    <constraint field="ALTITUDE" exp="" desc=""/>
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
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column name="GID" hidden="0" width="-1" type="field"/>
      <column name="DATE" hidden="0" width="-1" type="field"/>
      <column name="VITESSE" hidden="0" width="-1" type="field"/>
      <column name="ALTITUDE" hidden="0" width="-1" type="field"/>
      <column name="DISTANCE" hidden="0" width="-1" type="field"/>
      <column name="DERIVE" hidden="0" width="-1" type="field"/>
      <column name="NBSARM" hidden="0" width="-1" type="field"/>
      <column name="DIAM" hidden="0" width="-1" type="field"/>
      <column name="BIOM" hidden="0" width="-1" type="field"/>
      <column name="NBSARMM2" hidden="0" width="-1" type="field"/>
      <column name="NBSARCEP" hidden="0" width="-1" type="field"/>
      <column name="BIOMM2" hidden="0" width="-1" type="field"/>
      <column name="BIOMGM2" hidden="0" width="-1" type="field"/>
      <column name="BIOMGCEP" hidden="0" width="-1" type="field"/>
      <column hidden="1" width="-1" type="actions"/>
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
