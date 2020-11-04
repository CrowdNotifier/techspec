DIAGRAMS_SRC := $(wildcard *.puml)
DIAGRAMS_PNG := $(addsuffix .png, $(basename $(DIAGRAMS_SRC)))
DIAGRAMS_SVG := $(addsuffix .svg, $(basename $(DIAGRAMS_SRC)))

PLANTUML = plantuml -config plantuml.config

all: png svg

png: $(DIAGRAMS_PNG)
svg: $(DIAGRAMS_SVG)

# clean up compiled files
clean:
	rm -f $(DIAGRAMS_PNG)

# compile individual png files
%.png: %.puml
	$(PLANTUML) -tpng $^

# compile individual svg files
%.svg: %.puml
	$(PLANTUML) -tsvg $^

# Quirk of GNU Make: https://www.gnu.org/software/make/manual/html_node/Phony-Targets.html
.PHONY: all clean
