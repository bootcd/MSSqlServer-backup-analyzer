# This func returns dictionary with data for POST request


def get_postrequest_data(database, metadata_status, base_backup_stats, backup_type, client_name):
    # This func returns error string from error list

    def geterrorstring(errors):
        errorstring = ";".join(errors)

        return errorstring

    # Dictionary with needful data for POST request

    request_item_dict = {'database': database, 'common_status': metadata_status['status'],
                         'backup_item_status': metadata_status['item_status'],
                         'backup_data_status': metadata_status['data_status'],
                         'backup_status': base_backup_stats['status'],
                         'power_of_compressing': base_backup_stats['power_of_compressing'],
                         'size': base_backup_stats['size'], 'duration': base_backup_stats['duration'],
                         'backup_date': base_backup_stats['date'], 'client_name': client_name,
                         'backup_type': backup_type, 'backup_file_status': base_backup_stats['filestatus'],
                         'errors': geterrorstring(base_backup_stats['errors'])}

    return request_item_dict

#def get_maintplan_errors_request()