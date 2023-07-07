import pandas
import matplotlib.pyplot as plt
import math
import os

class Radar:

    def __init__(self, data: pandas.DataFrame) -> None:
        self.data: pandas.DataFrame = data

    def run(self, save_path: str = None) -> None:

        # create a figure and axis
        fig, ax = plt.subplots(2, figsize=(10, 10), subplot_kw=dict(polar=True))

        # create one plot with the amount of subplots per data frames in data
        for i, d in enumerate(self.data):

            # get the number of categories minus the plot color if it is there
            if 'plot_color' in d.columns:
                num_labels = len(d.columns) - 1
            else:
                num_labels = len(d.columns)

            # convert the labels to radians
            angles = [x / float(num_labels) * 2 * math.pi for x in range(num_labels)]
            angles += angles[:1]

            # create the radar plot
            handles = []
            d_no_color = d.loc[:, d.columns != 'plot_color']
            for j, (row, color) in enumerate(zip(d_no_color.values, d['plot_color'].values)):

                # plot the values
                values = row.flatten().tolist()
                values += values[:1]
                handles.append(ax[i-1].plot(angles, values, linewidth=1, linestyle='solid', label=d.index[j], color=color)[0])
                ax[i-1].fill(angles, values, alpha=0.25, color=color)

            # fix the axis to go in the right order and start at 12 o'clock
            ax[i-1].set_theta_offset(math.pi / 2)
            ax[i-1].set_theta_direction(-1)

            # draw axis lines for each angle and label
            labels = d.index.tolist()
            ax[i-1].set_thetagrids([a * 180 / math.pi for a in angles[:-1]], list(d_no_color), size=10)

            # add the legend
            ax[i-1].legend(handles=handles, bbox_to_anchor=(1.1, 1.1))

            # set the ticks and limits
            ax[i-1].set_rticks([10, 20, 30, 40, 50], ['%10', '%20', '%30', '%40', '%50'], color='grey', size=10)
            ax[i-1].set_rlim(0, 50)

            # set the angle of the r axis labels
            ax[i-1].set_rlabel_position(0)

            # set the title
            if d.index.name == 'Primary Fur Color':
                ax[i-1].set_title('Primary Fur Color', size=15)
            elif d.index.name == 'Age':
                ax[i-1].set_title('Age', size=15)
            else:
                ax[i-1].set_title('', size=15)

        # set the title and tight layout
        fig.suptitle('Squirrel Behavior Percentage\nAcross Color and Age', size=20)
        fig.tight_layout()

        # if there is a save path, save the plot
        if save_path:

            # if the path has an extension treat it as a file
            if '.' in save_path.split('/')[-1]:

                # check the extension is png
                extension = save_path.split('/')[-1].split('.')[-1]
                if extension != 'png':
                    raise ValueError(f'Can only save in png format not {extension}')

            # otherwise treat it as a directory
            else:
                save_path = os.path.join(save_path, 'radar.png')

            # check the directory exists
            if not os.path.exists(os.path.dirname(save_path)):
                # make the directory
                os.makedirs(os.path.dirname(save_path))
            
            # save the plot
            plt.savefig(save_path, bbox_inches='tight')

        # show the plot
        plt.show()