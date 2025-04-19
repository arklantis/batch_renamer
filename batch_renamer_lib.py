import os
import logging
import shutil

class BatchRenamer:
    def __init__(self, 
                 filepath          = None,
                 copy_files        = False,
                 filetypes         = None,
                 strings_to_find   = None,
                 string_to_replace = '',
                 prefix            = None,
                 suffix            = None):
        self.filepath          = filepath
        self.copy_files        = copy_files
        self.filetypes         = filetypes
        self.strings_to_find   = strings_to_find
        self.string_to_replace = string_to_replace
        self.prefix            = prefix
        self.suffix            = suffix

        self.initialize_logger()


    def initialize_logger(self, print_to_screen = False):
        """
        Creates a logger

        Args:
            print_to_screen: for printing to screen as well as file
        """

        ###############
        # Basic Setup #
        ###############
        app_title = 'Test'
        version_number = '1.0.0'
        # get the path the script was run from, storing with forward slashes
        source_path = os.path.dirname(os.path.realpath(__file__))
        # create a log filepath
        logfile_name = f'{app_title}.log'
        logfile = os.path.join(source_path, logfile_name)

        # tell the user where the log file is
        print(f'Logfile is {logfile}')

        # more initialization
        self.logger = logging.getLogger(f'{app_title} Logger')
        self.logger.setLevel(logging.INFO)
        
        ###############################
        # Formatter and Handler Setup #
        ###############################
        file_handler = logging.FileHandler(logfile)
        file_handler.setLevel(logging.INFO)
        # formatting information we want (time, self.logger name, version, etc.)
        formatter = logging.Formatter(f'%(asctime)s - %(name)s {version_number} - '
                                    '%(levelname)s - %(message)s')
        # setting the log file format
        file_handler.setFormatter(formatter)
        # clean up old handlers
        self.logger.handlers.clear()

        # add handler
        self.logger.addHandler(file_handler)

        # allowing to print to screen
        if print_to_screen:
            # create a new "stream handler" for logging/printing to screen
            console = logging.StreamHandler()
            self.logger.addHandler(console)
            # setting the print log format
            console.setFormatter(formatter)

        self.logger.info('Logger Initiated')


    def get_renamed_file_path(self, existing_name, string_to_find, 
                            string_to_replace, prefix, suffix):
        
        file_name, file_extension = os.path.splitext(existing_name)
        
        #check is mutipul file name or not
        if isinstance(string_to_find, (list, tuple)): 
            string_to_find = sorted(string_to_find, key=len, reverse=True)
            for s in string_to_find:
                file_name = file_name.replace(s, string_to_replace)
        else:  
            file_name = file_name.replace(string_to_find, string_to_replace)
        
        #rename file(s) and combine essential words
        new_file_name = f"{prefix}{file_name}{suffix}{file_extension}"
        
        return new_file_name
        
        """
        Returns the target file path given an existing file name and 
        string operations

        Args:
            existing_name: the existing file's name
            string_to_find: a string to find and replace in the existing filename
            string_to_replace: the string you'd like to replace it with
            prefix: a string to insert at the beginning of the file path
            suffix: a string to append to the end of the file path
        """

        '''
        REMINDERS

        This function should only take in strings and return a string.  
        No file renaming/copying/moving should happen here

        Make sure to support string_to_find being an array of multiple strings!  
            Hint: you may need to check its type...
        '''
        pass

    def get_files_with_extension(self, folder_path, extension):
        
        # check is file or folder
        if not os.path.isdir(folder_path):
            return []  # null
        
        file_list = []
        for f_ext in os.listdir(folder_path):
            if f_ext.endswith(extension):
                file_list.append(f_ext)
        return(file_list)
    
        """
        Returns a collection of files in a given folder with an extension that 
        matches the provided extension

        Args:
            folder_path: The path of the folder whose files you'd like to search
            extension: The extension of files you'd like to include in the return
        """

        '''
        REMINDERS

        This function should only take in strings and return an array
        No file renaming/copying/moving should happen here

        Make sure to catch and handle errors if the folder doesn't exist!
        '''
        pass

    def rename_file(self, existing_name, new_name, copy=False):
        if not os.path.exists(existing_name): 
            self.logger.error(f"\nfile is not exsit: {existing_name}")
            return False
        
        # copy or rename files
        try:
            if copy:
                shutil.copy(existing_name, new_name)
                self.logger.info(f"\ncopy: {existing_name} to {new_name}\n")
            else:
                os.rename(existing_name, new_name)
                self.logger.info(f"\nrename: {existing_name} to {new_name}\n")
            return True
        except Exception as e:
            self.logger.error(f"\nerror: {e}\n")
            return False  
        """
        Renames a file if it exists
        By default, should move the file from its original path to its new path--
        removing the old file
        If copy is set to True, duplicate the file to the new path

        Args:
            existing_name: full filepath a file that should already exist
            new_name: full filepath for new name
            copy_mode: copy instead of rename
        """

        '''
        REMINDERS

        Copy files using shutil.copy
        make sure to import it at the top of the file
        '''
        pass

    def rename_files_in_folder(self, folder_path, extension, string_to_find,
                            string_to_replace, prefix, suffix, copy=False):
        if not os.path.isdir(folder_path):
            self.logger.error(f"\nfolder not exsit: {folder_path}\n")
            return False
        
        # check files .ext
        matching_files = self.get_files_with_extension(folder_path, extension)
    
        if not matching_files:
            self.logger.info(f"\nno matching file with '{extension}' type\n")
            return True 
        
        for file_name in matching_files:
            existing_path = os.path.join(folder_path, file_name)
    
            new_file_name = self.get_renamed_file_path(file_name, string_to_find,
                                               string_to_replace, prefix, suffix)
            new_path = os.path.join(folder_path, new_file_name)
    
            self.rename_file(self.logger, existing_path, new_path, copy)
      
        return True
        """
        Renames all files in a folder with a given extension
        This should operate only on files with the provided extension
        Every instance of string_to_find in the filepath should be replaced
        with string_to_replace
        Prefix should be added to the front of the file name
        Suffix should be added to the end of the file name

        Args:
            folder_path: the path to the folder the renamed files are in
            extension: the extension of the files you'd like renamed
            string_to_find: the string in the filename you'd like to replace
            string_to_replace: the string you'd like to replace it with
            prefix: a string to insert at the beginning of the file path
            suffix: a string to append to the end of the file path
            copy: whether to rename/move the file or duplicate/copy it
        """

        '''
        REMINDERS
        #
        This function should:
            - Find all files in a folder that use a certain extension
                - Use get_files_with_extension for this
            - *For each* file...
                - Determine its new file path
                    - Use get_renamed_file_path for this
                - Rename or copy the file to the new path
                    - Use rename_file for this
            - Use the logger instance to document the process of the program
        '''
        pass