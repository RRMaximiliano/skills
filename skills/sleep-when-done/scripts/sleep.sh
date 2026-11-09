#!/bin/bash
# End any Amphetamine session, then put the Mac to sleep after a delay,
# in a detached process so the calling agent can finish its turn first.
#
# Usage: sleep.sh [--delay SECONDS] [--dry-run]
#   --delay    seconds to wait before sleeping (default 60)
#   --dry-run  do everything except ending Amphetamine and sleeping

delay=60
dry=0
while [ $# -gt 0 ]; do
  case "$1" in
    --delay) delay="$2"; shift 2 ;;
    --dry-run) dry=1; shift ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

log="$HOME/Library/Logs/sleep-when-done.log"
stamp() { date '+%Y-%m-%d %H:%M:%S'; }

if pgrep -x Amphetamine >/dev/null; then
  if [ "$dry" = 1 ]; then
    echo "dry run: would end Amphetamine session"
  else
    osascript -e 'tell application "Amphetamine" to end session' \
      && echo "Amphetamine session ended"
  fi
else
  echo "Amphetamine not running"
fi

if [ "$dry" = 1 ]; then
  cmd="echo \"\$(date '+%Y-%m-%d %H:%M:%S') dry run: would sleep now\" >> '$log'"
else
  cmd="echo \"\$(date '+%Y-%m-%d %H:%M:%S') sleeping\" >> '$log'; pmset sleepnow"
fi

nohup /bin/bash -c "sleep $delay; $cmd" </dev/null >/dev/null 2>&1 &
disown
echo "$(stamp) scheduled sleep in ${delay}s (pid $!)" | tee -a "$log"
