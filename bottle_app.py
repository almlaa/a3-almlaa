
#####################################################################
### Assignment skeleton
### You can alter the below code to make your own dynamic website.
### The landing page for assignment 3 should be at /
#####################################################################

from bottle import route, run, default_app, debug, get, post, request
import csv

categories = [
	"years", "changes"
]
columns = [
	"Nation",
	"2014",
	"2015" ,
	"2016" ,
	"2014 to 2015" ,
	"2015 to 2016" ,
	"Average" 
]




def htmlify(title,text):
	page = """
		<!DOCTYPE html>
		<html lang="en">
			<head>
				<meta charset="utf-8" />
				<style>
				
				body{
				background-color: #260116;
				color:#cffcfa;
				font-style:sans-serif, italic, Georgia;

				}
				.yazı{
				float:right;
				}
				
				
				form{
				color:#cffcfa;
				background-color:
				
				}		
				input, option{
				background-color:#cffcfa;
				color:#042738;
				}
				input[type=submit] {
				width:60px;
				height:34px;
				font-size:15px;
				
				}
				input[type=checkbox]:not(:checked) {
				background-color: #49889b;
				
				}
				
				
				
				
				
				table{
				border:1px solid #cffcfa;
				width:80%%;
				background-color:#cffcfa;
				color:#042738;
				margin-left:10px;
				margin-top:25px;
				border-collapse:collapse;	
					}
				th, td,table {
				border:1px solid grey;
				text-align:center;
				}
				th{
				height:40px;
				}
				td{
				height:32px;
				}
				tr:hover {background-color: #49889b;}
				a:link {				
				color:#cffcfa;
				text-decoration:none;
				font-weight:bold;
				}
				a:visited{				
				color:white;
				text-decoration:none;
				}
				a:hover{
				text-decoration:none;
				color:#042738;

				}
				a:active{
				color:black;
				text-decoration:underline;
					}
				#box1 {
				background-image: linear-gradient(to right, #398e8b, #123e49);
				margin-top:0px;
				float:left;
				padding:140px 7%% 0px 7%%;
				font-size:45px;
				width:36%%;
				height:360px;
				}
				#box2 {
				float:left;
				background-image: linear-gradient(to right, #398e8b, #123e49);
				padding:140px 7%% 0px 7%%;
				width:36%%;
				font-size:45px;
				height:360px;

				}
				input{
				box-sizing: border-box;
				}
				.homelink{
				background-image: linear-gradient(to right, #398e8b, #123e49);
				position:absolute;
				left:800px;
				top:3px;
				width:75px;
				border-radius:2px;
				height:40px;
				padding:4px 0px 4px 15px;
				
				}
				.tablelink{
				background-image: linear-gradient(to right, #398e8b, #123e49);
				position:absolute;
				left:700px;
				top:3px;
				width:70px;
				border-radius:2px;
				height:40px;
				padding:4px 0px 4px 20px;
				
				}
				#searching{
												clear: both;

				margin-top:10px;
				font-size:20px;
				}
				#aramakutusu{
				height:32px;
				}
				.alanya{
				float:right;
				width:406px;
				
				}
				
				</style>
				<title>%s</title>
			</head>
			<body>
			%s	
			</body>
		</html>

	""" % (title,text)
	return page
	
	


def read_data(filename):
	with open(filename) as input_file:
		data = []
		i = 0
		for row in csv.reader(input_file):
			if i > 2 and i < 23:
				data.append(row)
				data[i-3][1] = int(data[i-3][1])
				data[i-3][2] = int(data[i-3][2])
				data[i-3][3] = int(data[i-3][3])
				data[i-3][4] = float(data[i-3][4].rstrip("%"))
				data[i-3][5] = float(data[i-3][5].rstrip("%"))
				data[i-3][6] = int(data[i-3][6])

			i += 1
	return data


def apply_search(search, data):
	
	for i in reversed(range(len(data))):
		if search.lower() not in data[i][0].lower():
			del data[i]
	
	
# returns false if there is no custom request or all selected, otherwise returns true
def get_selected_columns():
	global columns
	if request.forms.get('custom') is None:
		return False
		
	selecteds = [0]
	for i in range(1, len(columns)):
		if request.forms.get('column_'+str(i)):
			selecteds.append(i)
	if i+1 == len(selecteds):
		return False
	return selecteds
		
	

def create_table(data):
	global columns
	
	if len(data) == 0:
		return "No Result Found!"
	selected_columns = get_selected_columns()
	if selected_columns:
		column_count = len(selected_columns)
	else:
		column_count  = len(columns)
	ret = "<table><tr><th colspan='%d'>Number of Tourist coming Turkey from Europe</tr>" % (column_count)
	#creating header
	ret += "<tr>"
	for i in range(len(columns)):
		if selected_columns == False or i in selected_columns:
			ret += "<th>" + columns[i] + "</th>"
	ret += "</tr>"
	
	if selected_columns:
		for row in data:
			ret += "<tr>"
			for column_id in selected_columns:
				ret += "<td>" + str(row[column_id]) + "</td>"
			ret += "</tr>"
	else:
		for row in data:
			ret += "<tr>"
			for cell in row:
				ret += "<td>" + str(cell) + "</td>"
			ret += "</tr>"
	
	ret += "</table>"
	return ret


def create_form(i = 0, reverse = False):
	global columns
	selected_columns = get_selected_columns()
	form ='<form method="POST"><select name="sort_by">'
	for x in (selected_columns if selected_columns else range(len(columns))):
		if x == i:
			form += """<option value="%d" selected>Sort by %s</option>""" % (x, columns[x])
		else:
			form += """<option value="%d">Sort by %s</option>""" % (x, columns[x])
	form +="</select>"
	
	if request.forms.get('search'):
		form += """<input type="hidden" name="search" value="%s">""" % (request.forms.get('search'))
		
	if selected_columns:
		form +='<input type="hidden" name="custom" value="1">'
		for i in selected_columns:
			form += """<input type="hidden" name="column_%d" value="1">""" % (i)
	checked = ""
	if reverse:
		checked = "checked"
	form +="""
	
	<input type="checkbox" name="reverse" value="1" %s> Descending Order
	<input type="submit" value = "Sort">
	</form>""" % (checked)
	
	return form




def index():
	page = """
	<div style="width: 100%; overflow:hidden;">
	<div id="box1"> <a href="/table"> Make Sortings on Table </a></div>
	<div id="box2"> <a href="custom_table">Create a New Table </a> </div>
	</div>
	<p id="searching"> Search Nation </p>
	<form method="POST" action="table">
		<input id="aramakutusu" type="text" name="search">
		<input type="submit" value="Search">


	<br><br><br>
 <h2>Tourism Destinations in Turkey</h2>
<div  class="yazı"  ><img class="alanya" src="http://tourismforall.org.tr/Img/Photos/578330620.jpg" alt="İmage of Alanya">	
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; İmage from Alanya</p> </div>

<p>Beach vacations and Blue Cruises, particularly for Turkish delights and visitors from Western Europe, are also central to the Turkish tourism industry. Most beach resorts are located along the southwestern and southern coast, called the Turkish Riviera, especially along the Mediterranean coast near Antalya. Antalya is also accepted as the tourism capital of Turkey. Major resort towns include Bodrum, Fethiye, Marmaris, Kuşadası, Çeşme, Didim and  &#9829; Alanya  &#9829;. Also Turkey has been chosen second in the world in 2015 with its 436 blue-flagged beaches, according to the Chamber of Shipping.

Lots of cultural attractions elsewhere in the country include the sites of Ephesus, Troy, Pergamon, House of the Virgin Mary, Pamukkale, Hierapolis, Trabzon (where one of the oldest monasteries is the Sümela Monastery), Konya (where the poet Rumi had spent most of his life), Didyma, Church of Antioch, ancient pontic capital and king rock tombs with its acropolis in Amasya, religious places in Mardin (such as Deyrülzafarân Monastery), and the ruined cities and landscapes of Cappadocia.

Diyarbakır is also an important historic city, although tourism is on a relatively small level due to waning armed conflicts.</p>

<p>Ankara has an historic old town, and although it is not exactly a tourist city, is usually a stop for travelers who go to Cappadocia. The city enjoys an excellent cultural life too, and has several museums. The Anıtkabir is also in Ankara. It is the mausoleum of Atatürk, the founder of the Republic of Turkey.

Gallipoli and Anzac Cove - a small cove on the Gallipoli peninsula, which became known as the site of World War I landing of the ANZAC (Australian and New Zealand Army Corps) on 25 April 1915. Following the landing at Anzac Cove, the beach became the main base for the Australian and New Zealand troops for the eight months of the Gallipoli campaign.</p>
	 
	 
	 
	 <h2>Development of tourism</h2>

  <div class="yazı">  <img class="alanya" src="https://www.gezitta.com/wp-content/uploads/2016/09/Kapadokya-Balon-Turu.jpg" alt="İmage of Cappadocia">
  <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; İmage from Cappadocia</p> 	</div>
	<p>Foreign tourist arrivals increased substantially in Turkey between 2000 and 2005, from 8 million to 21.2 million, which made Turkey a top-10 destination in the world for foreign visitors. 2005 revenues were US$17.5 billion which also made Turkey one of the top-10 biggest revenue owners in the world. In 2011, Turkey ranked as the 6th most popular tourist destination in the world and 4th in Europe, according to UNWTO World Tourism barometer. See World Tourism rankings. At its height in 2014, Turkey attracted around 42 million foreign tourists, still ranking as the 6th most popular tourist destination in the world.From 2015, tourism to Turkey entered a steep decline. In 2016, only around 25 million people visited Turkey. 2016 is described as the second year of huge losses on both visitor numbers and income, a "year of devastating losses", with Turkish tourism businesses stating that they "cannot remember a worse time in the sector".

In early 2017, the Turkish government urged Turkish citizens living abroad to take their vacations in Turkey, attempting to revive the struggling tourism sector of an economy that went into contraction from late 2016. After the April 2017 constitutional referendum, another sharp drop in tourist bookings from Germany was recorded.</p>
	<br>   <hr/>  
	 <p> <a href="https://en.wikipedia.org/wiki/Tourism_in_Turkey"> Source: Wikipedia </a> </p>
	</form>
	"""
	print(create_table)
	return htmlify("Tourism Statistics", page)
	
def custom_table():
	global columns
	page = """
	<div class="homelink"> <a href="/"> Home Page </a></div>
	<div class="tablelink"> <a href="/table">Real Table</a></div>
	<form method="POST" action="/table">"""
	for i in range(1,len(columns)):
		page += """<input type="checkbox" name="column_%d" id="column_%d"><label for="column_%d">%s</label>""" % (i, i, i, columns[i])
		
	page += """
	<input type="submit" name="custom" value="Create">
	</form>
	"""
	return htmlify("Tourism Statistics", page)

def table():
	
	data = read_data("a2_input.csv")
	
	if request.forms.get('search'):
		apply_search(request.forms.get('search'), data)
		
	if request.forms.get('reverse') == "1":
		reverse = True
	else:
		reverse = False
	sort_by = request.forms.get('sort_by')
	if sort_by:
		sort_by = int(sort_by)
		data.sort(key=lambda x: x[sort_by], reverse = reverse)
		form = create_form(sort_by, reverse)
	else:
		 form = create_form()
	form +=	"""<div class='homelink'> <a href="/"> Home Page </a></div>
	<div class='tablelink'> <a href="/custom_table">Make Table</a></div>"""
	
	return htmlify("Tourism Statistics", form + create_table( data))



route('/', 'GET', index)
route('/custom_table', 'GET', custom_table)
route('/table', 'GET', table)
route('/table', 'POST', table)

#####################################################################
### Don't alter the below code.
### It allows this website to be hosted on Heroku
### OR run on your computer.
#####################################################################

# This line makes bottle give nicer error messages
debug(True)
# This line is necessary for running on Heroku
app = default_app()
# The below code is necessary for running this bottle app standalone on your computer.
if __name__ == "__main__":
  run()

