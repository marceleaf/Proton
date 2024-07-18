import json

def loadSetting():
    with open("settings.json", 'r') as openfile:
        configData = json.load(openfile)
        return configData