from flask import Flask, render_template, request, redirect, url_for
from neo4j import GraphDatabase


 
app = Flask(__name__)
@app.route('/')
def geoportal():
    return render_template('KNTUGeoportal2.html')
uri             = "bolt://localhost:7687"

userName        = "neo4j"

password        = "12345678"

 

# Connect to the neo4j database server

graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))





cqlNodeQuery1         = "MATCH (x:dataset) RETURN x.title as dstitle, x.source as dssource, x.num as identifier"
cqlNodeQuery11         = "MATCH (x:dataset) WHERE x.top > $lat AND x.bottom < $lat RETURN x.title as dstitle, x.source as dssource, x.num as identifier"
cqlNodeQuery12         = "MATCH (x:dataset) WHERE x.right > $lon AND x.left < $lon RETURN x.title as dstitle, x.source as dssource, x.num as identifier"
cqlNodeQuery13         = "MATCH (x:dataset) WHERE x.solardate CONTAINS $solar1 RETURN x.title as dstitle, x.source as dssource, x.num as identifier"
cqlNodeQuery14         = "MATCH (x:dataset) WHERE x.christiandate CONTAINS $christian1 RETURN x.title as dstitle, x.source as dssource, x.num as identifier"
cqlNodeQuery21         = "MATCH (x:dataset) WHERE x.datatype CONTAINS $datatype RETURN x.title as dstitle, x.source as dssource, x.num as identifier"
cqlNodeQuery22         = "MATCH (x:dataset) WHERE x.province = $province RETURN x.title as dstitle, x.source as dssource, x.num as identifier"
cqlNodeQuery23         = "MATCH (x:dataset) WHERE x.city = $city RETURN x.title as dstitle, x.source as dssource, x.num as identifier"
cqlNodeQuery24         = "MATCH (x:dataset) WHERE x.solardate CONTAINS $solar2 RETURN x.title as dstitle, x.source as dssource, x.num as identifier"
cqlNodeQuery25         = "MATCH (x:dataset) WHERE x.christiandate CONTAINS $christian2 RETURN x.title as dstitle, x.source as dssource, x.num as identifier"
cqlNodeQuery26         = "MATCH (x:dataset) WHERE x.location CONTAINS $location RETURN x.title as dstitle, x.source as dssource, x.num as identifier"
cqlNodeQuery27         = "MATCH (x:dataset) WHERE x.title CONTAINS $eshi RETURN x.title as dstitle, x.source as dssource, x.num as identifier"




@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
    result = request.form
    if request.form['formID'] == '213023402613438':
      initialkey11= request.form['The Latitude']
      initialkey12= request.form['The Longitude']

      try:
          key11= float(initialkey11)
      except ValueError:
          key11= 2000;

      try:
          key12= float(initialkey12)
      except ValueError:
          key12= 2000;

      key13= request.form['Data collection solardate1'] or 'ggg'
      key14= request.form['Data collection christiandate1'] or 'ggg'

      print(key11)
      print(key12)
      print(key13)
      print(key14)



      with graphDB_Driver.session() as graphDB_Session:

          nodes1 = graphDB_Session.run(cqlNodeQuery1)
          nodes11 = graphDB_Session.run(cqlNodeQuery11, lat=key11)
          nodes12 = graphDB_Session.run(cqlNodeQuery12, lon=key12)
          nodes13 = graphDB_Session.run(cqlNodeQuery13, solar1=key13)
          nodes14 = graphDB_Session.run(cqlNodeQuery14, christian1=key14)



          nodes_m = [nodes11, nodes12, nodes13, nodes14]
          nodeset = set(nodes1)

          set1 = [(key11 != 2000), (key12 != 2000), (key13 != 'ggg'), (key14 != 'ggg')]
          print(set1)
          if set1[0] == 0 and set1[1] == 0 and set1[2] == 0 and set1[3] == 0:
              nodeset = []
          else:
              for i in range(len(set1)):
                  if set1[i] == 1:
                      nodes_mi = set(nodes_m[i])
                      nodeset = nodeset.intersection(nodes_mi)
          nodes = list(nodeset)

      return render_template("result2.html", df= nodes,length = len(nodes))
      if __name__ == '__main__':
         app.run(debug=True)
    if request.form['formID'] == '212993096711461':

      key21 = request.form['Data type'] or 'ggg'
      key22 = request.form['province2']
      key23 = request.form['city']
      key24 = request.form['Data collection solardate2'] or 'ggg'
      key25 = request.form['Data collection christiandate2'] or 'ggg'
      key26 = request.form['Keywords on Location'] or 'ggg'
      key27 = request.form['Keywords on data content'] or 'ggg'

      print(key21)
      print(key22)
      print(key23)
      print(key24)
      print(key25)
      print(key26)
      print(key27)
      set1 = [(key21 == 'ggg'), (key22 == 'ggg'), (key23 == '0'), (key24 == 'ggg'), (key25 == 'ggg'),
              (key26 == 'ggg'), (key27 == 'ggg')]

      print(set1)
      with graphDB_Driver.session() as graphDB_Session:

          nodes1 = graphDB_Session.run(cqlNodeQuery1)
          nodes21 = graphDB_Session.run(cqlNodeQuery21, datatype=key21)
          nodes22 = graphDB_Session.run(cqlNodeQuery22, province=key22)
          nodes23 = graphDB_Session.run(cqlNodeQuery23, city=key23)
          nodes24 = graphDB_Session.run(cqlNodeQuery24, solar2=key24)
          nodes25 = graphDB_Session.run(cqlNodeQuery25, christian2=key25)
          nodes26 = graphDB_Session.run(cqlNodeQuery26, location=key26)
          nodes27 = graphDB_Session.run(cqlNodeQuery27, eshi=key27)

          nodes_m = [nodes21, nodes22, nodes23, nodes24, nodes25, nodes26, nodes27]
          nodeset = set(nodes1)


          if set1[0] == 1 and set1[1] == 1 and set1[2] == 1 and set1[3] == 1 and set1[4] == 1 and set1[5] == 1 and set1[6] == 1:
              nodeset = []
          else:
              for i in range(len(set1)):
                  if set1[i] == 0:
                      nodes_mi = set(nodes_m[i])
                      nodeset = nodeset.intersection(nodes_mi)
          nodes = list(nodeset)

      return render_template("result2.html", df= nodes,length = len(nodes))
      if __name__ == '__main__':
                  app.run(debug = True)






