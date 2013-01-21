# Vivify

Vivify is my personal bootstrap for initializing a usable environment on a
Windows box. The goal is to produce a single command to generate a working
python environment, which can then allow further setup to be automated in a
reasonable scripting environment.

## Quick Start

Run the [bootstrapper](https://github.com/djs/vivify/raw/master/bootstrap.cmd)
with administrator privileges.

## Installation and Use

On a fresh Windows box, there are three steps required to vivify the system:

1. Download and install [msysgit](http://code.google.com/p/msysgit/downloads/list).
   Choose to install git (only) in the system path.
2. Download and execute bootstrap.cmd as an administrator.

## What it does

Bootstrap.cmd will clone vivify.git and automatically execute vivify.cmd,
reducing the number of steps required by one. Vivify.cmd is a windows batch file
that will download and silently install Python on your system, along with pip.
It will properly configure your system PATH to persistently reference this installation.

## How it works

The trickiest part is setting up the path *properly* from a batch file. This is
accomplished by a helper script written in VBScript. This script will use the
Windows Scripting Host environment to modify the system PATH without losing
nested environment variables or merging user and system paths.

# Enlighten

Enlighten is a quickly-growing script I wrote to automatically install all the
software I find necessary in order to develop and work in a Windows environment.

The script functions as a very, very rudimentary package manager of sorts (a la
easy_install ... no uninstallation!). You can specify a piece of software on the
command line and it will install it, or specify you want to install everything:

    python enlighten.py all

It uses a variety of mechanisms to sort through the cruft of the internet and
download either the latest package, or just whatever was the latest version at
the time I added it, if that was easier.

Though I'd like to keep it dependency free, this is already untrue since I use
the life-saving BeautifulSoup4 module to de-cruft horrors like Google Code
Hosting download links. Install dependencies after bootstrapping python like
this:

    pip install -r requirements.txt

## TODO

* Add devivification script for testing and general fun
* Enhance addtopath.vbs to allow user path modification and not to duplicate
  entries
* Figure out how to reduce installation to one step

This is a work in progress.
Caveat Emptor.
