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
          <item value="200" color="#e9e9d8" label="BIOMGCEP &lt; 200" alpha="255"/>
          <item value="300" color="#eff797" label="200 &lt; BIOMGCEP &lt; 300" alpha="255"/>
          <item value="350" color="#9dd798" label="300 &lt; BIOMGCEP &lt; 350" alpha="255"/>
          <item value="400" color="#54b466" label="350 &lt; BIOMGCEP &lt; 400" alpha="255"/>
          <item value="450" color="#1d9340" label="400 &lt; BIOMGCEP &lt; 450" alpha="255"/>
          <item value="500" color="#00741f" label="450 &lt; BIOMGCEP &lt; 500" alpha="255"/>
          <item value="600" color="#244d7a" label="500 &lt; BIOMGCEP &lt; 600" alpha="255"/>
          <item value="700" color="#67387a" label="600 &lt; BIOMGCEP &lt; 700" alpha="255"/>
          <item value="800" color="#78205d" label="700 &lt; BIOMGCEP &lt; 800" alpha="255"/>
          <item value="9999" color="#5e0440" label="800 &lt; BIOMGCEP " alpha="255"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation colorizeGreen="128" colorizeStrength="100" colorizeOn="0" colorizeRed="255" colorizeBlue="128" saturation="0" grayscaleMode="0"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
