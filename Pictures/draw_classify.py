import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Wedge
import matplotlib.patches as mpatches

# Data preparation
summary_data = {
    "Command Execution": 6052,
    "Obfuscation Techniques": 2458,
    "Persistence Mechanisms": 6136,
    "Data Exfiltration": 10719,
    "Network Communication": 10761,
    "System Reconnaissance": 11106,
    "File Operations": 1022,
    "Malicious Payload Delivery": 1021,
    "Credential Theft": 749,
    "Proxy Manipulation": 386,
    "Anti-Analysis": 315,
    "Browser Manipulation": 1196,
    "Prototype Pollution": 113,
    "NSFW Content": 13,
    "Privilege Escalation": 21,
    "DDoS Capabilities": 34
}

package_data = {
    "Obfuscation Techniques": 1300,
    "Command Execution": 5167,
    "System Reconnaissance": 4895,
    "Data Exfiltration": 4751,
    "Network Communication": 4634,
    "Persistence Mechanisms": 5293,
    "File Operations": 609,
    "Malicious Payload Delivery": 698,
    "Credential Theft": 290,
    "Proxy Manipulation": 253,
    "Anti-Analysis": 177,
    "Browser Manipulation": 441,
    "Prototype Pollution": 61,
    "NSFW Content": 10,
    "Privilege Escalation": 20,
    "DDoS Capabilities": 17
}

# # Style 1: Horizontal Bar Chart with Academic Style
# plt.figure(figsize=(14, 10))
# categories = list(summary_data.keys())
# values = list(summary_data.values())

# # Sort by value for better visualization
# sorted_data = sorted(zip(categories, values), key=lambda x: x[1], reverse=True)
# categories_sorted = [x[0] for x in sorted_data]
# values_sorted = [x[1] for x in sorted_data]

# colors = plt.cm.Set3(np.linspace(0, 1, len(categories_sorted)))
# bars = plt.barh(categories_sorted, values_sorted, color=colors)

# plt.xlabel('Number of Occurrences', fontsize=12, fontweight='bold')
# plt.title('Distribution of Malicious Behavior Categories\n(Summary Analysis)', 
#           fontsize=14, fontweight='bold', pad=20)
# plt.grid(axis='x', alpha=0.3, linestyle='--')

# # Add value labels on bars
# for i, (bar, value) in enumerate(zip(bars, values_sorted)):
#     plt.text(value + 100, i, f'{value:,}', va='center', fontsize=10)

# plt.tight_layout()
# plt.savefig('malware_categories_horizontal.pdf', dpi=300, bbox_inches='tight')
# plt.show()

# Style 1: Horizontal Bar Chart with Academic Style
plt.figure(figsize=(12, 8))
categories = list(summary_data.keys())
values = list(summary_data.values())

# Sort by value for better visualization
sorted_data = sorted(zip(categories, values), key=lambda x: x[1], reverse=True)
categories_sorted = [x[0] for x in sorted_data]
values_sorted = [x[1] for x in sorted_data]

colors = plt.cm.Set3(np.linspace(0, 1, len(categories_sorted)))
bars = plt.barh(categories_sorted, values_sorted, color=colors)

plt.xlabel('Number of Occurrences', fontsize=16, fontweight='bold')
plt.title('Distribution of Malicious Behavior Categories\n(Summary Analysis)', 
          fontsize=20, fontweight='bold', pad=20)

for i, (bar, value) in enumerate(zip(bars, values_sorted)):
    plt.text(value + 50, i, f'{value:,}', va='center', fontsize=14)  # Increased from 10, reduced offset

plt.grid(axis='x', alpha=0.3, linestyle='--')

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars, values_sorted)):
    plt.text(value + 100, i, f'{value:,}', va='center', fontsize=10)

plt.tight_layout()
plt.savefig('malware_categories_horizontal.pdf', dpi=300, bbox_inches='tight')
plt.show()


# Style 2: Donut Chart for Top Categories
plt.figure(figsize=(12, 8))
top_n = 8
top_categories = sorted_data[:top_n]
other_sum = sum([x[1] for x in sorted_data[top_n:]])
if other_sum > 0:
    top_categories.append(('Others', other_sum))

labels = [x[0] for x in top_categories]
sizes = [x[1] for x in top_categories]

colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
wedges, texts, autotexts = plt.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                   startangle=90, colors=colors,
                                   pctdistance=0.85)

# Create donut shape
centre_circle = plt.Circle((0,0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.title('Top Malicious Behavior Categories\n(Donut Chart)', 
          fontsize=14, fontweight='bold', pad=20)
plt.axis('equal')
plt.tight_layout()
plt.savefig('malware_categories_donut.pdf', dpi=300, bbox_inches='tight')
plt.show()




# # Style 3: Comparison Plot (Summary vs Package)
# plt.figure(figsize=(16, 10))
# categories_common = set(summary_data.keys()) & set(package_data.keys())
# categories_list = sorted(list(categories_common))

# summary_values = [summary_data[cat] for cat in categories_list]
# package_values = [package_data[cat] for cat in categories_list]

# x = np.arange(len(categories_list))
# width = 0.35

# fig, ax = plt.subplots(figsize=(16, 10))
# bars1 = ax.bar(x - width/2, summary_values, width, label='Summary Analysis', 
#                color='skyblue', alpha=0.8)
# bars2 = ax.bar(x + width/2, package_values, width, label='Package Analysis', 
#                color='lightcoral', alpha=0.8)

# ax.set_xlabel('Malicious Behavior Categories', fontsize=12, fontweight='bold')
# ax.set_ylabel('Count', fontsize=12, fontweight='bold')
# ax.set_title('Comparison of Malicious Behavior Categories\n(Summary vs Package Analysis)', 
#              fontsize=14, fontweight='bold', pad=20)
# ax.set_xticks(x)
# ax.set_xticklabels(categories_list, rotation=45, ha='right')
# ax.legend()
# ax.grid(axis='y', alpha=0.3, linestyle='--')

# # Add value labels on bars
# def autolabel(bars):
#     for bar in bars:
#         height = bar.get_height()
#         ax.annotate(f'{int(height):,}',
#                     xy=(bar.get_x() + bar.get_width() / 2, height),
#                     xytext=(0, 3),
#                     textcoords="offset points",
#                     ha='center', va='bottom', fontsize=8, rotation=90)

# autolabel(bars1)
# autolabel(bars2)

# plt.tight_layout()
# plt.savefig('malware_categories_comparison.pdf', dpi=300, bbox_inches='tight')
# plt.show()


# Style 3: Comparison Plot (Summary vs Package)


# Style 3: Comparison Plot (Summary vs Package) - Optimized
plt.figure(figsize=(12, 8))  # Reduced from (16, 10)
categories_common = set(summary_data.keys()) & set(package_data.keys())
categories_list = sorted(list(categories_common))

summary_values = [summary_data[cat] for cat in categories_list]
package_values = [package_data[cat] for cat in categories_list]

x = np.arange(len(categories_list))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 8))  # Reduced from (16, 10)
bars1 = ax.bar(x - width/2, summary_values, width, label='Summary Analysis', 
               color='skyblue', alpha=0.8)
bars2 = ax.bar(x + width/2, package_values, width, label='Package Analysis', 
               color='lightcoral', alpha=0.8)

#ax.set_xlabel('Malicious Behavior Categories', fontsize=16, fontweight='bold')  # Increased from 12
ax.set_ylabel('Count', fontsize=16, fontweight='bold')  # Increased from 12
ax.set_title('Comparison of Malicious Behavior Categories', 
             fontsize=18, fontweight='bold', pad=20)  # Increased from 14
ax.set_xticks(x)
ax.set_xticklabels(categories_list, rotation=45, ha='right', fontsize=12)  # Added fontsize
ax.tick_params(axis='y', labelsize=12)  # Added y-axis tick font size
ax.legend(fontsize=14)  # Added legend font size
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on bars
def autolabel(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height):,}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, rotation=90)  # Increased from 8

autolabel(bars1)
autolabel(bars2)

# Remove top and right spines (border lines)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('malware_categories_comparison.pdf', dpi=300, bbox_inches='tight')
plt.show()



# Style 4: Heatmap Style Visualization
plt.figure(figsize=(14, 8))
df = pd.DataFrame({
    'Summary Analysis': [summary_data.get(cat, 0) for cat in categories_list],
    'Package Analysis': [package_data.get(cat, 0) for cat in categories_list]
}, index=categories_list)

# Normalize for better heatmap visualization
df_norm = df.div(df.max(axis=1), axis=0)

sns.heatmap(df_norm.T, annot=df.T, fmt='d', cmap='YlOrRd', 
            cbar_kws={'label': 'Normalized Intensity'})
plt.title('Malicious Behavior Categories Heatmap\n(Summary vs Package Analysis)', 
          fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Malicious Behavior Categories', fontsize=12, fontweight='bold')
plt.ylabel('Analysis Type', fontsize=12, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('malware_categories_heatmap.pdf', dpi=300, bbox_inches='tight')
plt.show()

# Style 5: Stacked Area Chart
plt.figure(figsize=(14, 8))
categories_sorted_common = [cat for cat in categories_sorted if cat in package_data]
summary_vals = [summary_data[cat] for cat in categories_sorted_common]
package_vals = [package_data[cat] for cat in categories_sorted_common]

x = range(len(categories_sorted_common))
plt.stackplot(x, summary_vals, package_vals, 
              labels=['Summary Analysis', 'Package Analysis'],
              alpha=0.7, colors=['lightblue', 'lightgreen'])

plt.xlabel('Category Index (Sorted by Summary Count)', fontsize=12, fontweight='bold')
plt.ylabel('Cumulative Count', fontsize=12, fontweight='bold')
plt.title('Cumulative Distribution of Malicious Behavior Categories', 
          fontsize=14, fontweight='bold', pad=20)
plt.legend(loc='upper right')
plt.grid(alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('malware_categories_stacked.pdf', dpi=300, bbox_inches='tight')
plt.show()

print("All visualizations have been generated and saved as PDF files!")