# -*- coding: utf-8 -*-
"""Create archive file.
"""
import os
import re
import zipfile
from ebook_homebrew.core import Common
from ebook_homebrew.utils.logging import get_logger
from ebook_homebrew.exceptions import ZipFileExistError

logger = get_logger("MakeArchive")


class MakeArchive(Common):
    """Make archive file.

    """
    def __init__(self, extension, directory_path=None):
        """Constructor

        Args:
            extension (str): Target file extension.
            directory_path (str): Target directory path.
        """
        super().__init__()
        self.__extension = self._convert_extension_with_dot(extension)
        self.__regex_ext = re.compile(self.__extension)
        if directory_path is not None:
            self.__directory_path = directory_path
        else:
            self.__directory_path = os.getcwd()
            logger.debug("Current Directory: {cwd}".format(cwd=self.__directory_path))
        os.chdir(self.__directory_path)

    def make_zip(self, filename, remove_flag=False, overwrite=False):
        """Make zip file for adding specify extension files.

        Make zip file for files which you choose extension.

        Args:
            filename (str): Zip file name
            remove_flag (bool): If true, remove original files
            overwrite (bool): If true, overwrite zip file even if exist same name file

        Returns:
            bool: If success, return true.

        """
        count = 0
        files = os.listdir(self.__directory_path)
        if overwrite:
            file_mode = "w"
        else:
            file_mode = "x"
        for file in files:
            if not self.__regex_ext.search(file):
                logger.debug("Skip(No target extension): {filename}".format(filename=file))
            else:
                try:
                    with zipfile.ZipFile(filename, file_mode, zipfile.ZIP_DEFLATED) as zip_file:
                        zip_file.write(file)
                        count += 1
                        logger.debug("Add Zipfile n files: {count}. Filename: "
                                     "{filename}".format(count=count, filename=file))
                        file_mode = "a"
                except FileExistsError:
                    raise ZipFileExistError()

                if remove_flag:
                    self._remove_file(file, assume_yes=True)
                    logger.debug("File removed: {filename}".format(filename=file))
        logger.info("-" * 55)
        logger.info("Finished. Zipfile: {filename}".format(filename=filename))
        return True


if __name__ == '__main__':
    obj = MakeArchive("txt", "../tests")
    obj.make_zip("test.zip", overwrite=False, remove_flag=True)