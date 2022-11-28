import sys  # to allow for command line argument retrieval.		example: walkers = sys.argv[3]
import random  # to randomly select which 'direction' to go. 		example: random.choice(who['ways'])
import turtle  # to display the data points in a graphic window
import statistics  # to find the 'mean' and 'standard deviation' of data in the 'distances' list
import subprocess  # to save the turtle plot as an image


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def main():  # main() will only be called if this file (random_walk.py) is ran directly
    '''
    If this file 'Random Walk.py' is ran directly...
    Parameters:
    This function will retrieve 3 command line arguements.
    Then will call simulate() passing in those arguements.
    '''
    # If True - This will allow bypassing command line argument requirements. <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    testing = True
    # Retrieve command line arguements
    try:
        list_of_steps_per_trial = list(
            map(int, sys.argv[1].split(',')))  # Converts 'steps' from string into a list of integers
        walks_per_trial = int(sys.argv[2])  # Converts 'walks' from string into an integer
        walkers = sys.argv[3]
    # If any arguement is bad or missing  --- return Error..
    except:
        if testing:
            # manually set input variables
            list_of_steps_per_trial = [100, 1000]
            walks_per_trial = 50
            walkers = 'all'
        else:
            print(
                'Error: Ensure you enter "python3 random_walk.py <integer(steps)> <integer(walks)> <walker>".\nFor more details - See Module DOCSTRING')
            return
    # Simulates Random Walk algorithm
    simulate(walkers, walks_per_trial, list_of_steps_per_trial)


# End - main()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def simulate(walkers, walks_per_trial, list_of_steps_per_trial):
    ''' The Autograder calls this function with three arguments each time '''
    do_trials(walkers, walks_per_trial, list_of_steps_per_trial)
    plot()


# End - simulate()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def initialize(walkers, called_from_plot):
    '''
    Intitializes walkers (as dictionaries)
    Parameters:
    walkers 		 - A (list) of at least one walker dictionary. See below for more details.
    called_from_plot - If True - This modifies each the directions' increment value to +/-5, normally +/-1.
    '''
    # Assigns starting point and directions to variables
    start_point = [0, 0]
    north, east, south, west = ([0, 1], [1, 0], [0, -1], [-1, 0]) if not called_from_plot else (
    [0, 5], [5, 0], [0, -5], [-5, 0])

    ########## Assigns walker dictionaries ##########
    # ----------------------Pa-----------------------#
    _pa = {'name': 'Pa',
           'start': start_point,
           'now_point': [0, 0],
           'ways': (north, east, south, west),
           'end_points_for_100': [],
           'end_points_for_1000': []}
    # ---------------------Mi-Ma----------------------#
    _ma = {'name': 'Mi-Ma',
           'start': start_point,
           'now_point': [0, 0],
           'ways': (north, east, south, south, west),
           'end_points_for_100': [],
           'end_points_for_1000': []}
    # ----------------------Reg-----------------------#
    reg = {'name': 'Reg',
           'start': start_point,
           'now_point': [0, 0],
           'ways': (east, west),
           'end_points_for_100': [],
           'end_points_for_1000': []}
    ########### End - Dictionary assignment ##########

    # Assigns 'walkers' with the corresponding dictionary of (_pa, _ma, or reg) OR include all dictionaries
    if walkers == 'Pa':
        return [_pa]
    elif walkers == 'Mi-Ma':
        return [_ma]
    elif walkers == 'Reg':
        return [reg]
    elif walkers == 'all':
        return [_pa, _ma, reg]
    else:
        return print('please enter "Pa", "Mi-Ma", "Reg", or "all" for the <walkers> parameter.')


# End - initialize()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def do_trials(walkers, walks_per_trial, list_of_steps_per_trial, called_from_plot=False):
    '''
    Executes random walks for each walker, for each trail specified.
    Parameters:
    walkers 				- A (list) of at least one walker dictionary. See initialize() for more details.
    walks_per_trial			- An (integer) of how many walks will be simulated per trial.
    list_of_steps_per_trial - A (list) of integers indicating how many steps. Each list element/integer represents one trial.
    called_from_plot		- If True - Prevents 'result_data' from being printed twice. (this function is called twice)
    '''
    walkers = initialize(walkers, called_from_plot)
    result_data = []
    for who in walkers:  # example: for _pa in [_pa, _ma, reg]:
        for steps_per_walk in list_of_steps_per_trial:  # example: for 100 in [100, 1000]:
            for _ in range(walks_per_trial):  # example: will iterate 50 time because 'walks_per_trial' is equal to 50.
                who['now_point'] = who['start']  # Resets the 'now_point' to [0, 0]
                for _ in range(
                        steps_per_walk):  # example: will iterate 100 time because 'steps_per_walk' is equal to 100.
                    # The following line of code uses List Comprehension and zip()
                    # Gets the sum of cooresponding elements from two lists and returns one list
                    who['now_point'] = [x_cor + y_cor for x_cor, y_cor in
                                        zip(who['now_point'], random.choice(who['ways']))]
                # End - for _ in steps_...

                if steps_per_walk == 100:
                    who['end_points_for_100'] += [who['now_point']]
                elif steps_per_walk == 1000:
                    who['end_points_for_1000'] += [who['now_point']]
            # End - for _ in walks_...
            result_data += [get_mean_max_min_cv(who, steps_per_walk)]
            # End - for steps_...
    # End - for who

    if not called_from_plot:
        for i in range(len(result_data)):
            print(result_data[i])
    return walkers


# End - do_trials()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_mean_max_min_cv(who, steps_per_walk):
    '''
    Calculate the Mean, Max, Min, and _cv of all of one walkerss walks_per_trial
    Parameters:
    who 		   - the current walker/dictionary
    steps_per_walk - number of steps taken from list_of_steps_per_trial
    '''
    # Initializes a list
    distances = [1, 2]

    # List Comprehension - Fills list by iterating the 'endpoints' list for either 100 or 1000 steps and by calculating the distances with Pythagoras' theorem
    if steps_per_walk == 100:
        distances = [a ** 2 + b ** 2 for a, b in who['end_points_for_100']]
    elif steps_per_walk == 1000:
        distances = [a ** 2 + b ** 2 for a, b in who['end_points_for_1000']]

    min_d = min(distances) ** (0.5)
    max_d = max(distances) ** (0.5)
    avg_d = statistics.mean(distances) ** (0.5)
    std_dev = statistics.stdev(distances) ** (0.5)
    _cv = std_dev / avg_d

    return f"{who['name']} random walk of {steps_per_walk} steps\nMean = {avg_d:.1f} CV = {_cv:.1f}\nMax = {max_d:.1f} Min = {min_d:.1f}"


# End - get_mean_max_min_cv()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def plot():
    ''' Plots all the data points of the 'end_points_for_100' list for each walker '''
    # Gets walkers with their random walk 'end_points_for_100' lists
    walkers = do_trials('all', 50, [100], called_from_plot=True)

    # Initializes the Turtle() and Screen() object
    petes_plot = turtle.Screen()  # This plot (screen object) belongs to Pete the trutle
    petes_plot.setup(width=300, height=400)  # Sets up window dimensions.
    petes_plot.screensize(canvwidth=250, canvheight=350)  # Prevents the appearance of scrollbars on the plot window.
    # ^^^^(also, specifies the turtle canvas 'working area')
    turtle.title("Random Walks")  # Sets window title.
    turtle.tracer(0, 0)  # Prevents drawing until update() is called.
    pete = turtle.Turtle()  # Pete is a turtle.
    pete.hideturtle()  # Pete is a stealthy turtle.
    pete.up()  # Pete's tail is always up and wagging.
    pete.speed(0)  # Pete is so fast.
    turtle.tracer(0, 0)  # Prevents drawing until update() is called.
    pete.shapesize(stretch_wid=.5, stretch_len=.5)  # Pete is half his normal size... "He's just a lil' guy".

    # Assigns spicified shape and color to walker then plots their 'end_points_for_100'.
    for who in walkers:

        if who['name'] == 'Pa':     pete.shape('circle'); pete.color('black')
        if who['name'] == 'Mi-Ma':  pete.shape('square'); pete.color('green')
        if who['name'] == 'Reg':    pete.shape('triangle'); pete.color('red')

        for x, y in who['end_points_for_100']: pete.goto(x, y); pete.stamp()
    # End - for who

    turtle.update()  # Reveals plot data in the plot window.
    petes_plot.exitonclick()

    if __name__ != '__main__':  # Only 'True' if this file (random_walk.py) is NOT ran directly.
        save_to_image()


# End - plot()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def save_to_image():
    ''' Saves the turtle canvas to 'random_walk.png'. Do not modify this function.
'''
    turtle.getcanvas().postscript(file='random_walk.eps')
    subprocess.run(['gs',
                    '-dSAFER',
                    '-o',
                    'random_walk.png',
                    '-r200',
                    '-dEPSCrop',
                    '-sDEVICE=png16m',
                    'random_walk.eps'],
                   stdout=subprocess.DEVNULL)


# End - save_to_image()


if __name__ == '__main__':
    main()  # Excucte main function