#!/bin/bash

session="tsg-toolsuite"
mainSession="main"

SESSIONEXISTS=$(tmux ls | grep $session)

if [ "$SESSIONEXISTS" = "" ]
then
	tmux new-session -d -s $session
	tmux rename-window -t 1 $mainSession

	# Start second console session
	consoleSession="console"
	tmux new-window -t $session:2 -n $consoleSession

	# Read -v as "open new pane in vertical direction"
	tmux split-window -v
	tmux send-keys -t $consoleSession "cd kickstart-gui;npm run dev" C-m
	tmux split-window -h
	tmux send-keys -t $consoleSession "cd saison_kickstarter;uv run fastapi dev saison_kickstarter/api.py" C-m
	tmux select-pane -t 1
	tmux send-keys -t $consoleSession "gemini" C-m

fi

tmux attach-session -t $session:1
