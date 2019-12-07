import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
import csv
from os import path
from os import path
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image


def preprocess(df, keywords):
    '''
    this function preprocesses the data in df for job titles containing the given keywords
    df: the given df you want to preprocess
    keywords: a list of keywords you want to filter for
    '''

    tmp = df.job_title.str.contains(keywords[0],na=False)
    for i in range(1,len(keywords)):
        tmp = tmp | (df.job_title.str.contains(keywords[i],na=False))
    new_df = df[tmp]
    return new_df



def getavg(df,rating):
    '''
    this function returns the average ratings of a given dataframe
    df: the df you want to get the ratings for
    rating: the type of rating or column you want the average of
    '''
    return df[rating].mean()

def HvSCompany(company, aVals, theData, numCompanies, figSize, title):
    overall=theData[0]
    worklife=theData[1]
    culture=theData[2]
    opportunities=theData[3]
    benefits=theData[4]
    management=theData[5]
    n_companies=numCompanies
    index=np.arange(n_companies)
    bar_width=0.15
    opacity=0.8
    plt.figure(figsize=(figSize,6))
    group_overall=plt.bar(index, overall, bar_width, alpha=opacity, color='#d1543e', label='Overall Rating')
    group_worklife=plt.bar(index+bar_width, worklife, bar_width, alpha=opacity, color='#4a89b9', label='Work/Life Balance Rating')
    group_culture=plt.bar(index+2*bar_width, culture, bar_width, alpha=opacity, color='#9590d0', label='Culture Rating')
    group_opportunities=plt.bar(index+3*bar_width, opportunities, bar_width, alpha=opacity, color='#777777', label='Opportunities Rating')
    group_benefits=plt.bar(index+4*bar_width, benefits, bar_width, alpha=opacity, color='#f4c271', label='Benefits Rating')
    groupculture=plt.bar(index+5*bar_width, management, bar_width, alpha=opacity, color='#a0e6cf', label='Senior Management Rating')

    plt.xlabel('Job Type')
    plt.ylabel('Ratings')
    companyName=company
    plt.title(title)
    plt.xticks(index+2.5*bar_width, ('Hardware', 'Software'))
    plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")

    for i, v in enumerate(overall):
        plt.text(index[i]+aVals[0], v + aVals[1], str(round(v,2)))

    for i, v in enumerate(worklife):
        plt.text(index[i]+aVals[2], v + aVals[3], str(round(v,2)))

    for i, v in enumerate(culture):
        plt.text(index[i]+aVals[4], v + aVals[5], str(round(v,2)))

    for i, v in enumerate(opportunities):
        plt.text(index[i]+aVals[6], v + aVals[7], str(round(v,2)))

    for i, v in enumerate(benefits):
        plt.text(index[i]+aVals[8], v + aVals[9], str(round(v,2)))

    for i, v in enumerate(management):
        plt.text(index[i]+aVals[10], v + aVals[11], str(round(v,2)))



    plt.tight_layout()
    plt.show()
