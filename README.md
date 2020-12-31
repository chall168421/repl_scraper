# repl_scraper
 A tool to download classroom assignments, student submissions, unit tests etc. from the soon-to-be-deprecated  repl.it classroom.<br>
 
 I discovered today that repl.it have provided an official export feature, so it is probably sensible to use that instead :) A slight waste of time making this - but I had never used Selenium before so useful learning curve perhaps. https://repl.it/classroom-migration
 
 ## How to use?

 Install Selenium Chromedriver: https://chromedriver.chromium.org/getting-started and the pyautogui and BeautifulSoup4 packages.
Run the script, sign into your repl.it account and navigate to the root of your classroom. Let the script do its work - it does not
do this quickly! As repl.it kindly encrypt their HTML content in the browser I had to go down the route of an automated click-copy-paste
to grab the actual student submission code. In order for the window selection to work correctly - please resize your Chrome window so
it fills roughly 50% of your screen - it should be placed on the left hand side.<br>

 
## What does it do?
Downloads the HTML root for each assignment in a repl.it classroom. Creates a .txt file of the assignment brief and a .py file of the
automated unit tests if any. If input/output matching is used instead, it creates a json-style .py file containing the test data. Each
student submission + corresponding feedback (if any) is then automatically 'scraped' (see above) into a separate file within the assignment
directory.<br><br>

 

![alt text](https://github.com/chall168421/repl_scraper/blob/main/Capture.JPG?raw=true)
