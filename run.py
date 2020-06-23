# Program level import
from sys import argv
from dataset import *
from analitics import *
from request_lib import *


def run(arg1, arg2):
    # System level import
    import json
    import requests

    ####### VARIABLES ########
    client_name = argv[1]
    backup_type = argv[2]
    backup_item_set = ('physical_device_name',
                       'backup_start_date',
                       'backup_finish_date',
                       'compressed_backup_size',
                       'backup_size',
                       'recovery_model',
                       'media_set_id')

    # Getting user database list (without system databases)
    user_db_list = get_database_list()

    # Getting dict with {database: mediaset_id}
    db_mediasetid_dict = get_db_mediaset_id_dict(user_db_list, backup_type)

    # getting dictionary {database: {backup_item: data}
    backup_bases_item_dict = get_whole_backup_dict(backup_item_set, db_mediasetid_dict)

    #### JSON Works  - truncate file ####

    # Open the output file for json output
    json_output_file = open("json_output.txt", "w")

    # Purge the output file
    json_output_file.truncate()

    # For each database and it's backup data...
    for key, value in backup_bases_item_dict.items():
        # ...getting dictionary with metadata status
        metadata_status = get_metadata_status(value, backup_item_set)

        # ...getting dictionary with backup parameters and it's values
        base_backup_stats = get_base_backup_stats(value)

        # Getting dictionary with FINAL data for future POST request to WEB server
        post_request_data_dict = get_postrequest_data(key, metadata_status, base_backup_stats, backup_type, client_name)

        # POST request to WEB server
        requests.post("http://zabbix.ekord.ru/datareceiver.php", data=post_request_data_dict)

        print(post_request_data_dict)

        # Write data to JSON file
        json_output_file.write(json.dumps(post_request_data_dict) + "\n")

    # Close JSON output file
    json_output_file.close()

    # Getting dictionary with maintplans history {maintplan_name: maintplan_data{parameter: value}}
    maintplan_history = get_maintplan_history_dict()

    if backup_type == "L":
        # For each maintplan and it's data...
        for maintplan_name, subplans in maintplan_history.items():
            for subplan_name, subplan_history in subplans.items():
                print(subplan_name)

                # ... POST request to WEB server
                requests.post("http://10.1.0.43/zabbix/maintplan_status.php", data={'plan_name': maintplan_name,
                                                                                    'subplan_name': subplan_name,
                                                                                    'subplan_status': subplan_history[
                                                                                        'status'],
                                                                                    'subplan_last_date':
                                                                                        subplan_history[
                                                                                            'subplan_last_date'],
                                                                                    'client_name': client_name,
                                                                                    'subplan_last_date_finish':
                                                                                        subplan_history[
                                                                                            'subplan_last_date_finish']})
