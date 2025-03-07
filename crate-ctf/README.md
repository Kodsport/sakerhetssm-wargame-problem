# Crate-CTF
Challenges ported from [Crate CTF](https://github.com/CrateOrg/crate-ctf/tree/main).

## Changes
- Some of the dymanic challenges had a description which includes connection info. Since our tooling takes care of this, this was removed.
- Some author names were changed for consistency (toblun -> toblu, larhel -> larshson, Lars -> larshson, johahed -> Johan)

### Categories
Most of the challenges in the "exploit" categories were placed into pwn, with the following exceptions:
- `2023/exploit/Moment_22` (strcmp timing attack) was changed to `misc`.
- `2024/exploit/Notes` was changed to `misc`.
- `2024/exploit/JSFS` was changed to `web`

### Modified Challenges
- `2021/reversing/FutureFlag` had a date changed from 2024 to 2124 and was recompiled.
- `2021/crypto/PumpaPumpaPumpa` had its name changed, since `challtools` didn't work for challenges with emoji-only name
- `2020/exploit/format_string_read` was changed to quit gracefully when receiving an EOF
- `2024/crypto/ZKP` got an additional flag

### Removed/non-ported challenges
The following challenges were skipped, mainly due to infrastructure requirements which we don't want to deal with right now. A few of them might be added in the future.

- `2020/web/wordpress` was a single wordpress site with many different flags, not great for a classic CTF platform.
- `2021/web/Switched` requires multiple containers.
- `2022/misc/Rorigt` requires network infrastructure we can't guarantee (`network_mode: host`).
- `2023/forensics/UnicornShredder` stores userdata which need to be cleared at times.
- `2023/misc/HemligAgent` requires some rework.
- `2023/misc/SourceControl` requires network infrastructure we can't guarantee (`network_mode: host`).
- `2023/osint/Intern` is OSINT, using external services we don't control.
- `2023/reversing/Kokbok` requires multiple network services.
- `2023/web/Diktafon` requires multiple containers.
- `2024/crypto/Kassaskapet2` requires multiple network services.
- `2024/crypto/KrEncyclopedia` requires some rework.
- `2024/forensics/Langtidsminne` misses a file (and most likely requires external hosting due to size).
- `2024/forensics/UnicornShredder2.0` stores userdata which need to be cleared at times.
- `2024/misc/Buggigt` was hosted on some web TTY, requires some rework.
- `2024/misc/Kassaskapet` requires multiple network services.
- `2024/osint/HittaHit2` is OSINT, which might be outdated soon.
- `2024/osint/Intern2` is OSINT, using external services we don't control.
- `2024/reversing/FalletOmKARNkraftverket` was hosted on an external platform, can probably be hosted by using QEMU in Docker, but requires rework.
- `2024/web/Fillagringstjänst` stores userdata which need to be cleared at times.
- `2024/web/Robotfilter` requires complicated infra.
- `2024/web/Sök` requires multiple containers.
