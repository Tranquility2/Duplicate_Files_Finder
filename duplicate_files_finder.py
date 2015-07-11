"""
    Simple duplicate files finder
    Python Version: 2.7
"""
__license__ = "GPL"
__version__ = "0.2"
__status__ = "Prototype"


import os
import hashlib


def get_file_hash(file_name, block_size=2**20):

    md5_hash = hashlib.md5()

    with open(os.path.join(file_name), "rb") as file_to_check:
        while True:
            # read file contents
            file_buffer = file_to_check.read(block_size)
            if not file_buffer:
                break
            # update file md5
            md5_hash.update(file_buffer)

    return md5_hash.hexdigest()


def unique_file_finder(files_location_path, calculate_file_function):
    files_dict = {}

    try:
        os.chdir(files_location_path)
    finally:
        file_list = os.listdir(files_location_path)
        for item in file_list:
            if os.path.isfile(item):
                # get the file property using calculate_file_function (size/hash)
                file_prop = calculate_file_function(item)
                if file_prop in files_dict:
                    # append the file name to the existing array
                    files_dict[file_prop].append(item)
                else:
                    # create a new array
                    files_dict[file_prop] = [item]

    return files_dict


def unique_file_tester_print(test_location_path, unique_dictionary_function, calculate_file_function):

    dictionary_unique_file = unique_dictionary_function(test_location_path, calculate_file_function)

    for key, value in dictionary_unique_file.iteritems():
        print '{0: <16} | {1}'.format(key, value)

    print 'Total of {} items\n'.format(len(dictionary_unique_file))


def get_duplicate_files(files_location_path, unique_dictionary_function, calculate_file_function):

    dict_unique_file = unique_dictionary_function(files_location_path, calculate_file_function)

    filter_result = filter(lambda x: len(x) > 1, dict_unique_file.values())

    for duplicate_items in filter_result:
        print duplicate_items

    print 'Total of {} items\n'.format(len(filter_result))


if __name__ == '__main__':
    dir_location = "C:\demo_dup"
    unique_file_tester_print(dir_location, unique_file_finder, os.path.getsize)
    unique_file_tester_print(dir_location, unique_file_finder, get_file_hash)
    get_duplicate_files(dir_location, unique_file_finder, get_file_hash)

