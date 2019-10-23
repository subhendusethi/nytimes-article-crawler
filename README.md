Dependencies:

  - Python 2.7.11+
  - BeautifulSoup 4.5.1

### HOT TO EXECUTE


```sh
$ python crawler_usage.py <start-url-string> <number-of-documents-to-crawl> <results-directory-path>

Note:
  <start-url-string> : Root of the BFS tree of article document URLs
  
  <number-of-documents-to-crawl> : Number of article documents to crawl
  
  <results-directory-path> : Result directory path without "/" at the end.
  Here the output of the crawled documents will be stored in this format:
  "DOC"-<ID>-".txt"
```


### EXTRACTED DOCUMENT FORMAT

The format of the retrieved articles files:

Name: 

    DOC_<ID>.txt
Content
:

    URL
    TITLE
    META-KEYWORDS
    DATE
    DOC ID
    CONTENT

### IMPROVEMENTS
Improvements: Add Depth in the BFS routine.
Add more documentation
Add more functionality: Like crawling specific type of content e.g. [music, crime, politics, etc]


License
----
MIT
