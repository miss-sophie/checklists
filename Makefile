# Set 
SOURCE_DIR := source
BUILD_DIR := build
OUTPUT_DIR := pdf

SOURCES := $(wildcard $(SOURCE_DIR)/*.tex)

all: prepare_directories compile publish cleanup

prepare_directories:
	mkdir -p $(BUILD_DIR)
	mkdir -p $(OUTPUT_DIR)

compile: $(SOURCES)
	@set -ex; \
	for i in $(SOURCES); do \
		echo "Building $$i from source"; \
		xelatex -output-dir=$(BUILD_DIR) "$$i"; \
		xelatex -output-dir=$(BUILD_DIR) "$$i"; \
		xelatex -output-dir=$(BUILD_DIR) "$$i"; \
	done

publish:
	mv $(BUILD_DIR)/*.pdf $(OUTPUT_DIR)

cleanup:
	@echo Removing $(BUILD_DIR)
	rm -rf $(BUILD_DIR)

list_sources:
	@set -ex; \
	for i in $(SOURCES); do \
		echo "$$i"; \
	done
