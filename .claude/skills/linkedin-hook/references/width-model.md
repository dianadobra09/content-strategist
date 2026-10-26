# LinkedIn hook width model

How much of a LinkedIn post shows before "...more", measured on real posts in 2026. `scripts/hook_check.py` uses it.
It is approximate and cannot predict every device or a future interface. Check the real composer when you can.

Letters are not equal widths. The real constraint is pixel width, not character count.

## Width scoring

| Character class | Units |
|---|---|
| Narrow letters (i, l, 1, !, ., ,, ;, :, ', j, f, t, r) | 1.0 |
| Space | 1.2 |
| Common punctuation (-, (, ), ?, $, &, @, ") | 1.5 |
| Uppercase narrow (I, J, L) | 1.5 |
| Regular lowercase and digits | 2.2 |
| Uppercase regular (A-H, K, N-V, X-Z) | 2.6 |
| Wide lowercase (m, w) | 2.8 |
| Uppercase wide (M, W) | 4.0 |
| Emoji | 4.0 |

Ordinary sentence-case prose runs at about **1.75 units per character** (measured range 1.66-1.87 on real wrapped lines, 13% spread). ALL CAPS breaks this badly and must be measured directly.

## Measured budgets

| | Full line | Last visible line |
|---|---|---|
| **Mobile** | **~90 units (~50 chars)** | **~78 units (~45 chars)** |
| iPad | ~120 units | ~100 units |
| Desktop preview tools | ~135-146 units | ~120 units |
| LinkedIn's real feed | ~128 units | ~120 units |

Total mobile hook budget across three visible lines: **~258 units (~147 characters)**.

The last visible line is smaller because "...more" sits on it, taking roughly 12-15 units.

## Two findings that change how you work

**1. No preview tool matches LinkedIn.** Measured across three separate tools, desktop previews render at 135, 145 and 146 units per line. LinkedIn's real feed renders at ~128. A hook can pass in every preview and still wrap in the feed. Compose against mobile; treat previews as decorative.

**2. The cut zone is characters 40 to 70.** Mobile cuts near 42, desktop near 66. You cannot control where inside that range the cut lands, so a trailing line must stay interesting across the whole zone.

## Model validation

The model was validated against one creator's 179-character hook (309 units), observed at the same time in the real feed and in a preview tool at three widths:

| Layout | Budget | Predicted | Observed |
|---|---|---|---|
| Mobile | 258u | cut | cut in its last sentence ✓ |
| iPad | 340u | fits | fits ✓ |
| Preview desktop | 404u | fits | fits ✓ |
| LinkedIn real feed | 376u | fits | fits ✓ |

Four for four. This hook reads perfectly on every surface except the one where most people see it. The line that justifies the whole post sits past the mobile cut.
