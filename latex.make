L=pdflatex

LATEX=$(wildcard *.tex)
PDF=$(LATEX:.tex=.pdf)
BIBTEX=$(wildcard *.bib)

all: $(PDF)

%.pdf: %.tex $(BIBTEX)
	$(L) $<
	- bibtex $*
	$(L) $<
	$(L) $<
	while ( grep -q '^LaTeX Warning: Label(s) may have changed' $*.log) \
	do $(L) $<; done

clean:
	$(RM) *.aux *.bbl *.blg *.log *.out

superclean: clean
	$(RM) *.pdf
