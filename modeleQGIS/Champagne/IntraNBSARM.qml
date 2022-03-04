<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" version="3.4.12-Madeira" minScale="1e+8" maxScale="0">
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
    <rasterrenderer type="singlebandpseudocolor" opacity="1" band="1" classificationMin="110" classificationMax="inf" alphaBand="-1">
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
        <colorrampshader colorRampType="DISCRETE" clip="0" classificationMode="2">
          <colorramp type="gradient" name="[source]">
            <prop v="253,231,37,255" k="color1"/>
            <prop v="68,1,84,255" k="color2"/>
            <prop v="0" k="discrete"/>
            <prop v="gradient" k="rampType"/>
            <prop v="0.019608;241,229,29,255:0.039216;229,228,25,255:0.058824;216,226,25,255:0.078431;202,225,31,255:0.098039;189,223,38,255:0.117647;176,221,47,255:0.137255;162,218,55,255:0.156863;149,216,64,255:0.176471;137,213,72,255:0.196078;124,210,80,255:0.215686;112,207,87,255:0.235294;101,203,94,255:0.254902;90,200,100,255:0.27451;80,196,106,255:0.294118;70,192,111,255:0.313725;61,188,116,255:0.333333;53,183,121,255:0.352941;46,179,124,255:0.372549;40,174,128,255:0.392157;36,170,131,255:0.411765;33,165,133,255:0.431373;31,161,136,255:0.45098;30,156,137,255:0.470588;31,151,139,255:0.490196;32,146,140,255:0.509804;33,142,141,255:0.529412;35,137,142,255:0.54902;37,132,142,255:0.568627;39,128,142,255:0.588235;41,123,142,255:0.607843;42,118,142,255:0.627451;44,113,142,255:0.647059;46,109,142,255:0.666667;49,104,142,255:0.686275;51,99,141,255:0.705882;53,94,141,255:0.72549;56,89,140,255:0.745098;58,83,139,255:0.764706;61,78,138,255:0.784314;63,72,137,255:0.803922;65,66,135,255:0.823529;67,61,132,255:0.843137;69,55,129,255:0.862745;70,48,126,255:0.882353;71,42,122,255:0.901961;72,36,117,255:0.921569;72,29,111,255:0.941176;72,23,105,255:0.960784;71,16,99,255:0.980392;70,8,92,255" k="stops"/>
          </colorramp>
          <item alpha="255" value="3.0" color="#eff797" label="Très faible : &lt;= 3.0"/>
          <item alpha="255" value="5.8" color="#ddf2d7" label="Faible : entre 3.0 et 5.8"/>
          <item alpha="255" value="6.8" color="#b2e0ab" label="Moyenne - : entre 5.8 et 6.8"/>
          <item alpha="255" value="7.9" color="#3da75a" label="Moyenne + : entre 6.8 et 7.9"/>
          <item alpha="255" value="11.1" color="#38578c" label="Elevée : entre 7.9 et 11.1"/>
          <item alpha="255" value="inf" color="#440154" label="Très élevée : > 11.1"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast contrast="0" brightness="0"/>
    <huesaturation colorizeOn="0" saturation="0" grayscaleMode="0" colorizeRed="255" colorizeStrength="100" colorizeGreen="128" colorizeBlue="128"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
