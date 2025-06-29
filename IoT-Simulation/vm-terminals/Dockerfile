FROM ubuntu:22.04

# Install QEMU and required packages
RUN apt-get update && apt-get install -y \
    qemu-system-x86 \
    qemu-utils \
    qemu-system-common \
    python3 \
    python3-pip \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Configure system settings
RUN echo 'vm.overcommit_memory=1' >> /etc/sysctl.conf \
    && echo 'vm.swappiness=0' >> /etc/sysctl.conf

# Create required directories
RUN mkdir -p /dev/shm && chmod 777 /dev/shm

WORKDIR /vm

# Copy setup scripts
COPY setup-scripts/ /vm/setup-scripts/
RUN chmod +x /vm/setup-scripts/*.sh

# Install Python requirements for the monitoring service
COPY requirements.txt .
RUN pip3 install -r requirements.txt

ENTRYPOINT ["/vm/setup-scripts/startup.sh"]