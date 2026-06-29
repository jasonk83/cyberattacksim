### 🤖 IT System Impact: AI Prompt Injection
An unauthorized user is manipulating the corporate LLM. IT must balance the need to patch the AI's guardrails against the business requirement to keep customer-facing chatbots online.

**Recovery Timelines & Technical Impact by Decision:**
* **Hard Offline & Revert AI Model:** (RTO: 24 Hours) Completely suspends all AI-driven business tools. Guaranteed to stop the injection, but causes massive service degradation for customers.
* **Deploy Aggressive Input Sanitization Filter:** (RTO: 4 Hours) Keeps the AI online but routes all prompts through a strict keyword blocker. Fast, but causes high "false positives" that frustrate legitimate users.
* **Rate-Limit and Alert:** (RTO: 1 Hour) Throttles the number of questions any user can ask the AI, buying IT time to manually review chat logs for the malicious inputs.
* **Do Nothing:** (RTO: Indefinite) The AI continues to leak data or perform unauthorized backend commands.
