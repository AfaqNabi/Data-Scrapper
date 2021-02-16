## Data Scraper
This Script will take your Yahoo watchlist and collect 5 min data on it 

## Installing
To use this bot
1. Clone the repo
2. cd into the repo
3. run ```./depen.sh``` in the terminal to download all dependencies
4. ```depen.sh``` will ask for email and password for yahoo
+ their might be issues with permissions simply do ```chmod u+x depen.sh``` and run the previous command again
5. the email and password will be securly stored on your OS through keyring
6. go to https://chromedriver.chromium.org/downloads and download the chrome driver that corresponds to the chrome version installed on your computer
7. open ```exec.sh``` in an IDE copy and paste your absolute path to the chrome driver in place of ```path/to/chrome/driver``` 
8. replace ```version``` in ```Chrome/version``` with your corresponding version of chrome ex: ```Chrome/88.0.4324.150```
9. back in the terminal run the command ```exec.sh``` to run the bot
+ their might be issues with permissions simply do ```chmod u+x exec.sh``` and run the previous command again
10. the webscraping is done headlessly (it wont actually open a chrome browser)
