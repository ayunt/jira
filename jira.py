#!/usr/bin/python
import requests
import json
import sys

SERVER_IP = '54.187.244.122:8080'

if (sys.argv[1] == 'CRITICAL' and sys.argv[2] == 'HARD'):
        headers = {'Content-Type': 'application/json'}
        payload = {
           "fields": {
                "project": {
                        "key": "SKYF"
                        },
                "summary": "Mysql CRITICAL issue!!! Python script",
                "description": "Dear Customer,\n Our monitoring system has noticed that MySQL service is down",
                "issuetype": {
                        "name": "Incident"
                                }
                        }
                   }
        url = 'http://{}/rest/api/2/issue/'.format(SERVER_IP)
        json_response = requests.post(
            url,
            auth=('nagios', 'nagios'),
            data=json.dumps(payload),
            headers=headers
            )
        decoded = json_response.json()
        MySQL_ID = decoded.get('key')
        # Write the ticket number to the file. This value will be used to close the ticket
        f = open("/home/ayunt/mysql_id.txt", "w")
        f.write(MySQL_ID)
        f.close()
        # Write this incident to the log file with Nagios parameters
        f = open("/home/ayunt/jira.log", "a")
        args = sys.argv[1:]
        args = " ".join(str(x) for x in args)
        f.write("{}\nThe ticket {} has been created\n{:*^40}\n".format(args, MySQL_ID, ''))
        f.close()
        sys.exit()
else:
    if (sys.argv[1] == 'OK' and sys.argv[2] == 'HARD'):
        f = open("/home/ayunt/mysql_id.txt", "r")
        MySQL_ID = f.read()
        f.close()
        headers = {'Content-Type': 'application/json'}
        mysql_up = {
            "update": {
                "comment": [
                   {
                    "add": {
                        "body": "Dear Customer,\n We have fixed the MySQL problem. Please check and let us know"
                           }
                    }
                          ]
                        },
                "fields": {
                    "resolution": {
                        "name": "Done"
                                  }
                           },
                "transition": {
                 "id": "5"
                        }
        }
        url = 'http://{}/rest/api/2/issue/{}/transitions'.format(SERVER_IP, MySQL_ID)
        closeResponce = requests.post(
            url,
            auth=('nagios', 'nagios'),
            data=json.dumps(mysql_up),
            headers=headers
            )
        # Read the ticket number from the file in order to close the corresponding ticket
        f = open("/home/ayunt/jira.log", "a")
        args = sys.argv[1:]
        args = " ".join(str(x) for x in args)
        f.write("{}\nThe ticket {} has been closed\n{:*^40}\n".format(args, MySQL_ID, ''))
        f.close()
        sys.exit()

