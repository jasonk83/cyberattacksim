### 🔀 IT System Impact: APT Deep Persistence & UEFI Rootkits
Sub-OS hardware persistence detected. Traditional endpoint re-imaging and OS wiping will NOT eradicate the threat, as implants reside in motherboard SPI flash and BMC firmware.

**Recovery Timelines & Technical Impact by Decision:**
* **Full Hardware Scuttle & Cloud Migration:** (RTO: 5-7 Days) Decommission and physically air-gap all compromised bare-metal cluster nodes. Procure emergency cloud instances and restore from verified pre-intrusion golden images.
* **Firmware Reflashing & Secure Boot Audit:** (RTO: 48-72 Hours) Attempt hardware SPI programmer reflashing with vendor cryptographic hashes. High risk of persistence survival if zero-day UEFI modules remain undetected.
* **Kernel Isolation & Network Egress Blockade:** (RTO: 12-24 Hours) Leave existing hardware online while applying aggressive outbound zero-trust firewalls and DNS sinkholes to sever C2 auction channels.
