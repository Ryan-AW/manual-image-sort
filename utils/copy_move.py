def copy_move(input_file, *output_directories):
    if output_directories:
        last_directory = output_directories[0]
        for directory in output_directories[1:]:
            print('COPY:', input_file, '--->', directory)
        print('MOVE:', input_file, '--->', last_directory)
    else:
        raise KeyError('output directories must be specified')
