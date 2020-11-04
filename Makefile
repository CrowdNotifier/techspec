# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = -W
SPHINXBUILD   = sphinx-build
SPHINXAUTOBUILD = sphinx-autobuild
SPHINXPROJ    = DP3TTechnicalSpecification
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

figures:
	plantuml source/figures -o ../pngs

.PHONY: help Makefile figures

venv:
	python3 -m venv venv
	. ./venv/bin/activate && \
	pip install -r requirements.txt

autobuild-html: venv Makefile
	@. ./venv/bin/activate && \
	$(SPHINXAUTOBUILD) "$(SOURCEDIR)" "$(BUILDDIR)/html" $(O)


# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: venv Makefile
	@. ./venv/bin/activate && \
	$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
