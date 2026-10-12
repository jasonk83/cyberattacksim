# game_data.py

# Hacker Choices
hacker_options = [
    {
        "id": "H1",
        "name": "Phishing Campaign",
        "description": "This action involves sending fake emails to employees to trick them into giving away their passwords.",
        "assessment": "It has a high likelihood of success because people often make mistakes, but the immediate damage is usually limited to a few compromised accounts.",
        "complexity": "Low",
        "projected_impact": -10
    },
    {
        "id": "H2",
        "name": "DDoS Attack",
        "description": "This action overwhelms the company's website with fake traffic so that real customers cannot access it.",
        "assessment": "It has a moderate likelihood of success, causing temporary financial loss and reputation damage while the site is down.",
        "complexity": "Medium",
        "projected_impact": -20
    },
    {
        "id": "H3",
        "name": "Ransomware Deployment",
        "description": "This action uses malicious software to lock up the company's files until a sum of money is paid.",
        "assessment": "It has a lower likelihood of success due to modern security defenses, but the damage can completely halt all business operations if successful.",
        "complexity": "High",
        "projected_impact": -35
    }
]

# IT Choices
it_options = [
    {
        "id": "IT1",
        "name": "Isolate Affected Systems",
        "description": "This action disconnects infected computers from the rest of the network to stop the attack from spreading.",
        "assessment": "The pro is that it quickly stops further damage, but the con is that isolated departments cannot do their work. Projected Impact: +10 System Defense.",
        "complexity": "Low",
        "projected_impact": 10
    },
    {
        "id": "IT2",
        "name": "Restore from Backups",
        "description": "This action wipes the infected computers and replaces their data with a safe, older copy.",
        "assessment": "The pro is that it removes the attacker without paying a ransom, but the con is that any work done since the last backup is lost forever. Projected Impact: +20 System Defense.",
        "complexity": "Medium",
        "projected_impact": 20
    },
    {
        "id": "IT3",
        "name": "Deploy Advanced Threat Hunting",
        "description": "This action involves security experts actively searching the network to find and remove hidden attackers.",
        "assessment": "The pro is that it can completely secure the network from complex threats, but the con is that it is very expensive and takes a lot of time. Projected Impact: +35 System Defense.",
        "complexity": "High",
        "projected_impact": 35
    }
]

# Executive Choices
exec_options = [
    {
        "id": "E1",
        "name": "Public Apology and Transparency",
        "description": "This action involves releasing a public statement explaining the breach and apologizing to customers.",
        "assessment": "The pro is that it builds long-term trust, but the con is that it invites immediate bad press. Projected Impact: +10 Company Resilience.",
        "complexity": "Low",
        "projected_impact": 10
    },
    {
        "id": "E2",
        "name": "Hire External PR and Legal Firm",
        "description": "This action brings in outside experts to handle media relations and navigate legal risks.",
        "assessment": "The pro is that professionals can minimize reputation damage, but the con is that it costs a significant amount of the company's budget. Projected Impact: +20 Company Resilience.",
        "complexity": "Medium",
        "projected_impact": 20
    },
    {
        "id": "E3",
        "name": "Negotiate and Pay Ransom",
        "description": "This action involves secretly paying the hackers in hopes they unlock the systems and delete stolen data.",
        "assessment": "The pro is that it might quickly restore operations, but the con is that it encourages future attacks and the hackers might not keep their word. Projected Impact: +35 Company Resilience.",
        "complexity": "High",
        "projected_impact": 35
    }
]
