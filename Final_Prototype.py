#Source:  http://www.eia.gov/
# http://nbviewer.ipython.org/gist/keflavich/4042018

import csv
import datetime
import matplotlib,matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from pylab import *
import math
import statsmodels.api as sm
import scipy, scipy.stats
from statsmodels.sandbox.regression.predstd import wls_prediction_std


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
    
    SetUp2Graph(description, value, date_YYYMM)
    file_path.close()
    f.close()
    
    #print description[0], len(description)
    #print value[0], len(value)
    #print date_YYYMM[0], len(date_YYYMM)

def SetUp2Graph(Desc, Value, Dates):
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
        elif Desc[j] == 'Total Renewable Energy Production':
            renewable_energy_production.append(Value[j])
        elif Desc[j] == 'Primary Energy Stock Change and Other':
            energy_stock_change.append(Value[j])
        elif Desc[j] == 'Total Primary Energy Production':
            primary_energy_production.append(Value[j])
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
    ####Sorting Dates out so that graph doesn't look like shit
    ####Graphing each individual Sector
    ###################Graphing EACH Sector###################
    #Graph_Data_Simple(Dates,primary_energy_consumption,"US Total Primary Energy Consumption 1973-2013",'Primary Energy Consumption','-b','-r')
    #Graph_Data_Simple(Dates,primary_energy_production,"US Total Primary Energy Production 1973-2013",'Primary Energy Production','-g','-k')
    #Graph_Data_Simple(Dates,primary_energy_exports,"US Total Primary Energy Exports 1973-2013",'Primary Energy Exports','-m','-c')
    #Graph_Data_Simple(Dates,primary_energy_imports,"US Total Primary Energy Imports 1973-2013",'Primary Energy Imports','-k','-r')
    #Graph_Data_Simple(Dates,nuclear_electric_consumption,"US Total Nuclear Electric Consumption 1973-2013",'Nuclear Electric Consumption','-g','-k')
    #Graph_Data_Simple(Dates,nuclear_electric_production,"US Total Nuclear Electric Production 1973-2013",'Nuclear Electric Production','-b','-g')
    #Graph_Data_Simple(Dates,renewable_energy_consumption,"US Total Renewable Energy Consumption 1973-2013",'Renewable Energy Consumption','-g','-r')
    #Graph_Data_Simple(Dates,renewable_energy_production,"US Total Renewable Energy Production 1973-2013",'Renewable Energy Production','-r','-b')
    #Graph_Data_Simple(Dates,fossil_fuel_production,"US Total Fossil Fuel Production 1973-2013",'Fossil Fuel Production','-g','-b')
    #Graph_Data_Simple(Dates,fossil_fuel_consumption,"US Total Fossil Fuel Consumption 1973-2013",'Fossil Fuel Consumption','-b','-r')
    
    ###################Primary Energy CONSUMPTION vs Sector###################
    ##Primary Nuclear###
    #Graph_Data_Simple2(Dates,primary_energy_consumption,nuclear_electric_consumption,"Primary Energy Consumption VS Nuclear Electric Consumption 1973-2013",'Primary Energy Consumption','Nuclear Electric Consumption','-b','-r','-g','-k')
    #Correlate_Data(primary_energy_consumption,nuclear_electric_consumption,Dates)
    
    ##Primary Renewable###
    #Graph_Data_Simple2(Dates,primary_energy_consumption,renewable_energy_consumption,"Primary Energy Consumption VS Renewable Energy Consumption 1973-2013",'Primary Energy Consumption','Renewable Energy Consumption','-b','-r','-g','-r')
    #Correlate_Data(primary_energy_consumption,renewable_energy_consumption,Dates)
    
    ##Primary Fossil###
    #Graph_Data_Simple2(Dates,primary_energy_consumption,fossil_fuel_consumption,"Primary Energy Consumption VS Fossil Fuel Consumption 1973-2013",'Primary Energy Consumption','Fossil Fuel Consumption','-b','-r','-k','-m')
    #Correlate_Data(primary_energy_consumption,fossil_fuel_consumption,Dates)
    
    ##################Primary Energy PRODUCTION vs Sector###################
    ##Primary Nuclear###
    #Graph_Data_Simple2(Dates,primary_energy_production,nuclear_electric_production,"Primary Energy Production VS Nuclear Electric Production 1973-2013",'Primary Energy Production','Nuclear Electric Production','-b','-r','-g','-k')
    #Correlate_Data(primary_energy_production,nuclear_electric_production,Dates)
    
    ##Primary Renewable###
    #Graph_Data_Simple2(Dates,primary_energy_production,renewable_energy_production,"Primary Energy Production VS Renewable Energy Production 1973-2013",'Primary Energy Production','Renewable Energy Production','-b','-r','-c','-r')
    #Correlate_Data(primary_energy_production,renewable_energy_production,Dates)
    
    ##Primary Fossil###
    #Graph_Data_Simple2(Dates,primary_energy_production,fossil_fuel_production,"Primary Energy Production VS Fossil Fuel Production 1973-2013",'Primary Energy Production','Fossil Fuel Production','-b','-r','-k','-m')
    #Correlate_Data(primary_energy_production,fossil_fuel_production,Dates)
    
    ###################Production vs Consumption###################
    ###Nuclear ###
    #Graph_Data_Simple2(Dates,nuclear_electric_production,nuclear_electric_consumption,"Nuclear Electric Production VS Nuclear Electric Consumption 1973-2013",'Nuclear Electric Production','Nuclear Electric Consumption','-b','-r','-g','-k')
    #Correlate_Data(nuclear_electric_production,nuclear_electric_consumption,Dates)
    #
    ###Renewable###
    #Graph_Data_Simple2(Dates,renewable_energy_production,renewable_energy_consumption,"Renewable Energy Production VS Renewable Energy Consumption 1973-2013",'Renewable Energy Production','Renewable Energy Consumption','-b','-r','-g','-m')
    #Correlate_Data(renewable_energy_production,renewable_energy_consumption,Dates)
    #
    ###Fossil###
    #Graph_Data_Simple2(Dates,fossil_fuel_production,fossil_fuel_consumption,"Fossil Fuel Production VS Fossil Fuel Consumption 1973-2013",'Fossil Fuel Production','Fossil Fuel Consumption','-b','-r','-k','-m')
    #Correlate_Data(fossil_fuel_production,fossil_fuel_consumption,Dates)
    
    ###Interesting...huge gap between production and consumption.  Wonder if imports makes up for it...
    #x = []
    #y = []
    #[x.append(float(val)) for val in fossil_fuel_consumption]
    #[y.append(float(val)) for val in fossil_fuel_production]
    #z2=[]
    #x2=[]
    #y2=[]
    #[x2.append(float(val)) for val in primary_energy_imports]
    #[y2.append(float(val)) for val in primary_energy_net_imports]
    #[z2.append(x2+y2) for x2,y2 in zip(x2,y2)]
    #plt.plot(Dates,x,'-b',Dates,y,'-g',Dates,z2,'-r')
    #plt.legend(['Fossil Fuel Consumption','Fossil Fuel Production','Total Energy Imports'],loc='best')
    #plt.show()
    
    ###################Renewable PRODUCTION vs Sectors###################
    ###NUCLEAR###
    #Graph_Data_Simple2(Dates,renewable_energy_production,nuclear_electric_production,"Renewable Energy Production VS Nuclear Electric Production 1973-2013",'Renewable Energy Production','Nuclear Electric Production','-b','-r','-g','-k')
    #Correlate_Data(renewable_energy_production,nuclear_electric_consumption,Dates)
    
    ###PRIMARY###
    #Graph_Data_Simple2(Dates,renewable_energy_production,primary_energy_production,"Renewable Energy Production VS Primary Energy Production 1973-2013",'Renewable Energy Production','Primary Energy Production','-g','-r','-b','-g')
    #Correlate_Data(renewable_energy_production,primary_energy_production,Dates)
    
    ###FOSSIL###
    #Graph_Data_Simple2(Dates,renewable_energy_production,fossil_fuel_production,"Renewable Energy Production VS Fossil Fuel Production 1973-2013",'Renewable Energy Production','Fossil Fuel Production','-b','-g','-r','-c')
    #Correlate_Data(renewable_energy_production,primary_energy_production,Dates)
    
    ###################Nuclear PRODUCTION vs Sectors###################
    ###FOSSIL###
    #Graph_Data_Simple2(Dates,nuclear_electric_production,fossil_fuel_production,"Nuclear Electric Production VS Fossil Fuel Production 1973-2013",'Nuclear Electric Production','Fossil Fuel Production','-g','-k','-c','-r')
    #Correlate_Data(nuclear_electric_production,fossil_fuel_production,Dates)
    
    ###RENEWABLE###
    #Graph_Data_Simple2(Dates,nuclear_electric_production,renewable_energy_production,"Nuclear Electric Production VS Renewable Energy Production 1973-2013",'Nuclear Electric Production','Renewable Energy Production','-g','-k','-b','-c')
    #Correlate_Data(nuclear_electric_production,renewable_energy_production,Dates)
    
    ###PRIMARY###
    #Graph_Data_Simple2(Dates,nuclear_electric_production,renewable_energy_production,"Nuclear Electric Production VS Primary Energy Production 1973-2013",'Nuclear Electric Production','Primary Energy Production','-r','-k','-m','-c')
    #Correlate_Data(nuclear_electric_production,primary_energy_production,Dates)
    
    ###################Fossil Fuel PRODUCTION vs Sectors###################
    ###NUCLEAR###
    #Graph_Data_Simple2(Dates,fossil_fuel_production,nuclear_electric_production,"Fossil Fuel Production VS Nuclear Electric Production 1973-2013",'Fossil Fuel Production','Nuclear Electric Production','-c','-r','-g','-k')
    #Correlate_Data(fossil_fuel_production,nuclear_electric_production,Dates)
    #
    ###RENEWABLE###
    #Graph_Data_Simple2(Dates,fossil_fuel_production,renewable_energy_production,"Fossil Fuel Production VS Renewable Production 1973-2013",'Fossil Fuel Production','Renewable Energy Production','-c','-r','-b','-m')
    #Correlate_Data(fossil_fuel_production,renewable_energy_production,Dates)
    #
    ###PRIMARY###
    #Graph_Data_Simple2(Dates,fossil_fuel_production,primary_energy_production,"Fossil Fuel Production VS Primary Energy Production 1973-2013",'Fossil Fuel Production','Primary Energy Production','-c','-r','-b','-g')
    #Correlate_Data(fossil_fuel_production,primary_energy_production,Dates)
    
def Graph_Data_Simple(Dates,Data_Set,Graph_Title,Data_Set_Title,line_color,poly_lc):
    plt.figure()
    x = mdates.date2num(Dates)
    #Setting up dates so that they can plot correctly
    x = x.tolist()
    #Converting x to list from np.array so that polyfit line can be generated
    y=[]
    [y.append(float(Data_Set[i])) for i in range(len(Data_Set))]
    #Setting up the BTU measures
    poly_fit_ln = polyfit(x,y,5)
    poly_fit_fn = poly1d(poly_fit_ln)
    #Linear regression
    plt.plot(Dates, Data_Set,line_color,Dates,poly_fit_fn(x),poly_lc)
    plt.title(Graph_Title)
    plt.ylabel('Quadrillion BTU')
    plt.xlabel('Years')
    #plt.legend([Data_Set_Title], loc='upper left')
    plt.show()
    
def Graph_Data_Simple2(Dates,Data_Set1,Data_Set2,Graph_Title,Data_Set_Title1,Data_Set_Title2,line_color1,poly_lc1,line_color2,poly_lc2):
    x = mdates.date2num(Dates)
    #Setting up dates so that they can plot correctly
    x = x.tolist()
    #Converting x to list from np.array so that polyfit line can be generated
    y1=[]
    y2=[]
    [y1.append(float(Data_Set1[i])) for i in range(len(Data_Set1))]
    [y2.append(float(Data_Set2[i])) for i in range(len(Data_Set2))]
    #Setting up the BTU measures
    poly_fit_ln1 = polyfit(x,y1,5)
    poly_fit_fn1 = poly1d(poly_fit_ln1)
    poly_fit_ln2 = polyfit(x,y2,5)
    poly_fit_fn2 = poly1d(poly_fit_ln2)
    
    #Linear regression
    plt.plot(Dates, Data_Set1,line_color1,Dates,poly_fit_fn1(x),poly_lc1)
    plt.plot(Dates, Data_Set2,line_color2,Dates,poly_fit_fn2(x),poly_lc2)
    plt.title(Graph_Title)
    plt.ylabel('Quadrillion BTU')
    plt.xlabel('Years')
    plt.grid()
    plt.legend([Data_Set_Title1,(Data_Set_Title1+" Best Fit"),Data_Set_Title2,(Data_Set_Title2+" Best Fit")], loc='best')
    plt.show()
    
def Correlate_Data(Data_Set1, Data_Set2,Dates):
    Data_Set1 = [float(val) for val in Data_Set1]
    Data_Set2 = [float(val) for val in Data_Set2]
    Dates = mdates.date2num(Dates)
    # Fit regression model
    X = np.column_stack((Data_Set1,Dates))
    X = sm.add_constant(X, prepend=True)
    model = sm.OLS(Data_Set2,X).fit() # our matrix data
    print model.summary()


Main()