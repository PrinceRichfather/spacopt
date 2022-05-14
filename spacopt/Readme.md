# Python Scripts for Optimization

`analysis_run.py` - main file for running the automated pipeline.

* Output (subject to minimize):
  * loss function (scaler response)
  * for beginning it is energy resolution

## Optimization step news:

* 3 packages have been tested (not thorougly, but however):
  * `skopt` - giving Segmentation Break after RandomSearchOptimizer is out of random points (random sampling) and "starts optimizing"
  * `grad-free-optimizers` - package which also had problems regarding to documentation (didn't have time for code review)
  * `hyperactive` - most successful optimization package so far! Huge chances project will be held with respect to this package. 

## Future changes

* Almost all functions go to OOP (possibly one class)
* More convinient names  
* `skopt` integration for classical BBO (__under question!__)
* `torch` intagration for NN BBO
* `user-defined` optimization functions


# Resources:

## [skopt](https://scikit-optimize.github.io/stable/)

## [grad-free-optimizers](https://github.com/SimonBlanke/Gradient-Free-Optimizers)

## [Hyperactive](https://github.com/SimonBlanke/Hyperactive)
