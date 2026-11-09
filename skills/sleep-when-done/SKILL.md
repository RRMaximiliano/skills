---
name: sleep-when-done
description: Watch every running T3 Code thread and put the Mac to sleep once all are finished, ending any Amphetamine session first. Run it from a no-project thread.
---

# Sleep When Done

Arguments (optional, free text): a title filter (`only Nicaragua`), a time cap (`max 4h`), or `stay awake if waiting`.

## Workflow

1. **List.** `t3_thread_list` with `allProjects: true`, statuses `preparing, queued, starting, running, waiting`. Ignore your own thread (`currentThreadId`). Apply any title filter.
2. **Wait.** `t3_thread_wait` on every listed thread in parallel, `timeoutMs: 3600000`. For top-level threads add `untilDelegatedWorkSettled: true`. Then list again: parents start new children after one finishes. Repeat until nothing is left.
3. **Blocked threads.** A thread whose `updatedAt` stops moving may be waiting on the user. `t3_thread_read` it (`view: activity`, small `limit`); a `user_input_request` item with status `waiting` means it is blocked. Count it as done, unless the user said `stay awake if waiting`; then stop and report without sleeping.
4. **Confirm quiet.** List once more a few minutes later (one more short `t3_thread_wait`). Sleep only if still nothing is active.
5. **Time cap.** If the cap passes, go to step 6 anyway and say which threads were cut off.
6. **Sleep.** Run `bash <skill-dir>/scripts/sleep.sh`. It ends the Amphetamine session and sleeps the Mac 60 seconds later in a detached process. Then end your turn at once: while this thread runs, T3 Code keeps starting `caffeinate`, which wakes the Mac back up.
7. **Report** before running step 6, in your final message: what finished, what is waiting on the user (with thread `link`s), and when the Mac will sleep.

Never cancel, interrupt, or answer other threads.
