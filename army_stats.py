import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

jsa_df = pd.read_csv('Japanese Secessionist Army_dataframe')
jsa_sub_df = pd.read_csv('Japanese Secessionist Army_sub-units_dataframe')
mil_orders_df = pd.read_csv('Military Orders_dataframe')
mil_orders_sub_df = pd.read_csv('Military Orders_sub-units_dataframe')


columns = jsa_df.columns.tolist()
columns = columns[3:15]
n=len(jsa_df.columns)
fig, ax = plt.subplots(figsize=(20,n*4))
pltrows = 3
pltcol = 4
counter = 1

for col in columns:
    plt.subplot(pltrows, pltcol, counter)
    sns.countplot(jsa_df[col].values)
    plt.xticks(rotation=45)
    plt.title(f'{col} Value Counts')
    counter +=1

plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.75)
fig.suptitle('JSA Stats')
plt.show()
plt.clf()

columns = mil_orders_df.columns.tolist()
columns = columns[3:15]
n=len(mil_orders_df.columns)
fig, ax = plt.subplots(figsize=(20,n*4))
pltrows = 3
pltcol = 4
counter = 1

for col in columns:
    plt.subplot(pltrows, pltcol, counter)
    sns.countplot(mil_orders_df[col].values)
    plt.xticks(rotation=45)
    plt.title(f'{col} Value Counts')
    counter +=1

plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.75)
fig.suptitle('Military Orders Stats')
plt.show()
plt.clf()