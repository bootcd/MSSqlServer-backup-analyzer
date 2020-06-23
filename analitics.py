# This func returns dictionary with statuses of metadata as common status of backup set
from db_connect import *


def get_metadata_status(backupdict, backup_item_list):
    item_number = len(backup_item_list)
    metadata_status = {'item_status': "ok", 'data_status': "ok", 'status': "ok", 'nodata': [], 'noitem': []}

    if len(backupdict) != item_number:
        metadata_status['status'] = "not ok!"
        metadata_status['item_status'] = "Itemproblem"
        for backup_item in backup_item_list:
            try:
                if backupdict[backup_item]:
                    pass
            except KeyError:
                metadata_status['noitem'].append(backup_item)
    metadata_status['noitem'] = ",".join(metadata_status['noitem'])

    for key, value in backupdict.items():
        if len(value) == 0:
            metadata_status['status'] = "not ok!"
            metadata_status['nodata'].append(key)
            metadata_status['data_status'] = "Dataproblem"
    metadata_status['nodata'] = ",".join(metadata_status['nodata'])

    return metadata_status


def get_file_status(file):
    import os
    check_file = os.path.exists(file)

    if check_file:
        file_status = "ok"
    else:
        file_status = "file does not exists!"

    return file_status


def get_power_of_compressing(size, compressed_size):
    if size != compressed_size:
        power_of_compressing = int(size) / float(compressed_size)
        power_of_compressing = round(power_of_compressing, 2)
    else:
        power_of_compressing = 0

    return power_of_compressing


def get_backup_duration_time(start_date, finish_date):
    start_day = start_date.split()[0]
    start_time = start_date.split()[1]

    finish_day = finish_date.split()[0]
    finish_time = finish_date.split()[1]

    backup_duration_time = (int(finish_time.split(":")[0]) * 3600 +
                            int(finish_time.split(":")[1]) * 60 +
                            int(finish_time.split(":")[2])) \
                           - \
                           (int(start_time.split(":")[0]) * 3600
                            + int(start_time.split(":")[1]) * 60
                            + int(start_time.split(":")[2]))

    return backup_duration_time


def get_backup_status(file_status, backup_duration_time, backup_size):
    backup_status = {}
    errors = []

    if file_status == "ok":
        backup_status['file_status'] = "ok"
        backup_status['status'] = 'ok!'
    else:
        errors.append(file_status)
        backup_status['status'] = 'not ok!'

    if backup_duration_time == 0:
        pass

    if backup_size == 0:
        errors.append("file zero size!")
        backup_status['status'] = 'not ok!'

    backup_status['errors'] = errors

    return backup_status


def get_base_backup_stats(backup_dict):
    base_backup_stats = {}
    file = backup_dict['physical_device_name']
    size = round((int(backup_dict['backup_size']) / 1024 / 1024), 2)
    compressed_size = round(int(backup_dict['compressed_backup_size']) / 1024 / 1024, 2)
    start_date = backup_dict['backup_start_date']
    finish_date = backup_dict['backup_finish_date']
    backup_duration_time = get_backup_duration_time(backup_dict['backup_start_date'], backup_dict['backup_finish_date'])
    power_of_compressing = get_power_of_compressing(size, compressed_size)
    file_status = get_file_status(file)
    backup_status = get_backup_status(file_status, backup_duration_time, size)

    if len(backup_status['errors']) == 0:
        backup_status['errors'].append("no errors")

    base_backup_stats['power_of_compressing'] = power_of_compressing
    base_backup_stats['status'] = backup_status['status']
    base_backup_stats['errors'] = backup_status['errors']
    base_backup_stats['duration'] = backup_duration_time
    base_backup_stats['size'] = compressed_size
    base_backup_stats['filestatus'] = file_status
    base_backup_stats['date'] = start_date

    return base_backup_stats
