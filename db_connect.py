import pyodbc

# vars

db_name = "msdb"


server_name = "116.202.79.250"
username = "sa"
password = "2-uFaVcV239869"


# function returns "connection" object for MS SQL Server connect

def db_connect(server, database_name):
    connection = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database_name + ';' + 'UID=' + username + ';PWD=' + password + ';')

    return connection
