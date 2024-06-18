from flask import Flask,request,render_template,make_response
import mysql.connector
from mysql.connector import Error
import json
import csv
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin

app=Flask(__name__)
cors=CORS(app)
app.config['CORS_HEADERS']='content-Type'
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/donation')
def donation():
    return render_template('donation.html')
    
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/regdata', methods =  ['GET','POST'])
def regdata():
    #Data gathering
    nm=request.args['uname']
    em=request.args['email']
    ph=request.args['phone']
    gen=request.args['gender']
    pswd=request.args['pswd']
    addr=request.args['addr']

    
    #Data transmission to db
    connection = mysql.connector.connect(host='localhost',database='blooddb',user='root',password='')
    sqlquery="insert into userdata(uname,email,phone,gender,pswd,addr) values('"+nm+"','"+em+"','"+ph+"','"+gen+"','"+pswd+"','"+addr+"')"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Data Saved Successfully"
    #return render_template('register.html')
    resp = make_response(json.dumps(msg))
    
    print(msg, flush=True)
    #return render_template('register.html',data=msg)
    return resp


@app.route('/donatedata', methods =  ['GET','POST'])
def donatedata():
    #Data gathering
    id=request.args['id']
    nm=request.args['name']
    age=request.args['age']
    em=request.args['email']
    ph=request.args['phone']
    gen=request.args['gender']
    bgroup=request.args['bgroup']
    haemoglobin=request.args['haemoglobin']
    platelets=request.args['platelets']
    weight=request.args['weight']
    message=request.args['message']
    bp=request.args['bp']
    disease=request.args['disease']
    mention=request.args['mention']
    addr=request.args['addr']

    
    #Data transmission to db
    connection = mysql.connector.connect(host='localhost',database='blooddb',user='root',password='')
    sqlquery="insert into donatedata(id,name,age,email,phone,gender,bgroup,haemoglobin,platelets,weight,message,bp,disease,mention,addr) values('"+id+"','"+nm+"','"+age+"','"+em+"','"+ph+"','"+gen+"','"+bgroup+"','"+haemoglobin+"','"+platelets+"','"+weight+"','"+message+"','"+bp+"','"+disease+"','"+mention+"','"+addr+"')"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Data Saved Successfully"
    #return render_template('register.html')
    resp = make_response(json.dumps(msg))
    
    print(msg, flush=True)
    #return render_template('register.html',data=msg)
    return resp



@app.route('/logdata', methods =  ['GET','POST'])
def logdata():
    #Data gathering
    em=request.args['email']
    pswd=request.args['pswd']

    
    #Data transmission to db
    connection = mysql.connector.connect(host='localhost',database='blooddb',user='root',password='')
    sqlquery="select count(*) from  userdata where email='"+em+"' and pswd='"+pswd+"'"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    data=cursor.fetchall()
    print(data) 
    connection.close()
    cursor.close()
    msg=""
    if data[0][0]==0:
        msg="Failure"
    else:
        msg="Success"
    #return render_template('register.html')
    resp = make_response(json.dumps(msg))
    
    print(msg, flush=True)
    #return render_template('register.html',data=msg)
    return resp


        
@app.route('/cleardataset', methods = ['POST'])
def cleardataset():
    print("request :"+str(request), flush=True)
    if request.method == 'POST':
        connection = mysql.connector.connect(host='localhost',database='blooddb',user='root',password='')
        sqlquery="delete from dataset"
        print(sqlquery)
        cursor = connection.cursor()
        cursor.execute(sqlquery)
        connection.commit() 
        connection.close()
        cursor.close()
        return render_template('dataloader.html',data="Data cleared successfully")
   
@app.route('/planning')
def planning():
    connection = mysql.connector.connect(host='localhost',database='blooddb',user='root',password='')
    sqlquery="select * from donatedata limit 100"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    data=cursor.fetchall()
    print(data) 
    connection.close()
    cursor.close()
    return render_template('planning.html',patdata=data)

@app.route('/donor')
def donor_page():
    connection = mysql.connector.connect(host='localhost',database='blooddb',user='root',password='')
    sqlquery="select * from blood_donation limit 100"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    data=cursor.fetchall()
    print(data) 
    connection.close()
    cursor.close()
    return render_template('donor.html',patdata=data)

@app.route('/recepient')
def recepient_page():
    connection = mysql.connector.connect(host='localhost',database='blooddb',user='root',password='')
    sqlquery="select * from recepient limit 100"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    data=cursor.fetchall()
    print(data) 
    connection.close()
    cursor.close()
    return render_template('recepient.html',patdata=data)

@app.route('/inventory')
def inventory_page():
    connection = mysql.connector.connect(host='localhost',database='blooddb',user='root',password='')
    sqlquery="select * from blood_inventory limit 100"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    data=cursor.fetchall()
    print(data) 
    connection.close()
    cursor.close()
    return render_template('inventory.html',patdata=data)



    























@app.route('/savedatasetang', methods = ['POST'])
def savedatasetang():
    print("request :"+str(request), flush=True)
    if request.method == 'POST':
        connection = mysql.connector.connect(host='localhost',database='skitdb',user='root',password='')
        cursor = connection.cursor()
    
        prod_mas = request.files['dt_file']
        filename = secure_filename(prod_mas.filename)
        prod_mas.save(os.path.join("./static/Uploads/", filename))

        #csv reader
        fn = os.path.join("./static/Uploads/", filename)

        # initializing the titles and rows list 
        fields = [] 
        rows = []
        
        with open(fn, 'r') as csvfile:
            # creating a csv reader object 
            csvreader = csv.reader(csvfile)  
  
            # extracting each data row one by one 
            for row in csvreader:
                rows.append(row)
                print(row)

        try:     
            #print(rows[1][1])       
            for row in rows[1:]: 
                # parsing each column of a row
                if row[0][0]!="":                
                    query="";
                    query="insert into dataset values (";
                    for col in row: 
                        query =query+"'"+col+"',"
                    query =query[:-1]
                    query=query+");"
                print("query :"+str(query), flush=True)
                cursor.execute(query)
                connection.commit()
        except:
            print("An exception occurred")
        csvfile.close()
        
        print("Filename :"+str(prod_mas), flush=True)       
        
        
        connection.close()
        cursor.close()
        msg="Dataset Uploaded Successfully"
        resp=make_response(json.dumps(msg))
        return resp
        return render_template('dataloader.html',data="Data loaded successfully")

@app.route('/planningang')
def planningang():
    connection = mysql.connector.connect(host='localhost',database='skitdb',user='root',password='')
    sqlquery="select * from dataset limit 100"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    data=cursor.fetchall()
    print(data) 
    connection.close()
    cursor.close()
    finaloplist=[]
    oplist=[]
    for i in range(len(data)):
        oplist=[]
        for j in range(len(data[i])):
            oplist.append(data[i][j])
        finaloplist.append(oplist)
    
    resp=make_response(json.dumps(finaloplist))
    return resp
    





if __name__=="__main__":
    app.run(debug=True)

