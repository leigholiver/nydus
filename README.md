# Nydus

Nydus is tool for the SC2 client api, extendable through plugins.

Icon by [@MinnyMausGG](https://twitter.com/MinnyMausGG)

## [Download](https://github.com/leigholiver/nydus/releases/latest/)

## Plugins
**Nydus Notes** - Keep notes on your opponents and automatically display them when you enter a game (Thanks to Aggression1 for inspiration)

**F2HabitBreaker** - Create overlays to prevent you from clicking the all army button or the command card (Windows only)

**Scene Switcher** - Switch scenes in Streamlabs OBS or OBS-Studio when you enter/leave a game (OBS-Studio requires the [obs-websocket plugin](https://github.com/Palakis/obs-websocket/releases/latest))

**Nydus Bet** - Betting game Twitch chat bot

**Sound of Victory** - Play sounds when you win or lose

**Score Tracker** - Track of your scores vs each race

**Webhook** - Send web requests with game data when you join or leave a game

---

## Creating plugins
Create a class extending `support.plugins.NydusPlugin` and put it in your `plugins` folder. Nydus will call functions on your plugin when the state of the SC2 client api changes. There are a couple of dummy plugins in the `examples` folder you can use as a starting point, along with the included plugins, but here is the most bare bones example:

```python
# plugins/CoolPlugin.py
from support.plugins.NydusPlugin import NydusPlugin

class CoolPlugin(NydusPlugin):
    name = "My Cool Plugin"

    def __init__(self):
        NydusPlugin.__init__(self)

    def enterGame(self, data, isReplay):
      print("joined a game!")
```

## Game Events
### `enterGame(self, data, isReplay)`
### `exitGame(self, data, isReplay)`
Called when a game begins/ends

**`data`** will be a dict containing the game state:
```{
  "players": [
    {
      "name": "playerA",
      "type": "user",
      "race": "Prot", # Terr | Zerg | Prot | random
      "result": "Victory", # | Defeat | Undecided
      "isme": True
    },
    {
      "name": "playerB",
      "type": "computer",
      "race": "random",
      "result": "Defeat",
      "isme": False
    }
  ],
  "displayTime": "5.000000"
}
```
**`isReplay`** will either be `True` or `False`

---
### `menuChanged(self, menu)`
Called when the current menu changes

**`menu`** will be one of:
```
"ScreenScore/ScreenScore"
"ScreenUserProfile/ScreenUserProfile"
"ScreenBattleLobby/ScreenBattleLobby"
"ScreenHome/ScreenHome"
"ScreenSingle/ScreenSingle"
"ScreenCollection/ScreenCollection"
"ScreenCoopCampaign/ScreenCoopCampaign"
"ScreenCustom/ScreenCustom"
"ScreenReplay/ScreenReplay"
"ScreenMultiplayer/ScreenMultiplayer"
"ScreenLoading/ScreenLoading"
```


## UI functions
### `getUI(self)`
Called when the user clicks on the "Open Plugin" button, or has your plugin set to open on startup. See `examples/Example` for a barebones example of a plugin with a user interface.

The `.ui` files can be created/edited using [Qt Designer](https://build-system.fman.io/qt-designer-download)


## Utility functions
### `start(self)`
### `stop(self)`
Called when the plugin starts/stops, to allow for setup/teardown tasks


## Logging
Call **`self.log(message)`** to add a message to the debug log


## Plugin dependencies

You must include any additional dependencies in `[plugin folder]/packages`

You can package your dependencies using: `pip install -r requirements.txt -t [plugin folder]/packages`

You can simulate SC2 client api responses to reduce development time by using [SC2ApiEmulator](https://github.com/leigholiver/SC2ApiEmulator)

---
## Building from source
Install the dependencies: `pip install -r requirements.txt`

(Windows) Run `build-win.bat`

(Linux) Run `./build-linux.sh`

The package will be built into the `dist` folder
