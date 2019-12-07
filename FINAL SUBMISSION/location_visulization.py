import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

def get_csv(filename):
    '''
    This function is used to read .csv file and get data for visualization
    :param filename: a string type filename
    :return: a dataframe for next step
    '''
    assert isinstance(filename,str)
    return pd.read_csv(filename)

'''
use defined keywords for different field filtering
sw_keywords: represents software related job titles
hw_keywords: represents hardware related job titles
'''
sw_keywords = ["it","software", "sde", "programmer", "programming", "developer","IT","Software", "SDE", "Programmer", "Programming", "Developer"]
hw_keywords = ["electrical","hardware", "electronics", "semiconductor", "embedded", "circuit", "fpga", "component", "Electrical","Hardware", "Electronics", "Semiconductor", "Embedded", "Circuit", "FPGA", "Component", "HW", "Network", "Processor"]
dummy_keywords=['associate', 'Senior']

#filtering for only hardware or software related
def preprocess(df, keywords):
    '''
    This function acts as a preprocessing stage for dataframe using related keywords
    :param df: input dataframe
    :param keywords: keywords for filtering
    :return: a new data frame only contains software or hardaware related job titles
    '''
    df["date"] = df["date"].map(lambda x : x[-4:])
    tmp = df.job_title.str.contains(keywords[0],na=False)
    for i in range(1,len(keywords)):
        tmp = tmp | (df.job_title.str.contains(keywords[i],na=False))
    new_df = df[tmp]
    return new_df


#Ratings over year analysis
def rating_over_year(df, rating):
    '''
    This function is used to analysis the different ratings numbers changes over year for most recent years
    :param df: the input dataframe
    :param rating: rating type used(overall_ratings, work_life_balance_ratings and etc)
    :return: a list of average ratings over most recent 7 years
    '''
    # consider thev last 5 years:2019,18,17,16,15
    df["date"] = df["date"].map(lambda x : x[-4:])
    years = ['2013','2014','2015','2016','2017','2018','2019']
    ratings = []
    for i in range(len(years)):
        ratings.append(round(df[df.date==years[i]][rating].mean(),2))
    return ratings

# dictionary for most popular location for all reviews
lo_dict = {'CA':(37.7792768,-122.4192704),'NY':(40.7305991,-73.9865812),'WA':(47.6038321,-122.3300624),
'TX':(30.2711286,-97.7436995),'MA':(42.3604823,-71.0595678),'IL':(41.8755546,-87.6244212),'GA':(33.7490987,-84.3901849),
'MI':(42.3486635,-83.0567375), 'PA':(40.4416941,-79.9900861),'MO':(40.0149856,-105.2705456),'VA':(37,-80),
'CO':(38,-106),'FL':(27,-83),'NJ':(39,74),'OH':(39.5,-82.5),'DC':(38,-77),'NC':(35,-80),'OR':(44,-120),'AZ':(34,-111.5),
'NM':(34,-106),'WI':(44.5,-89)}

def process_location(data):
    '''
    This function is used to process data for location related job title distribution
    :param data: dataframe generated after read_csv
    :return: a dataframe of top 10 popular location with latitude and longitude for a kind of field of job title
    '''
    values = {'location': ' '}
    df = data.fillna(value = values)
    df["location"] = df["location"].map(lambda x : x[-2:] if x[-2:].isupper() and x[-2:] in list(lo_dict.keys()) else '')
    #s=df.groupby(by='location').size().sort_values(ascending=False)[:11]
    s=df.groupby(by='location').size().sort_values(ascending=False)
    mask = s.index.map(lambda x: x!='')
    s = s[mask][:10]
    s.rename_axis('state').reset_index(name='value').to_dict('records')
    d = [dict(state=k, value=v) for k, v in s.items()]
    dff = pd.DataFrame(d[0:])
    dff["locat"]= dff['state'].map(lo_dict)
    lo_list=list(dff["locat"])
    lat_lst = [i[0] for i in lo_list]
    lon_lst =[i[1] for i in lo_list]
    lat = pd.Series(lat_lst)
    lon = pd.Series(lon_lst)
    dff['lat'] = lat.values
    dff['lon'] = lon.values
    return dff


def location_distribution(new_df,company):
    '''
    This function is used to generate data visualization part for location related job title
    :param new_df: dataframe after location_process stage
    :param company: company for this analysis
    :return will save a .png file under same project directory
    '''
    plt.figure(figsize=(16,5))
    map = Basemap(projection='stere',lat_0=90,lon_0=-105,\
            llcrnrlat=23.41 ,urcrnrlat=45.44,\
            llcrnrlon=-118.67,urcrnrlon=-64.52,\
            rsphere=6371200.,resolution='l',area_thresh=10000)
    map.drawmapboundary()
    #map.fillcontinents()
    map.drawstates()
    map.drawcoastlines()
    map.drawcountries()
    map.drawcounties()
    parallels = np.arange(0.,90,10.)
    map.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
    meridians = np.arange(-110.,-60.,10.)
    map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
    lat = np.array(new_df["lat"][:])
    lon = np.array(new_df["lon"][:])
    num_review = np.array(new_df["value"],dtype=float)
    size=(num_review/np.max(num_review))*4000
    x,y = map(lon,lat)
    map.scatter(x,y,s=size,c ='steelblue')
    plt.title('Job positon distribution of '+ company)
    plt.savefig('job_position_distribution_'+company +'.png')
    plt.show()

'''
This part will do numerical analysis and data visualization for ratings over locations(different states)
rating_over_location: will find the average overall_rating for top 10 popular states for software or hardware
'''
def rating_over_location(df):
    '''
    This function is used to calculate the average overall_ratings for different states
    :param df: input dataframe read from .csv file
    :return: a list of tuple contains locations and average ratings
    '''
    values = {'location': ' '}
    df = df.fillna(value = values)
    df["location"] = df["location"].map(lambda x : x[-2:])
    dff = process_location(df)
    locations = list(dff['state'])
    ratings = []
    for i in range(len(locations)):
         ratings.append(df[df.location==locations[i]]["overall_rating"].mean())
    return list(zip(locations,ratings))

def rating_figure(lst,company,mean):
    '''
    This function is used to generate the visualization file for ratings over location for different companies
    :param lst: a list of tuples contains locations and ratings
    :param company: company name for analysis
    :type company: string type
    :param mean: the mean value for overall_rating, can be calculated using df["overall_ratings"].mean()
    :return: save a .png file for data visualization
    '''
    #another one
    plt.figure(figsize=(10,6))
    #plt.style.use('fivethirtyeight')
    plt.style.use('ggplot')
    x =[i[0] for i in lst]
    y=np.array([i[1] for i in lst])
    xticks1=x
    plt.bar(x,y,width = 0.5,align='center',color = 'steelblue',alpha=0.8)
    plt.axhline(y=mean)
    plt.xticks(x,xticks1,size='small')
    plt.xlabel('States')
    plt.ylabel('Overall Ratings')
    plt.title('Job Rating Distribution of different states for hardware companies')
    for a,b in zip(x,y):
        plt.text(a, b+0.05, '%.2f' % b, ha='center', va= 'bottom',fontsize=10)
    plt.ylim(3,4.5)
    plt.savefig('job_rating_' + company +'.png')
    plt.show()

columns = ['date','summary', 'job_title','location','overall_rating','work_life_balance_rating',
           'culture_values_rating', 'career_opportunities_rating','comp_benefits_rating',
           'senior_management_rating','main_text','pros','cons', 'advice_management']
def cal_rating(df):
    '''
    This function is used to calculate different type of ratings over locations
    :param df: the input dataframe from .csv file
    :return: a dict type of ratings with states such 'CA' as key and ratings as value
    '''
    values = {'location': ' '}
    df = df.fillna(value = values)
    df["location"] = df["location"].map(lambda x : x[-2:])
    dff = process_location(df)
    locations = list(dff['state'])
    ratings = {}
    for locat in locations:
        ratings[locat] = []
    for i in range(6):
        key = columns[i+4]
        for loc in locations:
            ratings[loc].append(df[df.location==loc][key].mean())
    return ratings

