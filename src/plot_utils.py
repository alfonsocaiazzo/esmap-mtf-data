#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 15:19:16 2020

@author: caiazzo
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import scipy.stats as ss

'''
Draw a bar chart using the dictionary data 
figure_name: if provided, figure is saved to file
title: if True, a title is added to the figure (data["title"])
'''


BLUE_COLORS = [
        "#EBF5FB",
        "#D6EAF8",
        "#AED6F1",
        "#85C1E9",
        "#5DADE2",
        "#2980B9", 
        "#2874A6",
        "#1B4F72"
        ]

RED_COLORS = [
        "#F8C471",
        "#FDEBD0",
        "#FDEDEC",
        "#F5B7B1",
        "#F1948A",
        "#E74C3C",
        "#B03A2E",
        "#78281F"]

RED_COLORS_rev = [
        
        "#B03A2E",
        "#78281F",
        "#B03A2E",
        "#E74C3C",
        "#FDEDEC",
        "#F8C471"]


YELLOW_COLORS = [
        "#FCF3CF", 
        "#F9E79F", 
        "#F7DC6F", 
        "#F4D03F", 
        "#F1C40F", 
        "#D4AC0D", 
        "#D4AC0D"]


VARIATION = [
        
        "#78281F",
        "#B03A2E",
        "#E74C3C",
        "#e36383",
        "#FDEDEC",
        "#F8C471",
        "#55d49e",
        "#F7DC6F", 
        "#F4D03F", 
        "#F1C40F", 
        "#D4AC0D", 
        "#D4AC0D"
        ]

def cramers_v(x, y):
    confusion_matrix = pd.crosstab(x,y)
    chi2 = ss.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2/n
    r,k = confusion_matrix.shape
    phi2corr = max(0, phi2-((k-1)*(r-1))/(n-1))
    rcorr = r-((r-1)**2)/(n-1)
    kcorr = k-((k-1)**2)/(n-1)
    return np.sqrt(phi2corr/min((kcorr-1),(rcorr-1)))


# compute correlation matrix
def get_corr(dataset):
    columns = dataset.columns

    corr = pd.DataFrame(index=columns, columns=columns)
    for i in range(0, len(columns)):
        row = []
        for j in range(0, len(columns)):
            if i == j:
                corr.loc[columns[i], columns[j]] = 1.0
            else:
                cell = cramers_v(dataset[columns[i]],dataset[columns[j]])
                ij = cell
                ji = cell
                corr.loc[columns[i], columns[j]] = ij if not np.isnan(ij) and abs(ij) < np.inf else 0.0
                corr.loc[columns[j], columns[i]] = ij if not np.isnan(ij) and abs(ij) < np.inf else 0.0
    return corr



def get_bar_chart_data(df,x,xname,y,yname):
    
    bars_data = []
    for a in y:
        bars_data.append([])
    
    for i in range(0,len(y)):
    
        df2 = df.loc[df[yname]==y[i]]
        for j in range(0,len(x)):
            bars_data[i].append(sum(df2[xname]==x[j]))
        
    return {
        'levels_labels': x,
        'bars_data': bars_data,
        'bars_labels': y
    }




def mean_value_bar_chart(df,x,categories,y,color_scheme,barWidth=1,figure_name=None,title=False,
                         length=9,height=6):
    
    names = []
    values = []
    for c in range(0,len(categories['choices']['names'])):
        df_t = df.loc[df[x]==categories['choices']['names'][c]]
        if len(df_t)/len(df)>0.02:
            names.append(categories['choices']['labels'][c])
            values.append(df_t[y].mean())
    ind = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(length,height)) 
    plt.bar(ind,values, edgecolor='white', color=color_scheme, width=barWidth)
    plt.xticks(ind, names,rotation=90)
    plt.axhline(y=df[y].mean(),linewidth=2, linestyle="dashed",color="black")
    plt.ylabel("%")
    # add title
    if title:
        plt.title(title)
        
    if not(figure_name==None):
        plt.savefig(figure_name,bbox_inches='tight')
        #print("** saving " + figure_name)
    plt.show()


def bar_chart(data,color_scheme,barWidth=1,figure_name=None,title=False,yLabel=None,
              length=9,height=6):
    fig, ax = plt.subplots(figsize=(length,height)) 
    
    # The position of the bars on the x-axis
    r = np.arange(len(data['levels_labels']))
    # Names of group and bar width
    names = data['levels_labels']
    
    
    b = data["bars_data"]
    bottom = 0*np.arange(len(data['levels_labels']))
    plt.bar(r,b, edgecolor='white', bottom = bottom, color=color_scheme,
            width=barWidth)
    # Custom X axis
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    
    plt.xticks(r, names,rotation=90)
    # add title
    if title:
        plt.title(data["title"])
        
    if not(yLabel==None):
        plt.ylabel(yLabel)
    if not(figure_name==None):
        plt.savefig(figure_name,bbox_inches='tight')
        #print("** saving " + figure_name)
    plt.show()


'''
Draw a stacked bar chart from several datasets. The data to be plotted
should be stored in the dictionary data
figure_name: if provided, figure is saved to file
'''
def stacked_bar_chart(data,color_scheme,barWidth=1,figure_name=None,
                      with_legend=False,title=False,
                      filename_legend=None,horizontal=False,
                      length=9,height=6):
    
    
    fig, ax = plt.subplots(figsize=(length,height)) 
    # The position of the bars on the x-axis
    r = np.arange(len(data['levels_labels']))
    # Names of group and bar width
    names = data['levels_labels']
    
    bottom = 0*np.arange(len(data['levels_labels']))
    
    for i in range(0,len(data["bars_data"])):
        b = data["bars_data"][i]
        # Create brown bars
        plt.bar(r,b, edgecolor='white', bottom = bottom, color=color_scheme[i],
                width=barWidth,label=data["bars_labels"][i])
        bottom = [sum(x) for x in zip(bottom, b)]

        
    # Custom X axis
    plt.xticks(r, names,rotation=90)
    
    if title:
        plt.title(data["title"])
    
    # create legend
    save_legend = not(filename_legend==None)
    
    save_figure = not(figure_name==None) 
    
    if with_legend or save_legend:
        plt.legend(framealpha=1,frameon=False,bbox_to_anchor=(1.2,1.0),
                           loc='upper center').set_draggable(True)
    if save_figure:
        plt.savefig(figure_name,bbox_inches='tight')
        #print("** saving " + figure_name)
    
    labels = data['levels_labels']
    ticks = np.arange(len(labels))  # the label locations    
    if (horizontal):
        ax.set_yticks(ticks)
        ax.set_yticklabels(labels)
        
    if save_legend:
        legend = ax.legend(framealpha=1,frameon=False,bbox_to_anchor=(1.2,1.0),
                           loc='upper center')
        figL  = legend.figure
        figL.canvas.draw()
        bbox  = legend.get_window_extent().transformed(figL.dpi_scale_trans.inverted())
        figL.savefig(filename_legend, dpi="figure", bbox_inches=bbox)
        
    # Show graphic
    plt.show()


def grouped_bar_chart(data,color_scheme,barWidth=1,figure_name=None,annotate=False,
                      with_legend=False,title=False,
                      horizontal=False,percent=False,
                      filename_legend=None,
                      length=12,height=8):
    
    labels = data['levels_labels']
    
    ticks = np.arange(len(labels))  # the label locations
    n = len(data["bars_data"])
    width = 1/(n+0.5)  # the width of the bars
    
    fig, ax = plt.subplots(figsize=(length,height)) 
    
    
    annotations = []
    rects = []
    for i in range(0,len(data["bars_data"])):
        if percent==True:
            b = data["percent_bars_data"][i]
            
        else:
            b = data["bars_data"][i]
            
        annotations.append(data["bars_data"][i])

        if (horizontal):
            rects.append(ax.barh(ticks + width*(-(n-1)/2+i), b, width, 
                                 label=data["bars_labels"][i],
                                 edgecolor="white",color=color_scheme[i]))



        else:
            rects.append(ax.bar(ticks + width*(-(n-1)/2+i), b, width, label=data["bars_labels"][i],edgecolor="white"))
    
    
    # Add some text for labels, title and custom x-axis tick labels, etc.

    if (horizontal):
        ax.set_yticks(ticks)
        ax.set_yticklabels(labels)
        if percent:
            ax.set_xlabel("%")
    
    else:
        ax.set_xticks(ticks)
        ax.set_xticklabels(labels,rotation=90)
        if percent:
            ax.set_ylabel("%")
        
    if title:
        ax.set_title(data["title"])
        
    save_legend = not(filename_legend==None)
    save_figure = not(figure_name == None)
    
    if with_legend or save_legend:
        ax.legend(framealpha=1,frameon=False,bbox_to_anchor=(1.5,1.0),
                           loc='upper center')
    
    
    
        
    

    def autolabel(rects,values,k):
        """Attach a text label above each bar in *rects*, displaying its height."""
        if horizontal:
            for rect in rects:
                width = rect.get_width()
                j = rects.index(rect)
                ax.annotate('{}'.format(values[k][j]),
                                xy=(width,rect.get_y() + rect.get_height() / 2),
                                xytext=(3, 0),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='left', va='center')
            
        else:
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')
    
    if annotate:
        for r in rects:
            k = rects.index(r)
            autolabel(r,annotations,k)

    #fig.tight_layout()
    
    if save_figure:
        plt.savefig(figure_name,bbox_inches='tight')
        #print("** saving " + figure_name)
    # Show graphic
    plt.show()
    
    if save_legend:
        legend = ax.legend(framealpha=1,frameon=False,bbox_to_anchor=(1.5,1.0),
                           loc='upper center')
        figL  = legend.figure
        figL.canvas.draw()
        bbox  = legend.get_window_extent().transformed(figL.dpi_scale_trans.inverted())
        figL.savefig(filename_legend, dpi="figure", bbox_inches=bbox)

    

def heatmap_matrix(df,x,y,annotations=True,colorbar=True,percent=False,
            figure_name=None):
    
    nx = len(x['choices']['names'])
    ny = len(y['choices']['names'])
    
    cross_mat = []
    xlabels = []
    norm = 1
    
        
    for i in range(0,nx):
        
        df_i = df.loc[ df[x['name']] == x['choices']['names'][i] ] 
        if len(df_i)>0.05*len(df):
            xlabels.append(x['choices']['names'][i])
            row = []
            rowsum=0
            for j in range(0,ny):
                df_j = df_i.loc[df_i[ y['name']] == y['choices']['names'][j] ] 
                row.append(round(len(df_j)/norm,2))
                rowsum += len(df_j)
            
            if percent:
                for j in range(0,len(row)):
                    row[j] = round(row[j]/rowsum*100,2)
                
            cross_mat.append(row)
    
    fig, ax = plt.subplots(figsize=(9,9)) 
    x_axis_labels = y['choices']['labels'] # labels for x-axis
    y_axis_labels = xlabels #x['choices']['labels'] # labels for y-axis
    ax = sns.heatmap(cross_mat,cmap="Oranges",annot=annotations,linewidths=.5,cbar=colorbar, 
                     xticklabels=x_axis_labels, yticklabels=y_axis_labels)
    plt.yticks(rotation=0) 
    if not(figure_name==None):
        plt.savefig(figure_name,bbox_inches='tight')
    plt.show()


# Functions that we need over the code

#TODO: Documentation 
def get_multiple_choice_values(df,questions):
    values = []
    for i in questions:
        values.append(sum(df[i]>0))

    # We return a dictionary with the count per injury type
    return {
        'major_accident': 100*(values[0]+values[1]+values[2]+values[3])/len(df),
        'minor_accident': 100*(values[4]+values[5]+values[6])/len(df),
        'no_accident': 100*(values[7])/len(df)
    }


def plot_bars(x_labels,bars_data,length=12,height=8,add_autolabel=True,percent=True):
    fig,ax = plt.subplots(figsize=(length,height))
    
    x = np.arange(len(x_labels))  # the label locations
    width = 1./(len(x))  # the width of the bars


    rects = []
    for k in range(0,len(bars_data)):
        rects.append(ax.bar(x + (-round(len(bars_data)/2,0) + k)*width, bars_data[k]['data'], width, label=bars_data[k]['label']))
    
    def autolabel(rects,percent=percent):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            if percent:
                ax.annotate('{}%'.format(round(height,1)),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')
            else:
                ax.annotate('{}'.format(round(height,1)),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')
           

    if add_autolabel:   
        for r in rects:
            autolabel(r)
       
    fig.tight_layout()

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    ax.legend()
    plt.show()


def simple_bar_plot(index,label,percent,title):
    
    pie_ = pd.DataFrame({label: percent},
                  index = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(index, percent)])
    pie_.plot.bar(y = label, figsize=(10, 10), title = title)
