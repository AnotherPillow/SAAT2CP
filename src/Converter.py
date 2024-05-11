import json5, shutil, os, json

from .Logger import logger

class Converter:
    manifest: dict = {}
    shops: dict = {}
    content: dict = {
        "Format": "2.0",
        "Changes": []
    }
    
    def __init__(self):
        self.manifest = json5.load(open('input/manifest.json', encoding='utf8'))
        self.shops = json5.load(open('input/content.json', encoding='utf8'))

        if os.path.exists('output'):
            shutil.rmtree('output')
        shutil.copytree('input', 'output')

    def convert(self):
        
        pass

    def translateManifest(self):
        self.manifest['UniqueID'] += '.CP'
        self.manifest['Author'] += ' ~ ___2CP'

        self.manifest['ContentPackFor']['UniqueID'] = 'Pathoschild.ContentPatcher'
        
        if 'Dependencies' in self.manifest:
            self.manifest['Dependencies'] = \
                [mod for mod in self.manifest['Dependencies'] if mod['UniqueID'] not in ['OldMod.Framework']]
        
    def save(self):
        
        with open('output/manifest.json', 'w') as f:
            json.dump(self.manifest, f, indent=4)
        
        with open('output/content.json', 'w') as f:
            json.dump(self.content, f, indent=4)