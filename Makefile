files := msc.tex introduction.tex appendices.tex
all: $(files)
		pdflatex --shell-escape msc.tex
		bibtex msc
see:
	evince msc.pdf
final: $(files)
		pdflatex msc.tex && pdflatex msc.tex
draft: $(files)
		pdflatex -draftmode msc.tex 

.PHONY: clean
clean:
	rm *aux *log *toc msc.pdf 2>/dev/null || true
