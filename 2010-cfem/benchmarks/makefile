MASTERROOT = benchmarks

TEXMASTER = $(MASTERROOT).tex

TEXSRCS = 

TEXFILES = $(TEXMASTER) $(TEXSRCS)

AUXFILES = $(TEXMASTER:.tex=.aux)

PDFFILE = $(TEXMASTER:.tex=.pdf)

DVIFILE = $(TEXMASTER:.tex=.dvi)

PSFILE = $(TEXMASTER:.tex=.ps)

PDFTMPFILE = tmp.pdf

default: pdf

pdf: $(PDFFILE)
ps: $(PSFILE)
dvi: $(DVIFILE)

again:
	pdflatex $(TEXMASTER) && mv $(PDFFILE) $(PDFTMPFILE)
	ppower4 $(PDFTMPFILE) $(PDFFILE)

$(PDFTMPFILE): $(TEXFILES) $(AUXFILES)
	pdflatex $(TEXMASTER) && mv $(PDFFILE) $(PDFTMPFILE)

$(PDFFILE): $(PDFTMPFILE)
	ppower4 $(PDFTMPFILE) $(PDFFILE)

$(PSFILE): $(DVIFILE)
	dvips -o $(PSFILE) $(DVIFILE)

$(DVIFILE): $(TEXFILES) $(AUXFILES)
	latex $(TEXMASTER)

$(AUXFILES):
	touch $(AUXFILES)

clean:
	rm -f $(AUXFILES) $(DVIFILE) $(PSFILE) $(PDFFILE) $(PDFTMPFILE)\
		$(MASTERROOT).log $(MASTERROOT).out *~
	rm -fr auto

