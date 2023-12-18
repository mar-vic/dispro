<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                      xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                      xmlns:tei="http://www.tei-c.org/ns/1.0"
                      xmlns:eltec="http://distantreading.net/eltec/ns">
  <xsl:template match="/">
    <TEI xmlns="http://www.tei-c.org/ns/1.0" xml:lang="slo">
      <xsl:copy-of select="//tei:teiHeader" />
      <text>
        <body>
          <xsl:for-each select="//tei:body/tei:p">
            <p>
              <xsl:value-of select="tei:hi" />
            </p>
          </xsl:for-each>
        </body>
      </text>
    </TEI>
  </xsl:template>
</xsl:stylesheet>
