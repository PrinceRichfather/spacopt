import matplotlib.pyplot as plt
import datetime


def plotting_scores(data):

    """

    Parameters
    ----------
    data :


    Returns
    -------

    """
    start = datetime.datetime.now()

    plt.rcParams["figure.figsize"] = (10, 10)
    plt.scatter(list(range(len(data))), data)
    plt.plot(data)
    plt.xticks(data.index)
    plt.ylim(0, 20)
    plt.grid()
    plt.title('Energy resolution after each iteration')
    plt.xlabel('Iteration number')
    plt.ylabel('Found minimum $\dfrac{\sigma}{E}$%')  
    # plt.show()
    plt.savefig(f'python_scripts/data/pcts/{start}.png')
