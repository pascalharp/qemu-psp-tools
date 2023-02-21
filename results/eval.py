import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
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

    qlabels = []
    ulabels = []
    fig, (qdata, udata) = plt.subplots(2, 1)
    #fig.tight_layout()


    qdata.set_title("QEMU-PSP")
    qdata.set_xticklabels([])
    qdata.set_xticks([])
    qviolins = qdata.violinplot([qemu_zen.raw, qemu_zen_plus.raw, qemu_zen_two.raw], widths=0.8)
    qviolins['cbars'].set_color('grey')
    qviolins['cmins'].set_color('grey')
    qviolins['cmaxes'].set_color('grey')

    qvio = qviolins['bodies']
    qvio[0].set_color('red')
    qlabels.append((mpatch.Patch(color='red'), "Zen"))
    qvio[1].set_color('green')
    qlabels.append((mpatch.Patch(color='green'), "Zen+"))
    qvio[2].set_color('blue')
    qlabels.append((mpatch.Patch(color='blue'), "Zen2"))
    qdata.legend(*zip(*qlabels), loc=1)


    udata.set_title("PSPEmu")
    udata.set_xticklabels([])
    udata.set_xticks([])
    uviolins = udata.violinplot([pspemu_zen.raw, pspemu_zen_plus.raw], widths=0.8)
    uviolins['cbars'].set_color('grey')
    uviolins['cmins'].set_color('grey')
    uviolins['cmaxes'].set_color('grey')

    uvio = uviolins['bodies']
    uvio[0].set_color('red')
    ulabels.append((mpatch.Patch(color='red'), "Zen"))
    uvio[1].set_color('green')
    ulabels.append((mpatch.Patch(color='green'), "Zen+"))
    udata.legend(*zip(*ulabels), loc=1)

    fig.supylabel("elapsed time in ns")
    plt.show()

    print(*all_data, sep='\n')
