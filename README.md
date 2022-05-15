# spacopt

[![image](https://img.shields.io/pypi/v/spacopt.svg)](https://pypi.python.org/pypi/spacopt)

[![image](https://img.shields.io/travis/PrinceRichfather/spacopt.svg)](https://travis-ci.com/PrinceRichfather/spacopt)

[![Documentation Status](https://readthedocs.org/projects/spacopt/badge/?version=latest)](https://spacopt.readthedocs.io/en/latest/?version=latest)

`spacopt` - short for `spacal-optimization`

## Description

spacopt is a package for bringing optimization techniques to spacal-simulation application, created for LHCb ECAL studies for different types of calorimeters, such as spacal and shashlik.
Should be considered as complementary to [spacal-simulation](https://gitlab.cern.ch/spacal-rd/spacal-simulation), hosted at gitlab under CERN domain.
Up to this point, the main package for optimization is considered [Hyperactive](https://github.com/SimonBlanke/Hyperactive).

## Features

* Create config files, with user defined parameters of the module.
* Run a MC simulation, using pyton script
* Run Optimization for finding best user-defined parameters of module, to minimize the loss function: $
\dfrac{a}{\sqrt{E}}+b,$
where $a$ - sampling term,
$b$ - constant term.

In fact, both $a$ and $b$ could be considered as independent subjects to minimize, as well as other functions of one or both of them.

## Installation

```{.shell}
pip install spacopt
```

## Usage

```
import spacopt

# Run Simulation
```

## Contributing

## License

* Free software: MIT license
* Documentation: <https://spacopt.readthedocs.io>.
