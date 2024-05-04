import os
import json
import datetime
import subprocess
import psutil

def read_config_file():
    config_path = "config.txt"  
    restart_after_sync = False
    with open(config_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("Playnite="):
                playnite_path = line.split("=")[1].strip()
                print("Playnite Path:", playnite_path)
            elif line.startswith("RestartAfterSync="):
                restart_after_sync = line.split("=")[1].strip().lower() == "true"
                print("RestartAfterSync:", restart_after_sync)
        return playnite_path, restart_after_sync

def scan_json_files(playnite_path):
    extensions_data_path = os.path.join(playnite_path, "ExtensionsData")
    if os.path.exists(extensions_data_path):
        for root, dirs, files in os.walk(extensions_data_path):
            for dir_name in dirs:
                if dir_name.startswith("cebe6d32-8c46-4459-b993-5a5189d60788"): 
                    folder_path = os.path.join(root, dir_name, "SuccessStory")
                    print("Scanning JSON files in folder:", folder_path)
                    for file in os.listdir(folder_path):
                        if file.endswith(".json"):
                            file_path = os.path.join(folder_path, file)
                            with open(file_path, 'r', encoding='utf-8') as json_file:
                                try:
                                    data = json.load(json_file)
                                    if "SourcesLink" in data:
                                        sources_link = data["SourcesLink"]
                                        if "Url" in sources_link and "GameName" in sources_link:
                                            url = sources_link["Url"]
                                            if "/stats/" in url and "/achievements" in url:
                                                game_name = sources_link["GameName"]
                                                game_id = url.split("/stats/")[1].split("/achievements")[0]
                                                print(f"{game_name} ({game_id})")
                                                appdata_path = os.getenv("APPDATA")
                                                achievements_folder = os.path.join(appdata_path, "Goldberg SteamEmu Saves", game_id)
                                                achievements_file_path = os.path.join(achievements_folder, "achievements.json")
                                                if os.path.exists(achievements_file_path):
                                                    print("- Achievement file found at:", achievements_file_path.split("Goldberg SteamEmu Saves")[1])
                                                    with open(achievements_file_path, 'r', encoding='utf-8') as achievements_file:
                                                        achievements_data = json.load(achievements_file)
                                                        for api_name, achievement_info in achievements_data.items():
                                                            if achievement_info.get("earned"):
                                                                earned_time_epoch = achievement_info.get("earned_time")
                                                                earned_time = datetime.datetime.fromtimestamp(earned_time_epoch).strftime('%Y-%m-%dT%H:%M:%S')
                                                                print(f"  - {api_name} (ApiName), Earned Time: {earned_time}")
                                                                for item in data["Items"]:
                                                                    if item.get("ApiName") == api_name and item.get("DateUnlocked") == "0001-01-01T00:00:00":
                                                                        item["DateUnlocked"] = earned_time
                                                                        print(f"    - Updated DateUnlocked for {api_name} to {earned_time}")
                                                    with open(file_path, 'w', encoding='utf-8') as json_out:
                                                        json.dump(data, json_out, indent=4)
                                                else:
                                                    print("- Achievement file not found at:", achievements_file_path.split("Goldberg SteamEmu Saves")[1])
                                except Exception as e:
                                    print(f"Error processing {file}: {e}")
    else:
        print("ExtensionsData folder not found. Please check the configuration.")

def restart_playnite(playnite_path):
    for proc in psutil.process_iter(['pid', 'name']):
        if "Playnite.DesktopApp" in proc.info['name']:
            print("Playnite.DesktopApp process found, killing it...")
            proc.kill()
            break
    
    playnite_exe = os.path.join(playnite_path, "Playnite.DesktopApp.exe")
    print("Launching Playnite.DesktopApp...")
    subprocess.Popen(playnite_exe)

playnite_path, restart_after_sync = read_config_file()
scan_json_files(playnite_path)

if restart_after_sync:
    restart_playnite(playnite_path)
