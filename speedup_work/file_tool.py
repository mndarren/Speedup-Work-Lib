#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. current_module:: file_tool.py
.. created_by:: Darren Xie
.. created_on:: 04/25/2021

Collect File action tools
"""
import os
import re
import shutil
import stat
from glob import glob
from pathlib import Path
from datetime import datetime
PERCENT_RE = re.compile(r'%(.+?)%')


class FileTool:
    """
    Contain all tools for file action.
    1. Load config text file for environment variables
    2. Unit to Dos format conversion
    3. Dos ot Unit format conversion.
    """
    def load_env(self, full_path):
        """
        Load environment vars by reading a config text file
        :param full_path: Path to the config text file.
        """
        try:
            with open(full_path, 'r') as in_fh:
                for line in in_fh:
                    line = str(line)
                    # skip comment line and lines without mark '='
                    if "#" in line or '=' not in line:
                        continue
                    line = line.strip()
                    key, value = line.split('=', 1)
                    key, value = key.strip(), value.strip().replace('\\', '/')

                    if '%' in value:
                        try:
                            while '%' in value:
                                try_k = re.search(PERCENT_RE, value).group(1)
                                value = re.sub(PERCENT_RE, os.environ[try_k].replace('\\', '/'), value, 1)
                        except Exception:
                            raise Exception(f"{try_k} not defined")
                    os.environ[key] = value.replace('/', '\\')
        except IOError:
            raise IOError(f"Cannot open file {full_path}")
        except Exception:
            raise Exception(f"Cannot open file {full_path}")

    def on_rm_error(self, func, path, exc_info):
        """
        This function is for shutil.rmtree() onerror=self.on_rm_error
        :param func:
        :param path:
        :param exc_info:
        :return:
        """
        # path contains the path of the file that couldn't be removed
        # let's just assume that it's read-only and unlink it.
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)

    def dos2unix(self, filename):
        """
        Convert Dos format to Unix format for EOF (\r\n to \n)
        :param filename: Full path to the file to be converted.
        """
        try:
            with open(filename, 'rb') as in_fh:
                text = in_fh.read().replace(b'\r\n', b'\n')
        except IOError as e:
            raise IOError(str(e))
        except Exception as e:
            raise Exception(str(e))
        with open(filename, 'wb') as out_fh:
            out_fh.write(text)

    def unix2dos(self, filename):
        """
        Convert Unix format to Dos format (\n to \r\n)
        :param filename: Full path to the file to be converted.
        """
        self.dos2unix(filename)
        try:
            with open(filename, 'rb') as in_fh:
                text = in_fh.read().replace(b'\n', b'\r\n')
        except IOError as e:
            raise IOError(str(e))
        except Exception as e:
            raise Exception(str(e))
        with open(filename, 'wb') as out_fh:
            out_fh.write(text)
