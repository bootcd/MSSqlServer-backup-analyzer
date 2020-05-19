# This func returns dictionary with statuses of metadata as common status of backup set


def getCommonStatus(backupdict, backup_item_list):
    item_number = len(backup_item_list)
    common_status = {'item_status': "ok", 'data_status': "ok", 'status': "ok", 'nodata': [], 'noitem': []}

    if len(backupdict) != item_number:
        common_status['status'] = "not ok!"
        common_status['item_status'] = "Itemproblem"
        for backup_item in backup_item_list:
            try:
                if backupdict[backup_item]:
                    pass
            except KeyError:
                common_status['noitem'].append(backup_item)
    common_status['noitem'] = ",".join(common_status['noitem'])

    for key, value in backupdict.items():
        if len(value) == 0:
            common_status['status'] = "not ok!"
            common_status['nodata'].append(key)
            common_status['data_status'] = "Dataproblem"
    common_status['nodata'] = ",".join(common_status['nodata'])

    return common_status


# This func returns dictionary with stats and values of backup set data

def getstatus(backupdict):
    import os
    base_backup_item_status = {}
    base_backup_stats = {}
    for base_data_item in backupdict:

        # Проверка на наличие файла

        if base_data_item == "physical_device_name":
            check_file = os.path.exists(backupdict['physical_device_name'])

            # Если файл имеется, вычисляем его размер
            if check_file:
                filesize = os.path.getsize(backupdict[base_data_item])

                # Проверяем размер на ноль

                if filesize == 0:
                    base_backup_item_status['filestatus'] = 'zero size'
                    base_backup_stats['size'] = 0
                else:
                    base_backup_item_status['filestatus'] = 'ok'

                    if backupdict['compressed_backup_size'] == backupdict['backup_size']:
                        base_backup_item_status['compressed'] = 0
                        base_backup_stats['power_of_compressing'] = base_backup_item_status['compressed']
                    else:
                        power_of_compressing = int(backupdict['backup_size']) / int(
                            backupdict['compressed_backup_size'])
                        power_of_compressing = round(power_of_compressing, 2)
                        base_backup_item_status['compressed'] = "ok"
                        base_backup_stats['power_of_compressing'] = power_of_compressing
                    backup_filesize = round(filesize / 1024 / 1024, 2)
                base_backup_stats['size'] = backup_filesize


            else:
                base_backup_item_status['filestatus'] = 'file does not exist!'
                base_backup_stats['size'] = base_backup_item_status['filestatus']

            base_backup_stats['filestatus'] = base_backup_item_status['filestatus']

        if base_data_item == "backup_start_date":

            start_day = backupdict['backup_start_date'].split()[0]
            start_time = backupdict['backup_start_date'].split()[1]

            finish_day = backupdict['backup_finish_date'].split()[0]
            finish_time = backupdict['backup_finish_date'].split()[1]

            duration = (int(finish_time.split(":")[0]) * 3600
                        + int(finish_time.split(":")[1]) * 60
                        + int(finish_time.split(":")[2])) \
                       - \
                       (int(start_time.split(":")[0]) * 3600
                        + int(start_time.split(":")[1]) * 60
                        + int(start_time.split(":")[2]))

            if duration == 0 or duration < 0:
                base_backup_item_status['durationstatus'] = 'not ok!'
            else:
                base_backup_item_status['durationstatus'] = 'ok'
            base_backup_stats['duration'] = duration

    for item_status in base_backup_item_status:
        backup_item_errors = {}
        base_backup_stats['errors'] = []
        if base_backup_item_status[item_status] == "ok":
            base_backup_stats['status'] = "ok"
            base_backup_stats['errors'] = "no errors"
        else:
            base_backup_stats['status'] = "not ok!"
            backup_item_errors[item_status] = base_backup_item_status[item_status]
            base_backup_stats['errors'].append(backup_item_errors)
    base_backup_stats['date'] = backupdict['backup_start_date']

    return base_backup_stats
