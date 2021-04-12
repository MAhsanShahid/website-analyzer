from urllib.parse import urlparse, urljoin

import colorama
import requests
from bs4 import BeautifulSoup

from Scrapper import Scrapper


class MyScrapper(Scrapper):
    url = ''
    max_webpages_crawl_limit = 0
    web_page_data = ''
    web_page_title = ''
    web_page_html_v = ''

    colorama.init()
    GREEN = colorama.Fore.GREEN
    GRAY = colorama.Fore.LIGHTBLACK_EX
    RESET = colorama.Fore.RESET

    # initialize the set of links (unique links)
    internal_urls = set()
    external_urls = set()
    total_webpages_visited = 0
    reachable_external_urls = 0

    def __init__(self, url, max_webpages_crawl_limit):
        self.url = url
        self.max_webpages_crawl_limit = max_webpages_crawl_limit

    def is_reachable_url(self, url):
        url_status_code = requests.get(url).status_code
        if url_status_code == 200:
            return True
        return False

    def is_valid_url(self, url):
        # Checks whether `url` is a valid URL.
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def set_html(self):
        self.web_page_data = str(BeautifulSoup(requests.get(self.url).content, "html.parser"))
        # web_page_data = url_request.urlopen(self.url).read()
        # self.web_page_data = str(web_page_data)
        # return self.web_page_data

    def get_website_title(self):
        if self.web_page_data != '':
            if '<title' in str(self.web_page_data):
                self.web_page_title = self.web_page_data.split('<title')[1].split('</title>')[0].split('>')[1]
            return self.web_page_title
        else:
            return 'No HTML Found for Webpage!'

    def get_html_version(self):
        html_v = self.web_page_data.split('<')[1].split('>')[0]
        if html_v.lower() == '!doctype html':
            self.web_page_html_v = 'HTML5'
            return self.web_page_html_v
        else:
            self.web_page_html_v = 'HTML'
            return self.web_page_html_v

    def contains_login_form(self):
        password_fields_count = 0
        forms = self.web_page_data.split('<form')
        for each_form in forms:
            input_tags = each_form.split("<input")
            for each_input in input_tags:
                if 'type="password"' in each_input:
                    password_fields_count += 1
        if password_fields_count == 0:
            return 'No Login Form Found'
        elif password_fields_count == 1:
            return 'Login Form Found'
        else:
            return 'May be a SignUp Form Found'

    def get_all_website_links(self, url):
        # Returns all URLs that is found on `url` in which it belongs to the same website
        # all URLs of `url`
        urls = set()
        # domain name of the URL without the protocol
        domain_name = urlparse(url).netloc
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                # href empty tag
                continue
            # join the URL if it's relative (not absolute link)
            href = urljoin(url, href)
            parsed_href = urlparse(href)
            # remove URL GET parameters, URL fragments, etc.
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if not self.is_valid_url(href):
                # not a valid URL
                continue
            if href in self.external_urls:
                # already in the set
                continue
            if domain_name in href:
                # internal link
                if href not in self.internal_urls:
                    # print(f"{self.GREEN}[*] Internal link: {href}{self.RESET}")
                    self.internal_urls.add(href)
                continue
            # external link
            # print(f"{self.GRAY}[!] External link: {href}{self.RESET}")
            urls.add(href)
            self.external_urls.add(href)
            is_reachable = self.is_reachable_url(href)
            if is_reachable:
                self.reachable_external_urls += 1

        return urls

    def crawl(self, url):
        # Crawls a web page and extracts all links.
        # You'll find all links in `external_urls` and `internal_urls`.
        #
        # global total_urls_visited
        self.total_webpages_visited += 1
        links = self.get_all_website_links(url)
        for link in links:
            if self.total_webpages_visited >= self.max_webpages_crawl_limit:
                break
            self.crawl(link)
        return self.total_webpages_visited, self.reachable_external_urls, len(self.external_urls), len(
            self.internal_urls)
