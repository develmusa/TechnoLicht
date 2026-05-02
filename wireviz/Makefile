WIREVIZ_FILES := $(wildcard *.yml)
SVG_OUTPUTS := $(patsubst %.yml,output/%.svg,$(WIREVIZ_FILES))
PDF_OUTPUTS := $(patsubst %.yml,output/%.pdf,$(WIREVIZ_FILES))

.PHONY: all diagrams svg pdf clean

all: diagrams

diagrams: svg pdf

svg: output $(SVG_OUTPUTS)

pdf: output $(PDF_OUTPUTS)

output:
	mkdir -p output

output/%.svg: %.yml
	wireviz $< -o output/$*

output/%.pdf: %.yml
	wireviz $< -o output/$* --format pdf

clean:
	rm -rf output/

install:
	pip install wireviz
