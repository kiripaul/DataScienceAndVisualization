#Source:  http://www.eia.gov/
# http://nbviewer.ipython.org/gist/keflavich/4042018

import csv
import datetime
import matplotlib,matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from pylab import *

def Main():
    file_path = open("TotalEnergyOverview_Monthly_1973-2013.csv",'r')
    
    TEO_CSV = csv.DictReader(file_path)
    
    description =[]
    value = []
    date_YYYMM = [] 
      
    f = open("Yearly_Summaries.txt","w")
    
    for line in TEO_CSV:
        year = line["YYYYMM"][0:4]
        month = line["YYYYMM"][4:6]
        year_month = year+"-"+month
        if month == "13":
            yearly_summary = line["Description"]+" "+line["Value"]+" "+year_month + "\n"
            f.write(yearly_summary)
        else:
            description.append(line["Description"])
            value.append(line["Value"])
            year_month = datetime.datetime.strptime(year_month,"%Y-%m")
            #Converting year_month to datetime format but still returns YYYY-MM-DD HH:MM:SS
            year_month = datetime.datetime.strftime(year_month,"%Y-%m")
            #Formatting year_month to fit format YYYY-M but now it is a string...
            year_month = datetime.datetime.strptime(year_month,"%Y-%m")
            #So converting year_month back into datetime object so it can be graphed

            date_YYYMM.append(year_month) 
    
    Graph_TEO_Monthly(description, value, date_YYYMM)
    #print description
    file_path.close()
    f.close()
    
    #print description[0], len(description)
    #print value[0], len(value)
    #print date_YYYMM[0], len(date_YYYMM)

def Graph_TEO_Monthly(Desc, Value, Dates):
    #Graphing TotalEnergyOverview_Monthly_1973-2013 .. Include multiple sectors
    
    primary_energy_consumption=[]
    primary_energy_production=[]
    primary_energy_exports=[]
    primary_energy_net_imports=[]
    primary_energy_imports=[]
    
    nuclear_electric_consumption = []
    nuclear_electric_production=[]
    
    renewable_energy_consumption=[]
    renewable_energy_production=[]
    
    fossil_fuel_production = []
    fossil_fuel_consumption=[]
    
    energy_stock_change=[] 
    
    #description = list(set(Desc)) #Finding unique descriptions
    #print description
    #val_desc = zip(Value, Desc) #Creating Tuples 
    
    #Pulling out the values for each Category
    for j in range(len(Desc)):
        if Desc[j] == 'Total Primary Energy Consumption':
            primary_energy_consumption.append(Value[j])
        elif Desc[j] == 'Nuclear Electric Power Consumption':
            nuclear_electric_consumption.append(Value[j])
        elif Desc[j] == 'Total Renewable Energy Consumption':
            renewable_energy_consumption.append(Value[j])
        elif Desc[j] == 'Total Fossil Fuels Production':
            fossil_fuel_production.append(Value[j])
        elif Desc[j] == 'Total Primary Energy Consumption':
            nuclear_electric_consumption.append(Value[j])
        elif Desc[j] == 'Total Renewable Energy Production':
            renewable_energy_production.append(Value[j])
        elif Desc[j] == 'Primary Energy Stock Change and Other':
            energy_stock_change.append(Value[j])
        elif Desc[j] == 'Total Primary Energy Production':
            primary_energy_production.append(Value[j])
        elif Desc[j] == 'Total Primary Energy Consumption':
            nuclear_electric_consumption.append(Value[j])
        elif Desc[j] == 'Nuclear Electric Power Production':
            nuclear_electric_production.append(Value[j])
        elif Desc[j] == 'Total Fossil Fuels Consumption':
            fossil_fuel_consumption.append(Value[j])
        elif Desc[j] == 'Primary Energy Exports':
            primary_energy_exports.append(Value[j])  
        elif Desc[j] == 'Primary Energy Net Imports':
            primary_energy_net_imports.append(Value[j])
        elif Desc[j] == 'Primary Energy Imports':
            primary_energy_imports.append(Value[j])
    
    Dates = list(set(Dates))
    Dates.sort()
    
    x = mdates.date2num(Dates)
    y=[]
    [y.append(float(primary_energy_consumption[i])) for i in range(len(primary_energy_consumption))]
    x = x.tolist()
    poly_fit_ln = polyfit(x,y,5)
    poly_fit_fn = poly1d(poly_fit_ln)
    plt.plot(Dates, primary_energy_consumption,'-b',x,poly_fit_fn(x))
    #plt.plot(x, y)
    plt.title("US Total Primary Energy Consumption 1973-2013")
    #print len(x), len(y)
    #g =np.polyfit(x,y,30)
    #h = np.poly1d(g)
    #print len(Dates), len(g), len(h), len(y)
    #plt.plot(Dates, g)
    
    
    
    #plt.plot(Dates, primary_energy_production)
    #plt.plot(Dates, primary_energy_imports)
    
    #plt.legend(['Primary Energy Consumption', 'Primary Energy Production', 'Primary Energy Imports'], loc='upper left')
    
    plt.show()
    
    #print Desc, Value, Dates


Main()