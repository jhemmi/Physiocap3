<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyMaxScale="1" simplifyDrawingHints="1" simplifyLocal="1" readOnly="0" maxScale="0" simplifyDrawingTol="1" hasScaleBasedVisibilityFlag="0" version="2.99.0-Master" mincale="0" simplifyAlgorithm="0">
  <renderer-v2 forceraster="0" enableorderby="0" symbollevels="0" type="singleSymbol">
    <symbols>
      <symbol name="0" clip_to_extent="1" alpha="1" type="fill">
        <layer locked="0" class="SimpleFill" pass="0" enabled="1">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="245,44,150,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,246,255" k="outline_color"/>
          <prop v="dash dot" k="outline_style"/>
          <prop v="0.26" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="no" k="style"/>
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
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="simple">
    <settings>
      <text-style fieldName="  concat(   &#xa;  ' Ilot : ', &quot;NOM_PHY&quot; , &#xa;  '~ Densité de points/ha : ', format_number(&quot;MESURE_HA&quot;, 0) , &#xa;  '~ ', format_number(&quot;0_MESURE&quot;, 0),'% sans mesure', &#xa;  '~ Biomasse == ',&#xa;   ' Médiane : ' , format_number( &quot;BIOM&quot;,0),&#xa; ' Ecartype : ' , format_number(&quot;E_BIOM&quot;,0)&#xa;  )" fontStrikeout="0" fontItalic="0" fontFamily="Ubuntu" textColor="0,0,0,255" fontSize="10" namedStyle="Regular" fontLetterSpacing="0" textOpacity="1" fontWeight="50" fontCapitals="0" blendMode="0" fontSizeUnit="Point" fontWordSpacing="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" useSubstitutions="0" previewBkgrdColor="#ffffff" isExpression="1" multilineHeight="1" fontUnderline="0">
        <text-buffer bufferColor="253,191,111,255" bufferSizeUnits="MM" bufferJoinStyle="64" bufferNoFill="0" bufferSize="1" bufferDraw="1" bufferOpacity="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferBlendMode="0"/>
        <background shapeSizeX="0" shapeBorderColor="128,128,128,255" shapeSizeY="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeRotation="0" shapeRadiiX="0" shapeRadiiY="0" shapeOpacity="1" shapeRotationType="0" shapeJoinStyle="64" shapeType="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeSVGFile="" shapeBorderWidthUnit="MM" shapeOffsetUnit="MM" shapeRadiiUnit="MM" shapeSizeUnit="MM" shapeSizeType="0" shapeBlendMode="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidth="0" shapeOffsetX="0" shapeOffsetY="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeDraw="0" shapeFillColor="255,255,255,255"/>
        <shadow shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetDist="1" shadowOpacity="0.7" shadowRadiusUnit="MM" shadowRadius="1.5" shadowOffsetGlobal="1" shadowUnder="0" shadowOffsetUnit="MM" shadowDraw="0" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowColor="0,0,0,255" shadowRadiusAlphaOnly="0" shadowOffsetAngle="135" shadowScale="100" shadowBlendMode="6"/>
        <substitutions/>
      </text-style>
      <text-format plussign="0" addDirectionSymbol="0" multilineAlign="0" placeDirectionSymbol="0" rightDirectionSymbol=">" leftDirectionSymbol="&lt;" reverseDirectionSymbol="0" decimals="3" wrapChar="~" formatNumbers="0"/>
      <placement offsetUnits="MapUnit" offsetType="0" preserveRotation="1" distMapUnitScale="3x:0,0,0,0,0,0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" placement="0" fitInPolygonOnly="0" centroidWhole="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" centroidInside="1" repeatDistance="0" distUnits="MM" priority="5" repeatDistanceUnits="MM" maxCurvedCharAngleOut="-20" yOffset="0" rotationAngle="0" placementFlags="0" maxCurvedCharAngleIn="20" dist="5" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" quadOffset="4" xOffset="0"/>
      <rendering obstacleType="0" minFeatureSize="0" scaleVisibility="0" mergeLines="0" limitNumLabels="0" fontMaxPixelSize="10000" fontMinPixelSize="3" scaleMax="10000000" displayAll="0" labelPerPart="0" maxNumLabels="2000" obstacle="1" fontLimitPixelSize="0" upsidedownLabels="0" obstacleFactor="1" drawLabels="1" scaleMin="1" zIndex="0"/>
      <dd_properties>
        <Option type="Map">
          <Option name="name" value="" type="QString"/>
          <Option name="properties"/>
          <Option name="type" value="collection" type="QString"/>
        </Option>
      </dd_properties>
    </settings>
  </labeling>
  <customproperties>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory labelPlacementMethod="XHeight" height="15" width="15" minScaleDenominator="0" rotationOffset="270" maxScaleDenominator="1e+8" penWidth="0" opacity="1" scaleBasedVisibility="0" lineSizeScale="3x:0,0,0,0,0,0" diagramOrientation="Up" scaleDependency="Area" barWidth="5" penColor="#000000" penAlpha="255" lineSizeType="MM" minimumSize="0" sizeScale="3x:0,0,0,0,0,0" backgroundColor="#ffffff" backgroundAlpha="255" enabled="0" sizeType="MM">
      <fontProperties style="" description="Ubuntu,11,-1,5,50,0,0,0,0,0"/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" linePlacementFlags="18" placement="0" showAll="1" priority="0" zIndex="0" obstacle="0">
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
    <field name="NOM_PHY">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ID_PHY">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="MESURE_HA">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="0_MESURE">
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
    <field name="M_NBSARM">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="E_NBSARM">
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
    <field name="M_DIAM">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="E_DIAM">
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
    <field name="M_BIOM">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="E_BIOM">
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
    <field name="M_ALTI">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="E_ALTI">
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
    <field name="M_DIST">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="E_DIST">
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
    <field name="M_DERIVE">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="E_DERIVE">
      <editWidget type="Range">
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
    <field name="M_VITESSE">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="E_VITESSE">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="DEBUT">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="FIN">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="SURF_HA">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="NOMBRE">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="GID" index="0"/>
    <alias name="" field="NOM_PHY" index="1"/>
    <alias name="" field="ID_PHY" index="2"/>
    <alias name="" field="MESURE_HA" index="3"/>
    <alias name="" field="0_MESURE" index="4"/>
    <alias name="" field="NBSARM" index="5"/>
    <alias name="" field="M_NBSARM" index="6"/>
    <alias name="" field="E_NBSARM" index="7"/>
    <alias name="" field="DIAM" index="8"/>
    <alias name="" field="M_DIAM" index="9"/>
    <alias name="" field="E_DIAM" index="10"/>
    <alias name="" field="BIOM" index="11"/>
    <alias name="" field="M_BIOM" index="12"/>
    <alias name="" field="E_BIOM" index="13"/>
    <alias name="" field="ALTITUDE" index="14"/>
    <alias name="" field="M_ALTI" index="15"/>
    <alias name="" field="E_ALTI" index="16"/>
    <alias name="" field="DISTANCE" index="17"/>
    <alias name="" field="M_DIST" index="18"/>
    <alias name="" field="E_DIST" index="19"/>
    <alias name="" field="DERIVE" index="20"/>
    <alias name="" field="M_DERIVE" index="21"/>
    <alias name="" field="E_DERIVE" index="22"/>
    <alias name="" field="VITESSE" index="23"/>
    <alias name="" field="M_VITESSE" index="24"/>
    <alias name="" field="E_VITESSE" index="25"/>
    <alias name="" field="DEBUT" index="26"/>
    <alias name="" field="FIN" index="27"/>
    <alias name="" field="SURF_HA" index="28"/>
    <alias name="" field="NOMBRE" index="29"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="GID"/>
    <default expression="" applyOnUpdate="0" field="NOM_PHY"/>
    <default expression="" applyOnUpdate="0" field="ID_PHY"/>
    <default expression="" applyOnUpdate="0" field="MESURE_HA"/>
    <default expression="" applyOnUpdate="0" field="0_MESURE"/>
    <default expression="" applyOnUpdate="0" field="NBSARM"/>
    <default expression="" applyOnUpdate="0" field="M_NBSARM"/>
    <default expression="" applyOnUpdate="0" field="E_NBSARM"/>
    <default expression="" applyOnUpdate="0" field="DIAM"/>
    <default expression="" applyOnUpdate="0" field="M_DIAM"/>
    <default expression="" applyOnUpdate="0" field="E_DIAM"/>
    <default expression="" applyOnUpdate="0" field="BIOM"/>
    <default expression="" applyOnUpdate="0" field="M_BIOM"/>
    <default expression="" applyOnUpdate="0" field="E_BIOM"/>
    <default expression="" applyOnUpdate="0" field="ALTITUDE"/>
    <default expression="" applyOnUpdate="0" field="M_ALTI"/>
    <default expression="" applyOnUpdate="0" field="E_ALTI"/>
    <default expression="" applyOnUpdate="0" field="DISTANCE"/>
    <default expression="" applyOnUpdate="0" field="M_DIST"/>
    <default expression="" applyOnUpdate="0" field="E_DIST"/>
    <default expression="" applyOnUpdate="0" field="DERIVE"/>
    <default expression="" applyOnUpdate="0" field="M_DERIVE"/>
    <default expression="" applyOnUpdate="0" field="E_DERIVE"/>
    <default expression="" applyOnUpdate="0" field="VITESSE"/>
    <default expression="" applyOnUpdate="0" field="M_VITESSE"/>
    <default expression="" applyOnUpdate="0" field="E_VITESSE"/>
    <default expression="" applyOnUpdate="0" field="DEBUT"/>
    <default expression="" applyOnUpdate="0" field="FIN"/>
    <default expression="" applyOnUpdate="0" field="SURF_HA"/>
    <default expression="" applyOnUpdate="0" field="NOMBRE"/>
  </defaults>
  <constraints>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="GID" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="NOM_PHY" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="ID_PHY" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="MESURE_HA" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="0_MESURE" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="NBSARM" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="M_NBSARM" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="E_NBSARM" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="DIAM" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="M_DIAM" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="E_DIAM" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="BIOM" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="M_BIOM" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="E_BIOM" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="ALTITUDE" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="M_ALTI" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="E_ALTI" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="DISTANCE" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="M_DIST" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="E_DIST" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="DERIVE" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="M_DERIVE" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="E_DERIVE" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="VITESSE" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="M_VITESSE" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="E_VITESSE" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="DEBUT" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="FIN" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="SURF_HA" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="NOMBRE" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="GID"/>
    <constraint desc="" exp="" field="NOM_PHY"/>
    <constraint desc="" exp="" field="ID_PHY"/>
    <constraint desc="" exp="" field="MESURE_HA"/>
    <constraint desc="" exp="" field="0_MESURE"/>
    <constraint desc="" exp="" field="NBSARM"/>
    <constraint desc="" exp="" field="M_NBSARM"/>
    <constraint desc="" exp="" field="E_NBSARM"/>
    <constraint desc="" exp="" field="DIAM"/>
    <constraint desc="" exp="" field="M_DIAM"/>
    <constraint desc="" exp="" field="E_DIAM"/>
    <constraint desc="" exp="" field="BIOM"/>
    <constraint desc="" exp="" field="M_BIOM"/>
    <constraint desc="" exp="" field="E_BIOM"/>
    <constraint desc="" exp="" field="ALTITUDE"/>
    <constraint desc="" exp="" field="M_ALTI"/>
    <constraint desc="" exp="" field="E_ALTI"/>
    <constraint desc="" exp="" field="DISTANCE"/>
    <constraint desc="" exp="" field="M_DIST"/>
    <constraint desc="" exp="" field="E_DIST"/>
    <constraint desc="" exp="" field="DERIVE"/>
    <constraint desc="" exp="" field="M_DERIVE"/>
    <constraint desc="" exp="" field="E_DERIVE"/>
    <constraint desc="" exp="" field="VITESSE"/>
    <constraint desc="" exp="" field="M_VITESSE"/>
    <constraint desc="" exp="" field="E_VITESSE"/>
    <constraint desc="" exp="" field="DEBUT"/>
    <constraint desc="" exp="" field="FIN"/>
    <constraint desc="" exp="" field="SURF_HA"/>
    <constraint desc="" exp="" field="NOMBRE"/>
  </constraintExpressions>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column name="GID" type="field" hidden="0" width="-1"/>
      <column name="NOM_PHY" type="field" hidden="0" width="-1"/>
      <column name="ID_PHY" type="field" hidden="0" width="-1"/>
      <column name="MESURE_HA" type="field" hidden="0" width="-1"/>
      <column name="0_MESURE" type="field" hidden="0" width="-1"/>
      <column name="NBSARM" type="field" hidden="0" width="-1"/>
      <column name="M_NBSARM" type="field" hidden="0" width="-1"/>
      <column name="E_NBSARM" type="field" hidden="0" width="-1"/>
      <column name="DIAM" type="field" hidden="0" width="-1"/>
      <column name="M_DIAM" type="field" hidden="0" width="-1"/>
      <column name="E_DIAM" type="field" hidden="0" width="-1"/>
      <column name="BIOM" type="field" hidden="0" width="-1"/>
      <column name="M_BIOM" type="field" hidden="0" width="-1"/>
      <column name="E_BIOM" type="field" hidden="0" width="-1"/>
      <column name="ALTITUDE" type="field" hidden="0" width="-1"/>
      <column name="M_ALTI" type="field" hidden="0" width="-1"/>
      <column name="E_ALTI" type="field" hidden="0" width="-1"/>
      <column name="DISTANCE" type="field" hidden="0" width="-1"/>
      <column name="M_DIST" type="field" hidden="0" width="-1"/>
      <column name="E_DIST" type="field" hidden="0" width="-1"/>
      <column name="DERIVE" type="field" hidden="0" width="-1"/>
      <column name="M_DERIVE" type="field" hidden="0" width="-1"/>
      <column name="E_DERIVE" type="field" hidden="0" width="-1"/>
      <column name="VITESSE" type="field" hidden="0" width="-1"/>
      <column name="M_VITESSE" type="field" hidden="0" width="-1"/>
      <column name="E_VITESSE" type="field" hidden="0" width="-1"/>
      <column name="DEBUT" type="field" hidden="0" width="-1"/>
      <column name="FIN" type="field" hidden="0" width="-1"/>
      <column name="SURF_HA" type="field" hidden="0" width="-1"/>
      <column name="NOMBRE" type="field" hidden="0" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
    </columns>
  </attributetableconfig>
  <editform>.</editform>
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
  <mapTip>Name</mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
