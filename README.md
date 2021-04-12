# website-analyzer
Python project takes URL as a comman-line parameter to extract the title, html version, distinct external links (reachable and unreachable), and check for login form existance in
the HTML of the webpage.

## Input
Provide a URL for the web page as a command-line parameter.

## Output (Print on Console): 
- Title
- HTML Version
- Login Form Availability
- Total External links
- Reachable External links
- Total Internal links
- Total Available Links

## Code Structure
Two Classes are implemented Scrapper and MyScrapper. Scrapper class is an abstract class with all the basic functionalities that scrapper must contain. Whereas, MyScrapper 
is extended from it and define all the functionalities for the abstract class. In the main class the object of MyScrapper class has to be built providing URL and 
max_crawl_webpages_limit as contructor parameters. Once it is done, you can easily perform all the required functionalities.

## Requirements
All the required dependencies and libraries are provided in the requirements.txt file. 

## How to Run
Once you are done with the setup successfully, you just have to open the directory in the command line and run the command 'python main.py -u <url>'. You can also run the 
command 'python main.py -h' for help.

## Challenges
Scrapping and HTML Parsing

## Module/Library Functionality:
If I have to make a library out of the project then just have to implement an expose function in MyScrapper class which calls the self functions and do all the stuff on its own.


