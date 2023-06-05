name='PCR123_CYP2C19 230009 + 230010 -  A D Results_ADSheet.csv'
pattern_len = len('PCR')
for idx, c in enumerate(name[pattern_len:]):
    if not c.isnumeric():
        break
batch_id = name[pattern_len:pattern_len+idx]
print(batch_id)