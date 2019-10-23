from bs4 import BeautifulSoup
from sys import stdout
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import re
from collections import deque
import logging

# TODO: Add Checkstyle PEP8
# TODO: Add Unit Test Cases
class Crawler():
    def __init__(self, log_level_info=False, threshold_words=150):
        self.__url_queue = deque()
        self.__url_map = {}
        self.__threshold_words = threshold_words
        self.__logger = self.__initialize_logger(log_level_info)

    def __initialize_logger(self, log_level_info):
        logger = logging.getLogger(__name__)
        logging_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler = logging.StreamHandler(stdout)
        stream_handler.setFormatter(logging_format)
        logger.addHandler(stream_handler)
        if log_level_info:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.ERROR)
        return logger

    # To discard irrelevant URLs and remove extra parts from the URLs
    def __remove_excess(self, url_list):
        final_list = []

        # Remove the extra parts from the URL that comes after ".html"
        for url in url_list:
            index = url.find(".html")
            parsed_url = url[:index+5]
            # If URL doesn't contain ".html"
            if index == -1:
                continue
            else:
                # Append the new URL after removing extra part
                final_list.append(parsed_url)

        # Empty "url_list"
        del url_list[:]
        url_list = []

        # Check for seed domain and discard irrelevant URLs
        for url in final_list:
            if(url.startswith("http://www.nytimes.com") or url.startswith("https://www.nytimes.com")):
                # Append URLs which contain "www.nytimes.com"
                self.__logger.info('Appending parsed url {}'.format(url))
                url_list.append(url)

        # Return the final list of URLs
        return url_list

    # Extract all the relevant URLs
    def __extract_href(self, data_received):
        href_links = []

        # Use "BeautifulSoup" function to parse on the HTML data received
        soup = BeautifulSoup(data_received, "html.parser")
        # Find all "a" tags where href is present
        for itHref in soup.findAll('a', href = True):
            # If "href = True", append the URL to href_links
            href_links.append(itHref.get('href'))
        # Return all URLs
        return href_links

    # Parse the data received and get TITLE, CONTENT, DATE, META-KEYWORDS
    # Create Documents with DOC IDs
    def __parse_data(self, data_received, url, current_index, results_path):
        if current_index == 0:
            return True

        # Use "BeautifulSoup" function to parse on the HTML data received
        soup = BeautifulSoup(data_received, "html.parser")

        # Extract content
        # Get paragraph elements from all div's having "class = StoryBodyCompanionColumn"
        # StoryBodyCompanionColumn is NY TIMES class that contains the article body
        body = soup.find('div', {'class' : 'StoryBodyCompanionColumn'})

        finalContent = ""
        numberOfWords = 0

        if body != None:
            for itContent in soup.findAll('p'):
                if itContent == None:
                    continue
                content = itContent.getText()
                # Remove newlines
                content = re.sub(r"\n+", " ", content)
                numberOfWords += len(content.split())
                finalContent += content
        else:
            return False

        if numberOfWords >= self.__threshold_words:
            # Open file with name as Document ID
            fileName = "DOC_" + str(current_index) + ".txt"
            file = open(results_path + "/" + fileName, "w")

            # Write URL in the File
            file.write(url + '\n')

            self.__parse_url_title_from_content(soup, file)
            self.__parse_webpage_meta_from_content(soup, file)
            self.__parse_webpage_date_from_content(soup, file)

            # Write DOCUMENT ID
            file.write(str(current_index) + "\n")

            # Write CONTENT
            file.write(finalContent)
            file.close()

            return True
        else:
            return False

    def __parse_url_title_from_content(self, soup, file):
        # Get TITLE by crawling through the HTML
        title = soup.find('head')
        if title != None:
            title = title.find('title')
            if title != None:
                # If "title" found, get text and write the text in the file
                title = title.getText()
                file.write(title + "\n")
            else:
                # Else write "TITLE NOT FOUND"
                file.write("TITLE NOT FOUND\n")

    def __parse_webpage_meta_from_content(self, soup, file):
        # Get META-KEYWORD and write it into the file
        meta = soup.find('meta', {'name' : 'keywords'})
        if(meta != None):
            meta = meta.get('content')
            file.write(meta + "\n")
        else:
            file.write("META-KEYWORDS NOT FOUND\n")

    def __parse_webpage_date_from_content(self, soup, file):
        # Get DATE and write it into the file
        date = soup.find('li',{'class' : 'date'})
        if(date != None):
            date = date.getText()
            file.write(date + "\n")
        else:
            date = soup.find('meta', {'name' : 'DISPLAYDATE'})
            if date != None:
                date = date.get('content')
                if date != None:
                    file.write(date + "\n")
                else:
                    file.write("DATE NOT FOUND\n")

    def __crawl_website(self, url, current_index, results_path):
        href_links = []
        flag = False
        # Get all the data of the current HTML page
        try:
            self.__logger.info('Crawling URL {} ::: Current Crawl Index {}.'.format(url, current_index))

            request = urllib2.urlopen(url)
            data_received = request.read()

            # Call parseData() to extract data, Content, meta-keyword, title, date
            flag = self.__parse_data(data_received, url, current_index, results_path)

            # Extract links from the page
            href_links = self.__extract_href(data_received)

            # Remove irrelevant URLs and extra parts from the URLs
            href_links = self.__remove_excess(href_links)
        except Exception :
            self.__logger.exception('Error occured while crawling a given URL')
            pass

        # returns list of article links extracted from "url" and flag if new Document was created

        return (href_links, flag)

    ''' 
        Given: 
        a) start_url : Entry point for the bfs routine to start crawling nytimes.
        b) url_limit : Integer denoting the number of url's to be crawled upon(with certain criteria)
                      before the halting.
        c) results_path : directory path to stored the parsed documents.
    '''
    def __bfs(self, start_url, url_limit, results_path):
        global_crawl_index = 0
        self.__url_queue.append(start_url)
        while global_crawl_index != url_limit+1:
            # If we reach a stage where we cannot generate new links from the bfs tree of url
            if len(self.__url_queue) == 0:
                self.__logger.INFO("urlQueue size turns ZERO")
                break
            url = self.__url_queue.popleft()
            if url not in self.__url_map:
                # Mark url as visited
                self.__url_map[url] = True

                # Assign unique DOCUMENT_ID to the document of the link
                current_index = global_crawl_index
                hrefList, should_increment_crawler_index = self.__crawl_website(url, current_index, results_path)

                # Add new links to the Queue
                self.__url_queue.extend(hrefList)

                # Flag will be 1 only if the generated document from "url" has content more than 150 words
                if should_increment_crawler_index:
                    # Thus increment the Document Index ID
                    global_crawl_index += 1
    def crawl(self, start, url_limit, results_path):
        self.__url_queue = deque()
        self.__url_map = {}
        self.__bfs(start, url_limit, results_path)