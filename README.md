# Moose mating

Moose mating for Python, basics for moose-evolution simulation.

Idea and algorithm stolen from [pixl](https://github.com/rec0de/pixl)

## Usage

To generate one random moose:

    python gen_moose.py

To test mating run orgy.py:

    python orgy.py

Running simulation with multiple mooses is easy as:

    python simulate.py


## Webmoose

Renders world into PNG image. HTML page to refresh image.
Requires moose images under "img" folder, not provided with this project.

    sudo apt-get install python-imaging
    sudo apt-get install python-pil

Get jQuery:

    wget http://code.jquery.com/jquery-2.1.3.min.js

Link webmoose.html to index.html:

    ln -s webmoose.html index.html

Setup your HTTP server to serve moose-mating folder.
Then run webmoose with statsfile:

    python webmoose.py --statsfile info.html


## Localmoose

Renders world into screen using Qt5.

    sudo apt-get install python-pyqt5

Then run:

    python localmoose.py
