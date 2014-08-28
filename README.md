This little server provides a web interface to control mplayer. It was intended to be used with a mobile device on the LAN as a remote control for a media PC.

It assumes the following:

 - The system uses OSS4 (http://www.opensound.com/)

 - mplayer is configured to accept slave-mode commands through a FIFO, configured at line 100. Do not use `$HOME` expansion unless you are sure that this server will be executed by the same user that runs mplayer.

 - Probably some other things
