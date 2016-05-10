#!/usr/bin/python
import requests
import json
import sys

MySQL_ID = 'SKYF-14'

if (sys.argv[1] == 'CRITICAL' and sys.argv[2] == 'HARD'):
        headers = {'Content-Type': 'application/json'}
        payload = {

       "fields":{

                "project":{

                        "key":"SKYF"

                        },

                "summary":"Mysql CRITICAL issue!!! Python script",

                "description":"Dear Customer,\n Our monitoring system has noticed that MySQL service is down",

                "issuetype":{

                        "name":"Incident"

                                }

                        }

}
        #json_response=requests.post('http://{}/rest/api/2/issue/.format(SERVER_IP)', auth=('nagios', 'nagios'), data=json.dumps(payload), headers=headers)
        #decoded = json_response.json()       
        #MySQL_ID=decoded.get('key')
        #f = open("/home/ayunt/mysql_id.txt","w")
        #f.write(MySQL_ID)
        #f.close()
        f = open("/home/ayunt/jira.log","a")
        #f.writelines("%s " % l for l in sys.argv[1:])
        args = str(sys.argv[1:])
        f.write("%s\n The ticket %s has been created\n" % (args, MySQL_ID))
        f.close()
        #print MySQL_ID
        sys.exit (1)    
else:
    if (sys.argv[1] == 'OK' and sys.argv[2] == 'HARD'):
        f = open("/home/ayunt/mysql_id.txt","r")
        MySQL_ID=f.read()
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
        closeResponce=requests.post('http://{}/rest/api/2/issue/{}/transitions'.format(SERVER_IP,MySQL_ID), auth=('nagios', 'nagios'),data=json.dumps(mysql_up), headers=headers)
        #print MySQL_ID
        f = open("/home/ayunt/jira.log","a")
        #f.writelines("%s " % l for l in sys.argv[1:])
        args = str(sys.argv[1:])
        f.write("%s\n The ticket %s has been closed\n" % (args, MySQL_ID))
        f.close()
        sys.exit (1)
