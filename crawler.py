# ----------------------------- #
#         WEB CRAWLER           #
#                               #
# Subhendu Sethi (CS13B1027)    #
# Rahul Kumar (ES13B1018)       #
# Prashant Dewangan (CS13B1025) #
# ----------------------------- #

import socket
import sys
from bs4 import BeautifulSoup
import os
import urllib2
import re
from collections import deque


# Queue DS for URL BFS Implementation
urlQueue = deque()

# Map to store distinct URLs
urlMAP = {}

# To discard irrelevant URLs and remove extra parts from the URLs
def removeExcess(urlList):
    finalList = []

    # Remove the extra parts from the URL that comes after ".html"
    for url in urlList:
        index = url.find(".html")
        urlNew = url[:index+5]
        # If URL doesn't contain ".html"
        if index == -1:
            continue
        else:
            # Append the new URL after removing extra part
            finalList.append(urlNew)

    # Empty "urlList"
    del urlList[:]
    urlList = []

    # Check for seed domain and discard irrelevant URLs
    for url in finalList:
        index = url.find("www.nytimes.com")
        if(index == -1):
            continue
        else:
            # Append URLs which contain "www.nytimes.com"
            urlList.append(url)

    # Return the final list of URLs
    return urlList

# Extract all the relevant URLs
def extractHref(dataReceived):
    hrefLinks = []

    # Use "BeautifulSoup" function to parse on the HTML data received
    soup = BeautifulSoup(dataReceived, "html.parser")

    # Find "div" where "class = story" and take all URLs from it
    for itDiv in soup.findAll('div', {'class' : 'story'}):
        # Find "a" inside each "div"
        for itHref in itDiv.findAll('a', href = True):
            # If "href = True", append the URL to hrefLinks
            hrefLinks.append(itHref.get('href').encode('utf-8'))

    # Find "article" where "class = story" and take all URLs from it
    for itArticle in soup.findAll('article', {'class' : 'story'}):
        # Find "a" inside each "article"
        for itHref in itArticle.findAll('a', href = True):
            # If "href = True", append the URL to hrefLinks
            hrefLinks.append(itHref.get('href').encode('utf-8'))

    # Return all URLs
    return hrefLinks

# Parse the data received and get TITLE, CONTENT, DATE, META-KEYWORDS
# Create Documents with DOC IDs
def parseData(dataReceived, url, index, resultsPath):
    if index == 0:
        return 1

    # Use "BeautifulSoup" function to parse on the HTML data received
    soup = BeautifulSoup(dataReceived, "html.parser")

    # Extract CONTENT
    # Extract text from all paragraphs having "class = story-body-text"
    body = soup.find('p', {'class' : 'story-body-text'})
    contentFinal = ""
    words = 0
    if body != None:
        for itContent in soup.findAll('p', {'class' : 'story-body-text'}):
            if itContent == None:
                continue
            content = itContent.getText()
            # Remove newlines
            content = re.sub(r"\n+", " ", content)
            words+=len(content.split())
            contentFinal+=content
    else:
        return -1

    if words >= 150:
        print url
        # Open file with name as Document ID
        fileName = "DOC_" + str(index) + ".txt"
        file = open(resultsPath + "/" +fileName, "w")
        
        # Write URL in the File
        file.write(url.encode('utf-8') + "\n")

        # Get TITLE by crawling through the HTML
        title = soup.find('head')
        if title != None:
            title = title.find('title')
            if title != None:
                # If "title" found, get text and write the text in the file
                title = title.getText()
                file.write(title.encode('utf-8') + "\n")
            else:
                # Else write "TITLE NOT FOUND"
                file.write("TITLE NOT FOUND\n")

        # Get META-KEYWORD and write it into the file
        meta = soup.find('meta', {'name' : 'keywords'})
        if(meta != None):
            meta = meta.get('content')
            file.write(meta.encode('utf-8') + "\n")
        else:
            file.write("META-KEYWORDS NOT FOUND\n")

        # Get DATE and write it into the file
        date = soup.find('li',{'class' : 'date'})
        if(date != None):
            date = date.getText()
            file.write(date.encode('utf-8') + "\n")
        else:
            date = soup.find('meta', {'name' : 'DISPLAYDATE'})
            if date != None:
                date = date.get('content')
                if date != None:
                    file.write(date.encode('utf-8') + "\n")
                else:
                    file.write("DATE NOT FOUND\n")
            
        # Write DOCUMENT ID
        file.write(str(index) + "\n")

        # Write CONTENT
        file.write(contentFinal.encode('utf-8'))
        file.close()
        return 1
    else:
        return -1

# 
def crawlWebsite(url, index, resultsPath):
    hrefLinks = []
    flag = -1

    try:
        # Get all the data of an HTML page
        req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
        dataReceivedTemp = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(req)
        dataReceived = dataReceivedTemp.read()

        # Call parseData() to extract data, Content, meta-keyword, title, date
        flag = parseData(dataReceived, url, index, resultsPath)
        
        # Extract links from the page
        hrefLinks = extractHref(dataReceived)
        # Remove irrelevant URLs and extra parts from the URLs
        hrefLinks = removeExcess(hrefLinks)
    except Exception:
        pass
    # returns list of article links extracted from "url" and flag if new Document was created
    return (hrefLinks,flag)

# bfs routine to iteratively generate new links given a starting url
def bfs(start, urlLimit, resultsPath):
    globalIndex = 0
    # Append the first URL
    urlQueue.append(start)    
    while globalIndex != urlLimit+1:
        # If we reach a stage where we cannot generate new links from the bfs tree of url
        if len(urlQueue) == 0:
            print "urlQueue ZERO"
            break
        url = urlQueue.popleft()
        if url not in urlMAP:                
            # Mark url as visited 
            urlMAP[url] = 1
            # Assign unique DOCUMENT_ID to the doucument of the link
            index = globalIndex 
            hrefList,flag = crawlWebsite(url, index, resultsPath)
            # Add new links to the Queue
            urlQueue.extend(hrefList)  
            # Flag will be 1 only if the generated document from "url" has content more than 150 words     
            if(flag == 1):
                # Thus increment the Document Index ID
                globalIndex+=1


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Too few arguments!"
        print "python crawler.py <start-url-string> <number-of-documents-to-crawl> <results-directory-path>"
    else:

        # Start/seed domain URL, homepage of nytimes
        start = sys.argv[1]

        # Upper limit on the number of URLs which need to be crawled
        urlLimit = sys.argv[2]

        # Path of the directory, where to write the documents
        resultsPath = sys.argv[3]

        # Check for valid path of the directory
        if (os.path.isdir(resultsPath)):
            # Call BFS with homepage of nytimes as root of the bfs tree
            bfs(start, int(urlLimit), resultsPath)
            print "Crawling Finished"
        else:
            print "Invalid Directory Path!"
            print "python crawler.py <start-url-string> <number-of-documents-to-crawl> <results-directory-path>"
        
        
        
    