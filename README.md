Musescore Sheetmusic Scraper
============================

Summary
--------
A program that querys musescore pages pulling all sheet music on the page as svgs or pngs then converts the images to pdfs and merges them. The program uses selenium to avoid anti-scraping measures on the page.

Requirements
-------------
+ Python already installed: https://www.python.org/downloads/  
+ Windows

How to use
-----------
After downloading, run setup.bat (setup.bat runs multiple pip commands to install necessary dependencies). After setup.bat is finished, simply run scraper.py and a UI will open allowing you to enter the url of the song you would like to download (will only work on free scores) (ex url: https://musescore.com/httpssoundcloud_comneverborn_music/scores/7216794) and a name to save the final pdf under. After clicking download, the UI will close and the scraper will run. Multiple errors will likely show that aren't important. Once your music is downloaded it can be found within the Music folder. To print, you may have to go to extra options and select fit to page as the pdfs may not fit to page.

Credits
-------
Center function for tkinter: https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter  