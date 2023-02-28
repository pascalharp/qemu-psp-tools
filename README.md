# qemu-psp-tools
Collection of tools to debug the qemu psp implementation

## sync\_bridge.py
Synchronizes two running gdb instances. Exchanges compatible register list and optional skip section list before Synchronization.
One instance runs as leader, other instance as follower.

Examples after the plugin is loaded:
* Leader: `sb_lead --skip 0xffff00c0:0xffff00a0`
* Follower: `sb_follow`

## sts.py
Helper plugin to continue to specific status port output. Creates a custom watchpoint and reports other passed status codes.

Usage example after plugin is loaded: `sts_continue 0x3`

## measure.py
Measures the time it requires to between a start and end breakpoint. Accepts an optional file argument where the result is logged to in csv format. Breakpoints can be provided in as gdb accepts it.

Usage example after plugin is loaded (exact addresses): `measure *0xffff00c0 *0x100 log.csv`
