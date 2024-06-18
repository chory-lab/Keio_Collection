def empty_val_assignment(k_val, b_val, new_df, x_range, y_range):
    i = 0
    for d in new_df:
        for y in range(y_range):
           for x in range(x_range):
               if str(d.iloc[x, y]) == 'nan' and x%2==0:
                   d.iloc[x, y] = k_val
                   d.iloc[x+1, y] = b_val
                   return i, x, y, False
               elif str(d.iloc[x, y]) == 'wild_type' and x % 2 == 0:
                   d.iloc[x, y] = k_val
                   d.iloc[x + 1, y] = b_val
                   return i, x, y, True
        i = i + 1