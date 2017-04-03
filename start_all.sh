#!/bin/sh

#tmux ls | grep : | cut -d. -f1 | awk '{print substr($1, 0, length($1)-1)}' | xargs kill
#tmux kill-session -t myname
#tmux new-session -s "proxy"

tmux kill-server
tmux new-session -d './start_proxy.sh' \; split-window -d \; attach

#tmux new-session -s "Mproxy" -d 'start_proxy.sh' \; split-window -d \; attach


tmux kill-session -tproxy

session=proxy
window=${session}:0
pane=${window}.0

tmux start-server
tmux new-session -s "proxy" \; split-window
tmux send-keys -t proxy:1 C-z 'loadavrg' Enter

tmux select-window -tproxy:0
#tmux attach-session -d -tproxy