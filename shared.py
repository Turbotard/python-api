# Initialisation du compteur de requêtes pour chaque route
global_request_counts = {
    'Root': 0,
    'Cities_add_entry': 0,
    'Cities_delete_entry': 0,
    'Cities_name_entry': 0,
    'Cities_update_entry': 0,
    'Cities_city_weathers_entry': 0,
    'Countries_add_entry': 0,
    'Countries_delete_entry': 0,
    'Countries_get_all_data': 0,
    'Countries_get_by_name': 0,
    'Countries_update_entry': 0,
    'Weathers_add_entry': 0,
    'Weathers_filter_by_date': 0,
    'Weathers_delete_entry': 0,
    'Weathers_get_all_data': 0,
    'Weathers_filter_by_precipitation': 0,
    'Weathers_filter_by_temperature': 0,
    'Weathers_update_entry': 0,
    'Weathers_patch_entry': 0,

}

cities_request_counts = {
    'add_entry': 0,
    'delete_entry': 0,
    'name_entry': 0,
    'update_entry': 0,
    'city_weathers_entry': 0,
}

countries_request_counts = {
    'add_entry': 0,
    'delete_entry': 0,
    'get_all_data': 0,
    'get_by_name': 0,
    'update_entry': 0,
}

weathers_request_counts = {
    'add_entry': 0,
    'filter_by_date': 0,
    'delete_entry': 0,
    'get_all_data': 0,
    'filter_by_precipitation': 0,
    'filter_by_temperature': 0,
    'update_entry': 0,
    'patch_entry': 0,
}
