MASTERROOT = poroelasticity

TEXMASTER = $(MASTERROOT).tex

TEXSRCS = 

TEXFILES = $(TEXMASTER) $(TEXSRCS)

AUXFILES = $(TEXMASTER:.tex=.aux)

PDFFILE = $(TEXMASTER:.tex=.pdf)

default: pdf

pdf: $(PDFFILE)

again:
	TEXINPUTS=./:../../texmf//: pdflatex $(TEXMASTER)

$(PDFFILE): $(TEXMASTER)
	TEXINPUTS=./:../../texmf//: pdflatex $(TEXMASTER)

clean:
	rm -f $(AUXFILES) $(PDFFILE) \
		$(MASTERROOT).log $(MASTERROOT).out $(MASTERROOT).nav \
		$(MASTERROOT).snm $(MASTERROOT).toc $(MASTERROOT).vrb *~
	rm -fr auto

dist: $(PDFFILE)
	mv -f $(PDFFILE) 2021_PyLith_User_Forum_$(MASTERROOT).pdf
