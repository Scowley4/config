tmux -S ~/.tmux-socket new-session \; \
  split-window -v -p 75 \; \
  split-window -h -p 70 \; \
  select-pane -t 1 \; \
  send-keys 'ipython3' C-m \; \
  # Split top\bottom rest\number
  # Split bottom left\right number\rest
  # -------------
  # |     0     |
  # |-----------|
  # |  1  |  2  |
  # -------------
