import mysql.connector

'''config = {
    'host':'srv1100.hstgr.io',
    'port':'3306',
    'user':'u317157586_cc_asg',
    'password':'$:XPL7VrH6',
    'database':'u317157586_cc_asg'
}'''


# config = {
#     'host':'cloud-assignment-1.database.windows.net',
#     'port':'1433',
#     'user':'ommair-01',
#     'password':'Omm@ir510219900',
#     'database':'user_database'
# }

config={'host':'127.0.0.1',
        'user':'root', 'password':'Omm@ir510219900',
                              
        'database':'cloud_assignment'}

# Establish a connection
connection = mysql.connector.connect(**config)
cur = connection.cursor()
