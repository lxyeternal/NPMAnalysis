import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

class MalwareDetectionAnalyzer:
    def __init__(self, json_file_path):
        """Initialize the analyzer with JSON data"""
        with open(json_file_path, 'r') as f:
            self.data = json.load(f)
        
        self.total_samples = 6547
        self.combinations = self.data['combinations']
        self.df = pd.DataFrame(self.combinations)
        
        # Calculate detection rates for each tool
        self.tool_detection_rates = self._calculate_individual_detection_rates()
        
    def _calculate_individual_detection_rates(self):
        """Calculate individual tool detection rates"""
        tool_stats = {}
        
        # Extract unique tools and their false negatives
        tools_fn = {}
        for combo in self.combinations:
            tool1 = combo['tool1_name']
            tool2 = combo['tool2_name']
            tools_fn[tool1] = combo['tool1_false_negatives']
            tools_fn[tool2] = combo['tool2_false_negatives']
        
        for tool, fn in tools_fn.items():
            detected = self.total_samples - fn
            detection_rate = (detected / self.total_samples) * 100
            tool_stats[tool] = {
                'detected': detected,
                'false_negatives': fn,
                'detection_rate': detection_rate
            }
        
        return tool_stats
    
    def generate_latex_tables(self):
        """Generate LaTeX tables for the analysis"""
        
        # Table 1: Individual Tool Performance
        latex_individual = self._generate_individual_performance_table()
        
        # Table 2: Top 10 Tool Combinations
        latex_combinations = self._generate_top_combinations_table()
        
        # Table 3: Overlap Analysis Matrix
        latex_overlap = self._generate_overlap_matrix_table()
        
        return latex_individual, latex_combinations, latex_overlap
    
    def _generate_individual_performance_table(self):
        """Generate LaTeX table for individual tool performance"""
        latex = """
\\begin{table}[htbp]
\\centering
\\caption{Individual Tool Detection Performance}
\\label{tab:individual_performance}
\\begin{tabular}{|l|r|r|r|}
\\hline
\\textbf{Tool} & \\textbf{Detected} & \\textbf{False Negatives} & \\textbf{Detection Rate (\\%)} \\\\
\\hline
"""
        
        # Sort tools by detection rate
        sorted_tools = sorted(self.tool_detection_rates.items(), 
                            key=lambda x: x[1]['detection_rate'], reverse=True)
        
        for tool, stats in sorted_tools:
            latex += f"{tool.replace('_', '\\_')} & {stats['detected']} & {stats['false_negatives']} & {stats['detection_rate']:.2f} \\\\\n"
        
        latex += """\\hline
\\end{tabular}
\\end{table}
"""
        return latex
    
    def _generate_top_combinations_table(self):
        """Generate LaTeX table for top tool combinations"""
        latex = """
\\begin{table}[htbp]
\\centering
\\caption{Top 10 Tool Combinations by Detection Improvement}
\\label{tab:top_combinations}
\\resizebox{\\textwidth}{!}{%
\\begin{tabular}{|l|l|r|r|r|r|r|}
\\hline
\\textbf{Tool 1} & \\textbf{Tool 2} & \\textbf{Joint FN} & \\textbf{Improvement T1} & \\textbf{Improvement T2} & \\textbf{Improve Rate T1 (\\%)} & \\textbf{Improve Rate T2 (\\%)} \\\\
\\hline
"""
        
        # Sort by total improvement (sum of both tools)
        sorted_combos = sorted(self.combinations, 
                             key=lambda x: x['improvement_over_tool1'] + x['improvement_over_tool2'], 
                             reverse=True)[:10]
        
        for combo in sorted_combos:
            t1 = combo['tool1_name'].replace('_', '\\_')
            t2 = combo['tool2_name'].replace('_', '\\_')
            latex += f"{t1} & {t2} & {combo['joint_false_negatives']} & {combo['improvement_over_tool1']} & {combo['improvement_over_tool2']} & {combo['improvement_rate_tool1_percent']:.2f} & {combo['improvement_rate_tool2_percent']:.2f} \\\\\n"
        
        latex += """\\hline
\\end{tabular}
}
\\end{table}
"""
        return latex
    
    def _generate_overlap_matrix_table(self):
        """Generate LaTeX table for overlap analysis"""
        tools = list(self.tool_detection_rates.keys())
        
        latex = """
\\begin{table}[htbp]
\\centering
\\caption{Tool Combination Overlap Matrix (Joint False Negatives)}
\\label{tab:overlap_matrix}
\\resizebox{\\textwidth}{!}{%
\\begin{tabular}{|l|""" + "c|" * len(tools) + """}
\\hline
\\textbf{Tool} & """ + " & ".join([f"\\textbf{{{t.replace('_', '\\_')}}}" for t in tools]) + """ \\\\
\\hline
"""
        
        # Create overlap matrix
        overlap_matrix = {}
        for combo in self.combinations:
            t1, t2 = combo['tool1_name'], combo['tool2_name']
            overlap_matrix[(t1, t2)] = combo['joint_false_negatives']
            overlap_matrix[(t2, t1)] = combo['joint_false_negatives']
        
        for tool1 in tools:
            row = tool1.replace('_', '\\_')
            for tool2 in tools:
                if tool1 == tool2:
                    row += f" & {self.tool_detection_rates[tool1]['false_negatives']}"
                else:
                    fn = overlap_matrix.get((tool1, tool2), '-')
                    row += f" & {fn}"
            row += " \\\\\n"
            latex += row
        
        latex += """\\hline
\\end{tabular}
}
\\end{table}
"""
        return latex
    
    def create_visualizations(self):
        """Create comprehensive visualizations"""
        plt.style.use('seaborn-v0_8')
        fig = plt.figure(figsize=(20, 16))
        
        # 1. Individual Tool Performance Bar Chart
        ax1 = plt.subplot(2, 3, 1)
        self._plot_individual_performance(ax1)
        
        # 2. Detection Improvement Heatmap
        ax2 = plt.subplot(2, 3, 2)
        self._plot_improvement_heatmap(ax2)
        
        # 3. Best Combinations Bar Chart
        ax3 = plt.subplot(2, 3, 3)
        self._plot_best_combinations(ax3)
        
        # 4. Overlap Analysis Matrix
        ax4 = plt.subplot(2, 3, 4)
        self._plot_overlap_matrix(ax4)
        
        # 5. Trade-off Analysis Scatter Plot
        ax5 = plt.subplot(2, 3, 5)
        self._plot_tradeoff_analysis(ax5)
        
        # 6. Tool Complementarity Network
        ax6 = plt.subplot(2, 3, 6)
        self._plot_complementarity_network(ax6)
        
        plt.tight_layout()
        plt.savefig('malware_detection_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def _plot_individual_performance(self, ax):
        """Plot individual tool performance"""
        tools = list(self.tool_detection_rates.keys())
        detection_rates = [self.tool_detection_rates[tool]['detection_rate'] for tool in tools]
        
        bars = ax.bar(range(len(tools)), detection_rates, color='steelblue', alpha=0.7)
        ax.set_xlabel('Tools')
        ax.set_ylabel('Detection Rate (%)')
        ax.set_title('Individual Tool Detection Performance')
        ax.set_xticks(range(len(tools)))
        ax.set_xticklabels([t.replace('_', ' ') for t in tools], rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, rate in zip(bars, detection_rates):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                   f'{rate:.1f}%', ha='center', va='bottom')
    
    def _plot_improvement_heatmap(self, ax):
        """Plot improvement rate heatmap"""
        tools = list(self.tool_detection_rates.keys())
        improvement_matrix = np.zeros((len(tools), len(tools)))
        
        tool_to_idx = {tool: i for i, tool in enumerate(tools)}
        
        for combo in self.combinations:
            i = tool_to_idx[combo['tool1_name']]
            j = tool_to_idx[combo['tool2_name']]
            improvement_matrix[i][j] = combo['improvement_rate_tool1_percent']
            improvement_matrix[j][i] = combo['improvement_rate_tool2_percent']
        
        im = ax.imshow(improvement_matrix, cmap='RdYlBu_r', aspect='auto')
        ax.set_xticks(range(len(tools)))
        ax.set_yticks(range(len(tools)))
        ax.set_xticklabels([t.replace('_', ' ') for t in tools], rotation=45, ha='right')
        ax.set_yticklabels([t.replace('_', ' ') for t in tools])
        ax.set_title('Detection Improvement Rate Heatmap (%)')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Improvement Rate (%)')
    
    def _plot_best_combinations(self, ax):
        """Plot best tool combinations"""
        top_10 = sorted(self.combinations, 
                       key=lambda x: x['improvement_over_tool1'] + x['improvement_over_tool2'], 
                       reverse=True)[:10]
        
        combo_names = [f"{c['tool1_name']}\n+\n{c['tool2_name']}" for c in top_10]
        total_improvements = [c['improvement_over_tool1'] + c['improvement_over_tool2'] for c in top_10]
        
        bars = ax.barh(range(len(combo_names)), total_improvements, color='lightcoral', alpha=0.7)
        ax.set_yticks(range(len(combo_names)))
        ax.set_yticklabels([name.replace('_', ' ') for name in combo_names])
        ax.set_xlabel('Total Detection Improvement')
        ax.set_title('Top 10 Tool Combinations by Total Improvement')
        
        # Add value labels
        for bar, improvement in zip(bars, total_improvements):
            ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2,
                   f'{improvement}', ha='left', va='center')
    
    def _plot_overlap_matrix(self, ax):
        """Plot overlap matrix as heatmap"""
        tools = list(self.tool_detection_rates.keys())
        overlap_matrix = np.zeros((len(tools), len(tools)))
        
        tool_to_idx = {tool: i for i, tool in enumerate(tools)}
        
        for combo in self.combinations:
            i = tool_to_idx[combo['tool1_name']]
            j = tool_to_idx[combo['tool2_name']]
            overlap_matrix[i][j] = combo['joint_false_negatives']
            overlap_matrix[j][i] = combo['joint_false_negatives']
        
        # Set diagonal to individual false negatives
        for i, tool in enumerate(tools):
            overlap_matrix[i][i] = self.tool_detection_rates[tool]['false_negatives']
        
        im = ax.imshow(overlap_matrix, cmap='Reds', aspect='auto')
        ax.set_xticks(range(len(tools)))
        ax.set_yticks(range(len(tools)))
        ax.set_xticklabels([t.replace('_', ' ') for t in tools], rotation=45, ha='right')
        ax.set_yticklabels([t.replace('_', ' ') for t in tools])
        ax.set_title('Joint False Negatives Matrix')
        
        # Add text annotations
        for i in range(len(tools)):
            for j in range(len(tools)):
                ax.text(j, i, f'{int(overlap_matrix[i][j])}', ha='center', va='center',
                       color='white' if overlap_matrix[i][j] > overlap_matrix.max()/2 else 'black')
    
    def _plot_tradeoff_analysis(self, ax):
        """Plot trade-off between detection rate and performance"""
        # Create scatter plot showing improvement vs joint false negatives
        improvements = [c['improvement_over_tool1'] + c['improvement_over_tool2'] for c in self.combinations]
        joint_fns = [c['joint_false_negatives'] for c in self.combinations]
        
        scatter = ax.scatter(joint_fns, improvements, alpha=0.6, s=60, c=improvements, cmap='viridis')
        ax.set_xlabel('Joint False Negatives')
        ax.set_ylabel('Total Detection Improvement')
        ax.set_title('Trade-off: Detection Improvement vs Joint FN')
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Total Improvement')
        
        # Highlight best combinations
        best_combos = sorted(self.combinations, 
                           key=lambda x: x['improvement_over_tool1'] + x['improvement_over_tool2'], 
                           reverse=True)[:3]
        
        for combo in best_combos:
            improvement = combo['improvement_over_tool1'] + combo['improvement_over_tool2']
            joint_fn = combo['joint_false_negatives']
            ax.annotate(f"{combo['tool1_name']}+{combo['tool2_name']}", 
                       (joint_fn, improvement), xytext=(10, 10), 
                       textcoords='offset points', fontsize=8,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    def _plot_complementarity_network(self, ax):
        """Plot tool complementarity network"""
        tools = list(self.tool_detection_rates.keys())
        n_tools = len(tools)
        
        # Position tools in a circle
        angles = np.linspace(0, 2*np.pi, n_tools, endpoint=False)
        positions = {tool: (np.cos(angle), np.sin(angle)) for tool, angle in zip(tools, angles)}
        
        # Draw tool nodes
        for tool, (x, y) in positions.items():
            detection_rate = self.tool_detection_rates[tool]['detection_rate']
            size = detection_rate * 10  # Scale node size by detection rate
            ax.scatter(x, y, s=size, alpha=0.7, c=detection_rate, cmap='RdYlGn', 
                      vmin=0, vmax=100, edgecolors='black', linewidth=1)
            ax.text(x*1.2, y*1.2, tool.replace('_', ' '), ha='center', va='center', fontsize=8)
        
        # Draw edges for strong complementarity (>50% improvement)
        for combo in self.combinations:
            if combo['improvement_rate_tool1_percent'] > 50 or combo['improvement_rate_tool2_percent'] > 50:
                x1, y1 = positions[combo['tool1_name']]
                x2, y2 = positions[combo['tool2_name']]
                
                # Line thickness based on improvement
                thickness = (combo['improvement_rate_tool1_percent'] + combo['improvement_rate_tool2_percent']) / 100
                ax.plot([x1, x2], [y1, y2], 'b-', alpha=0.5, linewidth=thickness)
        
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.set_title('Tool Complementarity Network\n(Node size = Detection Rate, Edge = Strong Complementarity)')
        ax.axis('off')
    
    def generate_research_insights(self):
        """Generate insights for the four research questions"""
        insights = {}
        
        # RQ4.1: Overlap and unique detection coverage
        insights['RQ4.1'] = self._analyze_overlap_coverage()
        
        # RQ4.2: Best tool combinations
        insights['RQ4.2'] = self._analyze_best_combinations()
        
        # RQ4.3: Trade-offs between detection rate and performance
        insights['RQ4.3'] = self._analyze_tradeoffs()
        
        # RQ4.4: Optimal tool combination strategy
        insights['RQ4.4'] = self._analyze_optimal_strategy()
        
        return insights
    
    def _analyze_overlap_coverage(self):
        """Analyze overlap and unique detection coverage"""
        tools = list(self.tool_detection_rates.keys())
        analysis = {}
        
        for tool in tools:
            unique_detections = []
            for combo in self.combinations:
                if combo['tool1_name'] == tool:
                    unique_detections.append(combo['packages_detected_by_tool1_only'])
                elif combo['tool2_name'] == tool:
                    unique_detections.append(combo['packages_detected_by_tool2_only'])
            
            analysis[tool] = {
                'detection_rate': self.tool_detection_rates[tool]['detection_rate'],
                'avg_unique_contribution': np.mean(unique_detections) if unique_detections else 0,
                'max_unique_contribution': max(unique_detections) if unique_detections else 0
            }
        
        return analysis
    
    def _analyze_best_combinations(self):
        """Analyze best tool combinations"""
        # Top combinations by different metrics
        best_total = max(self.combinations, key=lambda x: x['improvement_over_tool1'] + x['improvement_over_tool2'])
        best_rate = max(self.combinations, key=lambda x: x['improvement_rate_tool1_percent'] + x['improvement_rate_tool2_percent'])
        best_balanced = min(self.combinations, key=lambda x: x['joint_false_negatives'])
        
        return {
            'best_total_improvement': best_total,
            'best_improvement_rate': best_rate,
            'best_joint_coverage': best_balanced
        }
    
    def _analyze_tradeoffs(self):
        """Analyze trade-offs between detection rate and performance"""
        # Calculate efficiency metrics
        efficiency_metrics = []
        for combo in self.combinations:
            total_improvement = combo['improvement_over_tool1'] + combo['improvement_over_tool2']
            joint_fn = combo['joint_false_negatives']
            efficiency = total_improvement / (joint_fn + 1)  # +1 to avoid division by zero
            
            efficiency_metrics.append({
                'combination': f"{combo['tool1_name']}+{combo['tool2_name']}",
                'efficiency': efficiency,
                'total_improvement': total_improvement,
                'joint_fn': joint_fn
            })
        
        # Sort by efficiency
        efficiency_metrics.sort(key=lambda x: x['efficiency'], reverse=True)
        
        return {
            'most_efficient': efficiency_metrics[:5],
            'least_efficient': efficiency_metrics[-5:],
            'average_efficiency': np.mean([m['efficiency'] for m in efficiency_metrics])
        }
    
    def _analyze_optimal_strategy(self):
        """Analyze optimal tool combination strategy"""
        strategies = {
            'high_coverage': [],  # Minimize joint false negatives
            'high_improvement': [],  # Maximize improvement
            'balanced': []  # Good balance of both
        }
        
        # Sort combinations by different criteria
        by_coverage = sorted(self.combinations, key=lambda x: x['joint_false_negatives'])
        by_improvement = sorted(self.combinations, key=lambda x: x['improvement_over_tool1'] + x['improvement_over_tool2'], reverse=True)
        
        # Calculate balanced score (normalized improvement / normalized joint_fn)
        max_improvement = max(c['improvement_over_tool1'] + c['improvement_over_tool2'] for c in self.combinations)
        max_joint_fn = max(c['joint_false_negatives'] for c in self.combinations)
        
        balanced_scores = []
        for combo in self.combinations:
            improvement_norm = (combo['improvement_over_tool1'] + combo['improvement_over_tool2']) / max_improvement
            joint_fn_norm = combo['joint_false_negatives'] / max_joint_fn
            balanced_score = improvement_norm / (joint_fn_norm + 0.1)  # +0.1 to avoid division by zero
            balanced_scores.append((balanced_score, combo))
        
        balanced_scores.sort(reverse=True)
        
        strategies['high_coverage'] = by_coverage[:5]
        strategies['high_improvement'] = by_improvement[:5]
        strategies['balanced'] = [combo for score, combo in balanced_scores[:5]]
        
        return strategies
    
    def save_results(self):
        """Save all results to files"""
        # Generate LaTeX tables
        latex_individual, latex_combinations, latex_overlap = self.generate_latex_tables()
        
        # Save LaTeX tables
        with open('malware_analysis_tables.tex', 'w') as f:
            f.write("% Individual Tool Performance\n")
            f.write(latex_individual)
            f.write("\n% Top Tool Combinations\n")
            f.write(latex_combinations)
            f.write("\n% Overlap Matrix\n")
            f.write(latex_overlap)
        
        # Generate and save insights
        insights = self.generate_research_insights()
        with open('research_insights.json', 'w') as f:
            json.dump(insights, f, indent=2, default=str)
        
        # Create visualizations
        self.create_visualizations()
        
        print("Analysis complete! Files saved:")
        print("- malware_analysis_tables.tex")
        print("- research_insights.json")
        print("- malware_detection_analysis.png")

def main():
    # Initialize analyzer
    analyzer = MalwareDetectionAnalyzer('/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/tool_detect/tool_output_statistic/reports/complement/joint_detection_summary.json')
    
    # Save all results
    analyzer.save_results()
    
    # Print summary statistics
    print("\n=== SUMMARY STATISTICS ===")
    print(f"Total malicious samples: {analyzer.total_samples}")
    print(f"Total tool combinations analyzed: {len(analyzer.combinations)}")
    
    print("\n=== TOP 3 INDIVIDUAL TOOLS ===")
    sorted_tools = sorted(analyzer.tool_detection_rates.items(), 
                         key=lambda x: x[1]['detection_rate'], reverse=True)
    for i, (tool, stats) in enumerate(sorted_tools[:3]):
        print(f"{i+1}. {tool}: {stats['detection_rate']:.2f}% detection rate")
    
    print("\n=== TOP 3 TOOL COMBINATIONS ===")
    top_combos = sorted(analyzer.combinations, 
                       key=lambda x: x['improvement_over_tool1'] + x['improvement_over_tool2'], 
                       reverse=True)[:3]
    for i, combo in enumerate(top_combos):
        total_improvement = combo['improvement_over_tool1'] + combo['improvement_over_tool2']
        print(f"{i+1}. {combo['tool1_name']} + {combo['tool2_name']}: {total_improvement} total improvement")

if __name__ == "__main__":
    main()