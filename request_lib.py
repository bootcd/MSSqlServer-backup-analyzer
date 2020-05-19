# This func returns dictionary with data for POST request


def get_postrequest_data(database, common_status, base_backup_stats, backup_type):
    # This func returns error string from error list

    def geterrorstring(errors):
        if type(errors) == list:
            errorstring = ""
            for error in errors:
                for er, value in error.items():
                    errorstr = er + ": " + value + "; "
                    errorstring = errorstring + errorstr
            return errorstring

        else:
            return errors

    # Dictionary with needful data for POST request

    request_item_dict = {'database': database, 'common_status': common_status['status'],
                         'backup_item_status': common_status['item_status'],
                         'backup_data_status': common_status['data_status'],
                         'backup_status': base_backup_stats['status'],
                         'power_of_compressing': base_backup_stats['power_of_compressing'],
                         'size': base_backup_stats['size'], 'duration': base_backup_stats['duration'],
                         'backup_date': base_backup_stats['date'], 'client_name': 'test client',
                         'backup_type': backup_type, 'backup_file_status': base_backup_stats['filestatus'],
                         'errors': geterrorstring(base_backup_stats['errors'])}

    return request_item_dict
