"""
    Simple duplicate files finder
    Python Version: 2.7
"""
__license__ = "GPL"
__version__ = "0.1"
__status__ = "Prototype"


import os
import hashlib


def get_file_hash(file_name, block_size=2**20):

    md5_hash = hashlib.md5()

    with open(os.path.join(file_name), "rb") as file_to_check:
        # read file contents
        while True:
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
            if not os.path.isdir(item):
                # get the file property using func (size/hash)
                file_prop = calculate_file_function(item)
                if file_prop in files_dict:
                    # append the file name to the existing array
                    files_dict[file_prop].append(item)
                else:
                    # create a new array
                    files_dict[file_prop] = [item]

    return files_dict


def dir_tester_print(test_location, func_dict, func_prop):

    dict_unique_file = func_dict(test_location, func_prop)
    max_string_len = len(str(max(dict_unique_file)))

    for key, value in dict_unique_file.iteritems():
        string_space_needed = max_string_len - len(str(key))
        print "%s%s | %s" % (str(key), " " * string_space_needed, str(value))
    print "Total of %s items" % len(dict_unique_file)


def get_duplicates(test_location, func_dict, func_prop):
    counter = 0

    dict_unique_file = func_dict(test_location, func_prop)

    for key, value in dict_unique_file.iteritems():
        if len(value) > 1:
            counter += 1
            print value

    print "Total of %s items" % counter

dir_location = "C:\demo_dup"
dir_tester_print(dir_location, unique_file_finder, os.path.getsize)
dir_tester_print(dir_location, unique_file_finder, get_file_hash)
get_duplicates(dir_location, unique_file_finder, get_file_hash)

