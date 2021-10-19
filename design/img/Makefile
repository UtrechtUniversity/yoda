UML := $(shell find . -name '*.uml')
PNG := $(UML:%.uml=%.png)
SVG := $(UML:%.uml=%.svg)

PLANTUML     := plantuml

.PHONY: all

all: $(PNG) $(SVG)

%.png: %.uml
	$(PLANTUML) -tpng $<

%.svg: %.uml
	$(PLANTUML) -tsvg $<
