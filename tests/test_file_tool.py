#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. current_module:: test_file_tool.py
.. created_by:: Darren Xie
.. created_on:: 05/06/2021

Test module file_tool.py
"""
import unittest
from pathlib import Path
from codecs import open
from os import unlink
from speedup_work_lib.file_tool import FileTool


class MyTestCase(unittest.TestCase):
    test_dos_filename = 'test_dos.txt'
    test_unix_filename = 'test_unix.txt'
    test_dos_path_file = Path(__file__).parent.joinpath(test_dos_filename)
    test_unix_path_file = Path(__file__).parent.joinpath(test_unix_filename)

    def test_dos2unix(self):
        with open(self.test_dos_path_file, 'rb') as in_fh:
            last_char = in_fh.read()[-2:]
            self.assertEqual(last_char, b'\r\n')

        FileTool().dos2unix(self.test_dos_path_file)

        with open(self.test_dos_path_file, 'rb') as in_fh:
            last_char = in_fh.read()[-2:]
            self.assertEqual(last_char, b'.\n')

    def test_unix2dos(self):
        with open(self.test_unix_path_file, 'rb') as in_fh:
            last_char = in_fh.read()[-2:]
            self.assertEqual(last_char, b'.\n')

        file_tool = FileTool()
        file_tool.unix2dos(self.test_unix_path_file)

        with open(self.test_unix_path_file, 'rb') as in_fh:
            last_char = in_fh.read()[-2:]
            self.assertEqual(last_char, b'\r\n')

    def test_update_string_in_file(self):
        with open(self.test_unix_path_file, 'r') as in_fh:
            content = in_fh.read()
            self.assertTrue('line' in content)

        file_tool = FileTool()
        file_tool.update_string_in_file('line', 'nolie', self.test_unix_path_file)

        with open(self.test_unix_path_file, 'r') as in_fh:
            content = in_fh.read()
            self.assertTrue('nolie' in content)
            self.assertTrue('line' not in content)

    def create_unix_file(self):
        content = b'Test line with dos.\n'
        with open(self.test_unix_path_file, 'wb') as out:
            out.write(content)

    def create_dos_file(self):
        content = b'Test line with dos.\r\n'
        with open(self.test_dos_path_file, 'wb') as out:
            out.write(content)

    def files_setup(self) -> None:
        self.create_dos_file()
        self.create_unix_file()

    def clean_files(self) -> None:
        if Path(self.test_dos_path_file).exists:
            unlink(self.test_dos_path_file)
        if Path(self.test_unix_path_file).exists:
            unlink(self.test_unix_path_file)


if __name__ == '__main__':
    unittest.main()
