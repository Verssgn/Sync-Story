import os
import json
import yaml
import configparser
import logging
from datetime import datetime, timezone
import psutil
import subprocess
import time

logging.basicConfig(filename='sync_story.log', level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger()

def log_and_print(message):
    print(message)
    logger.info(message)

def find_folders(library_path):
    return [f for f in os.listdir(library_path) if os.path.isdir(os.path.join(library_path, f))]

def data_file_exists(folder_path, data_file):
    return find_data_file(folder_path, data_file) is not None

def convert_timestamp(timestamp, time_type):
    if time_type == "unix timestamp":
        return datetime.fromtimestamp(int(timestamp), timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
    else:
        format_parts = []
        format_string = ""
        for part in time_type.split():
            if part in ["yyyy", "mm", "dd", "hh", "nn", "ss"]:
                format_parts.append(part)
                format_string += "%Y" if part == "yyyy" else "%m" if part == "mm" else "%d" if part == "dd" else "%H" if part == "hh" else "%M" if part == "nn" else "%S"
            else:
                format_string += part

        try:
            dt = datetime.strptime(timestamp, format_string)
            return dt.strftime('%Y-%m-%dT%H:%M:%S')
        except ValueError:
            log_and_print(f"ERROR: parsing timestamp: {timestamp} with format: {format_string}")
            return None

def find_data_file(folder_path, data_file):
    for root, dirs, files in os.walk(folder_path):
        if data_file in files:
            return os.path.join(root, data_file)
    return None
    
def find_matching_achievements(game_data, data_file_path, name_type, time_type, ignore_time, time_line):
    matching_achievements = []
    skipped_achievements = []

    if data_file_path.endswith('.json'):
        try:
            with open(data_file_path, 'r') as file:
                data_file_content = json.load(file)
        except FileNotFoundError:
            log_and_print(f"ERROR: Data file not found: {data_file_path}")
            return matching_achievements, skipped_achievements
        except json.JSONDecodeError:
            log_and_print(f"ERROR: While decoding file in data file: {data_file_path}")
            return matching_achievements, skipped_achievements

        def find_time_value(data, time_line):
            if isinstance(data, dict):
                if time_line in data:
                    return data[time_line]
                for key, value in data.items():
                    result = find_time_value(value, time_line)
                    if result is not None:
                        return result
            return None

        for item in game_data.get('Items', []):
            search_key = item.get('Name' if name_type == 'name' else 'ApiName')
            if search_key in data_file_content:
                achievement_data = data_file_content[search_key]
                if isinstance(achievement_data, dict):
                    original_time = find_time_value(achievement_data, time_line)
                    if original_time is not None:
                        if str(original_time) == str(ignore_time):
                            matching_achievements.append({
                                'name': search_key,
                                'original_time': original_time,
                                'converted_time': '0001-01-01T00:00:00'
                            })
                        else:
                            converted_time = convert_timestamp(original_time, time_type)
                            if converted_time:
                                matching_achievements.append({
                                    'name': search_key,
                                    'original_time': original_time,
                                    'converted_time': converted_time
                                })

    elif data_file_path.endswith('.ini'):
        config = configparser.ConfigParser()
        config.read(data_file_path)
        
        for item in game_data.get('Items', []):
            search_key = item.get('Name' if name_type == 'name' else 'ApiName')
            if search_key in config.sections():
                if config.has_option(search_key, time_line):
                    original_time = config.get(search_key, time_line)
                    if str(original_time) == str(ignore_time):
                        matching_achievements.append({
                            'name': search_key,
                            'original_time': original_time,
                            'converted_time': '0001-01-01T00:00:00'
                        })
                    else:
                        converted_time = convert_timestamp(original_time, time_type)
                        if converted_time:
                            matching_achievements.append({
                                'name': search_key,
                                'original_time': original_time,
                                'converted_time': converted_time
                            })
    
    return matching_achievements, skipped_achievements


def update_game_json(json_path, matching_achievements):
    try:
        with open(json_path, 'r') as file:
            game_data = json.load(file)
        
        items_updated = 0
        for item in game_data.get('Items', []):
            for achievement in matching_achievements:
                if item['ApiName'] == achievement['name']:
                    item['DateUnlocked'] = achievement['converted_time']
                    items_updated += 1
        
        with open(json_path, 'w') as file:
            json.dump(game_data, file, indent=4)
        
        return items_updated
    except Exception as e:
        log_and_print(f"ERROR: updating game JSON: {str(e)}")
        return 0

config_path = os.path.join('Config file', 'config.yml')

def expand_path(path):
    if path.upper().startswith('APPDATA'):
        return path.replace('APPDATA', os.environ['APPDATA'], 1)
    elif path.upper().startswith('LOCALAPPDATA'):
        return path.replace('LOCALAPPDATA', os.environ['LOCALAPPDATA'], 1)
    elif path.upper().startswith('PUBLIC'):
        return path.replace('PUBLIC', os.environ['PUBLIC'], 1)
    return path

config_path = os.path.join('Config file', 'config.yml')

try:
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    if not config or 'settings' not in config:
        raise KeyError('The settings section is missing in the configuration.')

    settings = config['settings']
    playnite_path = expand_path(settings.get('Playnite location', ''))
    playnite_exe = settings.get('Playnite exe', '')
    restart_after_sync = settings.get('Restart after sync', False)

    if not playnite_path:
        raise KeyError('The Playnite location is missing/not set up properly.')

    libraries = config.get('libraries', {})

    logger.info("SCRIPT INITIATED")
    print("Sync Story")
    print("- Version: 2.0")
    print(f"- Running: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("Sync Story - Version 2.2")

    log_and_print(f"- Playnite folder: {playnite_path}")
    log_and_print(f"- Playnite executable: {playnite_exe}")
    log_and_print(f"- Restart after sync: {restart_after_sync}")

    success_story_path = os.path.join(playnite_path, 'ExtensionsData', 'cebe6d32-8c46-4459-b993-5a5189d60788', 'SuccessStory')

    json_files = [f for f in os.listdir(success_story_path) if f.endswith('.json')]
    json_file_count = len(json_files)

    if json_file_count == 0:
        log_and_print("ERROR: no json files in success story")
        exit()  

    folder_associations = []

    for json_file in json_files:
        json_path = os.path.join(success_story_path, json_file)
        with open(json_path, 'r') as file:
            data = json.load(file)

        if data.get('IsManual', False):
            game_name = data.get('SourcesLink', {}).get('GameName', 'Unknown')
            steam_id = data.get('SourcesLink', {}).get('Url', '').split('/')[-2]
            items = data.get('Items', [])
            number_of_achievements = len(items)
            
            unlocked_count = sum(1 for item in items if item.get('DateUnlocked', '0001-01-01T00:00:00') != '0001-01-01T00:00:00')
            locked_count = number_of_achievements - unlocked_count

            for library_name, library_details in libraries.items():
                if 'path' in library_details:
                    library_details['path'] = expand_path(library_details['path'])
                    library_path = library_details.get('path', '')
                    folder_data_type = library_details.get('folder data type', 'steam_id')
                    data_file = library_details.get('data file', 'achievement.json')
                    name_type = library_details.get('name type', 'name')
                    time_type = library_details.get('time type', 'unix timestamp')
                    ignore_time = library_details.get('ignore time', None)
                    time_line = library_details.get('time line', 'earned_time')

                    if not os.path.isdir(library_path):
                        log_and_print(f"Error: Library path not found: {library_path}")
                        continue
                    
                    folder_names = find_folders(library_path)

                    folder_name = steam_id if folder_data_type == 'steam_id' else game_name
                    folder_found = folder_name in folder_names
                    folder_path = os.path.join(library_path, folder_name) if folder_found else None
                    data_file_exists_flag = data_file_exists(folder_path, data_file) if folder_found else False

                    matching_achievements = []
                    skipped_achievements = []
                    if data_file_exists_flag:
                        data_file_path = find_data_file(folder_path, data_file)
                        if data_file_path is None:
                            log_and_print(f"ERROR: Data file '{data_file}' not found in {folder_path}")
                            continue
                        matching_achievements, skipped_achievements = find_matching_achievements(data, data_file_path, name_type, time_type, ignore_time, time_line)

                        items_updated = update_game_json(json_path, matching_achievements)

                    folder_associations.append({
                        'library': library_name,
                        'number_of_achievements': number_of_achievements,
                        'unlocked_count': unlocked_count,
                        'locked_count': locked_count,
                        'json_file': json_file,
                        'folder': folder_name,
                        'game_name': game_name,
                        'steam_id': steam_id,
                        'folder_found': folder_found,
                        'data_file_exists': data_file_exists_flag,
                        'matching_achievements': matching_achievements,
                        'skipped_achievements': skipped_achievements,
                        'time_type': time_type
                    })

    print("\nLibraries:")
    for library_name, library_details in libraries.items():
        if library_details.get('status', False):
            library_path = library_details.get('path', 'Not specified')
            time_type = library_details.get('time type', 'Not specified')
            log_and_print(f"- Name: {library_name} (Time format: {time_type})")
            log_and_print(f"- Path: {library_path} \n")

    print("\nSync setup:")
    if folder_associations:
        for association in folder_associations:
            print(f"{association['game_name']}")
            print(f" - Success story id: {association['json_file']}")
            print(f" - Library: {association['library']}")
            print(f" - Folder: {association['folder']}")
            print(f" - Steam ID: {association['steam_id']}")
            print(f" - Folder Found: {association['folder_found']}")
            print(f" - Data File Exists: {association['data_file_exists']}")
            
            if association['data_file_exists']:
                if association['matching_achievements']:
                    print(" - Syncing achievements:")
                    for achievement in association['matching_achievements']:
                        print(f"   - {achievement['name']}: {achievement['original_time']} -> {achievement['converted_time']}")
                else:
                    print(" - No matching achievements found")
                
                ignored_achievements = [ach for ach in association['matching_achievements'] if ach['converted_time'] == '0001-01-01T00:00:00']
                    
            else:
                print(" - No achievements or times (data file not found or empty)")
            
            print()  
            
            logger.info(f"Syncing {association['game_name']}\n Library: {association['library']},\n Folder: {association['folder']},\n Steam ID: {association['steam_id']},\n Folder Found: {association['folder_found']},\n Data File Exists: {association['data_file_exists']},\n Synced Achievements: {association['matching_achievements']},\n Skipped Achievements: {association['skipped_achievements']}")
        else:
          log_and_print("ERROR: No matching folders found for any JSON files.")

    if restart_after_sync:
        log_and_print("\nAttempting to restart Playnite...")
        
        def is_process_running(process_name):
            return process_name.lower() in (p.name().lower() for p in psutil.process_iter(['name']))

        def kill_process(process_name):
            for proc in psutil.process_iter(['name']):
                if proc.name().lower() == process_name.lower():
                    proc.kill()
                    log_and_print(f"Killed process: {process_name}")

        if is_process_running("Playnite.DesktopApp.exe"):
            kill_process("Playnite.DesktopApp.exe")
        if is_process_running("Playnite.FullscreenApp.exe"):
            kill_process("Playnite.FullscreenApp.exe")
            
        time.sleep(2)

        if playnite_exe:
            full_path = os.path.join(playnite_path, playnite_exe)
            full_path = expand_path(full_path)
            if os.path.exists(full_path):
                subprocess.Popen(full_path)
                log_and_print(f"Started Playnite: {full_path}")
            else:
                log_and_print(f"ERROR: Playnite executable not found at {full_path}")
        else:
            log_and_print("ERROR: Playnite executable not specified in configuration")

    log_and_print("\nSync Story operation completed.")

except FileNotFoundError as e:
    error_message = f"File not found: {str(e)}"
    log_and_print(error_message)
except KeyError as e:
    error_message = f"Configuration error: {str(e)}"
    log_and_print(error_message)
except Exception as e:
    error_message = f"An unexpected error occurred: {str(e)}"
    log_and_print(error_message)