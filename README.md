livestreamer-completion
=======================

Shell completion support for [Livestreamer](http://livestreamer.tanuki.se/).
Currently only bash is supported.

Features
--------

* Completes command line options
* Completes URLs from specified text files (by default this is from `~/.config/livestreamer/favorites*`), which should contain URLs separated by either a space or line-ending.


Installing (bash)
-----------------

a. Place [livestreamer.bash](livestreamer.bash) in a `bash-completion.d` directory:

  * /etc/bash-completion.d
  * /usr/local/etc/bash-completion.d

b. Or, copy it somewhere (e.g. `~/.config/livestreamer/completion.sh`) and put
   the following line in your .bashrc:

    source ~/.config/livestreamer/completion.sh
    

Extras
------

Also in this repo there is a [Python script](twitch_channels.py) that can query
Twitch for channels. Currently querying user follows and teams are supported. 

This script can be used to create a list of URLs to be used in the completion script. E.g. 

    $ ./twitch_channels.py --team eg --team teamliquid --follows myuser > ~/.config/livestreamer/favorites.twitch
     
Put it in your crontab to automate the process regularly.
