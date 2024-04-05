import os

def get_settings_path():
    app_data_path = os.getenv('APPDATA')
    settings_directory = os.path.join(app_data_path, 'Credentials Cacher')
    if not os.path.exists(settings_directory):
        os.makedirs(settings_directory)
    return os.path.join(settings_directory, 'settings.json')