# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 19:24:44 2017

@author: Dargor
"""

import requests
from bs4 import BeautifulSoup



def web_spider():
    #URL to explore
    url = 'https://news.ycombinator.com/'
    #Download URL
    source_code = requests.get(url)
    #HTML code
    plain_text = source_code.text
    #BeatufulSoup object, HTML without identation
    soup = BeautifulSoup(plain_text, "lxml")
    #Order list
    total_order = []
    #Title list
    final_title = []
    #Points and comments list
    points_comments=[]
    
    #Search in athing class
    for athing in soup.findAll('tr', {'class': 'athing'}):
        #Search for order
        for num in athing.find('span', {'class': 'rank'}):
            order = num.string
            order = order.encode('ascii', 'ignore')
            for s in order.split('.'):
                if s.isdigit():
                    order = int(s)
            total_order.append(order)
            #Search for title
            for name in athing.find('a', {'class': 'storylink'}):
                title = name.string
                title = title.encode('ascii', 'ignore')
                final_title.append(title)
                
    #Search in subtext class
    for subtext in soup.findAll('td', {'class': 'subtext'}):
        #Search for points
        if subtext.find('span', {'class': 'score'}) in subtext:
            for score in subtext.findAll('span', {'class': 'score'}):
                points = score.string
                for s in points.split():
                    if s.isdigit():
                        points = int(s)
                #Search for comments
                for comm in subtext.findAll('a'):
                    comment = comm.string
                    #Encode to UTF8 
                    comment = comment.encode('utf-8')
                    if ('comments' or 'comment' or 'discuss' in comment):
                        if comment == 'discuss':
                            comment = 0
                            points_comments.append([points, comment])
                        else:
                            #Solve non-breakable spaces problem
                            for s in comment.split('\xc2\xa0'):
                                if s.isdigit():
                                    comment = int(s)
                                    points_comments.append([points, comment])
        else:
            points_comments.append([0, 0])
                                
    #Final list
    crawler = []
    for i in xrange(len(total_order)):
        crawler.append((total_order[i], final_title[i], points_comments[i][0], points_comments[i][1]))
    
#==============================================================================
#     #Print 
#     for i in xrange(len(crawler)):
#         print crawler[i]
#==============================================================================
        
    return crawler


def moreThanFive(web_spider):
    #Sort by amount of comments, smaller first
    sorted_list = sorted(web_spider, key=lambda web_spider: web_spider[3])
    
    #Bigger first
    #sorted_list.reverse()
    
    #Print result
    for i in xrange(len(sorted_list)):
        #Check if title has more than 5 words
        if len(sorted_list[i][1].split()) > 5:
              print sorted_list[i]

def lessOrEqual(web_spider):
    #Sort by amount of points, smaller first
    sorted_list = sorted(web_spider, key=lambda web_spider: web_spider[2])
    
    #Bigger first
    #sorted_list.reverse()
    
    #Print result
    for i in xrange(len(sorted_list)):
        #Check if title has more than 5 words
        if len(sorted_list[i][1].split()) <= 5:
              print sorted_list[i]
    
moreThanFive(web_spider())
