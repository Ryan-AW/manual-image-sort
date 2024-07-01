''' copy a file to multiple directories then delete the original file '''
from shutil import copy2, move


def copy_move(input_file, *output_directories):
    ''' copy input_file to each of the output_directories then deletes the input_file '''
    if output_directories:
        last_directory = output_directories[0]
        for directory in output_directories[1:]:
            copy2(input_file, directory)
        move(input_file, last_directory)
