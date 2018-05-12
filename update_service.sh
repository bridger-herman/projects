#!/bin/bash
systemctl --user stop $1
systemctl --user disable $1
systemctl --user daemon-reload
systemctl --user enable $1
systemctl --user start $1
systemctl --user status $1
