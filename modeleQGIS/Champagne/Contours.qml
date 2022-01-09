<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyDrawingTol="1" minScale="0" readOnly="0" hasScaleBasedVisibilityFlag="0" maxScale="-4.65661e-10" simplifyMaxScale="1" labelsEnabled="0" simplifyAlgorithm="0" simplifyDrawingHints="1" simplifyLocal="1" version="3.4.12-Madeira" styleCategories="AllStyleCategories">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" type="singleSymbol" symbollevels="0" forceraster="0">
    <symbols>
      <symbol type="fill" alpha="1" name="0" clip_to_extent="1" force_rhr="0">
        <layer class="SimpleFill" pass="0" enabled="1" locked="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="109,177,135,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="248,0,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="1.06" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="no" k="style"/>
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
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>GID</value>
      <value>"GID"</value>
    </property>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory scaleDependency="Area" lineSizeScale="3x:0,0,0,0,0,0" diagramOrientation="Up" height="15" rotationOffset="270" width="15" penColor="#000000" penAlpha="255" enabled="0" backgroundColor="#ffffff" sizeScale="3x:0,0,0,0,0,0" barWidth="5" backgroundAlpha="255" labelPlacementMethod="XHeight" sizeType="MM" scaleBasedVisibility="0" opacity="1" minimumSize="0" minScaleDenominator="-4.65661e-10" maxScaleDenominator="1e+8" penWidth="0" lineSizeType="MM">
      <fontProperties description="Ubuntu,11,-1,5,50,0,0,0,0,0" style=""/>
      <attribute field="" color="#000000" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings obstacle="0" zIndex="0" linePlacementFlags="18" placement="0" dist="0" priority="0" showAll="1">
    <properties>
      <Option type="Map">
        <Option type="QString" name="name" value=""/>
        <Option name="properties"/>
        <Option type="QString" name="type" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="id">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="area">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="perimeter">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="FID">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Nom_Parcel">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="id" index="0"/>
    <alias name="" field="area" index="1"/>
    <alias name="" field="perimeter" index="2"/>
    <alias name="" field="FID" index="3"/>
    <alias name="" field="Nom_Parcel" index="4"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" expression="" field="id"/>
    <default applyOnUpdate="0" expression="" field="area"/>
    <default applyOnUpdate="0" expression="" field="perimeter"/>
    <default applyOnUpdate="0" expression="" field="FID"/>
    <default applyOnUpdate="0" expression="" field="Nom_Parcel"/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" notnull_strength="0" exp_strength="0" field="id" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="0" exp_strength="0" field="area" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="0" exp_strength="0" field="perimeter" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="0" exp_strength="0" field="FID" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="0" exp_strength="0" field="Nom_Parcel" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="area"/>
    <constraint exp="" desc="" field="perimeter"/>
    <constraint exp="" desc="" field="FID"/>
    <constraint exp="" desc="" field="Nom_Parcel"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column type="actions" hidden="1" width="-1"/>
      <column type="field" hidden="0" name="id" width="-1"/>
      <column type="field" hidden="0" name="area" width="-1"/>
      <column type="field" hidden="0" name="perimeter" width="-1"/>
      <column type="field" hidden="0" name="FID" width="-1"/>
      <column type="field" hidden="0" name="Nom_Parcel" width="-1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <editform tolerant="1">/media/jean/DATA/GIS/SCRIPT/QGIS/Physiocap3</editform>
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
    <field editable="1" name="FID"/>
    <field editable="1" name="Nom_Parcel"/>
    <field editable="1" name="area"/>
    <field editable="1" name="id"/>
    <field editable="1" name="perimeter"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="FID"/>
    <field labelOnTop="0" name="Nom_Parcel"/>
    <field labelOnTop="0" name="area"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="perimeter"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>GID</previewExpression>
  <mapTip>Name</mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
