import plotly
from plotly.graph_objs import Pie, Layout
import pandas as pd


if __name__ == '__main__':
    # Read CSV file
    df = pd.read_csv('./data/summary.csv')
    
    # Collect data
    column_to_category_sums = {}

    for category in df.category.unique():
        category_df = df.loc[df['category'] == category]
        category_df = category_df.drop(['keyword', 'category'], axis = 1)
        
        for column in category_df:
            if column not in column_to_category_sums:
                column_to_category_sums[column] = {}

            if category not in column_to_category_sums[column]:
                column_to_category_sums[column][category] = {}

            column_to_category_sums[column][category] = category_df[column].sum()

    # Draw pie charts
    colors = ['#0984e3', '#f368e0', '#9b59b6', '#01a3a4', '#74b9ff']

    for column in column_to_category_sums:
        print('Plotting for ' + column)
        labels = []
        values = []

        for category in column_to_category_sums[column]:
            labels.append(category)
            values.append(column_to_category_sums[column][category])
        
        trace = Pie(labels=labels, values=values, textfont=dict(size=24), marker=dict(colors=colors, line=dict(color='#000000', width=0)))
        plotly.offline.plot({
            'data': [trace],
            'layout': Layout(title=column, font=dict(family='Courier New, monospace', size=18, color='#000000'))
        })

        input("Press Enter to continue...")