#!/bin/bash

config=$HOME/.config/hypr

# Nightlight cuz my eyes hurts :')
killall gammastep
gammastep -PO 4300 &

# Notifications kek
killall -q dunst
while pgrep -u $UID -x dunst >/dev/null; do
  sleep 1
done
dunst &

# Killin waybar via script
$HOME/.config/hypr/restartinWaybar.sh

/usr/bin/emacs --daemon &

# Swww cuz I want wallpapers
swww kill
while pgrep -u $UID -x swww >/dev/null; do
  sleep 1
done
swww init 
swww img /home/delta/Pictures/Backgrounds/homura1.jpg

dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP &
