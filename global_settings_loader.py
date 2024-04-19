import os
from pickle import load, dump
from global_settings import GlobalSettings
class GlobalSettingsLoader:
    def __init__(self):
        self.path_to_pickle = os.path.join(os.path.dirname(__file__), 'global_settings.pickle')
        self.global_settings = None
    
    def load_global_settings(self):
        if os.path.exists(self.path_to_pickle):
            with open(self.path_to_pickle, 'rb') as f:
                self.global_settings = load(f)
        else:
            self.global_settings = GlobalSettings()
            self.global_settings.set_defaults()
            with open(self.path_to_pickle, 'wb') as f:
                dump(self.global_settings, f)
        return self.global_settings
    
    def save_global_settings(self, global_settings:GlobalSettings):
        with open(self.path_to_pickle, 'wb') as f:
            dump(global_settings, f)
        self.global_settings = global_settings
        return self.global_settings