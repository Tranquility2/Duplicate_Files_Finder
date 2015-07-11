"""
    Simple duplicate files finder
    Python Version: 2.7
"""
__license__ = "GPL"
__version__ = "0.3"
__status__ = "Prototype"


import os
import hashlib
import collections


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


def unique_file_finder(search_location_path, calculate_file_function):
    # setup default dictionary
    files_dictionary = collections.defaultdict(list)
    # read file names in the directories
    for dir_name, sub_directory_list, file_list in os.walk(search_location_path):
        for file_name in file_list:

            file_path = r'{0}\{1}'.format(dir_name, file_name)

            if os.path.isfile(file_path):
                # get the file property using calculate_file_function (size/hash)
                calculate_file_info = calculate_file_function(file_path)
                # append the file name to the existing list
                files_dictionary[calculate_file_info].append(file_path)

    return files_dictionary


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
    dir_location = r'C:\demo_dup'
    #unique_file_tester_print(dir_location, unique_file_finder, os.path.getsize)
    #unique_file_tester_print(dir_location, unique_file_finder, get_file_hash)
    get_duplicate_files(dir_location, unique_file_finder, get_file_hash)

