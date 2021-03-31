import gmail, json, emailDatabase, datetime


def ruleActions(serv, msgId, labl, actn):
    """
    Function :      Simple helper function to run the rules action.
    Arguments :     serv - GMAIL services API
                    msgID - The msgid for which the action to be taken
                    labl - label change for the action, eg: removeLabelIds(which is an parameter for gmail api to remove the labels)
                    actn - What action needs to be take with the laebl.
    Return Values : Returns success.
    """
    try:
        a = serv.users().messages().modify(userId='me', id=msgId, body={labl: [actn]}).execute()
        return "success"
    except Exception as e:
        print("ruleActions : ", e)

def rulesProcess(rows, rules, ser):
    """
        Function :      The below set of lines process the message with all the rules mentioned in the rules.json file one by one
        Arguments :     rows - DB rows to process the rules.
                        rules - the josn object from rules.json file which has the rules to be processed.
                        ser - GMAIL services API
        Return Values : No return values
        """
    try:
        for i in rows:
            From = i[2]
            Date = (datetime.datetime.fromisoformat(i[0])).date()
            Days = str((datetime.datetime.now().date() - Date).days)
            for rule in rules["rules"]:  # Loops through each and every rule in the rules.json and resolves the action mentioned.
                conditionCount = len(rule["conditions"])  # This variable counts that all the condition has met or not for all/any rule constraint to resolve
                for condition in rule["conditions"]:
                    field_name = condition["Fieldname"]
                    value = condition["Value"]
                    operator = condition["constraint"]
                    """The below line is a dynamic line to compare and do operations for the rules to process
                        example : eval("tenmiles.com" in "abcpvtltd@gmail.com")"""
                    if eval('"' + value + '"' + operator + '"' + eval(field_name) + '"'):
                        conditionCount -= 1
                    """Checks all or any rules processed and does action as per the rules."""
                    if rule["allow"] == "all" and conditionCount == 0:
                        for label, action in rule["actions"][0].items():
                            print(ruleActions(ser, i[3], label, action), "Rule Processed(msg[id]) : " + str(i[3]))

                    elif rule["allow"] == "any" and conditionCount < len(rule["conditions"]):
                        for label, action in rule["actions"][0].items():
                            print(ruleActions(ser, i[3], label, action), "Rule Processed(msg[id]) : " + str(i[3]))
                        break
    except Exception as e:
        print("rulesProcess : ", e)

if __name__ == '__main__':
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.modify'
    ]
    # Creating GMAIL service credentials.
    service = gmail.gmailCredential(SCOPES)
    # Opening the rules.josn file and creating as json object
    with open("rules.json") as json_file:
        rulesData = json.load(json_file)
    # Creating database connection
    DBcn, DBcr = emailDatabase.createDBconnection()
    # Reads the email from the database
    DBrows = emailDatabase.readTable(DBcr)
    # Process the rules as per the rules file.
    rulesProcess(DBrows, rulesData, service)
    print("Success - Process Completed.")