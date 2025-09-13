# Oracle VirtualBox

Oracle VirtualBox is a free and open-source type 2 hypervisor that allows users to run multiple operating systems simultaneously on a single physical computer. It provides virtualization by creating virtual machines (VMs), each acting as an independent computer with its own virtualized hardware.

## Key Characteristics
- **Cross-platform**: Available on Windows, Linux, macOS, and Solaris hosts.  
- **Open-source**: Licensed under the GNU General Public License (GPL), with additional features available in an extension pack.  
- **Hardware virtualization**: Supports Intel VT-x and AMD-V technologies for efficient performance.  
- **Snapshots**: Allows saving the state of a virtual machine and restoring it later, which is useful for testing and development.  
- **Portability**: Virtual machines are stored as files, making them easy to move or back up.  
- **Networking options**: Provides multiple modes such as NAT, bridged, host-only, and internal networking for flexible configuration.  

## Common Use Cases
- **Testing and development**: Enables developers to run different operating systems and test software in isolated environments.  
- **Education and training**: Provides a safe way to experiment with operating systems without affecting the host machine.  
- **Legacy software support**: Allows older operating systems to run on modern hardware.  
- **IoT and security simulations**: Useful for creating lightweight testbeds of multiple devices in controlled networks.  

## Role in the Project
In the IoT Intrusion Detection System project, Oracle VirtualBox is used to host simulated medical devices such as MRI machines, infusion pumps, X-ray machines, and heart monitors. Its role includes:  
- Running Alpine Linux as the operating system for each simulated device.  
- Managing multiple virtual machines efficiently on a single host.  
- Providing internal networking between the devices and the Ubuntu-based server.  
- Allowing snapshots and reconfiguration for testing different cybersecurity scenarios.
