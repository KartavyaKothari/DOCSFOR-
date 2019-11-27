.. Automated Essay Grader documentation master file, created by
   sphinx-quickstart on Wed Nov 27 01:05:04 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Automated Essay Grader's documentation!
==================================================

Automated Essay Grader is essentially a usable wrapper for using machine learning models based on Essay grading. Our project runs on ``Starlette server`` hosted on ``Heroku cloud`` with a no SQL database hosted on ``Firebase``. Using ``MVC architecture`` we have created a web interface powered by ``Bootstrap 4.0``. Our project also has a fully featured ``Android`` interface.

To check a live web demo `Check out <https://codigos.herokuapp.com/>`_

Project starting formalities
++++++++++++++++++++++++++++

To start the project you first need to install all dependencies:

    >>> pip install requirements.txt

After we have all the requirements set up, we will now create an environment

    >>> conda env create -f Softlab.yml

After the environment is set up you can initialize the environment somehow

    >>> conda activate Softlab

Yes that was it!! Now simply start the system by typing 

    >>> python3 main.py


Checkout some code now
++++++++++++++++++++++

.. toctree::
   :maxdepth: 3
   :caption: Back end:

   main
   prediction

.. toctree::
   :maxdepth: 3
   :caption: Front end:

   web
   android






Indices and tables
++++++++++++++++++

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
