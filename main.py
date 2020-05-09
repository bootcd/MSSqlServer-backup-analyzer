from dataset import *

# vars

backuptypes = {'D': "Полный", 'L': "Журнал Транзакций", 'I': "Разностный"}
backup_item_list = ['backup_start_date', 'backup_finish_date', 'compressed_backup_size', 'backup_size',
                    'recovery_model', 'media_set_id']

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

# just readable view. Need pack to func!!!!

print("Full")
for key, value in full_backup_bases.items():
    print(key, ": ", value, "/n")

print("journal")
for key, value in journal_backup_bases.items():
    print(key, ": ", value, "/n")

print("increment")
for key, value in inc_backup_bases.items():
    print(key, ": ", value, "/n")
