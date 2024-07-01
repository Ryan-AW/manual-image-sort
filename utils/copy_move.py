from shutil import copy2, move


def copy_move(input_file, *output_directories):
    if output_directories:
        last_directory = output_directories[0]
        for directory in output_directories[1:]:
            copy2(input_file, directory)
        move(input_file, last_directory)
