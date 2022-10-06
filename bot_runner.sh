#!/usr/bin/env bash

trap "exit" INT TERM ERR
trap "kill 0" EXIT

LOGS_DIR="logs"
LOG_FILE="bot_logging"
LOG_LOC=$LOGS_DIR/$LOG_FILE
echo "Bot runner has started"

echo "Starting up the bot"
if [ ! -d "$LOGS_DIR" ]; then
  echo "Creating logs directory"
  mkdir -p $LOGS_DIR
fi
# bot runner is running inside a venv right now, but should really make the venv itself

echo "Pulling from github to get latest version and "
git pull

CURRENT_HASH=$(git rev-parse --short HEAD)
echo "Starting commit hash: $CURRENT_HASH"

exec 3>&1 >> $LOG_LOC-$CURRENT_HASH 2>&1
pip3 install -r requirements.txt
python3 -u app.py &
BOT_PID=$!


while true
do
  git fetch
  MAIN_HASH=$(git rev-parse --short origin/main)

  if [ "$CURRENT_HASH" != "$MAIN_HASH" ]; then
    echo "Need to update branch to new hash $MAIN_HASH"
    git pull
    CURRENT_HASH=$(git rev-parse --short HEAD)
    exec 3>&1 >> $LOG_LOC-$CURRENT_HASH 2>&1
    echo "Start of new commit hash"
    pip3 install -r requirements.txt
    kill $BOT_PID
    python3 -u app.py &
    BOT_PID=$!
  else
    sleep 60
  fi
done