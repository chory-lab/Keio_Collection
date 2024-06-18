import pandas as pd
import math
import random
import numpy as np
from plate_parser import empty_val_assignment

df = pd.read_excel("C:/Users/Hamilton- AA36/Keyio_Collection/.venv/Scripts/keio_collectionsheet-1.xlsx")

plates = []
new_plates = [pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12)),pd.DataFrame(index=np.arange(16), columns=np.arange(12))]

i=0
#handle two random assignments of wild type per plate
for plate in new_plates:
    x = random.choice(range(0, 15, 2))
    y = random.randint(0, 11)

    x2 = random.choice(range(0, 15, 2))
    y2 = random.randint(0, 11)

    x3 = random.choice(range(0, 15, 2))
    y3 = random.randint(0, 11)

    #condition to handle if random coords are the same
    while(x == x2 and y == y2):
        x2 = random.choice(range(0, 15, 2))
        y2 = random.randint(0, 11)

    while(x == x3 and y == y3):
        x3 = random.choice(range(0, 15, 2))
        y3 = random.randint(0, 11)

    while(x2 == x3 and y2 == y3):
        x3 = random.choice(range(0, 15, 2))
        y3 = random.randint(0, 11)

    if i<3:
        plate.iloc[x, y] = 'wild_type'
        plate.iloc[x + 1, y] = 'wild_type'

        plate.iloc[x2, y2] = 'wild_type'
        plate.iloc[x2 + 1, y2] = 'wild_type'

    else:
        plate.iloc[x, y] = 'wild_type'
        plate.iloc[x+1, y] = 'wild_type'

        plate.iloc[x2, y2] = 'wild_type'
        plate.iloc[x2+1, y2] = 'wild_type'

        plate.iloc[x3, y3] = 'wild_type'
        plate.iloc[x3+1, y3] = 'wild_type'

    i = i + 1

for i in range(50):
    plates.append(df.iloc[40+(i*19):56+(i*19), 1:13])

i=0
row_list = []
for plate in plates:
    #parse and assign all non 'nan' vals to new plate
    for y in range(12):
        for x in range(16):
            if str(plate.iloc[x,y]) != 'nan' and x%2==0:
                new_plate, new_row, new_column, is_wild_type = empty_val_assignment(plate.iloc[x, y], plate.iloc[x+1, y], new_plates, 16, 12)

                if not(is_wild_type):
                    row_list.append([i+1, chr(ord('@')+int(x/2+1)), y+1, [chr(ord('@')+int(x/2+1)), y+1], plate.iloc[x, y], plate.iloc[x+1, y], new_plate+1, chr(ord('@')+int(new_row/2+1)), new_column+1, [chr(ord('@')+int(new_row/2+1)), new_column+1], 'no'])
                elif is_wild_type:
                    row_list.append(
                        [i + 1, chr(ord('@') + int(x / 2 + 1)), y + 1, [chr(ord('@') + int(x / 2 + 1)), y + 1], 'wild_type', 'wild_type', new_plate + 1, chr(ord('@') + int(new_row / 2 + 1)), new_column + 1, [chr(ord('@') + int(new_row / 2 + 1)), new_column + 1], 'no'])

    print('Plate ' + str(i))
    i += 1

combined_list = pd.DataFrame(row_list, columns=['orig_plate', 'orig_row', 'orig_col', 'orig_col_row', 'keio_name', 'genotype', 'new_plate', 'new_row', 'new_col', 'new_col_row', 'successfully_transferred'])

pd.concat([combined_list]).to_csv('combined_list_map.csv')
pd.concat(new_plates).to_csv('new_plates_map.csv')
pd.concat(plates).to_csv('old_plates_map.csv')
