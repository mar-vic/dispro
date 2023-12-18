<xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
 <xsl:output method="text"/>

 <xsl:template match="/*">
  <xsl:value-of select=
   " string-length(normalize-space(.))
    -
     string-length(translate(normalize-space(.),' ','')) +1"/>
 </xsl:template>
</xsl:stylesheet>
