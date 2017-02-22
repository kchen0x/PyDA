# pylint: disable=I0011,C0103,C0413,W0104,W0106

#%%
import pandas as pd

names1880 = pd.read_csv('data_set/names/yob1880.txt',
                        names=['name', 'sex', 'births'])
names1880[:5]

#%%
names1880.groupby('sex').births.sum()  # pylint: disable=I0011,E1101

#%%
years = range(1880, 2015)

pieces = []
columns = ['name', 'sex', 'births']

for year in years:
    path = 'data_set/names/yob%d.txt' % year
    frame = pd.read_csv(path, names=columns)

    frame['year'] = year
    pieces.append(frame)

names = pd.concat(pieces, ignore_index=True)
names[:5]

#%%
total_births = names.pivot_table(
    'births', index='year', columns='sex', aggfunc='sum')
total_births.tail()

#%%
total_births.plot(title='Total births by sex and year')

#%%


def add_prop(group):
    # integer devision will be round to integer
    births = group.births.astype(float)

    group['prop'] = births / births.sum()
    return group

names = names.groupby(['year', 'sex']).apply(add_prop)
names[:5]

#%% Validation check
import numpy as np

np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1)

#%%
pieces = []
for year, group in names.groupby(['year', 'sex']):
    pieces.append(group.sort_values(by='births', ascending=False)[:1000])
top1000 = pd.concat(pieces, ignore_index=True)
top1000[:5]

#%%
boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']

total_births = top1000.pivot_table(
    'births', index='year', columns='name', aggfunc='sum')
total_births[:5]

#%%
subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
subset.plot(subplots=True, figsize=(8, 8), grid=False,
            title='Number of births per year')
# they are interesting graphs, which seems like they were no longer the
# famous names in America, but truth could be much complicated

#%%
table = top1000.pivot_table('prop', index='year', columns='sex', aggfunc='sum')
table.plot(title='Sum of table1000.prop by year and sex',
           yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 20))
# people are no long willing to give the common names to their children

#%% calculate the cumsum of prop first, then find the accumulation of 0.5, so we can know how many names consist of the 50% over all the names
df = boys[boys.year == 2014]
prop_cumsum = df.sort_values(by='prop', ascending=False).prop.cumsum()
prop_cumsum.searchsorted(0.5)[0] + 1

#%% compare the result above in 1900
df = boys[boys.year == 1900]
df.sort_values(by='prop', ascending=False).prop.cumsum(
).searchsorted(0.5)[0] + 1

#%%


def get_quantile_count(group, q=0.5):
    return group.sort_values(by='prop', ascending=False).prop.cumsum().searchsorted(q)[0] + 1

diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')
diversity.plot(title='Diversity - Number of popular names in top 50%')

#%%
get_last_letter = lambda x: x[-1]
last_letters = names.name.map(get_last_letter)
last_letters.name = 'last_letter'

table = names.pivot_table('births', index=last_letters, columns=[
                          'sex', 'year'], aggfunc='sum')

# get representative 3 years data
subtable = table.reindex(columns=[1910, 1960, 2010], level='year')
subtable[:5]

#%% normalization
letter_prop = subtable / subtable.sum().astype(float)

import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 1, figsize=(8, 10))
letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1],
                      title='Female', legend=False)
# boy's name end up with 'n' changed a lot at 2010

#%% using the full talbe to check last letter of d, n, y
letter_prop = table / table.sum().astype(float)

dny_ts = letter_prop.ix[['d', 'n', 'y'], 'M'].T
dny_ts.plot()

#%%
all_names = top1000.name.unique()
mask = np.array(['lesl' in x.lower() for x in all_names])
lesley_like = all_names[mask]
lesley_like

#%%
filtered = top1000[top1000.name.isin(lesley_like)]
filtered.groupby('name').births.sum()

#%%
table = filtered.pivot_table(
    'births', index='year', columns='sex', aggfunc='sum')
table = table.div(table.sum(1), axis=0)
table.plot(title='The gender of Lesley-like name',
           style={'M': 'k-', 'F': 'k--'})
# it seems lesley-like names changed from male to female
