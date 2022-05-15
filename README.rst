=======
spacopt
=======


.. image:: https://img.shields.io/pypi/v/spacopt.svg
        :target: https://pypi.python.org/pypi/spacopt

.. image:: https://img.shields.io/travis/PrinceRichfather/spacopt.svg
        :target: https://travis-ci.com/PrinceRichfather/spacopt

.. image:: https://readthedocs.org/projects/spacopt/badge/?version=latest
        :target: https://spacopt.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status



`spacopt` - short for `spacal-optimization`
spacopt is a package for bringing optimization techniques to spacal-simulation application


* Free software: MIT license
* Documentation: https://spacopt.readthedocs.io.


Features
--------
* Create config files, with user defined parameters of the module.
* Run a MC simulation, using pyton script
* Run Optimization for finding best user-defined parameters of module, to minimize the loss function: $
\dfrac{a}{\sqrt{E}}+b,$
where $a$ - sampling term,
$b$ - constant term.

In fact, both $a$ and $b$ could be considered as independent subjects to minimize, as well as other functions of one or both of them.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
