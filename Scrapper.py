from abc import ABC


class Scrapper(ABC):

    def is_reachable_url(self, url):
        pass

    def is_valid_url(self, url):
        pass

    def set_html(self):
        pass

    def get_website_title(self):
        pass

    def get_html_version(self):
        pass

    def contains_login_form(self):
        pass

    def get_all_website_links(self, url):
        pass

    def crawl(self, url):
        pass
