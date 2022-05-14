import subprocess
import matplotlib.pyplot as plt
import datetime

def delRootFile(self, root_path: str) -> int:
    """

    Parameters
    ----------
    root_path: str :
        

    Returns
    -------

    """

    subprocess.call(['rm','-r', root_path])

    return 0

def delcfg(self, cfg_path: str) -> int:
    """

    Parameters
    ----------
    cfg_path: str :
        

    Returns
    -------

    """


    subprocess.call(['rm', f"python_scripts/data/my_configs/{cfg_path}.cfg"])

    
    return 0


def plotting_scores(data):
    """

    Parameters
    ----------
    data :
        

    Returns
    -------

    """
    start = datetime.datetime.now()


    plt.rcParams["figure.figsize"] = (10,10)
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