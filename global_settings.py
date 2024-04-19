from pickle import load, dump
import os
class GlobalSettings:
    def __init__(self):
        #get os (windows, mac or linux)
        self.os = os.name
        self.folder = None
        self.streamer_name = None
        self.file = None
    
    def set_defaults(self):
        self.set_default_db_path()

    def set_default_db_path(self):
        #if windows get appdata roaming folder
        if self.os == 'nt':
            self.folder = os.getenv('APPDATA')
        #if mac get home folder
        elif self.os == 'posix':
            self.folder = os.getenv('HOME')
        #if linux get home folder
        elif self.os == 'posix':
            self.folder = os.getenv('HOME')
        file_path = "/ChatGuessr/scores.db"

        if self.os == 'nt':
            file_path = "\\ChatGuessr\\scores.db"

        self.file = self.folder + file_path

    def get_db_path(self):
        if "file" not in self.__dict__ or self.file is None:
            self.set_default_file()
        return self.file
    
    def set_file(self, file):
        self.file = file
    
    def set_streamer_name(self, streamer_name):
        self.streamer_name = streamer_name

    def get_streamer_name(self):
        #if global_settings does not have a streamer_name set it to default
        if "streamer_name" not in self.__dict__ or self.streamer_name is None:
            return None
        return self.streamer_name

    def set_streamer_name(self, streamer_name):
        self.streamer_name = streamer_name

