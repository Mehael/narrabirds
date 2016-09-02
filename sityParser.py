import os, re
import urllib.request, json, sys
import codecs

def OpenData(path):
	file = open(path, 'r')
	lines = file.readlines()

	ppl = []
	for line in lines:
		tokens = line.split(",")
		man = {}
		for tok in tokens:
			sides = tok.split(":")
			key = sides[0].split('"')[1]
			m = re.search("[0-9]+", sides[1])
			if m:
				value = m.group(0) 
			else:
				value = sides[1][1:-1]			
			man[key] = value
			
		ppl.append(man)	
	return ppl

def SortPpl(ppl):	
	pplByTowns = {}
	towns = []
	for man in ppl:
		if man.get("city"):	#NotBanned
			if man["city"] in towns:
				pplByTowns[man["city"]].append(man)
			else:
				pplByTowns[man["city"]] = []
				towns.append(man["city"])
				pplByTowns[man["city"]].append(man)
			
	return (pplByTowns, towns);

def Generate(pplByTowns, path, townNames):	
	file = open(path, 'w', encoding='utf-8')
	file.write(u'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Птицы Нарраторики</title>')
	file.write(u'<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">')
	file.write(u'<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>')
	file.write(u'<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>')
	
	file.write('<style media="screen" type="text/css">')
	file.write('body {background-color: #28a7b8;}')
	file.write('.pic {margin-top:10px; width:450px;}')
	file.write('.tit { margin-top:10px; margin-left: 60px;}')
	file.write('.white { background-color: white; margin-top: 30px; padding-bottom: 30px; border-radius: 5px;}')
	file.write('p {color: rgb(17, 37, 82);}')
	file.write('.myh {font-size: 20px;}')
	file.write('h1 {color: rgb(17, 37, 82); font-size: 70px;}')
	file.write('.box {background-color: white; border-style: solid; border-color: rgb(17, 37, 82); padding: 5px; width: 440px;}')
	file.write('</style>')
	
	file.write('</head><body>')
	#header
	file.write('<div class="container">')
	file.write('<div class="row"><div class="col-md-8 pic"><img src="logo.png"></div><div class="tit col-md-4"><h1 class="box">Птицы Нарраторики</h1></div></div>')
	file.write('</div>')
	#content
	file.write('<div class="container white">')
	file.write('<br><br><div class="row"><p class="text-center myh">Одолела Вомгла? <br> Геймдев уже не тот? <br> Вся движуха слишком далеко? <br><br> Выпей за <a href="https://vk.com/narratorika">Нарратив</a> с котанами из своего города.</p></div><br><br>')
	file.write('<div class="panel-group">')
	for town in townNames:
		if len(pplByTowns[town[0]]) == 1:
			continue
		file.write('<div class="col-sm-4">')
		file.write('<div class="panel panel-default"><div class="panel-heading">')
		file.write('<h4 class="panel-title"><a data-toggle="collapse" data-parent="#accordion" href="#'+town[0]+'">('+ str(len(pplByTowns[town[0]])) + ') ' + town[1] + "</a></h4>")
		file.write('</div><div id="'+town[0]+'" class="panel-collapse collapse"><div class="panel-body"><ul>')
		for man in pplByTowns[town[0]]:
			file.write('<li><a href="https://vk.com/id'+ man["uid"] + '">'+ man["first_name"] +' '+ man["last_name"] +'</a></li>\n')
		file.write('</ul></div></div></div>')
		file.write('</div>')#col-sm-4
	file.write('</div></div>')
	#footer
	file.write('<br><div class="container"><p class="text-center">Собрал <a href="https://vk.com/linver">Михаил Петров</a></p></div>')
	file.write(u'</body>')

			
def GetTownList(towns):
	url  = "https://api.vk.com/method/database.getCitiesById"
	method = 'city_ids='
	for t in towns[1:]:
		method = method + t + ','
	method = method + towns[0]
	
	binary_data = method.encode('utf-8')
	url = urllib.request.urlopen(url, binary_data)
	res  = url.read().decode(url.headers.get_content_charset())
	data = json.loads( res )
	
	if 'error' in data:
		print(data)
		return list()
		
	townDict = {}
	for tn in data['response']:
		townDict[str(tn['cid'])] = tn['name'].encode('utf-8', 'replace').decode('utf-8')
	
	import operator
	sorted_x = sorted(townDict.items(), key=operator.itemgetter(1))
	#print(sorted_x[0][1]) #0 - cid #1 - sorted name
	return sorted_x	
			
dirPath = os.path.dirname(__file__)	
data = OpenData(dirPath+"\\narratorika")
pplByTowns, towns = SortPpl(data)
townNames = GetTownList(towns)
Generate(pplByTowns, dirPath+"\\index.html", townNames)