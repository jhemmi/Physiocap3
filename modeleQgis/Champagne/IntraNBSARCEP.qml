<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis minScale="1e+8" maxScale="0" hasScaleBasedVisibilityFlag="0" version="3.4.12-Madeira" styleCategories="AllStyleCategories">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property value="false" key="WMSBackgroundLayer"/>
    <property value="false" key="WMSPublishDataSourceUrl"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property value="Value" key="identify/format"/>
  </customproperties>
  <pipe>
    <rasterrenderer type="singlebandpseudocolor" alphaBand="-1" band="1" classificationMin="7.4" classificationMax="25" opacity="1">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Exact</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader clip="0" classificationMode="1" colorRampType="DISCRETE">
          <colorramp type="preset" name="[source]">
            <prop k="preset_color_0" v="217,217,217,255"/>
            <prop k="preset_color_1" v="255,0,0,255"/>
            <prop k="preset_color_2" v="255,255,0,255"/>
            <prop k="preset_color_3" v="0,255,255,255"/>
            <prop k="preset_color_4" v="106,168,79,255"/>
            <prop k="preset_color_5" v="14,0,0,255"/>
            <prop k="preset_color_name_0" v="#d9d9d9"/>
            <prop k="preset_color_name_1" v="#ff0000"/>
            <prop k="preset_color_name_2" v="#ffff00"/>
            <prop k="preset_color_name_3" v="#00ffff"/>
            <prop k="preset_color_name_4" v="#6aa84f"/>
            <prop k="preset_color_name_5" v="#0e0000"/>
            <prop k="rampType" v="preset"/>
          </colorramp>
          <item value="3" color="#e9e9d8" label="NBSARCEP &lt; 3" alpha="255"/>
          <item value="5.8" color="#eff797" label="3 &lt; NBSARCEP &lt; 5.8" alpha="255"/>
          <item value="6.3" color="#9dd798" label="5.8 &lt; NBSARCEP &lt; 6.3" alpha="255"/>
          <item value="6.8" color="#54b466" label="6.3 &lt; NBSARCEP &lt; 6.8" alpha="255"/>
          <item value="7.4" color="#1d9340" label="6.8 &lt; NBSARCEP &lt; 7.4" alpha="255"/>
          <item value="8" color="#00741f" label="7.4 &lt; NBSARCEP &lt; 8" alpha="255"/>
          <item value="9" color="#244d7a" label="8 &lt; NBSARCEP &lt; 9" alpha="255"/>
          <item value="10" color="#67387a" label="9 &lt; NBSARCEP &lt; 10" alpha="255"/>
          <item value="11" color="#78205d" label="10 &lt; NBSARCEP &lt; 11" alpha="255"/>
          <item value="30" color="#5e0440" label="11 &lt; NBSARCEP " alpha="255"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation colorizeGreen="128" colorizeStrength="100" colorizeOn="0" colorizeRed="255" colorizeBlue="128" saturation="0" grayscaleMode="0"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
