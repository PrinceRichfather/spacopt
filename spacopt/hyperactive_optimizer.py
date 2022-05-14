import numpy as np
import pandas as pd
import datetime

from hyperactive import Hyperactive
from hyperactive.optimizers import BayesianOptimizer

from Simulation import Simulation
from plotting import plotting_scores


start = datetime.datetime.now()

def model(opt):

    fit_df = Simulation(delete_cfg=True).runFitting(wall=opt['wall'],
                                     fiber_diameter=opt['fiber_diameter'],
                                     energies=[50],
                                     events=1000)
    # fit_df.to_excel(f'python_scripts/data/fitted/fitted_at_{start}.xlsx')
    return -fit_df.const_term.item()

search_space = {
                "wall": list([0.55]), #list(np.arange(0.1, 1, 0.01)),
                "fiber_diameter": list([2]) #list(np.arange(0.5, 4, 0.1))
                }

optimizer = BayesianOptimizer()

hyper = Hyperactive()
hyper.add_search(model, search_space, optimizer=optimizer, n_iter=1)
hyper.run()

data = hyper.search_data(model).copy()
data['true_score'] = np.abs(data['score'])
data.to_excel(f'python_scripts/data/optimizer_outputs/opt_dataframe_{start}.xlsx')
print(data)
plotting_scores(data['true_score'])