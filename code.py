# -*- coding: utf-8 -*-

from facebook_scraper import get_posts

# Commented out IPython magic to ensure Python compatibility.
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
# %matplotlib inline
import matplotlib.pyplot as plt

import time
import re

page_number = #number of pages you want to scrape
page_nick = 'nick of the chosen Facebook page'

cookies = 'your browser cookies file (json format)'

listposts = []
text_list = []
time_list = []
likes_countlist = []
comments_countlist = [] 
my_postid = []

my_commid = []
comments_text = []

count = 0

#report = 0

for post in get_posts(page_nick, pages=page_number, cookies=cookies, options={"comments": True}):
  if len(post['comments_full']) > 1:
    count += 1
    #listposts.append(post)
    text_list.append(post['text'])
    time_list.append(post['time'])
    likes_countlist.append(post['likes'])
    #comments_countlist.append(len(post['comments_full']))
    my_postid.append(count)
    for j in range(0, len(post['comments_full'])):
      if len(post['comments_full'][j]['replies']) == 0:
             comments_text.append(post['comments_full'][j]['comment_text'])
             my_commid.append(count)
      elif len(post['comments_full'][j]['replies']) > 0:
        for i in range(0, len(post['comments_full'][j]['replies'])):
          #count += 1
          comments_text.append(post['comments_full'][j]['replies'][i]['comment_text'])
          my_commid.append(count)

    #report += 1      

    #print(f'scraped till this comment for now: {report}')      
  
    time.sleep(5)

df_comments = pd.DataFrame(columns=['CommentID', 'Content'])

col_list_comm = [my_commid, comments_text]

for i in range(0, 2):
  df_comments.iloc[:, i] = col_list_comm[i]

df_overall = pd.DataFrame(columns=['PostID', 'Date', 'TotalLikes', 'PostContent'])

col_list = [my_postid, time_list, likes_countlist, text_list]

for i in range(0, 4):
  df_overall.iloc[:, i] = col_list[i]

comments_countlist_1 = []

for x in range(1, 348):
  comments_countlist_1.append(len(df_comments[df_comments['CommentID'] == x]))

df_overall['CommentsCount'] = comments_countlist_1

df_comments.to_excel('filename.xlsx') #database with comments only
df_overall.to_excel('filename.xlsx') #database with post ID, post date, post likes and post content too
