import copy
import datetime
from db_connect import *


### vars

now = datetime.datetime.now()

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
        query = "select MAX(m.media_set_id) from msdb.dbo.backupset b full join msdb.dbo.backupmediafamily m on " \
                "b.media_set_id = m.media_set_id where b.database_name = '" + database + "' " \
                                                                                         "and m.device_type = '2' and " \
                                                                                         "b.type = '" + type + "' "
        cursor.execute(query)

        media_set_ids = cursor.fetchall()
        if media_set_ids[0][0] is None:
            pass
        else:
            for media_set_id in media_set_ids:
                databasedict.update({database: str(media_set_id[0])})
    return databasedict


def get_maintplan_history():
    maintplan_name_id_dict = {}
    maintplan_history = {}
    maintplans_history = {}
    maintplan_errors_list = []
    cursor = db_connect(server_name, db_name).cursor()
    cursor.execute("select name, id from msdb.dbo.sysmaintplan_plans;")
    maintplan_name_ids = cursor.fetchall()
    for maintplan_name_id in maintplan_name_ids:
        plan_name = maintplan_name_id[0]
        plan_id = maintplan_name_id[1]
        maintplan_name_id_dict[plan_name] = plan_id
        cursor.execute("select TOP(1) succeeded, task_detail_id, start_time, end_time from msdb.dbo.sysmaintplan_log where plan_id='" + plan_id + "' order by  start_time DESC;")
        maintplan_succeeded = cursor.fetchall()
        if len(maintplan_succeeded) !=0:
            plan_last_date = str(maintplan_succeeded[0][2])
            plan_last_date_finish = str(maintplan_succeeded[0][3])
            print("plan_last_date", plan_last_date)
            if maintplan_succeeded[0][0] == True:
                maintplan_history['status'] = "ok"
            else:
                task_detail_id = maintplan_succeeded[0][1]
                cursor.execute("select error_message from msdb.dbo.sysmaintplan_logdetail where task_detail_id = '" + task_detail_id + "';")
                # cursor.execute("select error_message from msdb.dbo.sysmaintplan_logdetail where task_detail_id = '75E82C0F-19C6-48FE-8AB3-A43EBAE4B72E';")
                maintplan_errors = cursor.fetchall()
                maintplan_error_string = str(maintplan_errors[2][0]).split("\r\n")[0]
                maintplan_errors_list.append(maintplan_error_string)
                maintplan_errors_string = "\n".join(maintplan_errors_list)
                maintplan_history['status'] = maintplan_errors_string
            maintplan_history['plan_last_date'] = plan_last_date
            maintplan_history['plan_last_date_finish'] = plan_last_date_finish

        else:
            maintplan_history['status'] = "Не выполняется!"
            maintplan_history['plan_last_date'] = str(now)
            maintplan_history['plan_last_date_finish'] = str(now)
            pass
        maintplans_history[plan_name] = copy.deepcopy(maintplan_history)
    return maintplans_history

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
