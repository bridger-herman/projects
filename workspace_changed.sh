#!/bin/sh
# CREDIT: https://askubuntu.com/a/403969

# Show the auto-hidden workspace panel for a moment, then set it to autohide again
xfconf-query -c xfce4-panel -p /panels/panel-2/autohide-behavior -t int -s 0
# sleep 1
xfconf-query -c xfce4-panel -p /panels/panel-2/autohide-behavior -t int -s 2
