### 🛠️ IT System Impact: Zero-Day Exploit
A core software appliance has an unpatchable hole. IT cannot wait for the vendor to release an update; they must architect a custom defense to stop remote code execution.

**Recovery Timelines & Technical Impact by Decision:**
* **Air-Gap the Vulnerable Server:** (RTO: 12 Hours) Physically or virtually disconnects the vulnerable server from the rest of the network. Protects the core, but completely breaks dependent applications.
* **Implement Custom WAF Rules (Virtual Patching):** (RTO: 4 Hours) IT writes custom firewall scripts to block the specific exploit signatures. Keeps systems online, but the hacker might find a workaround.
* **Migrate Services to a New OS:** (RTO: 7 Days) Initiates a massive, emergency migration to a different, unaffected operating system. Total architectural overhaul.
* **Do Nothing:** (RTO: Indefinite) Leaves the backdoor wide open until the vendor eventually issues a patch.
