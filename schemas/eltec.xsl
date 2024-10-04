<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0"
                xmlns:eltec="http://distantreading.net/eltec/ns">
  <xsl:param name="id" />
  <xsl:param name="title" />
  <xsl:param name="title_ref" />
  <xsl:param name="author" />
  <xsl:param name="author_ref" />
  <xsl:param name="words" />
  <xsl:param name="pages" />
  <xsl:param name="vols" />
  <xsl:param name="pub_place" />
  <xsl:param name="publisher" />
  <xsl:param name="pub_date" />
  <xsl:param name="gender" />
  <xsl:param name="size" />
  <xsl:param name="time_slot" />
  <xsl:param name="canonicity" />
  <xsl:param name="creation_date" />
  <xsl:template match="/">
    <TEI xmlns="http://www.tei-c.org/ns/1.0" xml:lang="slo">
      <teiHeader>
        <xsl:attribute name="xml:id">SLK<xsl:value-of select="$pub_date" /><xsl:value-of select="$id" /></xsl:attribute>
        <title>
          <xsl:if test="$title_ref!=''">
            <xsl:attribute name="ref"><xsl:value-of select="$title_ref" /></xsl:attribute>
          </xsl:if>
          <xsl:value-of select="$title" /> : ELTeC edícia
        </title>
        <author>
          <xsl:if test="$author_ref!=''">
            <xsl:attribute name="ref"><xsl:value-of select="$author_ref" /></xsl:attribute>
          </xsl:if>
          <xsl:value-of select="$author" />
        </author>
        <extent>
          <measure unit="words"><xsl:value-of select="$words" /></measure>
          <xsl:if test="$pages!=''">
            <measure unit="pages"><xsl:value-of select="$pages" /></measure>
          </xsl:if>
          <xsl:if test="$vols!=''">
            <measure unit="vols"><xsl:value-of select="$vols" /></measure>
          </xsl:if>
        </extent>
        <publicationStmt>
          <p/>
        </publicationStmt>
        <sourceDesc>
          <bibl type="printSource">
            <author><xsl:value-of select="$author" /></author>
            <title><xsl:value-of select="$title" /></title>
            <pubPlace><xsl:value-of select="$pub_place" /></pubPlace>
            <publisher><xsl:value-of select="$publisher" /></publisher>
            <date><xsl:value-of select="$pub_date" /></date>
          </bibl>
        </sourceDesc>
        <profileDesc>
          <langUsage>
            <language ident="sk"/>
          </langUsage>
          <textDesc>
            <eltec:authorGender key="F"/>
            <eltec:size key="long"/>
            <eltec:canonicity key="high"/>
            <eltec:timeSlot key="T1"/>
          </textDesc>
        </profileDesc>
        <revisionDesc>
          <change>
            <xsl:attribute name="when"><xsl:value-of select="$creation_date" /></xsl:attribute>
            Initially created as an ELTeC file
          </change>
        </revisionDesc>
      </teiHeader>
      <!-- <xsl:copy-of select="tei:TEI/tei:teiHeader" /> -->
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
