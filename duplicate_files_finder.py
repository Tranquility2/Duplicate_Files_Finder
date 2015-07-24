"""
    Simple duplicate files finder
    Python Version: 2.7
"""
__license__ = "GPL"
__version__ = "0.6"
__status__ = "Prototype"


import os
import hashlib
import collections
import argparse


def get_file_hash(file_path, block_size=2**20):
    """
    Returns the hash of a given file
    :rtype : string of double length, containing only hexadecimal digits
    :param file_path: location of the file
    :param block_size: block size to use for buffer
    :return: hex digest of file hash
    """
    md5_hash = hashlib.md5()
    # open the file
    with open(file_path, "rb") as file_to_check:
        while True:
            # read file contents
            file_buffer = file_to_check.read(block_size)
            if not file_buffer:
                break
            # update file md5
            md5_hash.update(file_buffer)

    return md5_hash.hexdigest()


def unique_file_finder(search_location_path, calculate_file_function):
    """
    Used to build a dictionary of files based on a file property,
    for example: md5 based hash
    :rtype : dictionary
    :param search_location_path: location to scan
    :param calculate_file_function: function used to categorized the file
    :return: property based files dictionary
    """
    # setup default dictionary
    files_dictionary = collections.defaultdict(list)
    # read file names in the directories
    for dir_name, sub_directory_list, file_list in os.walk(search_location_path):
        for file_name in file_list:

            file_path = os.path.join(dir_name, file_name)

            if os.path.isfile(file_path):
                # get the file property using calculate_file_function (size/hash)
                calculate_file_info = calculate_file_function(file_path)
                # append the file name to the existing list
                files_dictionary[calculate_file_info].append(file_path)

    return files_dictionary


def find_duplicate_files(files_location_path, unique_dictionary_function, calculate_file_function,
                         filter_duplicates=True):
    """
    Returns a list of files based on unique property,
    for example: md5 based hash
    :param files_location_path: location to scan
    :param unique_dictionary_function: function used build the dictionary
    :param calculate_file_function: function used to categorized the file
    :param filter_duplicates: Output filters only lists of duplicates
    """
    dict_unique_file = unique_dictionary_function(files_location_path, calculate_file_function)

    if filter_duplicates:
        filter_result = filter(lambda x: len(x) > 1, dict_unique_file.values())
        return filter_result
    else:
        return dict_unique_file


def print_duplicate_files_tester(test_location_path, unique_dictionary_function, calculate_file_function):
    """
    Used for testing (output full dictionary info)
    Creates a list of files based on unique property,
    for example: md5 based hash
    :param test_location_path: location to scan
    :param unique_dictionary_function: function used build the dictionary
    :param calculate_file_function: function used to categorized the file
    """
    dictionary_unique_file = find_duplicate_files(test_location_path, unique_dictionary_function,
                                                  calculate_file_function, False)

    for key, value in dictionary_unique_file.iteritems():
        print '{0: <16} | {1}'.format(key, value)

    print 'Total of {} items\n'.format(len(dictionary_unique_file))


def print_duplicate_files(test_location_path, unique_dictionary_function):
    """
    Used for testing (output full dictionary info)
    Creates a list of files based on unique property,
    for example: md5 based hash
    :param test_location_path: location to scan
    :param unique_dictionary_function: function used build the dictionary
    """
    dictionary_unique_file = find_duplicate_files(test_location_path, unique_dictionary_function,
                                                  get_file_hash, True)

    for duplicate_items in dictionary_unique_file:
        print duplicate_items

    print 'Total of {} items\n'.format(len(dictionary_unique_file))


def main():
    """
    Handle basic operation using arguments
    """
    parser = argparse.ArgumentParser(description="Find duplicate files")

    parser.add_argument("dir", action="store", type=str, help="directory to search")
    parser.add_argument("-t", "--test", help="test in directory", action="store_true")

    args = parser.parse_args()

    if args.dir and args.test:
        print_duplicate_files_tester(args.dir, unique_file_finder, os.path.getsize)
        print_duplicate_files_tester(args.dir, unique_file_finder, get_file_hash)
        print_duplicate_files(args.dir, unique_file_finder)
    else:
        print_duplicate_files(args.dir, unique_file_finder)


if __name__ == '__main__':
    main()
