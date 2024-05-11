import json5, shutil, os, json

from .Logger import logger

def absify(fp):
    return '{{AbsoluteFilePath: ' + fp + '}}'

def tryDict(obj):
    if obj == None: return {}
    else: return obj

class Converter:
    manifest: dict = {}
    tracks: dict = {}
    content: dict = {
        "Format": "2.0",
        "Changes": []
    }
    
    def __init__(self):
        self.manifest = json5.load(open('input/manifest.json', encoding='utf8'))
        self.tracks = json5.load(open('input/tracks.json', encoding='utf8'))

        if os.path.exists('output'):
            shutil.rmtree('output')
        shutil.copytree('input', 'output')

    def convert(self):
        logger.info('Conversion started.')
        
        for track in self.tracks:
        
            if 'AddToJukebox' in tryDict(track.get('Settings')):
                jb_entry = {
                    track['Id']: {
                        "Name": f"{self.manifest['Name']} - {track['Id']}",
                        "Available": True,
                    }
                }
                jb_change = {
                    "Action": "EditData",
                    "Target": "Data/JukeboxTracks",
                    "Entries": jb_entry
                }
                self.content['Changes'].append(jb_change)
                

            entry = {
                track['Id']: {
                    'ID': track['Id'], 
                    'FilePaths': [
                        absify(track['Filepath'])
                    ],
                    'Category': track['Category'],
                    'Looped': True if tryDict(track.get('Settings')).get('Loop') else False
                }
            }

            change = {
                "Action": "EditData",
                "Target": "Data/AudioChanges",
                "Entries": entry
            }

            self.content['Changes'].append(change)

        self.save()

    def translateManifest(self):
        self.manifest['UniqueID'] += '.CP'
        self.manifest['Author'] += ' ~ SAAT2CP'

        self.manifest['ContentPackFor']['UniqueID'] = 'Pathoschild.ContentPatcher'
        
        if 'Dependencies' in self.manifest:
            self.manifest['Dependencies'] = \
                [mod for mod in self.manifest['Dependencies'] if mod['UniqueID'] not in ['ZeroMeters.SAAT.Mod']]
        
    def save(self):
        
        with open('output/manifest.json', 'w') as f:
            json.dump(self.manifest, f, indent=4)
        
        with open('output/content.json', 'w') as f:
            json.dump(self.content, f, indent=4)

        os.remove('output/tracks.json')