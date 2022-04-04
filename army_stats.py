import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

army_df = pd.read_csv('army_dataframe')

print(army_df.head())

columns = army_df.columns.tolist()
columns = columns[2:14]
n=len(army_df.columns)
fig, ax = plt.subplots(figsize=(20,n*4))
pltrows = 3
pltcol = 4
counter = 1

for col in columns:
    plt.subplot(pltrows, pltcol, counter)
    sns.countplot(army_df[col].values)
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
 
