# -*- coding: utf-8 -*- 

import os
import uuid
import json

class Item:
    def __init__(self, data):
        self.data = data

    def save(self):
        pass

class FileItem(Item):
    default_save_place = './data'

    def __init__(self, data, mode = 'w+', save_place = None):
        super().__init__(data)
        self.mode = mode
        self.save_place = save_place or self.default_save_place

    def filename(self):
        return uuid.uuid4().hex

    def filepath(self):
        filename = self.filename()
        filepath = os.path.join(self.save_place, filename)

        # 补充缺少的文件夹
        dirpath = os.path.dirname(filepath)
        if dirpath != '' and not os.path.isdir(dirpath):
            os.makedirs(dirpath)

        return filepath

    def save(self):
        path = self.filepath()
        with open(path, self.mode) as f:
            f.write(self.data)

class TextItem(FileItem):
    def __init__(self, data, save_place = None):
        super().__init__(data, save_place=save_place)

class JsonItem(TextItem):
    def filename(self):
        return super().filename() + '.json'

    def save(self):
        path = self.filepath()
        with open(path, self.mode) as f:
            json.dump(self.data, f, indent=4)