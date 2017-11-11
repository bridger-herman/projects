L=pdflatex

LATEX=$(wildcard *.tex)
PDF=$(LATEX:.tex=.pdf)

all: $(PDF)

%.pdf:  %.tex
	pdflatex $<
	- bibtex $*
	pdflatex $<
	pdflatex $<
	while ( grep -q '^LaTeX Warning: Label(s) may have changed' $*.log) \
	do pdflatex $<; done
