Dependencies:

  - Python 2.7.11+
  - BeautifulSoup 4.5.1
  - urllib2 2.7

### HOT TO EXECUTE


```sh
$ python crawler.py <start-url-string> <number-of-documents-to-crawl> <results-directory-path>

Note:
	<start-url-string> : Root of the BFS tree of article document URLs
	<number-of-documents-to-crawl> : Number of article documents to crawl
	<results-directory-path> : Result directory path without "/" at the end
```

For production environments...

```sh
$ npm install --production
$ npm run predeploy
$ NODE_ENV=production node app
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
Improvements: Add Depth in the BFS routine



License
----
MIT
