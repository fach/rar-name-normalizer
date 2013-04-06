RAR Filename Normalizer
===================

Imagine you had a rar archive split across multiple files with arbitrary filenames/extensions.
Imagine you also had a .sfv file containing the actual filenames and crc32 value for each file.
In order to decompress this archive, these files need to be renamed with the proper name/extension.

This script:   

1.  Takes a SFV file as an argument
2.  Pulls all files in the local directory
3.  Calculates the crc value of each file
4.  Iterates through the SFV file and attempts to match each crc value listed with that of a local file
5.  If there is a match, the local filename is renamed with the correct filename from the SFV 
