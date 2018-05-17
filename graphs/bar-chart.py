import plotly
from plotly.graph_objs import Bar, Layout
import pandas as pd
import math


if __name__ == '__main__':
    df = pd.read_csv('./data/summary.csv')
    
    sources = list(df)
    sources.remove('keyword')
    sources.remove('category')

    row_sums = None
    for header in sources:
        if row_sums is not None:
            row_sums += df[header]
        else:
            row_sums = df[header]
    
    df = df.loc[row_sums > 0]

    colors = ['#0984e3', '#f368e0', '#9b59b6', '#01a3a4', '#74b9ff']   

    labels = list(df['keyword'])  

    data_points_at_chart = 10
    for i in range(math.ceil(df.shape[0] / data_points_at_chart)):
        traces = []
        start = i*data_points_at_chart
        end = min([(i+1)*data_points_at_chart, df.shape[0]])

        for j in range(len(sources)):
            source = sources[j]
            color = colors[j]
            values = list(df[source])
            traces.append(Bar(x=labels[start:end], y=values[start:end], name=source, marker=dict(color=color)))

        plotly.offline.plot({
            'data': traces,
            'layout': Layout(
                title='Word Counts - ' + str(i),
                barmode='group',
                bargroupgap=0.4,
                font=dict(family='Courier New, monospace', size=24, color='#000000')
            )
        })

        input("Press Enter to continue...")
    
    