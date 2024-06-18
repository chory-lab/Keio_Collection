# Keio_Collection
Code and mapping for transferring of Keio Collection plates

data_reader_5000.py is used to read plate mapping from excel files and convert it into a csv file that is readable by old_to_newinator_6000.py to feed into the hamilton star.
 - An example of a formatted excel file to feed into the code is keio_collectionsheet-1.xlsx under the Excel folder

old_to_newinator_6000.py is used to read formatted csv files and convert it to pyhamilton commands for groupings of 4 plates at a time.
- An example of a formatted csv file to feed into old_to_newinator_6000.py is combine_list_map.csv under CSV Files 
