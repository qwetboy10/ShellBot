# Shell bot

Discord bot that runs shell commands. Works on any channel that starts with tty or pty. You need the "Shell" role to send commands, and the "President" role to be sudo. It also automatically downloads any files sent. This is potentially a *dangerous* bot by the way, and should only be used with people you trust. Putting it in a docker container makes it safer, but you're still giving people the ability to run code on your system. Put your bot key in a file called secrets.py in a string called token
