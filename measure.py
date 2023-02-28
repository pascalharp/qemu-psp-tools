from typing import Optional, IO
import gdb
import argparse
import time
import csv

def pretty_print(val: str):
    print("\033[93m[\033[01mMeasure\033[00m\033[93m]\033[00m {}" .format(val))

class Plugin(gdb.Command):

    def __init__(self):
        pretty_print("Loaded. Use: measure <start_addr> <end_add> [log_file]")
        self.sts_port = None
        gdb.Command.__init__(self, "measure", gdb.COMMAND_OBSCURE, gdb.COMPLETE_NONE)

    def invoke(self, args, tty):
        parser = argparse.ArgumentParser()
        parser.add_argument('start', type=str)
        parser.add_argument('end', type=str)
        parser.add_argument('-l', dest='log', type=str)
        args = parser.parse_args(args.split())

        data = MeasureData(args.start, args.end)
        log_file = None
        if args.log:
            log_file = open(args.log, "a+", encoding="utf8")

        StartBreakpoint(data)
        EndBreakpoint(data, log_file)

        gdb.execute("continue")

class MeasureData:
    def __init__(self, start, end):
        self.start_addr = start
        self.end_addr = end
        self.start_time: Optional[int] = None
        self.end_time: Optional[int] = None
        self.elapsed_time: Optional[int] = None

class StartBreakpoint(gdb.Breakpoint):
    def __init__(self, data: MeasureData):
        self.data: MeasureData = data
        super().__init__(self.data.start_addr, type=gdb.BP_BREAKPOINT, internal=True, temporary=True)
        pass

    def stop(self) -> bool:
        pretty_print("Hit measure starting point")
        self.data.start_time = time.monotonic_ns()
        return False

class EndBreakpoint(gdb.Breakpoint):
    def __init__(self, data: MeasureData, log_file: Optional[IO]):
        self.data: MeasureData = data
        self.log_file = log_file
        super().__init__(self.data.end_addr, type=gdb.BP_BREAKPOINT, internal=True, temporary=True)
        pass

    def stop(self) -> bool:
        self.data.end_time = time.monotonic_ns()
        pretty_print("Hit measure end point")

        if not self.data.start_time:
            pretty_print("Start point was never passed. Inconclusive result ignored")
            return True

        self.data.elapsed_time = self.data.end_time - self.data.start_time
        pretty_print("Elapsed time: {}ns".format(self.data.elapsed_time))

        if self.log_file:
            pretty_print("Writing to log file: {}".format(self.log_file.name))
            writer = csv.DictWriter(self.log_file, fieldnames=self.data.__dict__.keys())
            if self.log_file.tell() == 0:
                writer.writeheader()
            writer.writerow(self.data.__dict__)
            self.log_file.close()

        return True

if __name__ == "__main__":
   try:
       id(MEASURE)
       pretty_print("Plugin already loaded")
   except:
       MEASURE = Plugin()

