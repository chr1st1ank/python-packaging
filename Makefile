# Makefile for compiling requirements
# pip-compile must be installed

SOURCE_FOLDER = poetry
PYTHON = python
PIP_COMPILE = $(PYTHON) -m piptools compile
PIP_COMPILE_ARGS = --quiet --upgrade --resolver backtracking --no-emit-index-url --annotation-style line

.PHONY: help requirements clean

help:
	@echo "See README.md"

clean: 
	rm -rf $(SOURCE_FOLDER)/dist
	rm -rf ./*/__pycache__
	rm -rf ./*/langc/__pycache__
	rm -rf ./*/langc/langc.egg-info
	rm -rf ./*/.ruff_cache

$(SOURCE_FOLDER)/requirements.lock: Makefile $(SOURCE_FOLDER)/pyproject.toml
	cd $(SOURCE_FOLDER) && \
	$(PIP_COMPILE) $(PIP_COMPILE_ARGS) --output-file requirements.lock pyproject.toml

requirements: $(SOURCE_FOLDER)/requirements.lock

# Build the Python package (source distribution and wheel)
$(SOURCE_FOLDER)/dist: $(SOURCE_FOLDER)/langc/*.py $(SOURCE_FOLDER)/pyproject.toml
	cd $(SOURCE_FOLDER) && \
	$(PYTHON) -m build

docker: $(SOURCE_FOLDER)/dist $(SOURCE_FOLDER)/requirements.lock
	DOCKER_BUILDKIT=1 docker build --progress plain \
	--build-arg="SRC_FOLDER=$(SOURCE_FOLDER)" -f docker/Dockerfile.classic -t langapi .

dockerrun: docker
	docker run -it --rm -p 8080:8080 langapi
