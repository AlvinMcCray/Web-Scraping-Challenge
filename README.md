# Mission-To-Mars-Web-Scraping-App
A web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.

## Files:

* mission_to_mars.ipynb ---> Jupyter Notebook that houses original scrape code for entire project.

* scrape_mars.py ---> Python File that contains two functions; init_browser() (to initiate browser via chromedriver) and scrape() (to perform scrape of all pages taken from original Jupyter Notebook).

* mars_app.py ---> Python/Flask App that utilizes scrape() function from scrape_mars.py to update mars_app DB collection in MongoDB and load as webpage from index.html.

* templates(Folder) ---> HTML webpage used for Mission to Mars that displays the information from our web application scrape.

* Screenshots(Folder) ---> Four total JPG images of the Mission to Mars web HTML web page app.

## How to use:

In order to run application, please navigate to directory via console. Run mars_app.py as Python file.
