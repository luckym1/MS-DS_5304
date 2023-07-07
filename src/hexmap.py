import altair
import os
import altair_viewer

class Map:

    def __init__(self, data):
        self.data = data

    def run(self, save_path=None):

        size = 15
        hexagon = "M0,-2.3094010768L2,-1.1547005384 2,1.1547005384 0,2.3094010768 -2,1.1547005384 -2,-1.1547005384Z"
            
        # create the map
        map = altair.Chart(self.data).mark_circle(size=3).encode(
            longitude='Y:Q',
            latitude='X:Q'
        ).project(
            type='mercator'
        )

        # if there is a save path, save the plot
        # if save_path:

        #     # if the path has an extension treat it as a file
        #     if '.' in save_path.split('/')[-1]:

        #         # check the extension is png
        #         extension = save_path.split('/')[-1].split('.')[-1]
        #         if extension != 'png':
        #             raise ValueError(f'Can only save in png format not {extension}')

        #     # otherwise treat it as a directory
        #     else:
        #         save_path = os.path.join(save_path, 'map.png')

        #     # check the directory exists
        #     if not os.path.exists(os.path.dirname(save_path)):
        #         # make the directory
        #         os.makedirs(os.path.dirname(save_path))
            
        #     # save the plot
        #     map.save(save_path)

        # # otherwise show the plot
        # else:
        altair_viewer.show(map)
