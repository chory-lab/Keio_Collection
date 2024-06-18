import csv
import sys
from collections import defaultdict

#may have to be adjusted depending where pyhamilton is located in your file structure
sys.path.insert(0, 'C:/Users/Hamilton- AA36/pyhamilton')
from pyhamilton import *

# initialization of objects from .lay file
old_plates = []
new_plates = []
tip_racks = []

#standard liq class for water for 300ul tip
liq_class = 'StandardVolumeFilter_Water_DispenseSurface_Empty'

#getting deck and mapping info
lmgr = LayoutManager('Test_1.lay')

#assign plate values
for x in range(4):
    old_plates.append(layout_item(lmgr, Plate96, 'Nun_96_Fl_HB_000%s_Orig'%(x+1)))
    new_plates.append(layout_item(lmgr, Plate96, 'Nun_96_Fl_HB_000%s_New'%(x+1)))

#assign tip rack values
for x in range(4):
    tip_racks.append(layout_item(lmgr, Tip96, 'STF_L_000%s'%(x+1)))

# reading in the columns from the combined_list_map
columns = defaultdict(list)
with open('combined_list_map.csv', mode='r', encoding='utf8') as csvfile:
    csvFile = csv.DictReader(csvfile) #read rows in dict format
    for row in csvFile:               #read a row as {column1: value1, column2:v value2,...}
        for (k, v) in row.items():    #go over each column name and value
            columns[k].append(v)

# assigning columns vals from combined_list_map
orig_row_column = columns['orig_col_row']
new_row_column = columns['new_col_row']
giving_plates = columns['orig_plate']
receiving_plates = columns['new_plate']
genotype = columns['genotype']
successfully_transferred = columns['successfully_transferred']


# converts plate coords to well number i.e. [A,1] -> 0, [A,2] -> 8
def coords_converter(coords):
    row = ord(coords[2]) - 65

    try:
        column = int(coords[6:8]) - 1
    except:
        column = int(coords[6]) - 1

    return row+column*8


# passes 8 channel commands to hamilton and marks off successful transfers
def call_robot(tip_8, aspirate_8, dispense_8, vol_8, trans_index):
    tip_pick_up(ham_int, tip_8)
    aspirate(ham_int, aspirate_8, vol_8, liquidClass=liq_class, liquidHeight=0)
    dispense(ham_int, dispense_8, vol_8, liquidClass=liq_class, liquidHeight=0, mixCycles=3, mixVolume=70)
    tip_eject(ham_int)

    r = csv.reader(open('combined_list_map.csv'))
    lines = list(r)

    # # changes no to yes values for succesful transfers and then writes to csv file
    for i in range(len(trans_index)):
        if trans_index[i] != None:
            lines[trans_index[i]+1][11] = 'yes'

    with open('combined_list_map.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(lines)


if __name__ == '__main__':
    with HamiltonInterface(simulate=True) as ham_int:
        normal_logging(ham_int, os.getcwd())
        initialize(ham_int)

        transferred_index = []
        tips = []
        aspirate_wells = []
        dispense_wells = []
        vol = []
        count = 0

        starting_new_plate = 0
        starting_old_plate = 0

        # assign starting donor and receiver plates to serve as reference for .lay objects
        for i in range(len(giving_plates)):
            if successfully_transferred[i] == 'no':
                starting_new_plate = int(receiving_plates[i])-1
                starting_old_plate = int(giving_plates[i])-1
                break

        # 8 channel assignment logic handling by parsing through combined_list_map
        for i in range(len(giving_plates)+1):
            # reached end of list
            if i == len(giving_plates):
                while len(vol) != 8:
                    aspirate_wells.append(None)
                    dispense_wells.append(None)
                    tips.append(None)
                    vol.append(None)
                    transferred_index.append(None)

                call_robot(tips, aspirate_wells, dispense_wells, vol, transferred_index)

                input('Reached end')

            # manual stop call
            elif successfully_transferred[i] == 'stop':

                while len(vol) != 8:
                    aspirate_wells.append(None)
                    dispense_wells.append(None)
                    tips.append(None)
                    vol.append(None)
                    transferred_index.append(None)

                call_robot(tips, aspirate_wells, dispense_wells, vol, transferred_index)

                input('Reached stop')

            # handler for non-transferred non wild_type transfer
            elif genotype[i] != 'wild_type' and successfully_transferred[i] == 'no':

                if len(vol) == 8:
                    call_robot(tips, aspirate_wells, dispense_wells, vol, transferred_index)

                    tips = []
                    aspirate_wells = []
                    dispense_wells = []
                    vol = []
                    transferred_index = []

                # reading in donor well and donor plate numbers
                orig_well = coords_converter(orig_row_column[i])
                orig_plate = int(giving_plates[i])-1

                # reading in receiving well and plate numbers
                new_well = coords_converter(new_row_column[i])
                new_plate = int(receiving_plates[i]) - 1

                # triggered when 4 plates have been processed
                if (orig_plate-starting_old_plate == 4 or new_plate-starting_new_plate == 4) and orig_plate != 0 and new_plate != 0:
                    while len(vol) != 8:
                        aspirate_wells.append(None)
                        dispense_wells.append(None)
                        tips.append(None)
                        vol.append(None)
                        transferred_index.append(None)

                    call_robot(tips, aspirate_wells, dispense_wells, vol, transferred_index)

                    tips = []
                    aspirate_wells = []
                    dispense_wells = []
                    vol = []
                    transferred_index = []

                    input('Swap out plates')

                tip_rack = tip_racks[orig_plate - starting_old_plate]

                # appending vals to list to be passed to robot
                tips.append((tip_rack, orig_well))
                aspirate_wells.append((old_plates[orig_plate-starting_old_plate], orig_well))
                dispense_wells.append((new_plates[new_plate-starting_new_plate], new_well))
                vol.append(100)
                transferred_index.append(i)

            # handler for wild_type (do nothing as
            elif genotype[i] == 'wild_type' and successfully_transferred[i] == 'no':
                if len(vol) == 8:
                    call_robot(tips, aspirate_wells, dispense_wells, vol, transferred_index)

                    tips = []
                    aspirate_wells = []
                    dispense_wells = []
                    vol = []
                    transferred_index = []

                aspirate_wells.append(None)
                dispense_wells.append(None)
                tips.append(None)
                vol.append(None)
                transferred_index.append(i)