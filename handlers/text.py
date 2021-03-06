# -*- coding: utf-8 -*-
"""
Created on 2019-05-22 12:27

@author: a002028

"""
from __future__ import print_function

from builtins import object
from shutil import copyfile
import os
from .. import readers
from .. import writers


class TextFileHandler(object):
    """
    """
    def __init__(self, settings):
        self.settings = settings

    def _get_week_range(self, text):
        """
        :return:
        """
        text[0][0] = text[0][0].replace('START_DATE', self.settings.date_range_composite[0])
        text[0][0] = text[0][0].replace('END_DATE', self.settings.date_range_composite[-1])
        return text

    def adjust_weekmap_text(self, file_name):
        """
        :param file_name:
        :return:
        """
        args = (file_name, )
        kwargs = {'sep': '\t', 'header': None, 'encoding': 'utf-8'}
        text = readers.text_reader('pandas', *args, **kwargs)
        text = self._get_week_range(text)
        return text

    def copy_empty_files(self):
        """
        :return:
        """
        print('\nCopying empty textfiles to: %s' % self.settings.baws_USER_SELECTED_current_production_directory)
        pattern = 'BASE_TEXT'
        files_to_copy = self.settings.generate_filepaths(self.settings.settings_directory, pattern=pattern,
                                                         only_from_dir=False)

        for fid in files_to_copy:
            file_name = os.path.basename(fid)
            file_name = file_name.replace(pattern, self.settings.current_working_date)
            dst_path = os.path.join(self.settings.baws_USER_SELECTED_current_production_directory, file_name)
            if 'weekmap' in file_name:
                text = self.adjust_weekmap_text(fid)
                self._write(text, dst_path)
            else:
                copyfile(fid, dst_path)

        print('Files created!\n')

    def _write(self, text, dst_path):
        """
        :param text:
        :param dst_pat:
        :return:
        """
        args = (dst_path, )
        kwargs = {'df': text, 'index': None, 'header': None, 'encoding': 'utf-8'}
        writers.text_writer('pandas', *args, **kwargs)
