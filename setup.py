import ipywidgets as widgets
from ipywidgets import interact, interact_manual,fixed
import ipywidgets as widgets
import pandas as pd
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.io import output_notebook

def bokeh_scatter(date,xaxis,yaxis):
    output_notebook()
    df=dfs[date]
    source = ColumnDataSource(
        data=dict(
            x=df[xaxis],
            y=df[yaxis],
            desc=df.index + ', ' + df['State'],
        )
    )

    hover = HoverTool(
        tooltips=[("County", "@desc"),
            (xaxis, "$x"),
            (yaxis,"$y"),
        ]
    )
    p = figure(plot_width=700, plot_height=700, tools=[hover],
           title="Mouse over the dots",x_axis_label=xaxis,y_axis_label=yaxis)
    p.circle('x', 'y', size=10, source=source)
    show(p)

    import matplotlib.pyplot as plt

def plot_time_series(df,list_of_counties,per_capita=True):
    if per_capita:
        ax=df.loc[list_of_counties].iloc[:,11:].div(dfs['04-01'].loc[list_of_counties,'Total Population'].values,axis=0).T.plot()
        ax.set_ylabel("Cumulative cases per capita")
    else:
        ax=df.loc[list_of_counties].iloc[:,11:].T.plot()
        ax.set_ylabel("Cumulative cases")


def make_plots(date,yaxis, xaxis,dfs):
    print(f"Correlation between {xaxis} and {yaxis}: {dfs[date][xaxis].corr(dfs[date][yaxis])}")
    dfs[date].plot(xaxis,yaxis,kind='scatter')
    plt.show()
    return  dfs[date][[xaxis,yaxis]].hist()

dfs=pd.read_pickle('dfs.pkl')
df_california=pd.read_csv('california.csv').set_index('County')
df_texas=pd.read_pickle('texas.pkl')

kwargs = {'date':widgets.Dropdown(options=dfs.keys(),value='07-25'),'yaxis':widgets.Dropdown(options=list(dfs['04-01'].select_dtypes('number').columns[2:]),value='Confirmed cases per 100,000 residents'),'xaxis':widgets.Dropdown(options=list(dfs['04-01'].select_dtypes('number').columns[2:]),value='% Population > 64 years'),'dfs':fixed(dfs)}