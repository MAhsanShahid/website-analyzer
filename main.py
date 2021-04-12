import getopt
import sys

from MyScrapper import MyScrapper


def get_args(argv):
    url = ''
    opts, args = getopt.getopt(argv, "hu:", ["url="])
    for opt, arg in opts:
        if opt == '-h':
            url = 'main.py -u <url>'
            print(url)
            sys.exit(2)
        elif opt in ("-u", "--url"):
            url = arg
    # print('URL is ', url)
    return url


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    URL = get_args(sys.argv[1:])
    if URL:
        max_webpages_crawl_limit = 1
        myScrapper = MyScrapper(URL, max_webpages_crawl_limit)
        is_valid_url = myScrapper.is_valid_url(URL)
        is_reachable_url = myScrapper.is_reachable_url(URL)
        # print(is_reachable_url, is_valid_url)
        if is_valid_url and is_reachable_url:
            print('Loading...')
            myScrapper.set_html()
            title = myScrapper.get_website_title()
            html_v = myScrapper.get_html_version()
            contains_login_form = myScrapper.contains_login_form()
            total_webpages_visited, reachable_external_urls_count, external_urls_count, internal_urls_count = myScrapper.crawl(URL)
            print('Title: ', title)
            print('HTML Version: ', html_v)
            print('Login Form Availability: ', contains_login_form)
            print("Total External links:", external_urls_count)
            print("Reachable External links:", reachable_external_urls_count)
            print("Total Internal links:", internal_urls_count)
            print("Total Available Links:", external_urls_count + internal_urls_count)
            # print("Total Webpages Crawled:", total_webpages_visited)
        else:
            print('Webpage Not Reachable or Invalid URL')
