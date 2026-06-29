### 🔀 IT System Impact: Database Integrity Sabotage
Data cannot be trusted. IT cannot simply restore a backup without knowing *when* the sabotage started, requiring a massive data-reconciliation effort.

**Recovery Timelines & Technical Impact by Decision:**
* **Revert to 30-Day Old Backup:** (RTO: 4 Days) Restores a guaranteed clean database, but permanently deletes a full month of legitimate sales and customer data that must be manually re-entered.
* **Freeze Database and Audit Manually:** (RTO: 3 Weeks) Takes the system offline to run forensic scripts comparing current data against transaction logs line-by-line. Extremely slow.
* **Implement "Failsafe" Logic Moving Forward:** (RTO: 24 Hours) Leaves the corrupted data as-is, but adds strict verification rules to prevent future database changes.
