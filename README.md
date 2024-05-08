# Sorted Files

This Python script provides a file management utility for organizing files based on their extensions, removing duplicates, and handling existing file conflicts in specified directories.

## Features

- **File Extension Sorting**: Automatically categorizes files into folders based on their file extensions (e.g., PDF, JPG, TXT).
  
- **Duplicate File Handling**: Identifies and removes duplicate files within the same directory.

- **Existing File Management**: When encountering a naming conflict with an existing file, the script either backs up the existing file to a timestamped backup directory or renames it based on the file's creation time before moving the new file.

- **File Checksum Generation**: Computes and logs checksums (MD5) for files processed by the script.

- **Continuous Monitoring**: Monitors specified directories for new files, processing them periodically within a user-defined runtime limit.

## Key Functions

- `get_file_extension(file_path)`: Extracts the file extension from a given file path.
  
- `get_file_checksum(file_path)`: Calculates the MD5 checksum for a file.

- `move_file_to_directory(file_path, destination_directory)`: Moves a file to a specified destination directory, managing conflicts with existing files.

- `remove_numbered_files(directory_path)`: Deletes files with numbered names (e.g., (1).txt) within a specified directory.

- `organize_and_remove_duplicates(dir_path)`: Organizes files by extension, removes duplicates, and manages existing files in the specified directory.

- `watch_for_new_files(dir_path, max_runtime=10)`: Continuously monitors a directory for new files, processing them within a defined runtime limit.

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sorted_files.git
