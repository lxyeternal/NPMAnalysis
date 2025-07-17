import matplotlib.pyplot as plt
import numpy as np

# Data preparation
summary_data = {
    "Credential Theft": 944,
    "Browser Manipulation": 1911,
    "System Reconnaissance": 11646,
    "Data Exfiltration": 11726,
    "Network Communication": 11669,
    "File Operations": 1407,
    "Persistence Mechanisms": 6227,
    "Proxy Manipulation": 454,
    "Command Execution": 6558,
    "Obfuscation Techniques": 3428,
    "Malicious Payload Delivery": 1402,
    "Anti-Analysis": 376,
    "Prototype Pollution": 183,
    "Privilege Escalation": 35,
    "DDoS Capabilities": 68
}

package_data = {
    "Browser Manipulation": 441,
    "Network Communication": 4634,
    "Proxy Manipulation": 253,
    "Data Exfiltration": 4751,
    "System Reconnaissance": 4895,
    "Persistence Mechanisms": 5293,
    "Credential Theft": 290,
    "File Operations": 609,
    "Obfuscation Techniques": 1300,
    "Command Execution": 5167,
    "Malicious Payload Delivery": 698,
    "Anti-Analysis": 177,
    "Prototype Pollution": 61,
    "Privilege Escalation": 20,
    "DDoS Capabilities": 17
}

# Comparison Plot (Summary vs Package) - Optimized
plt.figure(figsize=(12, 8))
categories_common = set(summary_data.keys()) & set(package_data.keys())
categories_list = sorted(list(categories_common))

summary_values = [summary_data[cat] for cat in categories_list]
package_values = [package_data[cat] for cat in categories_list]

x = np.arange(len(categories_list))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 8))
bars1 = ax.bar(x - width/2, summary_values, width, label='Summary Analysis', 
               color='skyblue', alpha=0.8)
bars2 = ax.bar(x + width/2, package_values, width, label='Package Analysis', 
               color='lightcoral', alpha=0.8)

ax.set_ylabel('Count', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(categories_list, rotation=45, ha='right', fontsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.legend(fontsize=14)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on bars
def autolabel(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height):,}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, rotation=90)

autolabel(bars1)
autolabel(bars2)

# Remove top and right spines (border lines)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/behavior_annoation/key_results/malware_categories_comparison.pdf', dpi=300, bbox_inches='tight')
plt.show()

print("Comparison visualization has been generated and saved as PDF file!")