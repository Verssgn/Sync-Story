![Releases](https://img.shields.io/badge/DOWNLOAD-green?logo=Python&logoColor=white&link=https%3A%2F%2Fgithub.com%2FVerssgn%2FSync-Story%2Freleases%2Ftag%2F1.0)
[![Latest)](https://img.shields.io/github/v/release/Verssgn/Sync-Story?cacheSeconds=5000&logo=github)](https://github.com/Verssgn/Sync-Story/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/Verssgn/Sync-Story/total.svg)]()

# SYNC STORY
[Success story](https://github.com/Lacro59/playnite-successstory-plugin) is a plugin for playnite that allows you to use achievements.
This is a simple script that fetches achievement data from a preconfigured library and syncs it to the Success Story extension.

You can get the script in the [github releases](https://github.com/Verssgn/Sync-Story/releases).

Make sure you check out the [setup tutorial](https://github.com/Verssgn/Sync-Story/wiki/Setup).

## Maintaining and troubleshooting
Originally, I made this script for myself, but since there haven’t been any other scripts that function like this, I decided to share it. I am pointing this out because I am not a programmer, a lot of the script is written badly to the point I had to use AI at parts to fix some of it. There are many ways this script could be improved, and I wholeheartedly support anyone making forks and changes to this plugin. You can always ask for help in the thread. 

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


