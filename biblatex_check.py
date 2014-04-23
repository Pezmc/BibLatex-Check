#!/usr/bin/env python

"""
BibTeX check on missing fields and consistent name conventions (no BibTeX validator),
especially developed for requirements in Computer Science. 
"""

__author__ = "Fabian Beck"
__version__ = "0.2.0"
__license__ = "MIT"

####################################################################
# Properties (please change according to your needs)
####################################################################

# files
bibFile = "test.bib"
auxFile = "test.aux"                # use "" to deactivate restricting the check to the entries listed in the aux file
htmlOutput = "bibtex_check.html"

# links
citeulikeUsername = ""              # if no username is profided, no CiteULike links appear
citeulikeHref = "http://www.citeulike.org/user/"+citeulikeUsername+"/article/"
scholarHref = "http://scholar.google.de/scholar?hl=en&q="
googleHref = "https://www.google.de/search?q="
dblpHref = "http://dblp.org/search/index.php#query="

# fields that are required for a specific type of entry 
requiredFields = (("inproceedings",("author","booktitle","pages","publisher","title","year")),
                ("article",("author","journal","number","pages","title","volume","year")),
                ("techreport",("author","institution","title","year")),
                ("incollection",("author","booktitle","pages","publisher","title","year")),
                ("book",("author","publisher","title","year")),
                ("inbook",("author","booktitle","pages","publisher","title","year")),
                ("proceedings",("editor","publisher","title","year")),
                ("phdthesis",("author","school","title","year")),
                ("mastersthesis",("author","school","title","year")),
                ("electronic",("author","title","url","year")),
                ("misc",("author","howpublished","title","year")),
                )
				
####################################################################

import string
import re

usedIds = set()

try: 
    fInAux = open(auxFile, 'r', encoding="utf8")
    for line in fInAux:
        if line.startswith("\\citation"):
            ids = line.split("{")[1].rstrip("} \n").split(",")
            for id in ids:
                if (id != ""):
                    usedIds.add(id)
    fInAux.close()
except IOError as e:
    print("no aux file '"+auxFile+"' exists -> do not restrict entities")

fIn = open(bibFile, 'r', encoding="utf8")
completeEntry = ""
currentId = ""
ids = []
currentType = ""
currentArticleId = ""
currentTitle = ""
fields = []
problems = []
subproblems = []

counterMissingFields = 0
counterFlawedNames = 0
counterWrongTypes = 0
counterNonUniqueId = 0

removePunctuationMap = dict((ord(char), None) for char in string.punctuation)

for line in fIn:
    line = line.strip("\n")
    if line.startswith("@"):
        if currentId in usedIds or not usedIds:
            for requiredFieldsType in requiredFields:
                if requiredFieldsType[0] == currentType:
                    for field in requiredFieldsType[1]:
                        if field not in fields:
                            subproblems.append("missing field '"+field+"'")
                            counterMissingFields += 1
        else:
            subproblems = []
        if currentId in usedIds or (currentId and not usedIds):
            cleanedTitle = currentTitle.translate(removePunctuationMap)
            problem = "<div id='"+currentId+"' class='problem severe"+str(len(subproblems))+"'>"
            problem += "<h2>"+currentId+" ("+currentType+")</h2> "
            problem += "<div class='links'>"
            if citeulikeUsername:
                problem += "<a href='"+citeulikeHref+currentArticleId+"'>CiteULike</a>"
            problem += " | <a href='"+scholarHref+cleanedTitle+"'>Scholar</a>"
            problem += " | <a href='"+googleHref+cleanedTitle+"'>Google</a>"
            problem += " | <a href='"+dblpHref+cleanedTitle+"'>DBLP</a>"
            problem += "</div>"
            problem += "<div class='reference'>"+currentTitle
            problem += "</div>"
            problem += "<ul>"
            for subproblem in subproblems:
                problem += "<li>"+subproblem+"</li>"
            problem += "</ul>"
            problem += "<form class='problem_control'><label>checked</label><input type='checkbox' class='checked'/></form>"
            problem += "<div class='bibtex_toggle'>Current BibTeX Entry</div>"
            problem += "<div class='bibtex'>"+completeEntry +"</div>"
            problem += "</div>"
            problems.append(problem)
        fields = []
        subproblems = []
        currentId = line.split("{")[1].rstrip(",\n")
        if currentId in ids:
            subproblems.append("non-unique id: '"+currentId+"'")
            counterNonUniqueId += 1
        else:
            ids.append(currentId)
        currentType = line.split("{")[0].strip("@ ")
        completeEntry = line + "<br />"
    else:
        if line != "":
            completeEntry += line + "<br />"
        if currentId in usedIds or not usedIds:
            if "=" in line:
                field = line.split("=")[0].strip()
                fields.append(field)
                value = line.split("=")[1].strip("{} ,\n")
                if field == "author":
                    currentAuthor = filter(lambda x: not (x in "\\\"{}"), value.split(" and ")[0])
                if field == "citeulike-article-id":
                    currentArticleId = value
                if field == "title":
                    currentTitle = re.sub(r'\}|\{',r'',value)

                ####################################################################
                # Checks (please (de)activate/extend to your needs)
                ####################################################################

                    
                # check if type 'proceedings' might be 'inproceedings'
                if currentType == "proceedings" and field == "pages":
                    subproblems.append("wrong type: maybe should be 'inproceedings' because entry has page numbers")
                    counterWrongTypes += 1

                # check if abbreviations are used in journal titles
                if currentType == "article" and field == "journal":
                    if "." in line:
                        subproblems.append("flawed name: abbreviated journal title '"+value+"'")
                        counterFlawedNames += 1

                # check booktitle format; expected format "ICBAB '13: Proceeding of the 13th International Conference on Bla and Blubb"
                #if currentType == "inproceedings" and field == "booktitle":
                    #if ":" not in line or ("Proceedings" not in line and "Companion" not in line) or "." in line or " '" not in line or "workshop" in line or "conference" in line or "symposium" in line:
                        #subproblems.append("flawed name: inconsistent formatting of booktitle '"+value+"'")
                        #counterFlawedNames += 1   

                 # check if title is capitalized (heuristic)
                 #if field == "title":
                    #for word in currentTitle.split(" "):
                        #word = word.strip(":")
                        #if len(word) > 7 and word[0].islower() and not  "-" in word and not "_"  in word and not "[" in word:
                            #subproblems.append("flawed name: non-capitalized title '"+currentTitle+"'")
                            #counterFlawedNames += 1
                            #break
                 
                ####################################################################
                 
fIn.close()

html = open(htmlOutput, 'w')
html.write("""<html>
<head>
<title>BibTeX Check</title>
<style>
body {
    font-family: Calibri, Arial, Sans;
    padding: 10px;
    width: 1030px;
    margin: 10 auto;
    border-top: 1px solid black;
}

#title {
    width: 720px;
    
    border-bottom: 1px solid black;
}

#title h1 {
    margin: 10px 0px;
}

#title h1 a {
    color: black;
    text-decoration: none;
}

#control {
    clear: both;
}

#search {
    float: left;
}

#search input {
    width: 300px;
    font-size: 14pt;
}

#mode {
    text-align: right;
}

#mode label:first-child {
    font-weight: bold;
}

#mode input {
    margin-left: 20px;
}

.info {
    margin-top: 10px;
    padding: 10px;
    background: #FAFADD;
    width: 250px;
    float: right;
    box-shadow: 1px 1px 1px 1px #ccc;
    clear: both;
}

.info h2 {
    font-size: 12pt;
    padding: 0px;
    margin: 0px;
}

.problem {
    margin-top: 10px;
    margin-bottom: 10px;
    padding: 10px;
    background: #FFBBAA;
    counter-increment: problem;
    width: 700px;
    border: 1px solid #993333;
    border-left: 5px solid #993333;
    box-shadow: 1px 1px 1px 1px #ccc;
    float: left;
}

.active {
    box-shadow: 5px 5px 3px 3px #ccc;
    position: relative;
    top: -2px;
}

.severe0 {
    background: #FAFAFA;
    border: 1px solid black;
    border-left: 5px solid black;
}

.severe1 {
    background: #FFEEDD;
}

.severe2 {
    background: #FFDDCC;
}

.severe3 {
    background: #FFCCBB;
}

.problem_checked {
    border: 1px solid #339933;
    border-left: 5px solid #339933;
}

.problem h2:before {
    content: counter(problem) ". "; color: gray;
}

.problem h2 {
    font-size: 12pt;
    padding: 0px;
    margin: 0px;
}

.problem .links {
    float: right;
    position:relative;
    top: -22px;
}

.problem .links a {
    color: #3333CC;
}

.problem .links a:visited {
    color: #666666;
}

.problem .reference {
    clear: both;
    font-size: 9pt;
    margin-left: 20px;
    font-style:italic;
    font-weight:bold;
}

.problem ul {
    clear: both;
}

.problem .problem_control {
    float: right;
    margin: 0px;
    padding: 0px;
}

.problem .bibtex_toggle{
    text-decoration: underline;
    font-size: 9pt;
    cursor: pointer;
    padding-top: 5px;
}

.problem .bibtex {
    margin-top: 5px;
    font-family: Monospace;
    font-size: 8pt;
    display: none;
    border: 1px solid black;
    background-color: #FFFFFF;
    padding: 5px;
}
</style>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.5/jquery.min.js"></script>
<script>

function isInProblemMode() {
    return $('#mode_problems:checked').val() == 'problems'
}

function update() {
    $('.problem').hide();
    $('.problem[id*='+$('#search input').val()+']').show();
    $('.problem .checked').each(function () {
        if ($(this).attr('checked')) {
            $(this).parents('.problem').addClass('problem_checked');
        } else {
            $(this).parents('.problem').removeClass('problem_checked');
        }
    });
    if (isInProblemMode()) {
        $('.severe0').hide();
        $('.problem_checked').hide();
    }
}

$(document).ready(function(){

    $(".bibtex_toggle").click(function(event){
        event.preventDefault();
        $(this).next().slideToggle();
    });

    $('#search input').live('input', function() {
        update();
    });

    $('#mode input').change(function() {
        update();
    });

    $("#uncheck_button").click(function(){
        $('.problem .checked').attr('checked',false);
        localStorage.clear();
        update();
    });

    $('.problem a').mousedown(function(event) {
        $('.problem').removeClass('active');
        $(this).parents('.problem').addClass('active');
    });

    $('.problem .checked').change(function(event) {
        var problem = $(this).parents('.problem');
        problem.toggleClass('problem_checked');
        var checked = problem.hasClass('problem_checked');
        localStorage.setItem(problem.attr('id'),checked);
        if (checked && isInProblemMode()) {
            problem.slideUp();
        }
    });

    $('.problem .checked').each(function () {
        $(this).attr('checked',localStorage.getItem($(this).parents('.problem').attr('id'))=='true');
    });
    update();
});

</script>
</head>
<body>
<div id="title">
<h1><a href='http://code.google.com/p/bibtex-check'>BibTeX Check</a></h1>
<div id="control">
<form id="search"><input placeholder="search entry ID ..."/></form>
<form id="mode">
<label>show entries:</label>
<input type = "radio"
                 name = "mode"
                 id = "mode_problems"
                 value = "problems"
                 checked = "checked" />
          <label for = "mode_problems">problems</label>
          <input type = "radio"
                 name = "mode"
                 id = "mode_all"
                 value = "all" />
          <label for = "mode_all">all</label>
<input type="button" value="uncheck all" id="uncheck_button"></button>
</form>
</div>
</div>
""")
html.write("<div class='info'><h2>Info</h2><ul>")
html.write("<li>bib file: "+bibFile+"</li>")
html.write("<li>aux file: "+auxFile+"</li>")
html.write("<li># entries: "+str(len(problems))+"</li>")
html.write("<li># problems: "+str(counterMissingFields+counterFlawedNames+counterWrongTypes+counterNonUniqueId)+"</li><ul>")
html.write("<li># missing fields: "+str(counterMissingFields)+"</li>")
html.write("<li># flawed names: "+str(counterFlawedNames)+"</li>")
html.write("<li># wrong types: "+str(counterWrongTypes)+"</li>")
html.write("<li># non-unique id: "+str(counterNonUniqueId)+"</li>")
html.write("</ul></ul></div>")

problems.sort()
for problem in problems:
    html.write(problem)
html.write("</body></html>")
html.close()
