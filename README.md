# Infinite Trivia
The trivia that keeps on giving!

# How To Build:

## System Requirements

Infinite Trivia can be built and run on Linux, OSX, and Windows
Systems. The following Operating Systems are confirmed to support
Infinite Trivia:

1. Ubuntu 19
2. Windows 10

## Program Requirements

The following programs are required to build Infinite Trivia:
- Python 3.7.x ([link](<https://www.python.org/downloads/release/python-377/>))
- Pip python package manager, should come built in with python 3.7
- Sqlite3 ([install tutorial](https://www.servermania.com/kb/articles/install-sqlite/))

## Package Installation

To install the required python packages for Infinite Trivia, navigate
to the top-level folder of the project and run the following command:
`python3 -m pip install -r requirements.txt`. This will install every
package depencency, so it may take a while.

## Installing Spacy Language Models

After successfully installing the pre-requisite packages, run the
following two commands to download the spacy english language models:
- `python3 -m spacy download en_core_web_lg`
- `python3 -m spacy download en_core_web_sm`

# How To Run

## Starting Infinite Trivia

From the top level of the project, navigate to the `web_app` folder,
then run the `infinite_trivia.py` script with the following command:
`python3 infinite_trivia.py`. Note that for pathing to work properly,
you **must** run the `infinite_trivia` script from within the
`web_app` folder, **not** from the top level directory or elsewhere.

## Playing Infinite Trivia

If Infinite Trivia has successfully launched, you will get a message
on the terminal window which displays the IP and port number which it
is being hosted on (default: `127.0.0.1:5000`). Navigate to the
displayed webpage on your browser and start playing!
