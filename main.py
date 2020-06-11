import json

import requests

from sys import argv

from dataset import *

from analitics import *

from request_lib import *

# vars

backuptypes = {'D': "Полный", 'L': "Журнал Транзакций", 'I': "Разностный"}
backup_item_list = ['physical_device_name', 'backup_start_date', 'backup_finish_date', 'compressed_backup_size',
                    'backup_size',
                    'recovery_model', 'media_set_id']
client_name = argv[1]

# constructing lists of databases that haves various types of backups (full, journal, increment)
# !!!!! rewrite this shit to normal function with returns by 'type' !!!!!

for backuptype in backuptypes.keys():
    if backuptype == 'D':
        db_with_full_backup_list = getDatabaseList(backuptype)
    if backuptype == 'L':
        db_with_journal_backup_list = getDatabaseList(backuptype)
    if backuptype == 'I':
        db_with_inc_backup_list = getDatabaseList(backuptype)

# getting dictionaries with needful data

full_backup_bases = getdataitem(backup_item_list, db_with_full_backup_list)
journal_backup_bases = getdataitem(backup_item_list, db_with_journal_backup_list)
inc_backup_bases = getdataitem(backup_item_list, db_with_inc_backup_list)

#### JSON Works  - truncate file ####

# Open the output file for json output
json_output_file = open("json_output.txt", "w")

# Purge the output file
json_output_file.truncate()

for key, value in full_backup_bases.items():
    metadata_status = get_metadata_status(value, backup_item_list)
    base_backup_stats = get_base_backup_stats(value)

    post_data = get_postrequest_data(key, metadata_status, base_backup_stats, 'D', client_name)
    requests.post("http://zabbix.ekord.ru/datareceiver.php", data=post_data)

    # Write datat to JSON file

    json_output_file.write(json.dumps(post_data) + "\n")

# Close JSON output file
json_output_file.close()

maintplan_history = get_maintplan_history()
print(maintplan_history)
for maintplan_name, maintplan_data in maintplan_history.items():
    requests.post("http://zabbix.ekord.ru/maintplan_status.php", data={'plan_name': maintplan_name,
                                                                 'plan_status': maintplan_data['status'],
                                                                 'plan_last_date': maintplan_data['plan_last_date'],
                                                                 'client_name': client_name,'plan_last_date_finish': maintplan_data['plan_last_date_finish'] })


