# pylint: disable=I0011,C0103,C0413,W0104,W0106

#%%
path = 'data_set/usagov_bitly_data2013-05-17-1368832207'
open(path).readline()

#%%
import json
records = [json.loads(line) for line in open(path)]
records[0]

#%%
print records[0]['tz']

#%%
time_zones = [rec['tz'] for rec in records if 'tz' in rec]
time_zones[:10]

#%%


def get_counts(seq):
    counts_dict = {}
    for x in seq:
        if x in counts_dict:
            counts_dict[x] += 1
        else:
            counts_dict[x] = 1
    return counts_dict

counts = get_counts(time_zones)
counts['America/New_York']

#%%
len(time_zones)

#%%


def top_counts(counts_dict, n=10):
    count_pairs = [(count, tz) for tz, count in counts_dict.items()]
    count_pairs.sort()
    return count_pairs[-n:]

top_counts(counts)

#%%
from collections import Counter
counts = Counter(time_zones)
counts.most_common(10)

#%%
from pandas import DataFrame, Series
import pandas as pd
import numpy as np
frame = DataFrame(records)
frame

#%%
frame['tz'][:10]

#%%
tz_counts = frame['tz'].value_counts()
tz_counts[:10]

#%%
clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()
tz_counts[:10]

#%%
tz_counts[:10].plot(kind='barh', rot=0)

#%%
results = Series([x.split()[0] for x in frame.a.dropna()])
results[:5]

#%%
results.value_counts()[:10]

#%%
cframe = frame[frame.a.notnull()]
operating_system = np.where(cframe['a'].str.contains(
    'Windows'), 'Windows', 'Not Windows')
operating_system[:5]

#%% group tz by os / count group size for each tz / reshape
#   results / fill the NULL with 0
by_tz_os = cframe.groupby(['tz', operating_system])
agg_counts = by_tz_os.size().unstack().fillna(0)
agg_counts[:10]

#%% create index
indexer = agg_counts.sum(1).argsort()
indexer[:10]

#%% order by indexer incresely
count_subset = agg_counts.take(indexer)[-10:]
count_subset

#%%
count_subset.plot(kind='barh', stacked=True)

#%% normalized data to 1 with sum of each time_zone
normed_subset = count_subset.div(count_subset.sum(1), axis=0)
normed_subset.plot(kind='barh', stacked=True)
