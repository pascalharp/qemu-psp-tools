PSP_ON_CHIP_PATH="${HOME}/Documents/pspemu"
PSP_OFF_CHIP_PATH="${HOME}/Documents/pspemu"
PSP_QEMU_BIN="${HOME}/git/github.com/qemu/build/qemu-system-arm"
PSPEMU_BIN="${HOME}/git/github.com/PSPEmu/PSPEmu"
GDB_ARM_BIN="/usr/bin/arm-none-eabi-gdb"
START_ADDR="*0xffff0020"
ENDR_ADDR="*0x100"
ITERATIONS="100"

declare -A zen=( \
    ["machine"]="amd-psp-zen" \
    ["on-chip"]="on-chip-bl-Ryzen-Zen1-Desktop" \
    ["off-chip"]="PRIME-X370-PRO-ASUS-3803.ROM" \
    ["pspemu-profile"]="zen-standard" \
)

declare -A zenplus=( \
    ["machine"]="amd-psp-zen+" \
    ["on-chip"]="on-chip-bl-Ryzen-Zen+-Desktop" \
    ["off-chip"]="PRIME-X370-PRO-ASUS-3803.ROM" \
    ["pspemu-profile"]="zen+-standard" \
)

declare -A zentwo=( \
    ["machine"]="amd-psp-zen2" \
    ["on-chip"]="on-chip-bl-Ryzen-Zen2-Desktop" \
    ["off-chip"]="ASUS_PRIME-B450M-A-ASUS-1201.ROM" \
    ["pspemu-profile"]="zen2-standard" \
)

declare -A psps=(["zen"]=zen ["zen+"]=zenplus ["zen2"]=zentwo)

test_qemu() {
    declare -n psp=${psps["$1"]}
    for ((i = 0; i < $ITERATIONS; i++)); do
        echo "Iteration: $i"
        # Start emulator
        ${PSP_QEMU_BIN} \
            --machine ${psp[machine]} \
            -device loader,file=${PSP_ON_CHIP_PATH}/${psp[on-chip]},addr=0xffff0000,force-raw=on \
            -global driver=amd_psp.smnflash,property=flash_img,value=${PSP_OFF_CHIP_PATH}/${psp[off-chip]} \
            -s -S -nographic \
            &>/dev/null &

        if [ $? -ne 0 ]; then
            echo "GDB failed with $retVal. Exiting"
        fi

        emuPid=$!

        # Start gdb
        ${GDB_ARM_BIN} \
            -ex "target extended-remote localhost:1234" \
            -ex "set confirm off" \
            -ex "source ${HOME}/git/github.com/qemu-psp-tools/measure.py" \
            -ex "measure *0xffff0024 *0x100 -l ${2}" \
            -ex "kill" -ex "quit" \
            &>/dev/null

        wait $emuPid
        retVal=$?
        if [ $retVal -ne 0 ]; then
            echo "QEMU failed with $retVal. Exiting"
            exit 1
        fi
    done
}

test_pspemu() {
    declare -n psp=${psps["$1"]}
    for ((i = 0; i < $ITERATIONS; i++)); do
        echo "Iteration: $i"
        # Start emulator
        ${PSPEMU_BIN} \
            --emulation-mode on-chip-bl \
            --psp-profile ${psp[pspemu-profile]} \
            --on-chip-bl ${PSP_ON_CHIP_PATH}/${psp[on-chip]} \
            --flash-rom ${PSP_OFF_CHIP_PATH}/${psp[off-chip]} \
            --dbg 1225 \
            &>/dev/null &

        emuPid=$!

        # Start gdb
        ${GDB_ARM_BIN} \
            -ex "target extended-remote localhost:1225" \
            -ex "set confirm off" \
            -ex "source ${HOME}/git/github.com/qemu-psp-tools/measure.py" \
            -ex "measure *0xffff0024 *0x100 -l ${2}" \
            -ex "quit" \
            &>/dev/null

        if [ $? -ne 0 ]; then
            echo "GDB failed with $retVal. Exiting"
        fi

        wait $emuPid
        retVal=$?
        if [ $retVal -ne 1 ]; then #PSPEmu is a bit special here
            echo "PSPEmu failed with $retVal. Exiting"
            exit 1
        fi
    done
}

if [[ $# -lt 3 ]]; then
    echo "Missing argument"
    exit 1
fi

if [[ ! -v psps[$2] ]]; then
    echo "Unknown generation: $2"
    exit 1
fi

case $1 in
    qemu) test_qemu $2 $3
    ;;
    pspemu) test_pspemu $2 $3
    ;;
    *)
        echo "Invalid argument"
        exit 1
    ;;
esac

