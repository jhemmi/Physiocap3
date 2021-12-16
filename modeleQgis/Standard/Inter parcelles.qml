<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.0.3-Girona" hasScaleBasedVisibilityFlag="0" simplifyAlgorithm="0" labelsEnabled="1" simplifyMaxScale="1" minScale="0" maxScale="0" simplifyDrawingTol="1" readOnly="0" simplifyDrawingHints="1" simplifyLocal="1">
  <renderer-v2 enableorderby="0" type="singleSymbol" symbollevels="0" forceraster="0">
    <symbols>
      <symbol alpha="1" type="fill" name="0" clip_to_extent="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleFill">
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
      <text-style textColor="0,0,0,255" fontWeight="50" fontSize="10" fontLetterSpacing="0" blendMode="0" fontSizeUnit="Point" fontCapitals="0" textOpacity="1" previewBkgrdColor="#ffffff" fontSizeMapUnitScale="3x:0,0,0,0,0,0" isExpression="1" fontWordSpacing="0" fieldName="  concat(   &#xa;  ' Ilot : ', &quot;NOM_PHY&quot; , &#xa;  '~ Densité de points/ha : ', format_number(&quot;MESURE_HA&quot;, 0) , &#xa;  '~ ', format_number(&quot;0_MESURE&quot;, 0),'% sans mesure', &#xa;  '~ Biomasse == ',&#xa;   ' Médiane : ' , format_number( &quot;BIOM&quot;,0),&#xa; ' Ecartype : ' , format_number(&quot;E_BIOM&quot;,0)&#xa;  )" useSubstitutions="0" fontItalic="0" namedStyle="Regular" fontUnderline="0" fontFamily="Ubuntu" fontStrikeout="0" multilineHeight="1">
        <text-buffer bufferSize="1" bufferDraw="1" bufferBlendMode="0" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferNoFill="0" bufferSizeUnits="MM" bufferOpacity="1" bufferJoinStyle="64" bufferColor="253,191,111,255"/>
        <background shapeRotation="0" shapeRadiiX="0" shapeSVGFile="" shapeRadiiY="0" shapeRotationType="0" shapeBorderColor="128,128,128,255" shapeRadiiUnit="MM" shapeType="0" shapeOffsetX="0" shapeBorderWidthUnit="MM" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetY="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeBlendMode="0" shapeFillColor="255,255,255,255" shapeSizeUnit="MM" shapeSizeType="0" shapeOffsetUnit="MM" shapeDraw="0" shapeSizeX="0" shapeSizeY="0" shapeBorderWidth="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64"/>
        <shadow shadowDraw="0" shadowRadiusUnit="MM" shadowOpacity="0.7" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowUnder="0" shadowOffsetGlobal="1" shadowRadius="1.5" shadowRadiusAlphaOnly="0" shadowColor="0,0,0,255" shadowOffsetUnit="MM" shadowBlendMode="6" shadowScale="100" shadowOffsetAngle="135" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetDist="1"/>
        <substitutions/>
      </text-style>
      <text-format plussign="0" multilineAlign="0" reverseDirectionSymbol="0" placeDirectionSymbol="0" rightDirectionSymbol=">" decimals="3" wrapChar="~" leftDirectionSymbol="&lt;" formatNumbers="0" addDirectionSymbol="0"/>
      <placement offsetUnits="MapUnit" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" placement="0" centroidInside="1" repeatDistance="0" yOffset="0" xOffset="0" dist="5" preserveRotation="1" distUnits="MM" distMapUnitScale="3x:0,0,0,0,0,0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" placementFlags="0" centroidWhole="0" fitInPolygonOnly="0" offsetType="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" rotationAngle="0" quadOffset="4" maxCurvedCharAngleIn="20" maxCurvedCharAngleOut="-20" priority="5" repeatDistanceUnits="MM"/>
      <rendering scaleVisibility="0" scaleMin="1" maxNumLabels="2000" displayAll="0" zIndex="0" fontMaxPixelSize="10000" obstacleFactor="1" drawLabels="1" labelPerPart="0" fontMinPixelSize="3" obstacle="1" scaleMax="10000000" upsidedownLabels="0" minFeatureSize="0" limitNumLabels="0" obstacleType="0" mergeLines="0" fontLimitPixelSize="0"/>
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
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory diagramOrientation="Up" penWidth="0" scaleBasedVisibility="0" minScaleDenominator="0" lineSizeType="MM" lineSizeScale="3x:0,0,0,0,0,0" sizeScale="3x:0,0,0,0,0,0" height="15" maxScaleDenominator="1e+8" enabled="0" scaleDependency="Area" width="15" penColor="#000000" penAlpha="255" barWidth="5" minimumSize="0" backgroundColor="#ffffff" backgroundAlpha="255" rotationOffset="270" opacity="1" labelPlacementMethod="XHeight" sizeType="MM">
      <fontProperties style="" description="Ubuntu,11,-1,5,50,0,0,0,0,0"/>
      <attribute field="" color="#000000" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings linePlacementFlags="18" zIndex="0" showAll="1" dist="0" placement="0" priority="0" obstacle="0">
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
    <field name="0_MESURE">
      <editWidget type="Range">
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
    <field name="T_LONG_SEG">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="NBSARM_S">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="NB_SEG">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="LONG_S">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="M_LONG_S">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="E_LONG_S">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="PASSAGE">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="M_PASS">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="E_PASS">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ORIENT_A">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="M_ORIENT_A">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="E_ORIENT_A">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ORIENT_R">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="M_ORIENT_R">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="E_ORIENT_R">
      <editWidget type="TextEdit">
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
    <field name="PDOP">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="M_PDOP">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="E_PDOP">
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
    <alias field="0_MESURE" index="13" name=""/>
    <alias field="NBSART" index="14" name=""/>
    <alias field="T_LONG_SEG" index="15" name=""/>
    <alias field="NBSARM_S" index="16" name=""/>
    <alias field="NB_SEG" index="17" name=""/>
    <alias field="LONG_S" index="18" name=""/>
    <alias field="M_LONG_S" index="19" name=""/>
    <alias field="E_LONG_S" index="20" name=""/>
    <alias field="PASSAGE" index="21" name=""/>
    <alias field="M_PASS" index="22" name=""/>
    <alias field="E_PASS" index="23" name=""/>
    <alias field="ORIENT_A" index="24" name=""/>
    <alias field="M_ORIENT_A" index="25" name=""/>
    <alias field="E_ORIENT_A" index="26" name=""/>
    <alias field="ORIENT_R" index="27" name=""/>
    <alias field="M_ORIENT_R" index="28" name=""/>
    <alias field="E_ORIENT_R" index="29" name=""/>
    <alias field="ALTITUDE" index="30" name=""/>
    <alias field="M_ALTI" index="31" name=""/>
    <alias field="E_ALTI" index="32" name=""/>
    <alias field="PDOP" index="33" name=""/>
    <alias field="M_PDOP" index="34" name=""/>
    <alias field="E_PDOP" index="35" name=""/>
    <alias field="DISTANCE" index="36" name=""/>
    <alias field="M_DIST" index="37" name=""/>
    <alias field="E_DIST" index="38" name=""/>
    <alias field="DERIVE" index="39" name=""/>
    <alias field="M_DERIVE" index="40" name=""/>
    <alias field="E_DERIVE" index="41" name=""/>
    <alias field="VITESSE" index="42" name=""/>
    <alias field="M_VITESSE" index="43" name=""/>
    <alias field="E_VITESSE" index="44" name=""/>
    <alias field="DEBUT" index="45" name=""/>
    <alias field="FIN" index="46" name=""/>
    <alias field="SURF_HA" index="47" name=""/>
    <alias field="NOMBRE" index="48" name=""/>
    <alias field="ORIENT_LIB" index="49" name=""/>
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
    <default field="0_MESURE" applyOnUpdate="0" expression=""/>
    <default field="NBSART" applyOnUpdate="0" expression=""/>
    <default field="T_LONG_SEG" applyOnUpdate="0" expression=""/>
    <default field="NBSARM_S" applyOnUpdate="0" expression=""/>
    <default field="NB_SEG" applyOnUpdate="0" expression=""/>
    <default field="LONG_S" applyOnUpdate="0" expression=""/>
    <default field="M_LONG_S" applyOnUpdate="0" expression=""/>
    <default field="E_LONG_S" applyOnUpdate="0" expression=""/>
    <default field="PASSAGE" applyOnUpdate="0" expression=""/>
    <default field="M_PASS" applyOnUpdate="0" expression=""/>
    <default field="E_PASS" applyOnUpdate="0" expression=""/>
    <default field="ORIENT_A" applyOnUpdate="0" expression=""/>
    <default field="M_ORIENT_A" applyOnUpdate="0" expression=""/>
    <default field="E_ORIENT_A" applyOnUpdate="0" expression=""/>
    <default field="ORIENT_R" applyOnUpdate="0" expression=""/>
    <default field="M_ORIENT_R" applyOnUpdate="0" expression=""/>
    <default field="E_ORIENT_R" applyOnUpdate="0" expression=""/>
    <default field="ALTITUDE" applyOnUpdate="0" expression=""/>
    <default field="M_ALTI" applyOnUpdate="0" expression=""/>
    <default field="E_ALTI" applyOnUpdate="0" expression=""/>
    <default field="PDOP" applyOnUpdate="0" expression=""/>
    <default field="M_PDOP" applyOnUpdate="0" expression=""/>
    <default field="E_PDOP" applyOnUpdate="0" expression=""/>
    <default field="DISTANCE" applyOnUpdate="0" expression=""/>
    <default field="M_DIST" applyOnUpdate="0" expression=""/>
    <default field="E_DIST" applyOnUpdate="0" expression=""/>
    <default field="DERIVE" applyOnUpdate="0" expression=""/>
    <default field="M_DERIVE" applyOnUpdate="0" expression=""/>
    <default field="E_DERIVE" applyOnUpdate="0" expression=""/>
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
    <constraint unique_strength="0" exp_strength="0" field="GID" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="NOM_PHY" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="ID_PHY" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="MESURE_HA" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="NBSARM" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="M_NBSARM" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="E_NBSARM" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="DIAM" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="M_DIAM" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="E_DIAM" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="BIOM" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="M_BIOM" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="E_BIOM" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="0_MESURE" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="NBSART" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="T_LONG_SEG" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="NBSARM_S" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="NB_SEG" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="LONG_S" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="M_LONG_S" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="E_LONG_S" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="PASSAGE" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="M_PASS" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="E_PASS" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="ORIENT_A" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="M_ORIENT_A" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="E_ORIENT_A" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="ORIENT_R" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="M_ORIENT_R" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="E_ORIENT_R" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="ALTITUDE" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="M_ALTI" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="E_ALTI" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="PDOP" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="M_PDOP" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="E_PDOP" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="DISTANCE" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="M_DIST" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="E_DIST" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="DERIVE" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="M_DERIVE" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="E_DERIVE" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="VITESSE" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="M_VITESSE" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="E_VITESSE" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="DEBUT" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="FIN" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="SURF_HA" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="NOMBRE" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="ORIENT_LIB" constraints="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="GID" desc=""/>
    <constraint exp="" field="NOM_PHY" desc=""/>
    <constraint exp="" field="ID_PHY" desc=""/>
    <constraint exp="" field="MESURE_HA" desc=""/>
    <constraint exp="" field="NBSARM" desc=""/>
    <constraint exp="" field="M_NBSARM" desc=""/>
    <constraint exp="" field="E_NBSARM" desc=""/>
    <constraint exp="" field="DIAM" desc=""/>
    <constraint exp="" field="M_DIAM" desc=""/>
    <constraint exp="" field="E_DIAM" desc=""/>
    <constraint exp="" field="BIOM" desc=""/>
    <constraint exp="" field="M_BIOM" desc=""/>
    <constraint exp="" field="E_BIOM" desc=""/>
    <constraint exp="" field="0_MESURE" desc=""/>
    <constraint exp="" field="NBSART" desc=""/>
    <constraint exp="" field="T_LONG_SEG" desc=""/>
    <constraint exp="" field="NBSARM_S" desc=""/>
    <constraint exp="" field="NB_SEG" desc=""/>
    <constraint exp="" field="LONG_S" desc=""/>
    <constraint exp="" field="M_LONG_S" desc=""/>
    <constraint exp="" field="E_LONG_S" desc=""/>
    <constraint exp="" field="PASSAGE" desc=""/>
    <constraint exp="" field="M_PASS" desc=""/>
    <constraint exp="" field="E_PASS" desc=""/>
    <constraint exp="" field="ORIENT_A" desc=""/>
    <constraint exp="" field="M_ORIENT_A" desc=""/>
    <constraint exp="" field="E_ORIENT_A" desc=""/>
    <constraint exp="" field="ORIENT_R" desc=""/>
    <constraint exp="" field="M_ORIENT_R" desc=""/>
    <constraint exp="" field="E_ORIENT_R" desc=""/>
    <constraint exp="" field="ALTITUDE" desc=""/>
    <constraint exp="" field="M_ALTI" desc=""/>
    <constraint exp="" field="E_ALTI" desc=""/>
    <constraint exp="" field="PDOP" desc=""/>
    <constraint exp="" field="M_PDOP" desc=""/>
    <constraint exp="" field="E_PDOP" desc=""/>
    <constraint exp="" field="DISTANCE" desc=""/>
    <constraint exp="" field="M_DIST" desc=""/>
    <constraint exp="" field="E_DIST" desc=""/>
    <constraint exp="" field="DERIVE" desc=""/>
    <constraint exp="" field="M_DERIVE" desc=""/>
    <constraint exp="" field="E_DERIVE" desc=""/>
    <constraint exp="" field="VITESSE" desc=""/>
    <constraint exp="" field="M_VITESSE" desc=""/>
    <constraint exp="" field="E_VITESSE" desc=""/>
    <constraint exp="" field="DEBUT" desc=""/>
    <constraint exp="" field="FIN" desc=""/>
    <constraint exp="" field="SURF_HA" desc=""/>
    <constraint exp="" field="NOMBRE" desc=""/>
    <constraint exp="" field="ORIENT_LIB" desc=""/>
  </constraintExpressions>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column hidden="0" type="field" width="-1" name="GID"/>
      <column hidden="0" type="field" width="-1" name="NOM_PHY"/>
      <column hidden="0" type="field" width="-1" name="ID_PHY"/>
      <column hidden="0" type="field" width="-1" name="MESURE_HA"/>
      <column hidden="0" type="field" width="-1" name="0_MESURE"/>
      <column hidden="0" type="field" width="-1" name="NBSARM"/>
      <column hidden="0" type="field" width="-1" name="M_NBSARM"/>
      <column hidden="0" type="field" width="-1" name="E_NBSARM"/>
      <column hidden="0" type="field" width="-1" name="DIAM"/>
      <column hidden="0" type="field" width="-1" name="M_DIAM"/>
      <column hidden="0" type="field" width="-1" name="E_DIAM"/>
      <column hidden="0" type="field" width="-1" name="BIOM"/>
      <column hidden="0" type="field" width="-1" name="M_BIOM"/>
      <column hidden="0" type="field" width="-1" name="E_BIOM"/>
      <column hidden="0" type="field" width="-1" name="ALTITUDE"/>
      <column hidden="0" type="field" width="-1" name="M_ALTI"/>
      <column hidden="0" type="field" width="-1" name="E_ALTI"/>
      <column hidden="0" type="field" width="-1" name="DISTANCE"/>
      <column hidden="0" type="field" width="-1" name="M_DIST"/>
      <column hidden="0" type="field" width="-1" name="E_DIST"/>
      <column hidden="0" type="field" width="-1" name="DERIVE"/>
      <column hidden="0" type="field" width="-1" name="M_DERIVE"/>
      <column hidden="0" type="field" width="-1" name="E_DERIVE"/>
      <column hidden="0" type="field" width="-1" name="VITESSE"/>
      <column hidden="0" type="field" width="-1" name="M_VITESSE"/>
      <column hidden="0" type="field" width="-1" name="E_VITESSE"/>
      <column hidden="0" type="field" width="-1" name="DEBUT"/>
      <column hidden="0" type="field" width="-1" name="FIN"/>
      <column hidden="0" type="field" width="-1" name="SURF_HA"/>
      <column hidden="0" type="field" width="-1" name="NOMBRE"/>
      <column hidden="1" type="actions" width="-1"/>
      <column hidden="0" type="field" width="-1" name="NBSART"/>
      <column hidden="0" type="field" width="-1" name="T_LONG_SEG"/>
      <column hidden="0" type="field" width="-1" name="NBSARM_S"/>
      <column hidden="0" type="field" width="-1" name="NB_SEG"/>
      <column hidden="0" type="field" width="-1" name="LONG_S"/>
      <column hidden="0" type="field" width="-1" name="M_LONG_S"/>
      <column hidden="0" type="field" width="-1" name="E_LONG_S"/>
      <column hidden="0" type="field" width="-1" name="PASSAGE"/>
      <column hidden="0" type="field" width="-1" name="M_PASS"/>
      <column hidden="0" type="field" width="-1" name="E_PASS"/>
      <column hidden="0" type="field" width="-1" name="ORIENT_A"/>
      <column hidden="0" type="field" width="-1" name="M_ORIENT_A"/>
      <column hidden="0" type="field" width="-1" name="E_ORIENT_A"/>
      <column hidden="0" type="field" width="-1" name="ORIENT_R"/>
      <column hidden="0" type="field" width="-1" name="M_ORIENT_R"/>
      <column hidden="0" type="field" width="-1" name="E_ORIENT_R"/>
      <column hidden="0" type="field" width="-1" name="PDOP"/>
      <column hidden="0" type="field" width="-1" name="M_PDOP"/>
      <column hidden="0" type="field" width="-1" name="E_PDOP"/>
      <column hidden="0" type="field" width="-1" name="ORIENT_LIB"/>
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
  <editable>
    <field editable="1" name="0_MESURE"/>
    <field editable="1" name="ALTITUDE"/>
    <field editable="1" name="BIOM"/>
    <field editable="1" name="DEBUT"/>
    <field editable="1" name="DERIVE"/>
    <field editable="1" name="DIAM"/>
    <field editable="1" name="DISTANCE"/>
    <field editable="1" name="E_ALTI"/>
    <field editable="1" name="E_BIOM"/>
    <field editable="1" name="E_DERIVE"/>
    <field editable="1" name="E_DIAM"/>
    <field editable="1" name="E_DIST"/>
    <field editable="1" name="E_LONG_S"/>
    <field editable="1" name="E_NBSARM"/>
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
    <field editable="1" name="M_DERIVE"/>
    <field editable="1" name="M_DIAM"/>
    <field editable="1" name="M_DIST"/>
    <field editable="1" name="M_LONG_S"/>
    <field editable="1" name="M_NBSARM"/>
    <field editable="1" name="M_ORIENT_A"/>
    <field editable="1" name="M_ORIENT_R"/>
    <field editable="1" name="M_PASS"/>
    <field editable="1" name="M_PDOP"/>
    <field editable="1" name="M_VITESSE"/>
    <field editable="1" name="NBSARM"/>
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
    <field labelOnTop="0" name="DEBUT"/>
    <field labelOnTop="0" name="DERIVE"/>
    <field labelOnTop="0" name="DIAM"/>
    <field labelOnTop="0" name="DISTANCE"/>
    <field labelOnTop="0" name="E_ALTI"/>
    <field labelOnTop="0" name="E_BIOM"/>
    <field labelOnTop="0" name="E_DERIVE"/>
    <field labelOnTop="0" name="E_DIAM"/>
    <field labelOnTop="0" name="E_DIST"/>
    <field labelOnTop="0" name="E_LONG_S"/>
    <field labelOnTop="0" name="E_NBSARM"/>
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
    <field labelOnTop="0" name="M_DERIVE"/>
    <field labelOnTop="0" name="M_DIAM"/>
    <field labelOnTop="0" name="M_DIST"/>
    <field labelOnTop="0" name="M_LONG_S"/>
    <field labelOnTop="0" name="M_NBSARM"/>
    <field labelOnTop="0" name="M_ORIENT_A"/>
    <field labelOnTop="0" name="M_ORIENT_R"/>
    <field labelOnTop="0" name="M_PASS"/>
    <field labelOnTop="0" name="M_PDOP"/>
    <field labelOnTop="0" name="M_VITESSE"/>
    <field labelOnTop="0" name="NBSARM"/>
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
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <expressionfields>
    <field precision="2" type="6" expression=" &quot;ORIENT_A&quot; -90&#xa; " length="10" subType="0" name="ORIENT_LIB" comment="" typeName="double"/>
  </expressionfields>
  <previewExpression>GID</previewExpression>
  <mapTip>Name</mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
