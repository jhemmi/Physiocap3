<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis minScale="0" simplifyAlgorithm="0" labelsEnabled="1" readOnly="0" maxScale="0" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" simplifyDrawingHints="1" simplifyDrawingTol="1" simplifyMaxScale="1" version="3.4.12-Madeira" styleCategories="AllStyleCategories">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="singleSymbol" symbollevels="0" forceraster="0" enableorderby="0">
    <symbols>
      <symbol type="fill" name="0" force_rhr="0" clip_to_extent="1" alpha="1">
        <layer enabled="1" pass="0" locked="0" class="SimpleFill">
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
  <labeling type="simple">
    <settings>
      <text-style fontCapitals="0" fontItalic="0" namedStyle="Regular" fontWordSpacing="0" fontFamily="Ubuntu" fontSizeUnit="Point" fontWeight="50" fontLetterSpacing="0" fieldName="  concat(   &#xa;  ' Parcelle : ', &quot;NOM_PHY&quot; , &#xa;  '~ Densité de points/ha : ', format_number(&quot;MESURE_HA&quot;, 0), &#xa;  '~ Diamètre == ' , format_number( &quot;DIAM&quot;,0),&#xa;  '~ Sarment == ' , format_number( &quot;NBSARCEP&quot;,0),&#xa;  '~ Biomasse == ' , format_number( &quot;BIOMGCEP&quot;,0)&#xa;  )" textOpacity="1" multilineHeight="1" useSubstitutions="0" isExpression="1" previewBkgrdColor="#ffffff" fontSize="10" textColor="0,0,0,255" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontUnderline="0" blendMode="0" fontStrikeout="0">
        <text-buffer bufferSize="1" bufferJoinStyle="64" bufferDraw="1" bufferOpacity="1" bufferColor="219,219,219,255" bufferBlendMode="0" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferSizeUnits="MM" bufferNoFill="0"/>
        <background shapeRadiiY="0" shapeSVGFile="" shapeFillColor="255,255,255,255" shapeRotation="0" shapeSizeX="0" shapeOffsetUnit="MM" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeSizeY="0" shapeRotationType="0" shapeJoinStyle="64" shapeOffsetX="0" shapeOffsetY="0" shapeDraw="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeType="0" shapeSizeUnit="MM" shapeBorderWidth="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiUnit="MM" shapeOpacity="1" shapeBlendMode="0" shapeBorderWidthUnit="MM" shapeType="0" shapeBorderColor="128,128,128,255" shapeRadiiX="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0"/>
        <shadow shadowDraw="0" shadowUnder="0" shadowOffsetUnit="MM" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowColor="0,0,0,255" shadowOffsetAngle="135" shadowOpacity="0.7" shadowScale="100" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusAlphaOnly="0" shadowOffsetDist="1" shadowRadius="1.5" shadowBlendMode="6" shadowOffsetGlobal="1" shadowRadiusUnit="MM"/>
        <substitutions/>
      </text-style>
      <text-format wrapChar="~" leftDirectionSymbol="&lt;" multilineAlign="0" placeDirectionSymbol="0" rightDirectionSymbol=">" formatNumbers="0" plussign="0" autoWrapLength="0" addDirectionSymbol="0" reverseDirectionSymbol="0" useMaxLineLengthForAutoWrap="1" decimals="3"/>
      <placement placementFlags="0" quadOffset="4" preserveRotation="1" distMapUnitScale="3x:0,0,0,0,0,0" priority="5" distUnits="MM" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" fitInPolygonOnly="0" centroidWhole="0" yOffset="0" xOffset="0" repeatDistanceUnits="MM" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" centroidInside="1" dist="5" maxCurvedCharAngleOut="-20" rotationAngle="0" placement="0" repeatDistance="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MapUnit" maxCurvedCharAngleIn="20" offsetType="0"/>
      <rendering labelPerPart="0" maxNumLabels="2000" fontMinPixelSize="3" minFeatureSize="0" fontMaxPixelSize="10000" mergeLines="0" scaleMin="1" upsidedownLabels="0" displayAll="0" limitNumLabels="0" fontLimitPixelSize="0" scaleVisibility="0" obstacleType="0" drawLabels="1" obstacleFactor="1" zIndex="0" scaleMax="10000000" obstacle="1"/>
      <dd_properties>
        <Option type="Map">
          <Option type="QString" value="" name="name"/>
          <Option type="Map" name="properties">
            <Option type="Map" name="LabelRotation">
              <Option type="bool" value="true" name="active"/>
              <Option type="QString" value="ORIENT_LIB" name="field"/>
              <Option type="int" value="2" name="type"/>
            </Option>
          </Option>
          <Option type="QString" value="collection" name="type"/>
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
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory height="15" barWidth="5" minScaleDenominator="0" penColor="#000000" scaleDependency="Area" penAlpha="255" maxScaleDenominator="1e+8" sizeScale="3x:0,0,0,0,0,0" labelPlacementMethod="XHeight" width="15" lineSizeScale="3x:0,0,0,0,0,0" lineSizeType="MM" backgroundColor="#ffffff" sizeType="MM" backgroundAlpha="255" rotationOffset="270" diagramOrientation="Up" minimumSize="0" scaleBasedVisibility="0" enabled="0" penWidth="0" opacity="1">
      <fontProperties style="" description="Ubuntu,11,-1,5,50,0,0,0,0,0"/>
      <attribute field="" color="#000000" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings priority="0" obstacle="0" zIndex="0" placement="0" dist="0" linePlacementFlags="18" showAll="1">
    <properties>
      <Option type="Map">
        <Option type="QString" value="" name="name"/>
        <Option name="properties"/>
        <Option type="QString" value="collection" name="type"/>
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
    <default field="GID" expression="" applyOnUpdate="0"/>
    <default field="NOM_PHY" expression="" applyOnUpdate="0"/>
    <default field="ID_PHY" expression="" applyOnUpdate="0"/>
    <default field="MESURE_HA" expression="" applyOnUpdate="0"/>
    <default field="NBSARM" expression="" applyOnUpdate="0"/>
    <default field="M_NBSARM" expression="" applyOnUpdate="0"/>
    <default field="E_NBSARM" expression="" applyOnUpdate="0"/>
    <default field="DIAM" expression="" applyOnUpdate="0"/>
    <default field="M_DIAM" expression="" applyOnUpdate="0"/>
    <default field="E_DIAM" expression="" applyOnUpdate="0"/>
    <default field="BIOM" expression="" applyOnUpdate="0"/>
    <default field="M_BIOM" expression="" applyOnUpdate="0"/>
    <default field="E_BIOM" expression="" applyOnUpdate="0"/>
    <default field="BIOMGM2" expression="" applyOnUpdate="0"/>
    <default field="M_BIOMGM2" expression="" applyOnUpdate="0"/>
    <default field="E_BIOMGM2" expression="" applyOnUpdate="0"/>
    <default field="BIOMGCEP" expression="" applyOnUpdate="0"/>
    <default field="M_BIOMGCEP" expression="" applyOnUpdate="0"/>
    <default field="E_BIOMGCEP" expression="" applyOnUpdate="0"/>
    <default field="BIOMM2" expression="" applyOnUpdate="0"/>
    <default field="M_BIOMM2" expression="" applyOnUpdate="0"/>
    <default field="E_BIOMM2" expression="" applyOnUpdate="0"/>
    <default field="NBSARMM2" expression="" applyOnUpdate="0"/>
    <default field="M_NBSARMM2" expression="" applyOnUpdate="0"/>
    <default field="E_NBSARMM2" expression="" applyOnUpdate="0"/>
    <default field="NBSARCEP" expression="" applyOnUpdate="0"/>
    <default field="M_NBSARCEP" expression="" applyOnUpdate="0"/>
    <default field="E_NBSARCEP" expression="" applyOnUpdate="0"/>
    <default field="VITESSE" expression="" applyOnUpdate="0"/>
    <default field="M_VITESSE" expression="" applyOnUpdate="0"/>
    <default field="E_VITESSE" expression="" applyOnUpdate="0"/>
    <default field="DEBUT" expression="" applyOnUpdate="0"/>
    <default field="FIN" expression="" applyOnUpdate="0"/>
    <default field="SURF_HA" expression="" applyOnUpdate="0"/>
    <default field="NOMBRE" expression="" applyOnUpdate="0"/>
    <default field="ORIENT_LIB" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="GID" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="NOM_PHY" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="ID_PHY" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="MESURE_HA" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="NBSARM" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="M_NBSARM" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="E_NBSARM" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="DIAM" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="M_DIAM" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="E_DIAM" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="BIOM" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="M_BIOM" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="E_BIOM" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="BIOMGM2" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="M_BIOMGM2" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="E_BIOMGM2" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="BIOMGCEP" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="M_BIOMGCEP" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="E_BIOMGCEP" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="BIOMM2" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="M_BIOMM2" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="E_BIOMM2" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="NBSARMM2" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="M_NBSARMM2" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="E_NBSARMM2" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="NBSARCEP" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="M_NBSARCEP" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="E_NBSARCEP" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="VITESSE" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="M_VITESSE" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="E_VITESSE" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="DEBUT" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="FIN" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="SURF_HA" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="NOMBRE" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="ORIENT_LIB" unique_strength="0" constraints="0" notnull_strength="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="GID" desc="" exp=""/>
    <constraint field="NOM_PHY" desc="" exp=""/>
    <constraint field="ID_PHY" desc="" exp=""/>
    <constraint field="MESURE_HA" desc="" exp=""/>
    <constraint field="NBSARM" desc="" exp=""/>
    <constraint field="M_NBSARM" desc="" exp=""/>
    <constraint field="E_NBSARM" desc="" exp=""/>
    <constraint field="DIAM" desc="" exp=""/>
    <constraint field="M_DIAM" desc="" exp=""/>
    <constraint field="E_DIAM" desc="" exp=""/>
    <constraint field="BIOM" desc="" exp=""/>
    <constraint field="M_BIOM" desc="" exp=""/>
    <constraint field="E_BIOM" desc="" exp=""/>
    <constraint field="BIOMGM2" desc="" exp=""/>
    <constraint field="M_BIOMGM2" desc="" exp=""/>
    <constraint field="E_BIOMGM2" desc="" exp=""/>
    <constraint field="BIOMGCEP" desc="" exp=""/>
    <constraint field="M_BIOMGCEP" desc="" exp=""/>
    <constraint field="E_BIOMGCEP" desc="" exp=""/>
    <constraint field="BIOMM2" desc="" exp=""/>
    <constraint field="M_BIOMM2" desc="" exp=""/>
    <constraint field="E_BIOMM2" desc="" exp=""/>
    <constraint field="NBSARMM2" desc="" exp=""/>
    <constraint field="M_NBSARMM2" desc="" exp=""/>
    <constraint field="E_NBSARMM2" desc="" exp=""/>
    <constraint field="NBSARCEP" desc="" exp=""/>
    <constraint field="M_NBSARCEP" desc="" exp=""/>
    <constraint field="E_NBSARCEP" desc="" exp=""/>
    <constraint field="VITESSE" desc="" exp=""/>
    <constraint field="M_VITESSE" desc="" exp=""/>
    <constraint field="E_VITESSE" desc="" exp=""/>
    <constraint field="DEBUT" desc="" exp=""/>
    <constraint field="FIN" desc="" exp=""/>
    <constraint field="SURF_HA" desc="" exp=""/>
    <constraint field="NOMBRE" desc="" exp=""/>
    <constraint field="ORIENT_LIB" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields>
    <field type="6" subType="0" comment="" typeName="double" name="ORIENT_LIB" expression=" &quot;ORIENT_A&quot; -90&#xa; " length="10" precision="2"/>
  </expressionfields>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column type="field" hidden="0" width="-1" name="GID"/>
      <column type="field" hidden="0" width="-1" name="NOM_PHY"/>
      <column type="field" hidden="0" width="-1" name="ID_PHY"/>
      <column type="field" hidden="0" width="-1" name="MESURE_HA"/>
      <column type="field" hidden="0" width="-1" name="NBSARM"/>
      <column type="field" hidden="0" width="-1" name="M_NBSARM"/>
      <column type="field" hidden="0" width="-1" name="E_NBSARM"/>
      <column type="field" hidden="0" width="-1" name="DIAM"/>
      <column type="field" hidden="0" width="-1" name="M_DIAM"/>
      <column type="field" hidden="0" width="-1" name="E_DIAM"/>
      <column type="field" hidden="0" width="-1" name="BIOM"/>
      <column type="field" hidden="0" width="-1" name="M_BIOM"/>
      <column type="field" hidden="0" width="-1" name="E_BIOM"/>
      <column type="field" hidden="0" width="-1" name="VITESSE"/>
      <column type="field" hidden="0" width="-1" name="M_VITESSE"/>
      <column type="field" hidden="0" width="-1" name="E_VITESSE"/>
      <column type="field" hidden="0" width="-1" name="DEBUT"/>
      <column type="field" hidden="0" width="-1" name="FIN"/>
      <column type="field" hidden="0" width="-1" name="SURF_HA"/>
      <column type="field" hidden="0" width="-1" name="NOMBRE"/>
      <column type="actions" hidden="1" width="-1"/>
      <column type="field" hidden="0" width="-1" name="ORIENT_LIB"/>
      <column type="field" hidden="0" width="-1" name="BIOMGM2"/>
      <column type="field" hidden="0" width="-1" name="M_BIOMGM2"/>
      <column type="field" hidden="0" width="-1" name="E_BIOMGM2"/>
      <column type="field" hidden="0" width="-1" name="BIOMGCEP"/>
      <column type="field" hidden="0" width="-1" name="M_BIOMGCEP"/>
      <column type="field" hidden="0" width="-1" name="E_BIOMGCEP"/>
      <column type="field" hidden="0" width="-1" name="BIOMM2"/>
      <column type="field" hidden="0" width="-1" name="M_BIOMM2"/>
      <column type="field" hidden="0" width="-1" name="E_BIOMM2"/>
      <column type="field" hidden="0" width="-1" name="NBSARMM2"/>
      <column type="field" hidden="0" width="-1" name="M_NBSARMM2"/>
      <column type="field" hidden="0" width="-1" name="E_NBSARMM2"/>
      <column type="field" hidden="0" width="-1" name="NBSARCEP"/>
      <column type="field" hidden="0" width="-1" name="M_NBSARCEP"/>
      <column type="field" hidden="0" width="-1" name="E_NBSARCEP"/>
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
    <field name="0_MESURE" editable="1"/>
    <field name="ALTITUDE" editable="1"/>
    <field name="BIOM" editable="1"/>
    <field name="BIOMGCEP" editable="1"/>
    <field name="BIOMGM2" editable="1"/>
    <field name="BIOMM2" editable="1"/>
    <field name="DEBUT" editable="1"/>
    <field name="DERIVE" editable="1"/>
    <field name="DIAM" editable="1"/>
    <field name="DISTANCE" editable="1"/>
    <field name="E_ALTI" editable="1"/>
    <field name="E_BIOM" editable="1"/>
    <field name="E_BIOMGCEP" editable="1"/>
    <field name="E_BIOMGM2" editable="1"/>
    <field name="E_BIOMM2" editable="1"/>
    <field name="E_DERIVE" editable="1"/>
    <field name="E_DIAM" editable="1"/>
    <field name="E_DIST" editable="1"/>
    <field name="E_LONG_S" editable="1"/>
    <field name="E_NBSARCEP" editable="1"/>
    <field name="E_NBSARM" editable="1"/>
    <field name="E_NBSARMM2" editable="1"/>
    <field name="E_ORIENT_A" editable="1"/>
    <field name="E_ORIENT_R" editable="1"/>
    <field name="E_PASS" editable="1"/>
    <field name="E_PDOP" editable="1"/>
    <field name="E_VITESSE" editable="1"/>
    <field name="FIN" editable="1"/>
    <field name="GID" editable="1"/>
    <field name="ID_PHY" editable="1"/>
    <field name="LONG_S" editable="1"/>
    <field name="MESURE_HA" editable="1"/>
    <field name="M_ALTI" editable="1"/>
    <field name="M_BIOM" editable="1"/>
    <field name="M_BIOMGCEP" editable="1"/>
    <field name="M_BIOMGM2" editable="1"/>
    <field name="M_BIOMM2" editable="1"/>
    <field name="M_DERIVE" editable="1"/>
    <field name="M_DIAM" editable="1"/>
    <field name="M_DIST" editable="1"/>
    <field name="M_LONG_S" editable="1"/>
    <field name="M_NBSARCEP" editable="1"/>
    <field name="M_NBSARM" editable="1"/>
    <field name="M_NBSARMM2" editable="1"/>
    <field name="M_ORIENT_A" editable="1"/>
    <field name="M_ORIENT_R" editable="1"/>
    <field name="M_PASS" editable="1"/>
    <field name="M_PDOP" editable="1"/>
    <field name="M_VITESSE" editable="1"/>
    <field name="NBSARCEP" editable="1"/>
    <field name="NBSARM" editable="1"/>
    <field name="NBSARMM2" editable="1"/>
    <field name="NBSARM_S" editable="1"/>
    <field name="NBSART" editable="1"/>
    <field name="NB_SEG" editable="1"/>
    <field name="NOMBRE" editable="1"/>
    <field name="NOM_PHY" editable="1"/>
    <field name="ORIENT_A" editable="1"/>
    <field name="ORIENT_LIB" editable="0"/>
    <field name="ORIENT_R" editable="1"/>
    <field name="PASSAGE" editable="1"/>
    <field name="PDOP" editable="1"/>
    <field name="SURF_HA" editable="1"/>
    <field name="T_LONG_SEG" editable="1"/>
    <field name="VITESSE" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="0_MESURE" labelOnTop="0"/>
    <field name="ALTITUDE" labelOnTop="0"/>
    <field name="BIOM" labelOnTop="0"/>
    <field name="BIOMGCEP" labelOnTop="0"/>
    <field name="BIOMGM2" labelOnTop="0"/>
    <field name="BIOMM2" labelOnTop="0"/>
    <field name="DEBUT" labelOnTop="0"/>
    <field name="DERIVE" labelOnTop="0"/>
    <field name="DIAM" labelOnTop="0"/>
    <field name="DISTANCE" labelOnTop="0"/>
    <field name="E_ALTI" labelOnTop="0"/>
    <field name="E_BIOM" labelOnTop="0"/>
    <field name="E_BIOMGCEP" labelOnTop="0"/>
    <field name="E_BIOMGM2" labelOnTop="0"/>
    <field name="E_BIOMM2" labelOnTop="0"/>
    <field name="E_DERIVE" labelOnTop="0"/>
    <field name="E_DIAM" labelOnTop="0"/>
    <field name="E_DIST" labelOnTop="0"/>
    <field name="E_LONG_S" labelOnTop="0"/>
    <field name="E_NBSARCEP" labelOnTop="0"/>
    <field name="E_NBSARM" labelOnTop="0"/>
    <field name="E_NBSARMM2" labelOnTop="0"/>
    <field name="E_ORIENT_A" labelOnTop="0"/>
    <field name="E_ORIENT_R" labelOnTop="0"/>
    <field name="E_PASS" labelOnTop="0"/>
    <field name="E_PDOP" labelOnTop="0"/>
    <field name="E_VITESSE" labelOnTop="0"/>
    <field name="FIN" labelOnTop="0"/>
    <field name="GID" labelOnTop="0"/>
    <field name="ID_PHY" labelOnTop="0"/>
    <field name="LONG_S" labelOnTop="0"/>
    <field name="MESURE_HA" labelOnTop="0"/>
    <field name="M_ALTI" labelOnTop="0"/>
    <field name="M_BIOM" labelOnTop="0"/>
    <field name="M_BIOMGCEP" labelOnTop="0"/>
    <field name="M_BIOMGM2" labelOnTop="0"/>
    <field name="M_BIOMM2" labelOnTop="0"/>
    <field name="M_DERIVE" labelOnTop="0"/>
    <field name="M_DIAM" labelOnTop="0"/>
    <field name="M_DIST" labelOnTop="0"/>
    <field name="M_LONG_S" labelOnTop="0"/>
    <field name="M_NBSARCEP" labelOnTop="0"/>
    <field name="M_NBSARM" labelOnTop="0"/>
    <field name="M_NBSARMM2" labelOnTop="0"/>
    <field name="M_ORIENT_A" labelOnTop="0"/>
    <field name="M_ORIENT_R" labelOnTop="0"/>
    <field name="M_PASS" labelOnTop="0"/>
    <field name="M_PDOP" labelOnTop="0"/>
    <field name="M_VITESSE" labelOnTop="0"/>
    <field name="NBSARCEP" labelOnTop="0"/>
    <field name="NBSARM" labelOnTop="0"/>
    <field name="NBSARMM2" labelOnTop="0"/>
    <field name="NBSARM_S" labelOnTop="0"/>
    <field name="NBSART" labelOnTop="0"/>
    <field name="NB_SEG" labelOnTop="0"/>
    <field name="NOMBRE" labelOnTop="0"/>
    <field name="NOM_PHY" labelOnTop="0"/>
    <field name="ORIENT_A" labelOnTop="0"/>
    <field name="ORIENT_LIB" labelOnTop="0"/>
    <field name="ORIENT_R" labelOnTop="0"/>
    <field name="PASSAGE" labelOnTop="0"/>
    <field name="PDOP" labelOnTop="0"/>
    <field name="SURF_HA" labelOnTop="0"/>
    <field name="T_LONG_SEG" labelOnTop="0"/>
    <field name="VITESSE" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>GID</previewExpression>
  <mapTip>Name</mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
