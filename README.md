vwcr
====

The VoidWarranties cash register, for handling drink purchases.

installation
------------

Get the code and move into the directory

    git clone git://github.com/voidwarranties/vwcr.git
    cd vwcr

You will need to have version 2 of python, pip and virtualenv installed on your system. On debian-based systems these are provided by the packages python, python-pip and python-virtualenv. If installing on Arch linux you will need the packages python2, python2-pip and python2-virtualenv and will have to substitute 'virtualenv-2' for 'virtualenv' in the following command.

This will set up a isolated Python environment in the directory 'env' and install the python packages MALMan depends upon in this enviroment.

    virtualenv env
    env/bin/pip install -r requirements.txt

Copy config-template.py to config.py and fill in the security parameters.

    cp config{-template,}.py

You should now be be able to run vwcr

   env/bin/python vwcr.py
