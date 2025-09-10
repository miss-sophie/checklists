# Set 
SOURCE_DIR := examples/tex
BUILD_DIR := build
PDF_DIR := examples/pdf

SOURCES := $(wildcard $(SOURCE_DIR)/*.tex)

all: prepare_directories compile publish cleanup

prepare_directories:
	mkdir -p $(BUILD_DIR)
	mkdir -p $(PDF_DIR)

compile: $(SOURCES)
	@for i in $(SOURCES); do \
        echo Building $$i from source && \
		xelatex -output-dir=$(BUILD_DIR) $$i; \
		xelatex -output-dir=$(BUILD_DIR) $$i; \
		xelatex -output-dir=$(BUILD_DIR) $$i; \
    done
	
publish:
	mv $(BUILD_DIR)/*.pdf $(PDF_DIR)

cleanup:
	@echo Removing $(BUILD_DIR)
	rm -rf $(BUILD_DIR)

list_sources:
	@for i in $(SOURCES); do \
        echo $$i; \
    done