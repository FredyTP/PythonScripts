from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pandas as pd
import pyqtgraph as pg
from pyqtgraph.ptime import time
import matplotlib.pyplot as pl
import re
import random


#------------FUNCTION DEFINITION-----------------
def getVarExample(var_list):
    rand_list = getRandVarList(5,var_list)
    return f"{rand_list[0]},{rand_list[1]} ; {rand_list[2]},{rand_list[3]},{rand_list[4]}"
def getRandVarList(num,var_list):
    ret_list=[]
    for i in range(num):
        ret_list.append(var_list[random.randint(0,len(var_list)-1)])
    return ret_list

def getValidVars(var_list):
    valid_vars="("
    for i in range(len(var_list)):
        csv_var=var_list[i]
        if(i==0):
            valid_vars+=(csv_var)
        else:
            valid_vars+=(", " +csv_var)
    valid_vars+=")"
    return valid_vars

def getValidVarsRegex(var_list):
    sorted_var_list=sorted(var_list,key=len,reverse=True)
    valid_vars_regex="(?:"
    for i in range(len(sorted_var_list)):
        csv_var=re.escape(sorted_var_list[i])
        if(i==0):
            valid_vars_regex+=csv_var
        else:
            valid_vars_regex+=("|"+csv_var)
    valid_vars_regex+=")"
    return valid_vars_regex


#------------CLASS DEFINITION-----------------
class GraficPlotter:

    def __init__(self):
        self.running=True
        self.have_to_sort=False
        self.title=""
        self.plot_keys=[]
        self.data=0
        self.variable_list=0

        self.valid_vars=0
        self.valid_vars_regex=0

        self.fig=0
        self.plot=0


    def setPlotKeys(self,key_list=list):
        self.plot_keys=[]
        if(len(key_list)==0):
            print("Error: invalid input")
            return False
        for key_var in key_list:
            if len(key_var)<2 :
                print("Error: invalid input")
                return False
            var_list=key_var.split(",")
            var_list[0]=var_list[0].strip()
            y_vars=var_list[1:]
            for i in range(len(y_vars)):
                var_list[i+1]=y_vars[i].strip()
            self.plot_keys.append(tuple(var_list))
        return True
        


    def loadData(self,data_path):
        self.data=pd.read_csv(data_path)
        self.variable_list=self.data.columns

        self.valid_vars=getValidVars(self.variable_list)
        self.valid_vars_regex=getValidVarsRegex(self.variable_list)

    
    def processInput(self,user_input_str):
        is_command=self.processCommand(user_input_str)
        is_valid=False      
        if(not is_command):
            plot_list=re.findall(f"\s*{self.valid_vars_regex}\s*(?:,\s*{self.valid_vars_regex}\s*)+",user_input_str)
            is_valid = self.setPlotKeys(plot_list)
        return is_valid


    def initPlot(self):
        self.fig=pl.figure(num=0,figsize=(16,9))
        self.axis=self.fig.add_subplot(1,1,1)
        self.plot=self.fig.add_subplot(1,1,1)
        if(self.title==""):
            self.plot.set_title(f"{x_var} vs ( {', '.join(y_vars)} )",fontsize=20,verticalalignment="bottom")
        else:
            self.plot.set_title(self.title,fontsize=20,verticalalignment="bottom")
        #self.plot.set_xlabel(x_var,fontsize=15)
        #self.plot.set_ylabel( f"( {', '.join(y_vars)} )" ,fontsize=15)
        self.plot.grid(linewidth=0.5, color='.25', zorder=-10,which="both")

    def plotGrafic(self):
        for plot_key in self.plot_keys:
            x_var=plot_key[0]
            y_vars=plot_key[1:]
            for y_var in y_vars:
                y_var=y_var.strip()
                sorted_x=self.data[x_var]
                sorted_y=self.data[y_var]

                if(self.have_to_sort):
                    sorted_x, sorted_y = zip(*sorted(zip(self.data[x_var], self.data[y_var])))

                self.plot.plot(sorted_x,sorted_y, lw=2, label = y_var,zorder=10)
        pl.legend()
        pl.show()
        
    def printCommandHelp(self):
        print("Quick Explanation")
        print("Separe variables with ','' to be plotted in the same grafic, where the first variable is the x axis, and all others are in y axis")
        print("Separe groups of plots with ';', it creates a new window if acum is not set to true")
        print("COMMANDS AVAILABLE: ")
        print("exit : closes the program")
        print("sort : sort the variables printed based on x axis")
        print("plot -all : columns are paired (1,2) (3,4) ... and all plotted WARNING: could create too much windows, use acum to plot all together")
        print("plot -all -x1 : print all variables with first columns as x axis")
        print("vars : displays all available variables")
        print("title -title_to_display : substitute the default title by title_to_display")

    def processCommand(self,user_input_str):
        inp_str=user_input_str.strip()
        if(inp_str=="exit"):
            self.running=False
            return True

        if(inp_str == "help"):
            self.printCommandHelp() 
            return True
        if(inp_str=="sort"):
            self.have_to_sort=True
            return True
        if(inp_str=="vars"):
            print(f"Available plot variables: {self.valid_vars}")
            return True
        if("title -" in inp_str):
            self.title=inp_str[7:]
            return True
        if(inp_str=="plot -all"):
            var_lists=[]
            for i in range(len(self.variable_list)//2):
                var_lists.append(f"{self.variable_list[2*i]},{self.variable_list[2*i+1]}")
            print(var_lists)
            self.setPlotKeys(var_lists)
            self.initPlot()
            self.plotGrafic()
            return True
        if(inp_str=="plot -all -x1"):
            var_lists=""
            for i in range(len(self.variable_list)):
                var_lists=",".join(self.variable_list)
            self.setPlotKeys([var_lists])
            self.initPlot()
            self.plotGrafic()
            return True

        return False


    def main_loop(self):
        print(f"Available plot variables  {grafic_plotter.valid_vars} \nExample: {getVarExample(grafic_plotter.variable_list)} \nType help to show commands")
        while(self.running):
            inp_str=input(f"Select plot variables or command\n")
            is_valid = self.processInput(inp_str)
            if(is_valid) :
                self.initPlot()
                self.plotGrafic()




#data=pd.read_csv("CasoBaseVelProfile.csv")
#csv_vars=data.columns

#valid_vars_regex=getValidVarsRegex(csv_vars)
#valid_vars=getValidVars(csv_vars)



inp_str=""
have_to_sort=False
have_to_acum=False
title=""

grafic_plotter = GraficPlotter()
grafic_plotter.loadData("data.csv")
grafic_plotter.main_loop()

"""
print(f"Available plot variables  {grafic_plotter.valid_vars} \nExample: {getVarExample(grafic_plotter.variable_list)} \nType help to show commands")
while (1):
    var_lists=[]
    inp_str=input(f"Select plot variables\n")
    inp_str=inp_str.strip()
    if(inp_str=="help"):
        print("Quick Explanation")
        print("Separe variables with ','' to be plotted in the same grafic, where the first variable is the x axis, and all others are in y axis")
        print("Separe groups of plots with ';', it creates a new window if acum is not set to true")
        print("COMMANDS AVAILABLE: ")
        print("exit : closes the program")
        print("sort : sort the variables printed based on x axis")
        print("plot -all : columns are paired (1,2) (3,4) ... and all plotted WARNING: could create too much windows, use acum to plot all together") 
        print("vars : displays all available variables")
        print("title -title_to_display : substitute the default title by title_to_display")

    if(inp_str=="exit"):
        break
    if(inp_str=="sort"):
        have_to_sort=True
    if(inp_str=="vars"):
        print(f"Available plot variables  {valid_vars}")
    if(inp_str=="plot -all"):
        for i in range(len(csv_vars)//2):
            var_lists.append(f"{csv_vars[2*i]},{csv_vars[2*i+1]}")
    grafic_plotter.processInput(inp_str)
    grafic_plotter.initPlot()
    grafic_plotter.plotGrafic()


















var_lists+=re.findall(f"\s*{valid_vars_regex}\s*(?:,\s*{valid_vars_regex}\s*)+",inp_str)
print(var_lists)
plot_num=len(var_lists)
if(plot_num>0):
    for i in range(plot_num):
        var_list=var_lists[i].split(",")
        x_var=var_list[0].strip()
        y_vars=var_list[1:]
        for i in range(len(y_vars)):
            y_vars[i]=y_vars[i].strip()
        fig=pl.figure(num=0,figsize=(16,9))

        plot=fig.add_subplot(1,1,1)
        plot.set_title(f"{x_var} vs ( {', '.join(y_vars)} )",fontsize=20,verticalalignment="bottom")
        plot.set_xlabel(x_var,fontsize=15)
        plot.set_ylabel( f"( {', '.join(y_vars)} )" ,fontsize=15)
        plot.grid(linewidth=0.5, color='.25', zorder=-10,which="both")

        for y_var in y_vars:
            y_var=y_var.strip()
            sorted_x=data[x_var]
            sorted_y=data[y_var]

            if(have_to_sort):
                sorted_x, sorted_y = zip(*sorted(zip(data[x_var], data[y_var])))

            plot.plot(sorted_x,sorted_y, lw=2, label = y_var,zorder=10)
        pl.legend(loc="best")
    pl.show()
"""



