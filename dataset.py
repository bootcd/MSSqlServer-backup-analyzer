import copy
from db_connect import *


# functions for geting needful data
##################################
#################################

# function returns dictionary with lists of databases
# structured by 'type' of backup (full, journal, increment)

def getDatabaseList(type):
    databaselist = []
    databasedict = {}

    cursor = db_connect(server_name, db_name).cursor()
    cursor.execute("SELECT name FROM sys.databases WHERE name<>'tempdb' and name<>'master' and "
                   "name<>'msdb' and name<>'model'")
    databases = cursor.fetchall()

    for database in databases:
        databaselist.append(database[0])

    for database in databaselist:
        query = "SELECT MAX(media_set_id) FROM msdb.dbo.backupset WHERE type='" + type + "' and database_name='" + database + "';"
        cursor.execute(query)
        media_set_ids = cursor.fetchall()
        if media_set_ids[0][0] is None:
            pass
        else:
            for media_set_id in media_set_ids:
                databasedict.update({database: str(media_set_id[0])})
    return databasedict

# function returns dictionary 'db_backup_dict' with list of dictionaries
# marked with names of database. Inner dictionaries haves 'db_backup_item' = 'needful value'


def getdataitem(backup_items, databaseList):
    db_backup_dict = {}
    cursor = db_connect(server_name, db_name).cursor()

    for key, value in databaseList.items():
        db_backup_item_dict = {}
        database = key
        media_set_id = value
        for backup_item in backup_items:
            if backup_item == "physical_device_name":
                systembasetable = "msdb.dbo.backupmediafamily"
            else:
                systembasetable = "msdb.dbo.backupset"
            query = "SELECT " + backup_item + " FROM " + systembasetable + " WHERE  media_set_id='" + media_set_id + "'; "
            cursor.execute(query)
            dataitems = cursor.fetchall()

            if dataitems[0][0] is None:
                pass
            else:
                for rawdataitem in dataitems:
                    db_backup_item_dict[backup_item] = str(rawdataitem[0])
        db_backup_dict[database] = copy.deepcopy(db_backup_item_dict)

    return db_backup_dict
