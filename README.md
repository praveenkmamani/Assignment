This is an interview assignmet project which is a standalone python script to fetch mails from gmail using GMAIL API and process rules mentioned in rules.json file.

Please follow the below steps for successful execution of this script.

1. Run the below command and the install the required modules.
  ```pip install -r requirements.txt```

2. Enable the [GMAIL](https://developers.google.com/gmail/api/quickstart/python) API and place the credentials.json file in the project folder

3. Run the below command which will get the mails from GMAIL, creates a sqlite3 database (emails.db), stores the email in GMAIL table and process the rules as per rules.json.
  ```python gmail.py```
