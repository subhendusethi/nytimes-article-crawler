# -----------------------------------------#
#         NY-TIMES WORD CORPUS CRAWLER     #
#                                          #
# Subhendu Sethi (CS13B1027@iith.ac.in)    #
# Rahul Kumar (ES13B1018@iith.ac.in)       #
# Prashant Dewangan (CS13B1025@iith.ac.in) #
# -----------------------------------------#

import sys
import os

from crawler import nytimescrawler

if __name__ == "__main__":
    crawler = nytimescrawler.Crawler()
    if len(sys.argv) < 4:
        print("Too few arguments!")
        print("python crawler_usage.py <start-url-string> <number-of-documents-to-crawl> <results-directory-path>")
    else:
        # TODO Add command line parser

        # Start/seed domain URL
        start = sys.argv[1]

        # Upper limit on the number of URLs which need to be crawled
        urlLimit = sys.argv[2]

        # Path of the directory, where to write the documents
        resultsPath = sys.argv[3]

        # Check for valid path of the directory
        if (os.path.isdir(resultsPath)):
            # Call BFS with homepage of nytimes as root of the bfs tree
            crawler.crawl(start, int(urlLimit), resultsPath)
        else:
            print("Invalid Directory Path!")
            print("python crawler_usage.py <start-url-string> <number-of-documents-to-crawl> <results-directory-path>")
        
        
        
    