#!/usr/local/bin/python

import os
import sys
import zlib

def split_sfv(filename):
    file_crc = {}
    file = open(filename, 'r')
    for line in file.readlines():
        line = line.strip()
        rar_name, crc = line.split()
        file_crc[crc] = rar_name
    file.close()
    return file_crc 

def calc_crc(filename):
    prev = 0
    file = open(filename, 'rb')
    for line in file.readlines():
        prev = zlib.crc32(line, prev)
    crc = "%x" % (prev & 0xFFFFFFFF)
    if len(crc) == 7:
        # Zero pad if CRC value return is only 7 characters
        crc = "0" + crc
    return crc

def fetch_files(directory):
    files = []
    all_the_things = os.listdir(directory)
    for thing in all_the_things:
        if os.path.isfile(thing):
            files.append(thing)
        else:
            pass
    return files

def generate_file_crcs(files):
    file_crc = {}
    for file in files:
        print "Generating CRC for %s: " % (file),
        crc = calc_crc(file)
        print "%s" % (crc)
        file_crc[crc] = file
    return file_crc

def compare_sfv_to_files(sfv_files, other_files):
    fake_to_real_names = {}
    found_count = len(sfv_files.keys())
    not_found_count = 0 
    print "%d files found in SFV" % (found_count)
    for crc, rar_name in sfv_files.iteritems():
        if crc in other_files:
            print "%s is %s" % (rar_name, other_files[crc])
            fake_name = other_files[crc]
            fake_to_real_names[fake_name] = rar_name
        else:
            print "%s was not found" % (rar_name)
            not_found_count += 1
    print "%d of %d files found." % (found_count - not_found_count, found_count)
    return fake_to_real_names

def renamer(fake_to_real_names):
    for fake_name, real_name in fake_to_real_names.iteritems():
        print "Renaming %s to %s" % (fake_name, real_name)
        os.rename(fake_name, real_name)
    
def main(argv):
    file_crc = split_sfv(argv[0])
    files = fetch_files('.')
    other_file_crc = generate_file_crcs(files)
    fake_to_real_names = compare_sfv_to_files(file_crc, other_file_crc)
    renamer(fake_to_real_names)

if __name__ == "__main__":
    main(sys.argv[1:])
