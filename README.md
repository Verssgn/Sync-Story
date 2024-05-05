# SYNC STORY
Success story is a plug for playnite that allows you to use achievements.

Currently, this is a simple script that fetches achievement data from the Goldberg Emu folder in %appdata% and puts it in the Success Story addon in Playnite.

It is not a great solution and could be much improved if it were made by somebody who knows what they are doing, but it works.

The biggest issue is that the changes to achievements are visible only after restarting Playnite.

Install Python, run the following command after installation:
```
pip install psutil
```
---
1. Extract the files somewhere, before running the script, open the config file and set your Playnite path as well as whether Playnite should restart after running the sync command.

```
Playnite= Full path to the Playnite folder
RestartAfterSync=False
```

2. You can either run the script manually each time you want to update your achievements, or you can run it every time you close your game by going into Settings > Scripts > Execute after exiting a game.

Set it to this:

```
Start-Process -FilePath "PATH TO main.py"
```

For example:
```
Start-Process -FilePath "C:\SCRIPTS\main.py"
```

To my knowledge, there is currently no way to update the entire library with the script. Therefore, on your next start of Playnite, you will see the achievements updated. Alternatively, you can set RestartAfterSync=True (case-sensitive), and it will restart Playnite after the script runs.
