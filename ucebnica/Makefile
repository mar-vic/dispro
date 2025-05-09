.PHONY: help all docx epub pdf tex
.DEFAULT_GOAL := help

help:
	head -2 Makefile

all:
	make docx epub pdf tex

docx:
	(pandoc --defaults=defaults.yaml --defaults=docx.yaml)

epub:
	(pandoc --defaults=defaults.yaml --defaults=epub.yaml)

pdf:
	(pandoc --defaults=defaults.yaml --defaults=pdf.yaml)

tex:
	(pandoc --defaults=defaults.yaml --defaults=tex.yaml)
