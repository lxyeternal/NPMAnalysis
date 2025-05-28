import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

# Data from the table
years = ['2011-2020', '2021', '2022', '2023', '2024-2025']
malicious_counts = [292, 827, 1674, 1781, 1727]
total = 6292

# Set up the plotting style
plt.style.use('default')
sns.set_palette("husl")

# Create a figure with multiple subplots
fig = plt.figure(figsize=(20, 15))

# 1. Bar Chart - Classic Style
ax1 = plt.subplot(2, 3, 1)
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
bars = ax1.bar(years, malicious_counts, color=colors, edgecolor='black', linewidth=1.5)
ax1.set_title('Malicious NPM Packages by Year\n(Bar Chart)', fontsize=14, fontweight='bold', pad=20)
ax1.set_ylabel('Number of Malicious Packages', fontsize=12)
ax1.set_xlabel('Years', fontsize=12)
ax1.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bar, value in zip(bars, malicious_counts):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
             str(value), ha='center', va='bottom', fontweight='bold')

plt.xticks(rotation=45)

# 2. Line Chart with Markers
ax2 = plt.subplot(2, 3, 2)
ax2.plot(years, malicious_counts, marker='o', linewidth=3, markersize=10, 
         color='#E74C3C', markerfacecolor='#F39C12', markeredgecolor='white', 
         markeredgewidth=2)
ax2.fill_between(years, malicious_counts, alpha=0.3, color='#E74C3C')
ax2.set_title('Malicious NPM Packages Trend\n(Line Chart)', fontsize=14, fontweight='bold', pad=20)
ax2.set_ylabel('Number of Malicious Packages', fontsize=12)
ax2.set_xlabel('Years', fontsize=12)
ax2.grid(True, alpha=0.3)

# Add value labels
for i, (year, value) in enumerate(zip(years, malicious_counts)):
    ax2.annotate(str(value), (i, value), textcoords="offset points", 
                xytext=(0,10), ha='center', fontweight='bold')

plt.xticks(rotation=45)

# # 3. Pie Chart
# ax3 = plt.subplot(2, 3, 3)
# colors_pie = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC']
# wedges, texts, autotexts = ax3.pie(malicious_counts, labels=years, autopct='%1.1f%%',
#                                    colors=colors_pie, startangle=90, 
#                                    explode=(0.05, 0.05, 0.05, 0.05, 0.05))
# ax3.set_title('Distribution of Malicious NPM Packages\n(Pie Chart)', 
#               fontsize=14, fontweight='bold', pad=20)

# # Enhance pie chart text
# for autotext in autotexts:
#     autotext.set_color('white')
#     autotext.set_fontweight('bold')


# 3. Pie Chart
ax3 = plt.subplot(2, 3, 3)
colors_pie = [ 
                 '#e377c2', '#17becf',
                 '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5']  # Softer, more academic colors
wedges, texts, autotexts = ax3.pie(malicious_counts, labels=years, autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*sum(malicious_counts))})',
                                   colors=colors_pie, startangle=90, 
                                   explode=(0.05, 0.05, 0.05, 0.05, 0.05))
ax3.set_title('Distribution of Malicious NPM Packages', 
              fontsize=14, fontweight='bold', pad=20)

# Enhance pie chart text - larger font for better visibility when scaled
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(11)  # Larger font size

# Enhance year labels
for text in texts:
    text.set_fontsize(10)
    text.set_fontweight('bold')

# 4. Horizontal Bar Chart with Gradient Effect
ax4 = plt.subplot(2, 3, 4)
y_pos = np.arange(len(years))
colors_gradient = ['#FF6B6B', '#FF8E53', '#FF6B9D', '#C44569', '#F8B500']
bars_h = ax4.barh(y_pos, malicious_counts, color=colors_gradient, 
                  edgecolor='black', linewidth=1.5)
ax4.set_yticks(y_pos)
ax4.set_yticklabels(years)
ax4.set_xlabel('Number of Malicious Packages', fontsize=12)
ax4.set_title('Malicious NPM Packages\n(Horizontal Bar Chart)', 
              fontsize=14, fontweight='bold', pad=20)
ax4.grid(True, alpha=0.3, axis='x')

# Add value labels
for i, (bar, value) in enumerate(zip(bars_h, malicious_counts)):
    ax4.text(bar.get_width() + 30, bar.get_y() + bar.get_height()/2,
             str(value), ha='left', va='center', fontweight='bold')

# 5. Area Chart
ax5 = plt.subplot(2, 3, 5)
x_numeric = range(len(years))
ax5.fill_between(x_numeric, malicious_counts, alpha=0.7, color='#3498DB')
ax5.plot(x_numeric, malicious_counts, color='#2C3E50', linewidth=3, 
         marker='s', markersize=8, markerfacecolor='#E74C3C', 
         markeredgecolor='white', markeredgewidth=2)
ax5.set_xticks(x_numeric)
ax5.set_xticklabels(years, rotation=45)
ax5.set_title('Malicious NPM Packages Growth\n(Area Chart)', 
              fontsize=14, fontweight='bold', pad=20)
ax5.set_ylabel('Number of Malicious Packages', fontsize=12)
ax5.grid(True, alpha=0.3)

# 6. Stacked Bar Chart (showing cumulative effect)
ax6 = plt.subplot(2, 3, 6)
cumulative = np.cumsum(malicious_counts)
bottom_values = [0] + cumulative[:-1].tolist()

colors_stack = ['#E8F4FD', '#B8E6B8', '#FFB347', '#DDA0DD', '#F0E68C']
for i, (year, count, bottom) in enumerate(zip(years, malicious_counts, bottom_values)):
    ax6.bar(0, count, bottom=bottom, color=colors_stack[i], 
            edgecolor='black', linewidth=1, label=f'{year}: {count}')

ax6.set_title('Cumulative Malicious NPM Packages\n(Stacked Bar)', 
              fontsize=14, fontweight='bold', pad=20)
ax6.set_ylabel('Cumulative Count', fontsize=12)
ax6.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax6.set_xlim(-0.5, 0.5)
ax6.set_xticks([])

# Add total label
ax6.text(0, total + 50, f'Total: {total}', ha='center', va='bottom', 
         fontweight='bold', fontsize=12, bbox=dict(boxstyle="round,pad=0.3", 
         facecolor="yellow", alpha=0.7))

plt.tight_layout()
plt.savefig('malicious_npm_packages_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# Create a second figure with more artistic styles
fig2 = plt.figure(figsize=(15, 10))

# 7. Violin Plot Style (using scatter with varying sizes)
ax7 = plt.subplot(2, 2, 1)
x_pos = range(len(years))
sizes = [count/10 for count in malicious_counts]  # Scale for visibility
colors_scatter = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']

for i, (x, y, size, color) in enumerate(zip(x_pos, malicious_counts, sizes, colors_scatter)):
    ax7.scatter(x, y, s=size*10, color=color, alpha=0.7, edgecolors='black', linewidth=2)
    ax7.text(x, y + 100, str(y), ha='center', va='bottom', fontweight='bold')

ax7.set_xticks(x_pos)
ax7.set_xticklabels(years, rotation=45)
ax7.set_title('Malicious NPM Packages\n(Bubble Chart)', fontsize=14, fontweight='bold')
ax7.set_ylabel('Number of Malicious Packages', fontsize=12)
ax7.grid(True, alpha=0.3)

# 8. Radar Chart Style
ax8 = plt.subplot(2, 2, 2, projection='polar')
angles = np.linspace(0, 2 * np.pi, len(years), endpoint=False).tolist()
values = malicious_counts + [malicious_counts[0]]  # Complete the circle
angles += angles[:1]

ax8.plot(angles, values, color='#E74C3C', linewidth=3, marker='o', markersize=8)
ax8.fill(angles, values, color='#E74C3C', alpha=0.25)
ax8.set_xticks(angles[:-1])
ax8.set_xticklabels(years)
ax8.set_title('Malicious NPM Packages\n(Radar Chart)', fontsize=14, fontweight='bold', pad=30)

# 9. Heatmap Style
ax9 = plt.subplot(2, 2, 3)
data_matrix = np.array(malicious_counts).reshape(1, -1)
im = ax9.imshow(data_matrix, cmap='Reds', aspect='auto')
ax9.set_xticks(range(len(years)))
ax9.set_xticklabels(years, rotation=45)
ax9.set_yticks([0])
ax9.set_yticklabels(['Malicious Count'])
ax9.set_title('Malicious NPM Packages\n(Heatmap)', fontsize=14, fontweight='bold')

# Add text annotations
for i, value in enumerate(malicious_counts):
    ax9.text(i, 0, str(value), ha='center', va='center', 
             fontweight='bold', color='white' if value > 1000 else 'black')

plt.colorbar(im, ax=ax9, orientation='horizontal', pad=0.1)

# 10. 3D-style Bar Chart
ax10 = plt.subplot(2, 2, 4)
x_3d = range(len(years))
colors_3d = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']

# Create 3D effect with multiple bars
for i, (x, height, color) in enumerate(zip(x_3d, malicious_counts, colors_3d)):
    # Shadow bars
    ax10.bar(x-0.02, height-20, width=0.8, color='gray', alpha=0.3, zorder=1)
    # Main bars
    ax10.bar(x, height, width=0.8, color=color, edgecolor='black', 
             linewidth=2, zorder=2)
    # Top highlight
    ax10.bar(x, height*0.1, bottom=height*0.9, width=0.8, 
             color='white', alpha=0.4, zorder=3)

ax10.set_xticks(x_3d)
ax10.set_xticklabels(years, rotation=45)
ax10.set_title('Malicious NPM Packages\n(3D-style Bar Chart)', 
               fontsize=14, fontweight='bold')
ax10.set_ylabel('Number of Malicious Packages', fontsize=12)
ax10.grid(True, alpha=0.3, axis='y')

# Add value labels
for x, height in zip(x_3d, malicious_counts):
    ax10.text(x, height + 50, str(height), ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('malicious_npm_packages_artistic.png', dpi=300, bbox_inches='tight')
plt.show()

print("Created beautiful visualizations of your NPM malicious packages data!")
print(f"Total malicious packages: {total}")
print("Generated 10 different chart styles across 2 figures")