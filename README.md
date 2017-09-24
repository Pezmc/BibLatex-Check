BibLatex-Check
==============

*A python2/3 script for checking BibLatex .bib files*

BibTeX Check is a small Python script that goes through a list of references and checks if certain required fields are available, for instance, if each publication is assigned a year or if a journal article has a volume and issue number.

Additionally, it allows for consistency checks of names of conference proceedings and could easily be extended to other needs.

The results of the check are printed to an html file, which includes links to Google Scholar, DBLP, etc. for each flawed reference. These links help retrieving missing information and correcting the entries efficiently.

Please note that it is **not a BibLaTeX validator**. And in the current version, it might not yet be able to parse every valid bib file. The software targets the specific needs of Computer Scientist, but may be applicable in other fields as well.

## Getting Started

Just copy the file into a directory with write permission, then run the script

	./biblatex_check.py <-b input.bib> [-a input.aux] [-o output.html]

If you provide the additional aux file (created when compiling a tex document), then the check of the bib file is restricted to only those entries that are really cited in the tex document.

The html output is tested with Firefox and Chrome, but the current version does not properly work with Internet Explorer.

## Options

Specify these when calling the script.

- -b (--bib) Set the input Bib File
- -a (--aux) Set the input Aux File
- -o (--output) Set the HTML Output File
- -c (--config=file.json5) Load config file
- -v (--view) Open in Browser")

## Help

See `./biblatex_check.py -h` for basic help.

If your getting an environment error, try using `python ./biblatex_check.py` or `python3 ./biblatex_check.py` depending on your OS.

##Alternatives

BibLatex check is adapted from [BibTex Check](https://code.google.com/p/bibtex-check/) by Fabian Beck, which can be used to validate BibTex files.

See [BibTex vs BibLaTex vs NatBib](http://tex.stackexchange.com/questions/25701/bibtex-vs-biber-and-biblatex-vs-natbib) for a comparison of different referencing packages.

## Screenshot

![Screenshots of the BibLatex check screen](/../screenshots/screenshots/checkscreen.png?raw=true "BibLatex Check")

## License

MIT license
