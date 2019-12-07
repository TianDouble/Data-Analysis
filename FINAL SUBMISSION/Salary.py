import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
import csv
from os import path
from os import path
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image


def salary_data(fname, path_of_datasets):
    '''
    processes the data in advance - processes the csv file to only salary data and then outputs the average salary
    fname: the csv file to process

    '''
    df = pd.read_csv(path_of_datasets+fname)
    df = df.drop(["Title", "Location", "Company"], axis=1)
    num = df.shape[0]
    new_df = df[df['Salary'] != 'None']
    new_df['Salary'] = new_df['Salary'].str.replace(r'[^0-9-]+', '')
    new_df['Salary'] = new_df['Salary'].str.split('-')
    new_df['Salary'] = new_df['Salary'].map(lambda x : x[0])
    mask = new_df['Salary'].str.len()>4
    new_df =new_df.loc[mask]
    return int(new_df["Salary"].astype(int).mean())


def salary_figure(jobtype, path_of_datasets):
    '''
    converts the data files to graphs
    the jobtype can be hardware or software
    the output is the graphs and the average salary of the jobtype
    '''
    assert isinstance(jobtype, str)
    assert jobtype == 'software' or jobtype == 'hardware'
    if jobtype == 'software':
        locations = ['CA','FL','NY','TX','VA','WA']
    if jobtype == 'hardware':
        locations = ['hd_CA','hd_GA','hd_MA','hd_NC','hd_NY','hd_TX']
        locations_hd = ['CA','GA','MA','NC','NY','TX']
    salary=[]
    for i in range(len(locations)):
        salary.append(salary_data(locations[i]+'.csv', path_of_datasets))
    plt.figure(figsize=(10,6))
    mn = np.mean(salary)
    if jobtype == 'software':
        lst = list(zip(locations, salary))
    if jobtype =='hardware':
        lst = list(zip(locations_hd, salary))
    lst = sorted(lst,key=itemgetter(1))
    plt.style.use('ggplot')
    x = [i[0] for i in lst]
    y = np.array([i[1] for i in lst])
    xticks1=x

    if jobtype == 'software':
        plt.bar(x,y,width = 0.5,align='center',color = 'sandybrown',alpha=0.8)
        plt.axhline(y=mn, color = 'steelblue',linestyle = '--')
        plt.ylim(60000, 120000)
    if jobtype == 'hardware':
        plt.bar(x,y,width = 0.5,align='center',color = 'steelblue',alpha=0.8)
        plt.axhline(y=mn, color = 'sandybrown',linestyle = '--')
        plt.ylim(60000, 110000)
    plt.xticks(xticks1,size='small')
    plt.xlabel("States")
    plt.ylabel('Average Salary in US dollar')
    plt.title(str.title(jobtype) + ' Job Salary(per year) Distribution in different states')
    for a,b in zip(x,y):
        plt.text(a, b+0.05, '%d' % b, ha='center', va= 'bottom',fontsize=10)
    plt.xticks(x,xticks1,size='small')
    plt.show()
    print('Average salary of the '+ str(jobtype)+' engineer is: $'+'%d' %mn)
