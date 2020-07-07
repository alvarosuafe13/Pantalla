export DISPLAY=":0"
export XAUTHORITY=/home/username/.Xauthority
WID=$(xdotool search --onlyvisible --class firefox|head -1)
xdotool windowactivate ${WID}
xdotool key ctrl+F5
