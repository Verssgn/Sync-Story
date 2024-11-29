[![Latest)](https://img.shields.io/github/v/release/Verssgn/Sync-Story?cacheSeconds=5000&logo=github)](https://github.com/Verssgn/Sync-Story/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/Verssgn/Sync-Story/total.svg)]()

> [!TIP]
> # HOW TO GET ACHIEVEMENTS ON NON-STEAM GAMES
> The script is now archived, it should still work, but there is a better way.
> Please check out **eFMann's fork [(LINK)](https://github.com/eFMann/playnite-successstory-plugin)** of a success story that has integrated support for many emulators (Right-click an entry -> Force SteamAppID)

>
> # Background
>Thanks to the user u/Korieb98 for letting me know of the fork. When I started working on it the goal was to bring achievements from Goldberg to a success story, while the script was/is not great as I am not a programmer. I always said once there is a better solution I would retire it.  I still hope that it was useful. If the fork does not work for you can still use this script. Just know there might be issues.

---
# SYNC STORY (ARCHIVED)

[Success story](https://github.com/Lacro59/playnite-successstory-plugin) is a plugin for playnite that allows you to use achievements.
This is a simple script that fetches achievement data from a preconfigured library and syncs it to the Success Story extension.

You can get the script in the [github releases](https://github.com/Verssgn/Sync-Story/releases).

Make sure you check out the [setup tutorial](https://github.com/Verssgn/Sync-Story/wiki/Setup).

> [!NOTE]
> ## Important
> Success Story actually supports emu games, there is no documentation on the Git Hub, but if you go to the success story extension data folder and go to the config.json you can Enable local achievements. I was not able to get this to work (The reason why this repo is not archived). 
> 
> In theory, using this method would be way more consistent, from the code it seems like it can scan Goldberg and other emus but from what I've seen all the people who were able to get it to work added games manually, meaning it would require you to add all games to the config manually. The advantage of my script is that it does all of it automatically, but at the same time, it is also pretty scuffed. 

> [!TIP]
> If the script is not loading a specific game, check if the game's json file in Playnite\ExtensionsData\cebe6d32-8c46-4459-b993-5a5189d60788\SuccessStory\ has "IsManual": true

## Maintaining and troubleshooting
Originally, I made this script for myself, but since there haven’t been any other scripts that function like this, I decided to share it. I am pointing this out because I am not a programmer, a lot of the script is written badly to the point I had to use AI at parts to fix some of it. There are many ways this script could be improved, and I wholeheartedly support anyone making forks and changes to this script. You can always ask for help in the thread. 

## Quarks and customization
You can setup your own library that works by importing data from diffferent emulators.

The issue is that the way the script currently gets data is very rigid, for example emulators that save data in their game folder will not work, the script also uses a very specific way to parse data so if the emulator uses prefixes or suffixes for the achievement names it will not work. 

The biggest issue so far is the fact that the script doesn't have conflict managment meaning if you have 2 same games in different emulators they will currently overwrite each other.

---
### Current support (When configured):
| Emualtor  | Supported |
| ------------- | ------------- |
| Goldberg Emulator [Original] (tested - Ships with script)  | ✅  |
| RUNE (tested - Ships with script)  | ✅  |
| Goldberg forks (should work but you will need to change the path)  | 🟧  |
| Scripts that use a central folder should work (Skidrow, Empress)  | 🟧  |
| Scripts that use game folders for storing data or use different layout for storing achievements | 🟥  |


