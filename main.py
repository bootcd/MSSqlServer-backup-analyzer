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

for key, value in full_backup_bases.items():
    common_status = getCommonStatus(value, backup_item_list)
    base_backup_stats = getstatus(value)

    post_data = get_postrequest_data(key, common_status, base_backup_stats, 'D', client_name)

for key, value in full_backup_bases.items():
    common_status = getCommonStatus(value, backup_item_list)
    base_backup_stats = getstatus(value)

    post_data = get_postrequest_data(key, common_status, base_backup_stats, 'D', client_name)

    requests.post("url", data=post_data)

#### JSON Works ####

# Open the output file for json output
json_output_file = open("json_output.txt", "w")

# Purge the output file
json_output_file.truncate()

# Write datat to JSON file

json_output_file.write(json.dumps(post_data) + "\n")

# Close JSON output file
json_output_file.close()
