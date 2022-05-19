'''Exposing modules for User from subpackages'''
from .file_preparation import configWriter, macWriter
from .plotting import plotting_scores
from .Simulation import Simulation
from .Optimization_run import Optimization_run

'''
My optimization package for spacal-simulation
=============================================

spacopt is a complete package for implementing optimization automation 
for Geant4 spacal-simulation Monte-Carlo (MC) application,
developed for LHCb ECAL particle-matter interaction studies

'''


__version__ = '0.3.0'