# scratchy
Scratchy is a Python web scraper designed to automate internal url scraping and the sitemap creation process.

## Table of Contents

- [Features](#features)
- [Files](#files)
- [Contact](#contact)

## Features

- **Internal Scraping**: Automates the gathering of internal links on a domain. Supports limits to the amount of urls scraped
- **Sitemap Creation**: Automates the creation of .txt and .xml sitemaps. Supports the automation of writing the links scraped to the desired sitemap format
- **Url Cleaning**: Cleans urls and provides functionality to determine if two links are part of the same domain
- **Unique File Creation**: Manages the creation of uniquely named files
- **HTML Parsing**: Manages the parsing of html content to get absolute internal links

## Files

### Web Scraping
#### scratchy.py
``python from scratchy import *``  
Automates the scraping of internal links in a domain starting at a specified url. Automates the generation of sitemaps with the urls scraped.

### Sitemap Management
#### sitemap.py
``python from sitemap import *``  
Manages the creation of sitemaps in .txt or .xml format.

### Soup Management
#### soup.py
``python from soup import *``  
Manages the parsing of absolute urls from bs4.BeautifulSoup objects.

### Url Management
#### urlutil.py
``python from urlutil import *``  
Manages the cleaning of urls. Provides functionality to determine if two urls belong to the same domain.

### File Management
#### fileutil.py
``python from fileutil import *``  
Manages the creation of uniquely named files. The created files follow the format of {filename}({number}).{extension}.  
**For example**, new_file(1).txt will be created if new_file.txt already exists.

## Contact

For questions, feedback, or sending of cute cat pictures, reach me at:

- **Adam O'Regan**
Email: [adamoregan457@gmail.com](mailto:adamoregan457@gmail.com)  
Github: [adamoregan](https://github.com/adamoregan)  
LinkedIn: [adamoregan457](https://www.linkedin.com/in/adamoregan457)  
