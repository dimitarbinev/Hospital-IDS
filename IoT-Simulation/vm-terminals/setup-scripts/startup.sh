#!/bin/bash
set -e

VM_NAME=${VM_NAME:-"default_vm"}
RAM_SIZE=${RAM_SIZE:-4096}
CPU_CORES=${CPU_CORES:-"2"}
ISO_PATH="/vm-images/Win10_22H2_English_x32.iso"
VM_DISK="/vm-data/${VM_NAME}.qcow2"

# Check if ISO exists
if [ ! -f "$ISO_PATH" ]; then
    echo "Error: Windows ISO not found at $ISO_PATH"
    echo "Please ensure you have placed the Windows ISO in the vm-images directory"
    exit 1
fi

# Create VM disk if it doesn't exist
if [ ! -f "$VM_DISK" ]; then
    echo "Creating new VM disk at $VM_DISK"
    qemu-img create -f qcow2 "$VM_DISK" 16G
fi

echo "Starting VM: $VM_NAME"
echo "RAM: ${RAM_SIZE}MB"
echo "CPUs: $CPU_CORES"

# Start QEMU with compatible CPU settings
qemu-system-x86_64 \
    -name "$VM_NAME" \
    -m "${RAM_SIZE}" \
    -smp "${CPU_CORES}" \
    -cpu qemu64,+ssse3,+sse4.1,+sse4.2 \
    -drive file="$VM_DISK",format=qcow2,cache=writeback \
    -cdrom "$ISO_PATH" \
    -net nic,model=e1000 \
    -net user \
    -vga std \
    -display vnc=:0 \
    -monitor stdio \
    -machine pc-i440fx-2.8 \
    -boot order=dc \
    -rtc base=localtime \
    -usb \
    -device usb-tablet \
    -device virtio-balloon \
    -device virtio-rng-pci \
    -overcommit mem-lock=off \
    -no-shutdown &

QEMU_PID=$!

# Function to check if QEMU is running
check_qemu() {
    if ! kill -0 $QEMU_PID 2>/dev/null; then
        echo "QEMU process died unexpectedly"
        ps aux | grep qemu
        free -m
        echo "Memory info:"
        cat /proc/meminfo
        dmesg | tail -n 20 || true
        exit 1
    fi
}

echo "QEMU started with PID: $QEMU_PID"
echo "VNC server available on port 5900"

# Monitor QEMU process and keep container running
while true; do
    check_qemu
    sleep 5
done