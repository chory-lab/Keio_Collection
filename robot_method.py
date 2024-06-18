from pyhamilton import *
import pandas as pd

df = pd.read_csv('combined_list_map.csv')

liq_class = 'StandardVolumeFilter_Water_DispenseJet_Empty'

lmgr = LayoutManager('Test_1.lay')

old_plates = []
new_plates= []
tip_racks = []

old_plate_wells = {}
new_plate_wells = {}

#assign plate values
for x in range(5):
    old_plates.append(layout_item(lmgr, Plate96, 'Nun_96_Fl_HB_000%s_Orig'%(x+1)))
    new_plates.append(layout_item(lmgr, Plate96, 'Nun_96_Fl_HB_000%s_New'%(x+1)))

for plate in old_plates:
    for i in range(95):
        old_plate_wells.append((plate, i))


print(old_plate_wells[0])

#assign tip rack values
for x in range(6):
    tip_racks.append(layout_item(lmgr, Tip96, 'HT_L_000%s'%(x+1)))

tips = [(tip_racks[0], x) for x in range(8)]

wells_1 = [(plate_1, x) for x in range(8)]
wells_3 = [(plate_3, x) for x in range(8)]
vols = [30 for x in range(8)]
# a = serial.Serial("COM5", 9600, timeout=1)

if __name__ == '__main__':
    with HamiltonInterface(simulate=True) as ham_int:
        normal_logging(ham_int, os.getcwd())
        initialize(ham_int)

        tip_pick_up(ham_int, [(tip_carrier, 0)])
        aspirate(ham_int, [(plate_1, 0)], [30], liquidClass="HighVolume_Water_DispenseJet_Empty")
        dispense(ham_int, [(plate_1, 1)], [30], liquidClass="HighVolume_Water_DispenseJet_Empty")
        tip_eject(ham_int, tips)

        # move_plate(ham_int, plate_1, plate_2, gripHeight=10.0, gripWidth=80.0, gripMode=0, widthBefore = 100.0)
        #  grip_height=6.0, gripWidth=80.0, gripMode=0, widthBefore = 100.0

        # a.write(bytes('mv:ts 010\r', encoding='utf-8'))
        # requests.post(url, data='go_right')
        # move_plate(ham_int, plate_2, plate_1, gripHeight=10.0, gripWidth=80.0, gripMode=0, widthBefore = 100.0)

        # aspirate(ham_int, wells_1, vols, liquidClass="HighVolume_Water_DispenseJet_Empty")
        # dispense(ham_int, wells_3, vols, liquidClass="HighVolume_Water_DispenseJet_Empty")
        # move_by_seq(ham_int, 'Nun_96_FL_HB_0004_lid', 'Nun_96_FL_HB_0001_lid', grip_height=6.0, gripWidth=80.0, gripMode=0, widthBefore = 100.0)
