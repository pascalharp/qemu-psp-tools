import numpy as np
import matplotlib.pyplot as plt
import csv

class Data:
    def __init__(self, csv_file, name) -> None:
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            self.name = name
            self.raw = np.asarray([np.float64(x["elapsed_time"]) * np.float64(1e-6) for x in reader ], dtype=np.float64)
            self.mean = np.around(np.mean(self.raw, dtype=np.float64), decimals=2)
            self.std = np.around(np.std(self.raw, dtype=np.float64), decimals=2)

    def __str__(self):
        return "{} : \n    (mean) {}ms\n    (std ) {}ms".format(self.name, self.mean, self.std)

    def __repr__(self) -> str:
        return self.__str__()

if __name__ == "__main__":
    qemu_zen        = Data("qemu_zen.csv", "QEMU-PSP Zen")
    qemu_zen_plus   = Data("qemu_zen_plus.csv", "QEMU-PSP Zen+")
    qemu_zen_two   = Data("qemu_zen_two.csv", "QEMU-PSP Zen2")
    pspemu_zen      = Data("pspemu_zen.csv", "PSPEmu Zen")
    pspemu_zen_plus = Data("pspemu_zen_plus.csv", "PSPEmu Zen+")

    all_data = [ qemu_zen, qemu_zen_plus, qemu_zen_two, pspemu_zen, pspemu_zen_plus ]

    print(*all_data, sep='\n')
