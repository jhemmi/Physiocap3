<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" maxScale="0" simplifyAlgorithm="0" simplifyMaxScale="1" version="3.4.12-Madeira" hasScaleBasedVisibilityFlag="0" labelsEnabled="1" simplifyDrawingTol="1" styleCategories="AllStyleCategories" simplifyLocal="1" minScale="0" simplifyDrawingHints="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" symbollevels="0" type="singleSymbol" forceraster="0">
    <symbols>
      <symbol force_rhr="0" type="fill" clip_to_extent="1" alpha="1" name="0">
        <layer class="SimpleFill" pass="0" enabled="1" locked="0">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="245,44,150,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,246,255"/>
          <prop k="outline_style" v="dash dot"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="no"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
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
      <text-style fontFamily="Ubuntu" previewBkgrdColor="#ffffff" fontCapitals="0" fieldName="  concat(   &#xa;  ' Parcelle : ', &quot;NOM_PHY&quot; , &#xa;  '~ Densité de points/ha : ', format_number(&quot;MESURE_HA&quot;, 0), &#xa;  '~ Diamètre :  ' , format_number( &quot;DIAM&quot;,1),&#xa;  '~ Sarment par cep : ' , format_number( &quot;NBSARCEP&quot;,1),&#xa;  '~ Biomasse par cep : ' , format_number( &quot;BIOMGCEP&quot;,1)&#xa;  )" useSubstitutions="0" namedStyle="Regular" fontSizeUnit="Point" fontWordSpacing="0" fontUnderline="0" fontStrikeout="0" fontWeight="50" isExpression="1" textColor="0,0,0,255" multilineHeight="1" fontSize="10" textOpacity="1" blendMode="0" fontLetterSpacing="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontItalic="0">
        <text-buffer bufferSize="1" bufferDraw="1" bufferNoFill="0" bufferBlendMode="0" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferOpacity="1" bufferSizeUnits="MM" bufferJoinStyle="64" bufferColor="219,219,219,255"/>
        <background shapeRadiiUnit="MM" shapeSizeX="0" shapeOffsetUnit="MM" shapeSizeY="0" shapeBorderWidth="0" shapeOffsetX="0" shapeOffsetY="0" shapeBlendMode="0" shapeDraw="0" shapeFillColor="255,255,255,255" shapeRotation="0" shapeBorderColor="128,128,128,255" shapeRadiiX="0" shapeRadiiY="0" shapeOpacity="1" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeRotationType="0" shapeType="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeSVGFile="" shapeJoinStyle="64" shapeBorderWidthUnit="MM" shapeSizeUnit="MM" shapeSizeType="0"/>
        <shadow shadowDraw="0" shadowRadius="1.5" shadowOffsetAngle="135" shadowRadiusAlphaOnly="0" shadowUnder="0" shadowOffsetDist="1" shadowColor="0,0,0,255" shadowBlendMode="6" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusUnit="MM" shadowScale="100" shadowOffsetGlobal="1" shadowOpacity="0.7" shadowOffsetUnit="MM" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0"/>
        <substitutions/>
      </text-style>
      <text-format useMaxLineLengthForAutoWrap="1" plussign="0" reverseDirectionSymbol="0" autoWrapLength="0" leftDirectionSymbol="&lt;" placeDirectionSymbol="0" addDirectionSymbol="0" rightDirectionSymbol=">" formatNumbers="0" decimals="3" wrapChar="~" multilineAlign="0"/>
      <placement labelOffsetMapUnitScale="3x:0,0,0,0,0,0" quadOffset="4" rotationAngle="0" centroidInside="1" priority="5" maxCurvedCharAngleOut="-20" repeatDistance="0" maxCurvedCharAngleIn="20" yOffset="0" xOffset="0" placementFlags="0" offsetUnits="MapUnit" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" dist="5" preserveRotation="1" placement="0" distMapUnitScale="3x:0,0,0,0,0,0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" distUnits="MM" repeatDistanceUnits="MM" centroidWhole="0" fitInPolygonOnly="0" offsetType="0"/>
      <rendering upsidedownLabels="0" mergeLines="0" maxNumLabels="2000" labelPerPart="0" obstacleFactor="1" scaleMin="1" displayAll="0" zIndex="0" minFeatureSize="0" obstacleType="0" drawLabels="1" fontMaxPixelSize="10000" scaleVisibility="0" limitNumLabels="0" fontMinPixelSize="3" scaleMax="10000000" obstacle="1" fontLimitPixelSize="0"/>
      <dd_properties>
        <Option type="Map">
          <Option value="" type="QString" name="name"/>
          <Option type="Map" name="properties">
            <Option type="Map" name="LabelRotation">
              <Option value="true" type="bool" name="active"/>
              <Option value="ORIENT_LIB" type="QString" name="field"/>
              <Option value="2" type="int" name="type"/>
            </Option>
          </Option>
          <Option value="collection" type="QString" name="type"/>
        </Option>
      </dd_properties>
    </settings>
  </labeling>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory penColor="#000000" minimumSize="0" width="15" penAlpha="255" diagramOrientation="Up" scaleDependency="Area" barWidth="5" minScaleDenominator="0" lineSizeType="MM" maxScaleDenominator="1e+8" labelPlacementMethod="XHeight" sizeType="MM" enabled="0" backgroundColor="#ffffff" height="15" backgroundAlpha="255" penWidth="0" rotationOffset="270" lineSizeScale="3x:0,0,0,0,0,0" scaleBasedVisibility="0" opacity="1" sizeScale="3x:0,0,0,0,0,0">
      <fontProperties style="" description="Ubuntu,11,-1,5,50,0,0,0,0,0"/>
      <attribute field="" color="#000000" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings showAll="1" zIndex="0" linePlacementFlags="18" priority="0" obstacle="0" dist="0" placement="0">
    <properties>
      <Option type="Map">
        <Option value="" type="QString" name="name"/>
        <Option name="properties"/>
        <Option value="collection" type="QString" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
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
    <field name="BIOMGM2">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="M_BIOMGM2">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="E_BIOMGM2">
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
    <field name="M_BIOMGCEP">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="E_BIOMGCEP">
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
    <field name="M_BIOMM2">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="E_BIOMM2">
      <editWidget type="TextEdit">
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
    <field name="M_NBSARMM2">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="E_NBSARMM2">
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
    <field name="M_NBSARCEP">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="E_NBSARCEP">
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
    <field name="ORIENT_LIB">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="GID" index="0" name=""/>
    <alias field="NOM_PHY" index="1" name=""/>
    <alias field="ID_PHY" index="2" name=""/>
    <alias field="MESURE_HA" index="3" name=""/>
    <alias field="NBSARM" index="4" name=""/>
    <alias field="M_NBSARM" index="5" name=""/>
    <alias field="E_NBSARM" index="6" name=""/>
    <alias field="DIAM" index="7" name=""/>
    <alias field="M_DIAM" index="8" name=""/>
    <alias field="E_DIAM" index="9" name=""/>
    <alias field="BIOM" index="10" name=""/>
    <alias field="M_BIOM" index="11" name=""/>
    <alias field="E_BIOM" index="12" name=""/>
    <alias field="BIOMGM2" index="13" name=""/>
    <alias field="M_BIOMGM2" index="14" name=""/>
    <alias field="E_BIOMGM2" index="15" name=""/>
    <alias field="BIOMGCEP" index="16" name=""/>
    <alias field="M_BIOMGCEP" index="17" name=""/>
    <alias field="E_BIOMGCEP" index="18" name=""/>
    <alias field="BIOMM2" index="19" name=""/>
    <alias field="M_BIOMM2" index="20" name=""/>
    <alias field="E_BIOMM2" index="21" name=""/>
    <alias field="NBSARMM2" index="22" name=""/>
    <alias field="M_NBSARMM2" index="23" name=""/>
    <alias field="E_NBSARMM2" index="24" name=""/>
    <alias field="NBSARCEP" index="25" name=""/>
    <alias field="M_NBSARCEP" index="26" name=""/>
    <alias field="E_NBSARCEP" index="27" name=""/>
    <alias field="VITESSE" index="28" name=""/>
    <alias field="M_VITESSE" index="29" name=""/>
    <alias field="E_VITESSE" index="30" name=""/>
    <alias field="DEBUT" index="31" name=""/>
    <alias field="FIN" index="32" name=""/>
    <alias field="SURF_HA" index="33" name=""/>
    <alias field="NOMBRE" index="34" name=""/>
    <alias field="ORIENT_LIB" index="35" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="GID" applyOnUpdate="0" expression=""/>
    <default field="NOM_PHY" applyOnUpdate="0" expression=""/>
    <default field="ID_PHY" applyOnUpdate="0" expression=""/>
    <default field="MESURE_HA" applyOnUpdate="0" expression=""/>
    <default field="NBSARM" applyOnUpdate="0" expression=""/>
    <default field="M_NBSARM" applyOnUpdate="0" expression=""/>
    <default field="E_NBSARM" applyOnUpdate="0" expression=""/>
    <default field="DIAM" applyOnUpdate="0" expression=""/>
    <default field="M_DIAM" applyOnUpdate="0" expression=""/>
    <default field="E_DIAM" applyOnUpdate="0" expression=""/>
    <default field="BIOM" applyOnUpdate="0" expression=""/>
    <default field="M_BIOM" applyOnUpdate="0" expression=""/>
    <default field="E_BIOM" applyOnUpdate="0" expression=""/>
    <default field="BIOMGM2" applyOnUpdate="0" expression=""/>
    <default field="M_BIOMGM2" applyOnUpdate="0" expression=""/>
    <default field="E_BIOMGM2" applyOnUpdate="0" expression=""/>
    <default field="BIOMGCEP" applyOnUpdate="0" expression=""/>
    <default field="M_BIOMGCEP" applyOnUpdate="0" expression=""/>
    <default field="E_BIOMGCEP" applyOnUpdate="0" expression=""/>
    <default field="BIOMM2" applyOnUpdate="0" expression=""/>
    <default field="M_BIOMM2" applyOnUpdate="0" expression=""/>
    <default field="E_BIOMM2" applyOnUpdate="0" expression=""/>
    <default field="NBSARMM2" applyOnUpdate="0" expression=""/>
    <default field="M_NBSARMM2" applyOnUpdate="0" expression=""/>
    <default field="E_NBSARMM2" applyOnUpdate="0" expression=""/>
    <default field="NBSARCEP" applyOnUpdate="0" expression=""/>
    <default field="M_NBSARCEP" applyOnUpdate="0" expression=""/>
    <default field="E_NBSARCEP" applyOnUpdate="0" expression=""/>
    <default field="VITESSE" applyOnUpdate="0" expression=""/>
    <default field="M_VITESSE" applyOnUpdate="0" expression=""/>
    <default field="E_VITESSE" applyOnUpdate="0" expression=""/>
    <default field="DEBUT" applyOnUpdate="0" expression=""/>
    <default field="FIN" applyOnUpdate="0" expression=""/>
    <default field="SURF_HA" applyOnUpdate="0" expression=""/>
    <default field="NOMBRE" applyOnUpdate="0" expression=""/>
    <default field="ORIENT_LIB" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint field="GID" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="NOM_PHY" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="ID_PHY" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="MESURE_HA" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="NBSARM" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="M_NBSARM" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="E_NBSARM" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="DIAM" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="M_DIAM" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="E_DIAM" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="BIOM" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="M_BIOM" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="E_BIOM" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="BIOMGM2" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="M_BIOMGM2" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="E_BIOMGM2" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="BIOMGCEP" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="M_BIOMGCEP" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="E_BIOMGCEP" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="BIOMM2" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="M_BIOMM2" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="E_BIOMM2" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="NBSARMM2" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="M_NBSARMM2" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="E_NBSARMM2" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="NBSARCEP" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="M_NBSARCEP" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="E_NBSARCEP" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="VITESSE" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="M_VITESSE" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="E_VITESSE" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="DEBUT" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="FIN" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="SURF_HA" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="NOMBRE" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
    <constraint field="ORIENT_LIB" exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="GID" exp="" desc=""/>
    <constraint field="NOM_PHY" exp="" desc=""/>
    <constraint field="ID_PHY" exp="" desc=""/>
    <constraint field="MESURE_HA" exp="" desc=""/>
    <constraint field="NBSARM" exp="" desc=""/>
    <constraint field="M_NBSARM" exp="" desc=""/>
    <constraint field="E_NBSARM" exp="" desc=""/>
    <constraint field="DIAM" exp="" desc=""/>
    <constraint field="M_DIAM" exp="" desc=""/>
    <constraint field="E_DIAM" exp="" desc=""/>
    <constraint field="BIOM" exp="" desc=""/>
    <constraint field="M_BIOM" exp="" desc=""/>
    <constraint field="E_BIOM" exp="" desc=""/>
    <constraint field="BIOMGM2" exp="" desc=""/>
    <constraint field="M_BIOMGM2" exp="" desc=""/>
    <constraint field="E_BIOMGM2" exp="" desc=""/>
    <constraint field="BIOMGCEP" exp="" desc=""/>
    <constraint field="M_BIOMGCEP" exp="" desc=""/>
    <constraint field="E_BIOMGCEP" exp="" desc=""/>
    <constraint field="BIOMM2" exp="" desc=""/>
    <constraint field="M_BIOMM2" exp="" desc=""/>
    <constraint field="E_BIOMM2" exp="" desc=""/>
    <constraint field="NBSARMM2" exp="" desc=""/>
    <constraint field="M_NBSARMM2" exp="" desc=""/>
    <constraint field="E_NBSARMM2" exp="" desc=""/>
    <constraint field="NBSARCEP" exp="" desc=""/>
    <constraint field="M_NBSARCEP" exp="" desc=""/>
    <constraint field="E_NBSARCEP" exp="" desc=""/>
    <constraint field="VITESSE" exp="" desc=""/>
    <constraint field="M_VITESSE" exp="" desc=""/>
    <constraint field="E_VITESSE" exp="" desc=""/>
    <constraint field="DEBUT" exp="" desc=""/>
    <constraint field="FIN" exp="" desc=""/>
    <constraint field="SURF_HA" exp="" desc=""/>
    <constraint field="NOMBRE" exp="" desc=""/>
    <constraint field="ORIENT_LIB" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields>
    <field comment="" typeName="double" length="10" precision="2" type="6" expression=" &quot;ORIENT_A&quot; -90&#xa; " subType="0" name="ORIENT_LIB"/>
  </expressionfields>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column width="-1" type="field" hidden="0" name="GID"/>
      <column width="-1" type="field" hidden="0" name="NOM_PHY"/>
      <column width="-1" type="field" hidden="0" name="ID_PHY"/>
      <column width="-1" type="field" hidden="0" name="MESURE_HA"/>
      <column width="-1" type="field" hidden="0" name="NBSARM"/>
      <column width="-1" type="field" hidden="0" name="M_NBSARM"/>
      <column width="-1" type="field" hidden="0" name="E_NBSARM"/>
      <column width="-1" type="field" hidden="0" name="DIAM"/>
      <column width="-1" type="field" hidden="0" name="M_DIAM"/>
      <column width="-1" type="field" hidden="0" name="E_DIAM"/>
      <column width="-1" type="field" hidden="0" name="BIOM"/>
      <column width="-1" type="field" hidden="0" name="M_BIOM"/>
      <column width="-1" type="field" hidden="0" name="E_BIOM"/>
      <column width="-1" type="field" hidden="0" name="VITESSE"/>
      <column width="-1" type="field" hidden="0" name="M_VITESSE"/>
      <column width="-1" type="field" hidden="0" name="E_VITESSE"/>
      <column width="-1" type="field" hidden="0" name="DEBUT"/>
      <column width="-1" type="field" hidden="0" name="FIN"/>
      <column width="-1" type="field" hidden="0" name="SURF_HA"/>
      <column width="-1" type="field" hidden="0" name="NOMBRE"/>
      <column width="-1" type="actions" hidden="1"/>
      <column width="-1" type="field" hidden="0" name="ORIENT_LIB"/>
      <column width="-1" type="field" hidden="0" name="BIOMGM2"/>
      <column width="-1" type="field" hidden="0" name="M_BIOMGM2"/>
      <column width="-1" type="field" hidden="0" name="E_BIOMGM2"/>
      <column width="-1" type="field" hidden="0" name="BIOMGCEP"/>
      <column width="-1" type="field" hidden="0" name="M_BIOMGCEP"/>
      <column width="-1" type="field" hidden="0" name="E_BIOMGCEP"/>
      <column width="-1" type="field" hidden="0" name="BIOMM2"/>
      <column width="-1" type="field" hidden="0" name="M_BIOMM2"/>
      <column width="-1" type="field" hidden="0" name="E_BIOMM2"/>
      <column width="-1" type="field" hidden="0" name="NBSARMM2"/>
      <column width="-1" type="field" hidden="0" name="M_NBSARMM2"/>
      <column width="-1" type="field" hidden="0" name="E_NBSARMM2"/>
      <column width="-1" type="field" hidden="0" name="NBSARCEP"/>
      <column width="-1" type="field" hidden="0" name="M_NBSARCEP"/>
      <column width="-1" type="field" hidden="0" name="E_NBSARCEP"/>
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
    <field editable="1" name="0_MESURE"/>
    <field editable="1" name="ALTITUDE"/>
    <field editable="1" name="BIOM"/>
    <field editable="1" name="BIOMGCEP"/>
    <field editable="1" name="BIOMGM2"/>
    <field editable="1" name="BIOMM2"/>
    <field editable="1" name="DEBUT"/>
    <field editable="1" name="DERIVE"/>
    <field editable="1" name="DIAM"/>
    <field editable="1" name="DISTANCE"/>
    <field editable="1" name="E_ALTI"/>
    <field editable="1" name="E_BIOM"/>
    <field editable="1" name="E_BIOMGCEP"/>
    <field editable="1" name="E_BIOMGM2"/>
    <field editable="1" name="E_BIOMM2"/>
    <field editable="1" name="E_DERIVE"/>
    <field editable="1" name="E_DIAM"/>
    <field editable="1" name="E_DIST"/>
    <field editable="1" name="E_LONG_S"/>
    <field editable="1" name="E_NBSARCEP"/>
    <field editable="1" name="E_NBSARM"/>
    <field editable="1" name="E_NBSARMM2"/>
    <field editable="1" name="E_ORIENT_A"/>
    <field editable="1" name="E_ORIENT_R"/>
    <field editable="1" name="E_PASS"/>
    <field editable="1" name="E_PDOP"/>
    <field editable="1" name="E_VITESSE"/>
    <field editable="1" name="FIN"/>
    <field editable="1" name="GID"/>
    <field editable="1" name="ID_PHY"/>
    <field editable="1" name="LONG_S"/>
    <field editable="1" name="MESURE_HA"/>
    <field editable="1" name="M_ALTI"/>
    <field editable="1" name="M_BIOM"/>
    <field editable="1" name="M_BIOMGCEP"/>
    <field editable="1" name="M_BIOMGM2"/>
    <field editable="1" name="M_BIOMM2"/>
    <field editable="1" name="M_DERIVE"/>
    <field editable="1" name="M_DIAM"/>
    <field editable="1" name="M_DIST"/>
    <field editable="1" name="M_LONG_S"/>
    <field editable="1" name="M_NBSARCEP"/>
    <field editable="1" name="M_NBSARM"/>
    <field editable="1" name="M_NBSARMM2"/>
    <field editable="1" name="M_ORIENT_A"/>
    <field editable="1" name="M_ORIENT_R"/>
    <field editable="1" name="M_PASS"/>
    <field editable="1" name="M_PDOP"/>
    <field editable="1" name="M_VITESSE"/>
    <field editable="1" name="NBSARCEP"/>
    <field editable="1" name="NBSARM"/>
    <field editable="1" name="NBSARMM2"/>
    <field editable="1" name="NBSARM_S"/>
    <field editable="1" name="NBSART"/>
    <field editable="1" name="NB_SEG"/>
    <field editable="1" name="NOMBRE"/>
    <field editable="1" name="NOM_PHY"/>
    <field editable="1" name="ORIENT_A"/>
    <field editable="0" name="ORIENT_LIB"/>
    <field editable="1" name="ORIENT_R"/>
    <field editable="1" name="PASSAGE"/>
    <field editable="1" name="PDOP"/>
    <field editable="1" name="SURF_HA"/>
    <field editable="1" name="T_LONG_SEG"/>
    <field editable="1" name="VITESSE"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="0_MESURE"/>
    <field labelOnTop="0" name="ALTITUDE"/>
    <field labelOnTop="0" name="BIOM"/>
    <field labelOnTop="0" name="BIOMGCEP"/>
    <field labelOnTop="0" name="BIOMGM2"/>
    <field labelOnTop="0" name="BIOMM2"/>
    <field labelOnTop="0" name="DEBUT"/>
    <field labelOnTop="0" name="DERIVE"/>
    <field labelOnTop="0" name="DIAM"/>
    <field labelOnTop="0" name="DISTANCE"/>
    <field labelOnTop="0" name="E_ALTI"/>
    <field labelOnTop="0" name="E_BIOM"/>
    <field labelOnTop="0" name="E_BIOMGCEP"/>
    <field labelOnTop="0" name="E_BIOMGM2"/>
    <field labelOnTop="0" name="E_BIOMM2"/>
    <field labelOnTop="0" name="E_DERIVE"/>
    <field labelOnTop="0" name="E_DIAM"/>
    <field labelOnTop="0" name="E_DIST"/>
    <field labelOnTop="0" name="E_LONG_S"/>
    <field labelOnTop="0" name="E_NBSARCEP"/>
    <field labelOnTop="0" name="E_NBSARM"/>
    <field labelOnTop="0" name="E_NBSARMM2"/>
    <field labelOnTop="0" name="E_ORIENT_A"/>
    <field labelOnTop="0" name="E_ORIENT_R"/>
    <field labelOnTop="0" name="E_PASS"/>
    <field labelOnTop="0" name="E_PDOP"/>
    <field labelOnTop="0" name="E_VITESSE"/>
    <field labelOnTop="0" name="FIN"/>
    <field labelOnTop="0" name="GID"/>
    <field labelOnTop="0" name="ID_PHY"/>
    <field labelOnTop="0" name="LONG_S"/>
    <field labelOnTop="0" name="MESURE_HA"/>
    <field labelOnTop="0" name="M_ALTI"/>
    <field labelOnTop="0" name="M_BIOM"/>
    <field labelOnTop="0" name="M_BIOMGCEP"/>
    <field labelOnTop="0" name="M_BIOMGM2"/>
    <field labelOnTop="0" name="M_BIOMM2"/>
    <field labelOnTop="0" name="M_DERIVE"/>
    <field labelOnTop="0" name="M_DIAM"/>
    <field labelOnTop="0" name="M_DIST"/>
    <field labelOnTop="0" name="M_LONG_S"/>
    <field labelOnTop="0" name="M_NBSARCEP"/>
    <field labelOnTop="0" name="M_NBSARM"/>
    <field labelOnTop="0" name="M_NBSARMM2"/>
    <field labelOnTop="0" name="M_ORIENT_A"/>
    <field labelOnTop="0" name="M_ORIENT_R"/>
    <field labelOnTop="0" name="M_PASS"/>
    <field labelOnTop="0" name="M_PDOP"/>
    <field labelOnTop="0" name="M_VITESSE"/>
    <field labelOnTop="0" name="NBSARCEP"/>
    <field labelOnTop="0" name="NBSARM"/>
    <field labelOnTop="0" name="NBSARMM2"/>
    <field labelOnTop="0" name="NBSARM_S"/>
    <field labelOnTop="0" name="NBSART"/>
    <field labelOnTop="0" name="NB_SEG"/>
    <field labelOnTop="0" name="NOMBRE"/>
    <field labelOnTop="0" name="NOM_PHY"/>
    <field labelOnTop="0" name="ORIENT_A"/>
    <field labelOnTop="0" name="ORIENT_LIB"/>
    <field labelOnTop="0" name="ORIENT_R"/>
    <field labelOnTop="0" name="PASSAGE"/>
    <field labelOnTop="0" name="PDOP"/>
    <field labelOnTop="0" name="SURF_HA"/>
    <field labelOnTop="0" name="T_LONG_SEG"/>
    <field labelOnTop="0" name="VITESSE"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>GID</previewExpression>
  <mapTip>Name</mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
