import argparse
import hexmap
import pandas
import radar as radar

# create a method to contain the parser
def parse_args():
    # create the parser
    parser = argparse.ArgumentParser(description='Visualize the results of 2018 NYC Central Park Squirrel Census')

    # add the arguments
    parser.add_argument('data', type=str, help='The path to the data file')
    parser.add_argument('-t', '--type', type=str, help='Choose which visualization to run', default='map', choices=['map', 'm', 'radar', 'r'])
    parser.add_argument('-s', '--save', type=str, help='Save the visualization to the given path')
    
    # parse the arguments
    args = parser.parse_args()

    # return the arguments
    return args

# main method for the script
def main():
    args = parse_args()
    vis_type = args.type
    save_path = args.save
    data_path = args.data

    # read in the data
    data = pandas.read_csv(data_path)

    try:

        if vis_type in ['map', 'm']:

            # only use longitudes and latitudes as well as primary fur color
            data_coord = data[['X', 'Y', 'Primary Fur Color']]

            map = hexmap.Map(data_coord)
            map.run(save_path=save_path)

        elif vis_type in ['radar', 'r']:

            # clean data set. One data frame with [Running, Chasing, Climbing, Eating, Foraging] as columns and [Black, Cinnamon, Gray, Adult, Juvenile] totals per row
            labels = ['Running', 'Chasing', 'Climbing', 'Eating', 'Foraging']
            ages = ['Adult', 'Juvenile']
            colors = ['Black', 'Cinnamon', 'Gray']

            # group the data by color and age
            data_color = data[labels + ['Primary Fur Color']].groupby('Primary Fur Color').sum().loc[colors]
            data_age = data[labels + ['Age']].groupby('Age').sum().loc[ages]

            # change from totals to percentages as decimal out of 100
            data_color = data_color / data_color.sum(axis=1).values.reshape(-1, 1) * 100
            data_age = data_age / data_age.sum(axis=1).values.reshape(-1, 1) * 100

            # add a plot color for each row
            data_color['plot_color'] = ['black', 'tab:brown', 'tab:gray']
            data_age['plot_color'] = ['tab:red', 'tab:blue']
            
            data_set = [data_color, data_age]

            radar_chart = radar.Radar(data_set)
            radar_chart.run(save_path=save_path)


    except KeyboardInterrupt as e:
            
        exit(e)

# run the main method
if __name__ == '__main__':
    main()