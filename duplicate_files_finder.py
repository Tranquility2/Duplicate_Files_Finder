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


def find_duplicate_files_by_location(search_location_path, calculate_file_function):
    """
    Used to build a dictionary of files based on a file property,
    for example: md5 based hash
    :rtype : dictionary
    :param search_location_path: location to scan
    :param calculate_file_function: function used to categorized the file
    :return: property based files dictionary
    """
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


def find_duplicate_files_in_list(file_group_list, calculate_file_function):
    """
    Used to build a dictionary of files based on a file property from a given list,
    for example: md5 based hash
    :rtype : dictionary
    :param file_group_list: a list of lists that specify file location
    :param calculate_file_function: function used to categorized the file
    :return: property based files dictionary
    """
    files_dictionary = collections.defaultdict(list)

    for file_group in file_group_list:
        for file_path in file_group:
            if os.path.isfile(file_path):
                # get the file property using calculate_file_function (size/hash)
                calculate_file_info = calculate_file_function(file_path)
                # append the file name to the existing list
                files_dictionary[calculate_file_info].append(file_path)

    return files_dictionary


def print_duplicate_files_tester(test_location_path, calculate_file_function):
    """
    Used for testing (output full dictionary info)
    Prints a list of files based on unique property,
    for example: md5 based hash
    :rtype : string
    :param test_location_path: location to scan
    :param calculate_file_function: function used to categorized the file
    :return: formatted string containing summary
    """
    dictionary_unique_file = find_duplicate_files_by_location(test_location_path, calculate_file_function)

    for key, value in dictionary_unique_file.iteritems():
        print '{0: <16} | {1}'.format(key, value)

    return 'Total of {} items\n'.format(len(dictionary_unique_file))


def print_duplicate_files(test_location_path):
    """
    Prints a list of files based on md5 hash
    This uses 2 iteration:
    1st filter duplicated files by size (very fast)
    2nd part is to filter this list using hash to get better results (can be slow)
    --This way it will try and limit the number of files that we need to hash
    :rtype : string
    :param test_location_path: location to scan
    """
    # get list of unique files by size
    unique_files_list = find_duplicate_files_by_location(test_location_path, os.path.getsize)
    filtered_unique_files_list = filter(lambda x: len(x) > 1, unique_files_list.values())
    # improve the list by using hash
    dictionary_unique_file_improved = find_duplicate_files_in_list(filtered_unique_files_list, get_file_hash)
    filtered_dictionary_unique_file_improved = filter(lambda x: len(x) > 1, dictionary_unique_file_improved.values())

    for duplicate_items in filtered_dictionary_unique_file_improved:
        print duplicate_items

    return 'Total of {} items ({} items on 1st check)\n'.format(len(dictionary_unique_file_improved),
                                                                len(unique_files_list))


def main():
    """
    Handle basic operation using arguments
    """
    parser = argparse.ArgumentParser(description="Find duplicate files")

    parser.add_argument("dir", action="store", type=str, help="directory to search")
    parser.add_argument("-t", "--test", help="test in directory", action="store_true")

    args = parser.parse_args()

    if args.test:
        print print_duplicate_files_tester(args.dir, os.path.getsize)
        print print_duplicate_files_tester(args.dir, get_file_hash)

    print_duplicate_files(args.dir)


if __name__ == '__main__':
    main()
