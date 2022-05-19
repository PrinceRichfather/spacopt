import numpy as np
import datetime

from hyperactive import Hyperactive
from hyperactive.optimizers import BayesianOptimizer


def Optimization_run(model, search_space, optimizer = BayesianOptimizer(), n_iter=1, save_xl=True):

    start = datetime.datetime.now()

    
    hyper = Hyperactive()
    hyper.add_search(model, search_space, optimizer=optimizer, n_iter=n_iter)
    hyper.run()

    # Creating DataFrame from optimization data
    data = hyper.search_data(model).copy()

    # Adding new columns with true value of loss function, basically inverse of model() output
    data['true_score'] = np.abs(data['score'])

    # Saving .xlsx file to the <folder_name> directory
    if save_xl==True:
        print('Saving optimizer data to: python_scripts/data/optimizer_outputs/')
        data.to_excel(f'python_scripts/data/optimizer_outputs/opt_dataframe_{start}.xlsx')
    
    # Writing DataFrame Attribute with time spent within module
    end = datetime.datetime.now()
    data.time_left = end - start

    return data