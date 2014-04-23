BibLatex-Check
==============
A python3 script for checking BibLatex .bib files

BibTeX Check is a small Python script that goes through a list of references and checks if certain required fields are available, for instance, if each publication is assigned a year or if a journal article has a volume and issue number.
Moreover, it allows for first consistency checks of names of conference proceedings and you can easily extend it to support further of such checks. The results are printed to an html file, which includes links to Google Scholar, DBLP, etc. for each flawed reference.
These links help retrieving missing information and correcting the entries efficiently.

Please note that it is not a BibLaTeX validator. And in the current version, it might not yet be able to parse every valid bib file. The software targets the specific needs of Computer Scientist, but may be applicable in other fields as well.

Getting Started
===
Just copy the file into a directory with write permission, then either:

 * Change properties in the file to point to the bib file you want to test, and run the script with Python 3
 * Or, Specify the input on the command line `python3 biblatex_check.py <input.bib> [input.aux] [output.html]`

If you provide the additional aux file (usually created when compiling a tex document), then the check of the bib file is restricted to only those entries that are really cited in the tex document.

The html output is tested with Firefox and Chrome, but the current version does not properly work with Internet Explorer.

Screenshot
===
![Screenshots of the BibLatex check screen](/../screenshots/screenshots/checkscreen.png?raw=true "BibLatex Check")
