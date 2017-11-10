Docker
=======

How to run application in docker
--------------------------------

.. code:: zsh

    % export CLOUDSDK_PYTHON=/usr/bin/python2.7
    % gcloud beta app gen-config --custom


.. code:: zsh

    % docker build -t <container> .
    % docker run -p 127.0.0.1:8080:8080 <container>
