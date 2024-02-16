# Makefile for compiling requirements
# pip-compile must be installed

PYTHON = python
PIP_COMPILE = $(PYTHON) -m piptools compile
PIP_COMPILE_ARGS = --quiet --upgrade --resolver backtracking --no-emit-index-url --annotation-style line

.PHONY: all help requirements

help:
	@echo "See README.md"

all: requirements dist

requirements: Makefile pyproject.toml
	$(PIP_COMPILE) $(PIP_COMPILE_ARGS) --output-file requirements.lock pyproject.toml

# Build the Python package (source distribution and wheel)
dist: langc/ pyproject.toml
	$(PYTHON) -m build

docker: dist
	DOCKER_BUILDKIT=1 docker build --progress plain -f Dockerfile -t langapi .

dockerrun: docker
	docker run -it --rm -p 8080:8080 langapi
