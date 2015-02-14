files := msc.tex introduction.tex appendices.tex implementation.tex architecture.tex theory.tex
all: $(files)
		#convert mendeley format to bibtex
		sed -i.bak -e 's/url = {\(.*\)}\(.*\)/howpublished = "\\url\{\1\}"\2/' bibliography.bib
		pdflatex --shell-escape msc.tex
		bibtex msc
		pdflatex --shell-escape msc.tex 
		pdflatex --shell-escape msc.tex
see:
	evince msc.pdf
final: $(files)
		pdflatex --shell-escape msc.tex && pdflatex --shell-escape msc.tex
draft: $(files)
		pdflatex -draftmode msc.tex 

.PHONY: clean
clean:
	rm *bbl *blg *out *aux *log *toc msc.pdf 2>/dev/null || true
