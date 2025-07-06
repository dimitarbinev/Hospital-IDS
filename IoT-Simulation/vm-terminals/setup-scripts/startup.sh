#!/bin/bash
set -e

# Default to 4GB RAM unless overridden
VM_NAME=${VM_NAME:-"default_vm"}
RAM_SIZE=${RAM_SIZE:-4096}
CPU_CORES=${CPU_CORES:-"2"}
ISO_PATH="/vm-images/Win10_22H2_English_x32.iso"
VIRTIO_ISO_PATH="/vm-images/virtio-win.iso"
# Using workstation-data Docker volume
VM_DISK="/workstation-data/${VM_NAME}.qcow2"
FORCE_INSTALL=${FORCE_INSTALL:-false}
MONITOR_SOCKET="/workstation-data/${VM_NAME}.monitor"

# Ensure disk mount exists
mkdir -p "/workstation-data"

# Verify ISOs
for path in "$ISO_PATH" "$VIRTIO_ISO_PATH"; do
    if [ ! -f "$path" ]; then
        echo "Error: ISO missing at $path"
        exit 1
    fi
done

# Determine cgroup memory limit
MEM_BYTES=""
if [ -f "/sys/fs/cgroup/memory/memory.max" ]; then
    VAL=$(cat "/sys/fs/cgroup/memory/memory.max")
    [[ "$VAL" != "max" ]] && MEM_BYTES=$VAL
elif [ -f "/sys/fs/cgroup/memory/memory.limit_in_bytes" ]; then
    MEM_BYTES=$(cat "/sys/fs/cgroup/memory/memory.limit_in_bytes")
fi

# Cap VM RAM if limited by container cgroup
if [[ -n "$MEM_BYTES" ]]; then
    MEM_MB=$((MEM_BYTES/1024/1024))
    ALLOW_MB=$((MEM_MB-256))
    if (( RAM_SIZE > ALLOW_MB )); then
        echo "Capping RAM to ${ALLOW_MB}MB due to container limit"
        RAM_SIZE=$ALLOW_MB
    fi
fi

echo "Final VM RAM: ${RAM_SIZE}MB"

# Boot logic
if [[ ! -f "$VM_DISK" || "$FORCE_INSTALL" == "true" ]]; then
    echo "Installer boot"
    BOOT_FLAGS=("-boot" "order=d,once=c")
    if [[ ! -f "$VM_DISK" ]]; then
        echo "Creating disk at $VM_DISK"
        qemu-img create -f qcow2 "$VM_DISK" 16G
    fi
else
    echo "Disk boot"
    BOOT_FLAGS=("-boot" "order=c,once=d")
fi

# Launch QEMU (daemonized, monitor on UNIX socket)
echo "Launching VM: $VM_NAME (CPUs: $CPU_CORES)"
qemu-system-x86_64 \
    -name "$VM_NAME" \
    -m "$RAM_SIZE" \
    -smp "$CPU_CORES" \
    -cpu qemu64,+ssse3,+sse4.1,+sse4.2 \
    -drive format=qcow2,file="$VM_DISK",if=virtio,cache=writeback \
    -drive media=cdrom,if=ide,file="$ISO_PATH" \
    -drive media=cdrom,if=ide,file="$VIRTIO_ISO_PATH" \
    -net nic,model=e1000 -net user \
    -vga std -display vnc=:0 \
    -machine pc-i440fx-2.8 \
    "${BOOT_FLAGS[@]}" \
    -rtc base=localtime \
    -usb -device usb-tablet \
    -device virtio-balloon -device virtio-rng-pci \
    -overcommit mem-lock=off \
    -monitor unix:${MONITOR_SOCKET},server,nowait \
    -daemonize

# Block container to keep QEMU alive
echo "QEMU started in background with VNC on port 5900 and monitor at $MONITOR_SOCKET"
# Wait indefinitely
tail -f /dev/null
