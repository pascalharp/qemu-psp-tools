import gdb

_zen_sts_mmio = {
    "zen"  : 0x032000e8,
    "zen+" : 0x032000e8,
    "zen2" : 0x032000d8,
}

def sts_print(val: str):
    print("\033[93m[\033[01mSTS\033[00m\033[93m]\033[00m {}" .format(val))

class Plugin(gdb.Command):

    def __init__(self):
        sts_print("Loaded. Use sts_init to configure")
        self.sts_port = None
        gdb.Command.__init__(self, "sts_init", gdb.COMMAND_OBSCURE, gdb.COMPLETE_NONE)

    def invoke(self, args, tty):
        try:
            if args not in _zen_sts_mmio.keys():
                raise Exception("Invalid zen generation. Options: " + str(_zen_sts_mmio.keys()))
            self.sts_port = _zen_sts_mmio[args]
            sts_print("Port set to: {}".format(hex(self.sts_port)))
            StsContinue(self)
            sts_print("Initialized. Loaded command: sts_continue <val>")
        except:
            raise

class StsContinue(gdb.Command):

    def __init__(self, plug):
        self.plug = plug
        gdb.Command.__init__(self, "sts_continue", gdb.COMMAND_OBSCURE, gdb.COMPLETE_NONE)

    def invoke(self, argument: str, from_tty: bool) -> None:
        bp = StsWatchpoint(self.plug.sts_port, int(argument, 16))
        gdb.execute("continue")
        bp.delete()

class StsWatchpoint(gdb.Breakpoint):

    def __init__(self, addr, val):
        self.addr = addr
        self.val = val
        super().__init__("*{}".format(hex(addr)), type=gdb.BP_WATCHPOINT, wp_class=gdb.WP_WRITE, internal=True)

    def stop(self) -> bool:
        sts_val = gdb.parse_and_eval("*((unsigned int *) {})".format(hex(self.addr)))
        if gdb.Value(self.val) == sts_val:
            sts_print("Reached sts value: {}".format(hex(sts_val)))
            return True
        else:
            sts_print("Skipped sts value: {}".format(hex(sts_val)))
            return False

if __name__ == "__main__":
   try:
       id(STS)
       sts_print("Plugin already loaded")
   except:
       STS = Plugin()

