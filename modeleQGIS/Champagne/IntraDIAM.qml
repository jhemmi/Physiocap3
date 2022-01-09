<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.4.12-Madeira" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" minScale="1e+8" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property key="WMSBackgroundLayer" value="false"/>
    <property key="WMSPublishDataSourceUrl" value="false"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="identify/format" value="Value"/>
  </customproperties>
  <pipe>
    <rasterrenderer alphaBand="-1" type="singlebandpseudocolor" band="1" classificationMin="7.4" classificationMax="25" opacity="1">
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
            <prop v="217,217,217,255" k="preset_color_0"/>
            <prop v="255,0,0,255" k="preset_color_1"/>
            <prop v="255,255,0,255" k="preset_color_2"/>
            <prop v="0,255,255,255" k="preset_color_3"/>
            <prop v="106,168,79,255" k="preset_color_4"/>
            <prop v="14,0,0,255" k="preset_color_5"/>
            <prop v="#d9d9d9" k="preset_color_name_0"/>
            <prop v="#ff0000" k="preset_color_name_1"/>
            <prop v="#ffff00" k="preset_color_name_2"/>
            <prop v="#00ffff" k="preset_color_name_3"/>
            <prop v="#6aa84f" k="preset_color_name_4"/>
            <prop v="#0e0000" k="preset_color_name_5"/>
            <prop v="preset" k="rampType"/>
          </colorramp>
          <item color="#e9e9d8" label="DIAM &lt; 7.4" alpha="255" value="7.4"/>
          <item color="#eff797" label="7.4 &lt; DIAM &lt; 8.2" alpha="255" value="8.2"/>
          <item color="#9dd798" label="8.2 &lt; DIAM &lt; 8.4" alpha="255" value="8.4"/>
          <item color="#54b466" label="8.4 &lt; DIAM &lt; 8.6" alpha="255" value="8.6"/>
          <item color="#1d9340" label="8.6 &lt; DIAM &lt; 8.8" alpha="255" value="8.8"/>
          <item color="#00741f" label="8.8 &lt; DIAM &lt; 9" alpha="255" value="9"/>
          <item color="#244d7a" label="9 &lt; DIAM &lt; 9.5" alpha="255" value="9.5"/>
          <item color="#67387a" label="9.5 &lt; DIAM &lt; 10" alpha="255" value="10"/>
          <item color="#78205d" label="10 &lt; DIAM &lt; 10.5" alpha="255" value="10.5"/>
          <item color="#5e0440" label="10.5 &lt; DIAM " alpha="255" value="25"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation colorizeRed="255" saturation="0" colorizeStrength="100" colorizeBlue="128" colorizeGreen="128" grayscaleMode="0" colorizeOn="0"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
