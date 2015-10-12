files := pszostek_metadata_extraction.tex

pszostek_metadata_extraciton.pdf: $(files)
		xelatex $^

.PHONY: clean
clean:
	rm *bbl *blg *out *aux *log *nav *snm *toc pszostek_metadata_extraciton.pdf 2>/dev/null || true
