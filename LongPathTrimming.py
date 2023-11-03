import os
import shutil
from pathlib import Path

class FilePathShortener:
    """
    A class to abbreviate file names in a directory to ensure their full paths
    do not exceed a specified maximum length, with a method to back up the originals.
    """

    def __init__(self, target_size, max_length):
        # Initialize with the target file size and the maximum path length allowed.
        self.target_size = target_size
        self.max_length = max_length
        # Create a backup directory in the current working directory, if it doesn't exist.
        self.backup_folder_path = Path.cwd() / "original_copies"
        self.backup_folder_path.mkdir(exist_ok=True)

    def abbreviate_filename(self, file_path):
        # Abbreviate the filename to fit within the maximum path length.
        # Determine if abbreviation is necessary based on current path length.
        path_length = len(str(file_path))
        if path_length <= self.max_length:
            return file_path  # Return the original path if abbreviation is not needed.

        # Calculate how much the path needs to be shortened.
        excess_length = path_length - self.max_length
        # Split the file path into its parts and separate the file extension.
        parts = list(file_path.parts)
        filename = parts[-1]
        name, ext = os.path.splitext(filename)

        # Split the file name into words and attempt abbreviation by removing vowels.
        words = name.split()
        for i in range(len(words)):
            if len(words[i]) > 1 and excess_length > 0:
                original_word = words[i]
                words[i] = ''.join([letter for letter in words[i] if letter.lower() not in 'aeiou'])
                # Ensure that at least the first letter remains if all letters are vowels.
                if words[i] == '':
                    words[i] = original_word[0]
                # Reduce the excess_length with the number of characters removed.
                excess_length -= (len(original_word) - len(words[i]))

        # Reassemble the new abbreviated name with the original file extension.
        new_name = ''.join(words) + ext
        # Construct the new path using the original directory and the new file name.
        new_path = Path(*parts[:-1], new_name)

        return new_path

    def rename_file(self, original_path, new_path):
        # Rename the file while handling potential errors.
        try:
            if new_path.exists():
                # Prevent overwriting existing files.
                raise FileExistsError(f"The file {new_path} already exists. Cannot rename {original_path} to this name.")
            
            # Perform the file renaming.
            os.rename(original_path, new_path)
            print(f"Successfully renamed {original_path} to {new_path}")
        except FileExistsError as e:
            print(e)
        except OSError as e:
            print(f"Error while renaming file {original_path} to {new_path}: {e}")

    def backup_file(self, file_path):
        # Create a backup copy of the file if it doesn't already exist in the backup folder.
        backup_file_path = self.backup_folder_path / file_path.name
        if not backup_file_path.exists():
            # Only copy the file if it's not already backed up.
            shutil.copy2(file_path, backup_file_path)
            print(f"Backed up {file_path} to {backup_file_path}")
        else:
            print(f"Backup already exists for {file_path}, skipping copy.")

    def process_directory(self, directory):
        # Walk through the directory and process files that match the target size.
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = Path(root) / file
                # Check if the current file matches the target size.
                if file_path.is_file() and os.path.getsize(file_path) == self.target_size:
                    # Backup and then potentially rename the file.
                    self.backup_file(file_path)
                    new_path = self.abbreviate_filename(file_path)
                    if new_path != file_path:
                        self.rename_file(file_path, new_path)

def main():
    # The main function to execute the directory processing.
    # Change working directory to where the script is located.
    script_directory = Path(__file__).parent
    os.chdir(script_directory)
    
    # Define the directory to scan and parameters for the target file size and path length.
    directory_to_scan = script_directory / 'path/to/your/directory'  # Modify with the actual directory you wish to scan.
    file_size = 1024  # Target file size in bytes to find matches.
    max_path_length = 255  # Maximum file path length allowed.

    # Instantiate the FilePathShortener and run it on the specified directory.
    shortener = FilePathShortener(file_size, max_path_length)
    shortener.process_directory(directory