import copy
import datetime
from db_connect import *

### vars

now = datetime.datetime.now()


# functions for geting needful data
##################################
#################################

# This function returns lists of user databases (without system databases)

def get_database_list():
    database_list = []

    cursor = db_connect(server_name, db_name).cursor()
    cursor.execute("SELECT name FROM sys.databases WHERE name<>'tempdb' and name<>'master' and "
                   "name<>'msdb' and name<>'model'")
    databases = cursor.fetchall()

    for database in databases:
        database_list.append(database[0])

    return database_list


def get_db_mediaset_id_dict(database_list, backup_type):
    db_mediasetid_dict = {}

    for database in database_list:
        query = "select MAX(m.media_set_id) from msdb.dbo.backupset b full join msdb.dbo.backupmediafamily m on " \
                "b.media_set_id = m.media_set_id where b.database_name = '" + database + "' and m.device_type = '2' " \
                                                                                         "and b.type = '" + \
                backup_type + "' ; "

        cursor = db_connect(server_name, db_name).cursor()
        cursor.execute(query)

        media_set_ids = cursor.fetchall()
        if media_set_ids[0][0] is None:
            pass
        else:
            for media_set_id in media_set_ids:
                db_mediasetid_dict.update({database: str(media_set_id[0])})
    return db_mediasetid_dict


# This func returns dict of maintplans history dictionaries.

def get_maintplan_history_dict():
    maintplans_history_dict = {}
    maintplan_name_id_dict = {}
    subplan_history = {}
    subplans_history_dict = {}
    subplan_errors_list = []
    cursor = db_connect(server_name, db_name).cursor()
    cursor.execute("select name, id from msdb.dbo.sysmaintplan_plans;")
    maintplan_name_ids = cursor.fetchall()

    for maintplan_name_id in maintplan_name_ids:
        plan_name = maintplan_name_id[0]
        plan_id = maintplan_name_id[1]
        maintplan_name_id_dict[plan_name] = plan_id

        subplans_history_dict = {}
        ###########################################

        cursor.execute(
            "select subplan_id, subplan_name from msdb.dbo.sysmaintplan_subplans where plan_id='" + plan_id + "';")

        subplan_id_name = cursor.fetchall()

        for subplan in subplan_id_name:
            subplan_name = str(subplan[1])
            subplan_id = str(subplan[0])

            cursor.execute(
                "select TOP(1) task_detail_id from msdb.dbo.sysmaintplan_log where subplan_id = '" + subplan_id + "' "
                                                                                                                  "order by start_time DESC")
            task_detail_ids = cursor.fetchall()

            for task_detail_id in task_detail_ids:
                cursor.execute("select succeeded, start_time, end_time from msdb.dbo.sysmaintplan_log where "
                               "task_detail_id='" + task_detail_id[0] + "';")
                subplan_succeeded = cursor.fetchall()

                if len(subplan_succeeded) != 0:
                    succeded = str(subplan_succeeded[0][0])
                    subplan_last_date = str(subplan_succeeded[0][1])
                    subplan_last_date_finish = str(subplan_succeeded[0][2])

                    cursor.execute(
                        "select error_message from msdb.dbo.sysmaintplan_logdetail where task_detail_id = '" +
                        task_detail_id[0] + "';")
                    subplan_errors = cursor.fetchall()

                    for i in range(len(subplan_errors)):
                        subplan_error_string = str(subplan_errors[i][0]).split("\r\n")[0]
                        subplan_errors_list.append(subplan_error_string)
                        subplan_errors_string = "".join(subplan_errors_list)

                    if subplan_errors_string == "":
                        subplan_history['status'] = "ok"
                    else:
                        subplan_history['status'] = subplan_errors_string

                    subplan_history['subplan_last_date'] = subplan_last_date
                    subplan_history['subplan_last_date_finish'] = subplan_last_date_finish

                else:
                    subplan_history['status'] = "Не выполняется!"
                    subplan_history['subplan_last_date'] = "Нет данных"
                    subplan_history['subplan_last_date_finish'] = "Нет данных"
                subplans_history_dict[subplan_name] = copy.deepcopy(subplan_history)
        maintplans_history_dict[plan_name] = copy.deepcopy(subplans_history_dict)

    return maintplans_history_dict


# function returns dictionary 'whole_backup_dict' with list of dictionaries
# marked with names of database. Inner dictionaries haves 'db_backup_item' = 'needful value'

def get_whole_backup_dict(backup_items, databaseList):
    whole_backup_dict = {}
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
        whole_backup_dict[database] = copy.deepcopy(db_backup_item_dict)

    return whole_backup_dict
