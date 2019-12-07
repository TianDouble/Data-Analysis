import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
import csv
from os import path
from os import path
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image

def wordCloudFuncGood(company, path_of_datasets):
   '''
   returns a wordcloud figure of the "good" reviews at a given company
   '''
   # background pic
   im_path = path_of_datasets+company+".png"

   alice_coloring = np.array(Image.open(im_path))
   your_list = []
   with open(path_of_datasets+company+'.csv', 'r',encoding='utf-8') as f:
       reader = csv.reader(f)
       your_list = '\t'.join([i[12] for i in reader])

   stopwords =''
   wordcloud = WordCloud(width=800, height=880,background_color="white", max_words=100, mask=alice_coloring,min_font_size=10, random_state=42).generate(your_list)
   #print(your_list)
   # plot the WordCloud image
   fig=plt.figure(figsize=(40,40))
   plt.imshow(wordcloud, interpolation="bilinear")
   plt.axis("off")
   plt.margins(x=0, y=0)
   plt.show


def wordCloudFuncBad(company, path_of_datasets):
   '''
   returns a wordcloud figure of the "bad" reviews at a given company
   '''
   # background pic
   im_path = path_of_datasets+company+".png"


   alice_coloring = np.array(Image.open(im_path))
  
   # reader object is created
   your_list = []
   with open(path_of_datasets+company+'.csv', 'r',encoding='utf-8') as f:
       reader = csv.reader(f)
       your_list = '\t'.join([i[13] for i in reader])

   stopwords =['company','good',company]
   wordcloud = WordCloud(width=800, height=880,background_color="white", max_words=100, mask=alice_coloring,max_font_size=70, random_state=42,colormap = 'Reds').generate(your_list)

   # plot the WordCloud image
   fig=plt.figure(figsize=(40,40))
   plt.imshow(wordcloud, interpolation="bilinear")
   plt.axis("off")
   plt.margins(x=0, y=0)
   plt.show()

