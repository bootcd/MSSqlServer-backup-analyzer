import pyodbc

# vars
drivers = [item for item in pyodbc.drivers()]
driver = drivers[-1]
print("driver:{}".format(driver))

db_name = "msdb"


server_name = ""
username = ""
password = ""


# function returns "connection" object for MS SQL Server connect

def db_connect(server, database_name):
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database_name + ';' + 'UID=' + username + ';PWD=' + password + ';')

    return connection
