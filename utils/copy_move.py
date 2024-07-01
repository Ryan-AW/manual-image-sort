def copy_move(input_file, *output_directories):
    if output_directories:
        last_directory = output_directories.pop()
        for directory in output_directories:
            print('COPY:', input_file, '--->', directory)
        print('MOVE:', input_file, '--->', last_directory)
    else:
        raise KeyError('output directories must be specified')
