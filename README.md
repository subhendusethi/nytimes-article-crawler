---------------------------------------------------------------------------------------------------------
DEPENDENCIES:

Python 2.7.11+
BeautifulSoup 4.5.1
urllib2 2.7

---------------------------------------------------------------------------------------------------------
HOW TO EXECUTE:
	python crawler.py <start-url-string> <number-of-documents-to-crawl> <results-directory-path>

	Note:
		<start-url-string> : Root of the BFS tree of article document URLs
		<number-of-documents-to-crawl> : Number of article documents to crawl
		<results-directory-path> : Result directory path without "/" at the end
---------------------------------------------------------------------------------------------------------
Improvements:
ADD Depth in the DFS routine