#!/usr/bin/env bash

trap "exit" INT TERM ERR
trap "kill 0" EXIT

echo "Starting up the bot"
git pull
pip3 install -r requirements.txt
python3 app.py &
BOT_PID=$!
CURRENT_HASH=$(git rev-parse --short HEAD)
echo "Current commit hash: $CURRENT_HASH"

while true
do
  git fetch
  MAIN_HASH=$(git rev-parse --short origin/main)

  if [ "$CURRENT_HASH" != "$MAIN_HASH" ]; then
    echo "Need to update branch to new hash $MAIN_HASH"
    git pull
    CURRENT_HASH=$(git rev-parse --short HEAD)
    pip3 install -r requirements.txt
    kill $BOT_PID
    python3 app.py &
    BOT_PID=$!
  else
    sleep 60
  fi
done