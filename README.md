
# Twitter Sentiment Analysis



## How to run application

### Step: 1
* Create __Vitrual Environment__
* Using ` python -m venv YourVirtualEnvironmentName `
* Ex: ` python -m venv venv `

### Step: 2
* run __activate.bat__ file to activate virtual environment
* `venv/Scripts/activate.bat`

### Step: 3
* Fork the repo or download the repo
* Place it where the venv folder is present
* Ex: Dir Structure
  * MyFolder
    * NLPApplication
    * venv
    * reuirements.txt
    * README.txt

* Install all dependencies by using the following command
* ` pip install -r requirements.txt ` 
* change dir to __NLPApplication__
* Change values of variables in __NLPApplication\sentiment_analysis\twitter_data\twitter_credentials.py__ file to get data from twitter and store it on mongodb
* Then run the local server
* ` python manage.py runserver `
* link -> [localhost:8000](localhost:8000)
