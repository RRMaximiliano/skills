---
name: sleep-when-done
description: Watch every running T3 Code thread and put the Mac to sleep once all are finished, ending any Amphetamine session first. Run it from a no-project thread.
---

# Sleep When Done

Arguments (optional, free text): a title filter (`only Nicaragua`), a time cap (`max 4h`), or `stay awake if waiting`.

## Workflow

The user is away from the computer while this runs, so a thread waiting on them will not be answered tonight. By default, a thread blocked on the user's input never keeps the Mac awake.

1. **List.** `t3_thread_list` with `allProjects: true`, statuses `preparing, queued, starting, running, waiting`. Ignore your own thread (`currentThreadId`). Apply any title filter.
2. **Sort out blocked threads.** A thread is blocked on the user if its status is `waiting` or its `pendingRequestCount` is above 0. If neither field settles it, `t3_thread_read` it (`view: activity`, small `limit`): a `user_input_request` item with status `waiting` means it is blocked. Put blocked threads on a "waiting on you" list and stop watching them; they count as done. Only if the user said `stay awake if waiting`: stop now, report, and do not sleep.
3. **Wait.** `t3_thread_wait` on every remaining thread in parallel, `timeoutMs: 3600000`. For top-level threads add `untilDelegatedWorkSettled: true`. When a wait returns (finished or timed out), go back to step 1: parents start new children after one finishes, and a running thread can become blocked midway. Repeat until no thread is left except blocked ones.
4. **Confirm quiet.** List once more a few minutes later (a background `sleep 180` plus `t3_background_wait`). Sleep only if every listed thread is blocked or the list is empty. Read the last message of each thread that finished during the watch; if it ends with a question for the user, add it to the "waiting on you" list too.
5. **Time cap.** If the cap passes, go to step 6 anyway and say which threads were cut off.
6. **Sleep.** Run `bash <skill-dir>/scripts/sleep.sh`. It ends the Amphetamine session and sleeps the Mac 60 seconds later in a detached process. Then end your turn at once: while this thread runs, T3 Code keeps starting `caffeinate`, which wakes the Mac back up.
7. **Report** before running step 6, in your final message: what finished, what is waiting on the user (with thread `link`s), and when the Mac will sleep.

Never cancel, interrupt, or answer other threads.
