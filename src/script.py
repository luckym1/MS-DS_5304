import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy
import altair as alt

SAVE_PATH = pathlib.Path(__file__).parent.parent / 'output'
if not SAVE_PATH.exists():
    SAVE_PATH.mkdir()
    
DATA_PATH = pathlib.Path(__file__).parent.parent / 'data' / '2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv'

def sub_plot_radar(data: pd.DataFrame, ax: numpy.ndarray, colors: dict, title: str, i: int) -> None:

    # convert the labels to radians
    angles = [x / float(data.shape[1]) * 2 * math.pi for x in range(data.shape[1])]
    angles += angles[:1]

    handles = []
    for j, row in enumerate(data.values):
    
        # plot the values
        values = row.flatten().tolist()
        values += values[:1]
        handles.append(ax[i-1].plot(angles, values, linewidth=1, linestyle='solid', label=data.index[j], color=colors[data.index[j]])[0])
        ax[i-1].fill(angles, values, alpha=0.25, color=colors[data.index[j]])

    # fix the axis to go in the right order and start at 12 o'clock
    ax[i-1].set_theta_offset(math.pi / 2)
    ax[i-1].set_theta_direction(-1)

    # draw axis lines for each angle and label
    ax[i-1].set_thetagrids([a * 180 / math.pi for a in angles[:-1]], list(data), size=10)

    # add the legend and set the ticks and limits
    ax[i-1].legend(handles=handles, bbox_to_anchor=(1.1, 1.1))
    ax[i-1].set_rticks([10, 20, 30, 40, 50], ['%10', '%20', '%30', '%40', '%50'], color='grey', size=10)
    ax[i-1].set_rlim(0, 50)

    # set the angle of the r axis labels
    ax[i-1].set_rlabel_position(0)

    # set the title
    ax[i-1].set_title(title, size=15)

if __name__ == '__main__':

    # read in the data
    data = pd.read_csv(DATA_PATH)

    ############################################################################################
    ######### Create Radar Chart for Squirrel Behavior Percentage Across Color and Age #########

    # define the actions, colors, and ages
    actions = ['Running', 'Chasing', 'Climbing', 'Eating', 'Foraging']
    age_colors = {'Adult': 'tab:red', 'Juvenile': 'tab:blue'}
    fur_colors = {'Black': 'black', 'Cinnamon': 'tab:brown', 'Gray': 'tab:gray'}

    # group the data by color and age
    data_color = data[actions + ['Primary Fur Color']].groupby('Primary Fur Color').sum().loc[fur_colors.keys()]
    data_age = data[actions + ['Age']].groupby('Age').sum().loc[age_colors.keys()]

    # change from totals to percentages as decimal out of 100
    data_color = data_color / data_color.sum(axis=1).values.reshape(-1, 1) * 100
    data_age = data_age / data_age.sum(axis=1).values.reshape(-1, 1) * 100

    # create a figure and axis
    fig, ax = plt.subplots(2, figsize=(10, 10), subplot_kw=dict(polar=True))
        
    # plot the fur color data
    sub_plot_radar(data_color, ax, fur_colors, 'Primary Fur Color', 0)

    # plot the age data
    sub_plot_radar(data_age, ax, age_colors, 'Age', 1)

    # set the title and tight layout
    fig.suptitle('Squirrel Behavior Percentage\nAcross Color and Age', size=20)
    fig.tight_layout()

    # save the plot
    plt.savefig(SAVE_PATH / 'radar.png', bbox_inches='tight')

    ############################################################################################

    ############################################################################################
    ############## Create the hexbin plot for squirrel sightings across the park  ##############

    hexbin_path = SAVE_PATH / 'plot.html'

    # create a selector
    selector = alt.selection_point(empty=True, fields=['Primary Fur Color'])

    # make sure the black squirrels have black plots, cinnamon squirrels have brown plots, and gray squirrels have gray plots
    colors_obj = alt.Color(
        'Primary Fur Color:N',
        scale=alt.Scale(
            domain=['Black', 'Cinnamon', 'Gray'],
            range=['black', 'brown', 'gray']
        )
    )

    colors = alt.condition(selector, colors_obj, alt.value('lightgray'))

    chart = alt.Chart(data).mark_circle(size=10).encode(
        x=alt.X('X', scale=alt.Scale(domain=[-73.985, -73.945]), title='Latitude'),
        y=alt.X('Y', scale=alt.Scale(domain=[40.760, 40.805]), title='Longitude'),
        color=colors,
        tooltip=['Primary Fur Color', 'Age', 'Running', 'Chasing', 'Climbing', 'Eating', 'Foraging']

    ).properties(
        title='Squirrel Sightings in Cental Park'
    ).add_params(
        selector
    )
    
    chart.save(
        str(hexbin_path)
    )

    ############################################################################################
    