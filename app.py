import pandas as pd 
import numpy as np 
from flask import Flask
from flask import render_template
import json
import csv
import logging
from flask import request
from collections import defaultdict


app = Flask(__name__)

df2 = pd.read_csv(r'data/df2015-18.csv')
dfyear= pd.read_csv("data/df2015-18.csv")
@app.route("/")
def d3():
  
    return render_template('index2.html')

#get a country's data- pie
def dfbycountry(countrycode):
    dfcountry= df2.loc[df2['code'] ==countrycode] 
    return dfcountry

#get country's data - sun
def dfbycountrysun(countrycode):
    dfc1= dfyear.loc[dfyear['code'] ==countrycode] 
    return dfc1

#pie data
@app.route('/getDataPerCountryPie')
def getDataPerCountryPie():
    country = request.args.get('country', type=str)
    if country=='All':
        countdf=df2.groupby('success')['success'].count().reset_index(name="count")
        countdf["success"]= countdf["success"].astype(str)
        countdf["success"].replace({"0": "Fail", "1": "Success"}, inplace=True)

        piedata= countdf.to_json(orient='records')
        piedata = json.dumps(piedata, indent=2)
        return piedata
    else:
        countdf1= dfbycountry(country)
        countdf1=countdf1.groupby('success')['success'].count().reset_index(name="count")
        countdf1["success"]= countdf1["success"].astype(str)
        countdf1["success"].replace({"0": "Fail", "1": "Success"}, inplace=True)
        piedata1= countdf1.to_json(orient='records')
        piedata1 = json.dumps(piedata1, indent=2)
        return piedata1

#sunburst data
@app.route('/getDataSun')
def getDataSun():
    country = request.args.get('country', type=str)
    #sun data
    
    dfk=dfyear.groupby(['iyear','attacktype1_txt'])['nkill'].sum().reset_index(name="kill total")
    dfk.to_csv("year_attack.csv")
    if country=='All':
        #dictionary
        results = defaultdict(lambda: defaultdict(dict))
        with open('year_attack.csv') as csv_file:
            for val in csv.DictReader(csv_file):
                results[val['iyear']][val['attacktype1_txt']] = (float(val['kill total']))

        
        output = {  'name': 'TOTAL','children': []}

        
        

        for k1,v1 in results.items(): 
                children1=[]
                for k2,v2 in v1.items():
                    children1.append({'name':k2,'size':float(v2)})
                
                output['children'].append({
                    'name':k1,
                    'children':children1
                    
                    
                })
        
        sundata = json.dumps(output)
        return sundata
    else:
        dfy= dfbycountrysun(country)
        dfk1=dfy.groupby(['iyear','attacktype1_txt'])['nkill'].sum().reset_index(name="kill total")
        dfk1.to_csv("year_attack1.csv")
        results1 = defaultdict(lambda: defaultdict(dict))

        #nested dictionary
        with open('year_attack1.csv') as csv_file:
            for val in csv.DictReader(csv_file):
                results1[val['iyear']][val['attacktype1_txt']] = (float(val['kill total']))

        #json object
        output1 = {  'name': 'TOTAL','children': []}

        
        

        for k1,v1 in results1.items(): 
                children2=[]
                for k2,v2 in v1.items():
                    children2.append({'name':k2,'size':float(v2)})
                
                output1['children'].append({
                    'name':k1,
                    'children':children2
                    
                    
                })
        sundata1 = json.dumps(output1)
        return sundata1


@app.route('/getDataPerCountryBar')
def getDataPerCountryBar():
    country = request.args.get('country', type=str)
    if country=='All':
        df3=df2.groupby(['weaptype1_txt'])['weaptype1'].count().reset_index(name="count")
    else:
        print("insode app country selected is"+country)
        countryspecificdf = dfbycountry(country)
        df3=countryspecificdf.groupby(['weaptype1_txt'])['weaptype1'].count().reset_index(name="count")
    
    bardata= df3.to_json(orient='records')
    bardata = json.dumps(bardata, indent=2)

    #print("final bar data is " + bardata)    
    return bardata  


@app.route('/getTextData')
def getTextData():
    country = request.args.get('country', type=str)
    if country=="All":
        incidents = df2.shape[0]
        casulties = int(df2['nkill'].sum())
        wounded = int(df2['nwound'].sum())
    else:
        countryspecificdf = dfbycountry(country)
        incidents = countryspecificdf.shape[0]
        casulties = int(countryspecificdf['nkill'].sum())
        wounded = int(countryspecificdf['nwound'].sum())
    
    textdata = {"incidents":incidents, "casulties":casulties, "wounded":wounded}
    print (textdata)
    return json.dumps(textdata)    

if __name__ == "__main__":
    app.run( debug=True)