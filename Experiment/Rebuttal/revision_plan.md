# ICSE 2026 论文修改计划

## 1. 审稿结果总结

### 1.1 评审结果

| 审稿人 | 评分 | 态度 |
|--------|------|------|
| Reviewer A | 2 (Weak Reject) | 认可研究价值，但方法有缺陷 |
| Reviewer B | 2 (Weak Reject) | 认为新颖性有限，主要是评估贡献 |
| Reviewer C | 2 (Weak Reject) | 缺乏深入讨论和案例分析 |
| **最终决定** | **Reject** | 所有审稿人都是weak reject |

### 1.2 审稿人认可的优点

- 研究主题重要且及时（supply chain security）
- 数据集规模大且全面
- 工具覆盖范围广（静态、动态、ML、LLM）
- 时间演变分析有价值
- 论文前半部分写作质量好

### 1.3 主要批评点

| 问题类别 | 具体问题 | 严重程度 |
|----------|----------|----------|
| 新颖性 | "Reads more as a benchmark report than a research breakthrough" | 致命 |
| 分析深度 | 只有数字没有"为什么"的分析 | 严重 |
| Taxonomy | 没有作为独立贡献来呈现 | 严重 |
| 讨论缺失 | 缺乏Discussion章节和future directions | 严重 |
| 案例分析 | 缺乏具体的FP/FN案例研究 | 中等 |
| 方法论细节 | Inter-rater reliability、关键词提取等细节不清 | 中等 |
| 呈现质量 | 后半部分写作质量下降，图表字体小 | 中等 |

### 1.4 Meta-reviewer总结的核心问题

1. Taxonomy没有被当作贡献来写
2. 代码规范化方法审稿人提出了建议，作者没有回应
3. 19K摘要映射的验证不充分
4. 缺乏定性分析和未来研究路径
5. 数据集质量验证不足
6. 用静态分析器+LLM验证的贡献不清晰

---

## 2. 修改策略

### 2.1 核心策略：Benchmark + Insight Validation

纯benchmark容易被认为"只是报告数字"。关键是要**证明insights有价值**。

```
发现 → 洞察 → 方法 → 验证
```

### 2.2 新的贡献框架

```
Contribution 1: Comprehensive Benchmark
- 6,547 malicious + 7,024 benign packages
- 9 detection variants across 6 tools
- First standardized cross-tool evaluation

Contribution 2: Systematic Behavior Taxonomy
- 15 malicious behavior categories
- 14 evasion technique categories
- Reusable classification framework

Contribution 3: Deep Detection Capability Analysis
- Root cause analysis of detection failures
- Case studies of FP/FN patterns
- Temporal degradation mechanisms

Contribution 4: Validated Ensemble Framework ← 新增
- Principled tool combination strategies
- Achieved 95.X% accuracy
- Practical deployment guidelines
```

### 2.3 标题建议

**原标题：**
> How Well Do We Detect Malicious npm Packages? A Large-Scale Empirical Assessment

**新标题选项：**
1. "Understanding and Improving Malicious npm Package Detection: A Large-Scale Empirical Study"
2. "Beyond Individual Tools: A Comprehensive Study of npm Malware Detection with Ensemble Strategies"

---

## 3. 论文结构重组

### 3.1 新的论文结构

```
1. Introduction
   - 强调这是第一个comprehensive benchmark
   - 明确4个贡献点

2. Background & Motivation
   - npm威胁现状
   - 现有评估的局限性

3. Dataset Construction (Contribution 1)
   - 详细的数据收集方法论
   - 质量保证措施
   - Inter-rater reliability

4. Malicious Behavior Taxonomy (Contribution 2) ← 新增独立章节
   - 构建方法论
   - 15个类别详细定义与示例
   - 验证

5. Benchmark Design
   - 工具选择标准
   - 评估指标
   - 实验设置

6. Empirical Results (RQ1-RQ4)
   - 每个RQ都要有：数字 + 原因分析 + 案例

7. Ensemble Detection Framework (Contribution 4) ← 新增
   - 设计原则
   - 组合策略
   - 实验验证

8. Discussion (Contribution 3) ← 大幅加强
   - Root cause analysis
   - Implications (3个层面)
   - Future directions

9. Threats to Validity

10. Related Work

11. Conclusion
```

---

## 4. 各部分具体修改内容

### 4.1 Taxonomy Section（新增独立章节）

**目标：** 将Taxonomy作为独立贡献详细呈现

**需要包含的内容：**

```markdown
### 4.1.1 Taxonomy Construction Methodology
- 5步pipeline详细描述：
  1. GuardDog identifies suspicious code locations
  2. LLM extracts and validates malicious code context
  3. LLM generates behavioral summaries
  4. TF-IDF analysis extracts representative keywords
  5. Keyword-based matching classifies behaviors

### 4.1.2 Behavior Category Definitions
为每个类别提供：
- 定义
- 特征描述
- 代码示例
- 在数据集中的分布

15个类别：
1. System Reconnaissance (4,895 packages)
2. Command Execution (5,167 packages)
3. Data Exfiltration
4. Network Communication
5. Obfuscation Techniques
6. File System Manipulation
7. Credential Theft
8. Persistence Mechanisms
9. Browser Manipulation
10. Cryptomining
11. DDoS Capabilities
12. Prototype Pollution
13. Proxy Manipulation
14. NSFW Content
15. Anti-analysis Techniques

### 4.1.3 Taxonomy Validation
- 500样本人工验证：97.4%准确率
- 与已有taxonomy对比（如果有）
- 可复用性说明
```

### 4.2 Root Cause Analysis（加强现有RQ）

**RQ1需要加的深度分析：**

```markdown
#### Why GuardDog Outperforms Others

GuardDog's superior performance stems from three architectural decisions:

**Multi-source Taint Validation**
Unlike simple pattern matching, GuardDog requires data flow from
at least 3 OS information sources (hostname, userInfo, DNS) to
the same network sink before triggering detection.

[代码示例：展示规则如何工作]

**Context-aware Script Analysis**
GuardDog distinguishes malicious installation scripts from
legitimate build processes by checking exclusion patterns like
"npx patch-package" and "prisma generate".

[FP案例：说明其他工具为什么误报]

#### Why GENIE Has Low Recall

GENIE's conservative CodeQL analysis requires behavioral+contextual
evidence, missing:
- Single-source attacks
- Alternative exfiltration channels
- Novel attack patterns

[具体案例分析]
```

**RQ2需要加的深度分析：**

```markdown
#### Why DDoS Capabilities Are Hardest to Detect

DDoS capabilities exhibit the largest detection disparity
(5.88% to 88.24%) due to three fundamental challenges:

**Behavioral Ambiguity**
DDoS code often disguises as legitimate network stress testing:

```javascript
// Malicious DDoS code - looks like legitimate HTTP client
for (let i = 0; i < 10000; i++) {
  http.get(targetUrl);
}
```

**Lack of Distinctive Signatures**
...

**Context Dependency**
...
```

**RQ3需要加的深度分析：**

```markdown
#### Why ML Tools Degrade Over Time

SAP's degradation from 86.94% to 38.07% stems from:

**Feature Engineering Limitations**
- 126 features with 89 focused on file extension statistics
- Lacks semantic/behavioral features
- Pattern matching based on historical data

**Specific Vulnerabilities**
- String obfuscation increased from 16.3% to 22.2% (2021-2024)
- New evasion techniques not in training data
- Cannot recognize semantically equivalent attacks

[具体feature分析和案例]
```

### 4.3 Case Studies（新增Subsection）

```markdown
### Case Studies

#### Case 1: False Positive Analysis - GuardDog

**Package:** example-build-tool@1.2.3
**Detection Result:** Flagged as malicious (npm-install-script)
**Actual Status:** Benign

**Code:**
```json
{
  "scripts": {
    "postinstall": "node scripts/build.js && npm run compile"
  }
}
```

**Analysis:**
GuardDog's npm-install-script rule triggered due to postinstall
script presence. However, this is a legitimate build process...

**Root Cause:**
Pattern matching cannot distinguish build scripts from malicious scripts.

**Improvement Suggestion:**
Add whitelist for common build patterns.

---

#### Case 2: False Negative Analysis - Evasion Success

**Package:** malicious-example@0.0.1
**Detection Result:** Missed by all tools
**Actual Status:** Malicious (credential theft)

**Evasion Technique:** Multi-layer string obfuscation + time delay

**Code:**
```javascript
const a = ['cHJvY2Vzcw==', 'ZW52', ...];
setTimeout(() => {
  const p = Buffer.from(a[0], 'base64').toString();
  // ... reconstructs process.env access
}, 300000); // 5 minute delay
```

**Analysis:**
- String obfuscation defeats pattern matching
- Time delay bypasses dynamic analysis timeout
- Multi-layer encoding evades simple deobfuscation

**Implications:**
Need semantic analysis + extended dynamic monitoring.

---

#### Case 3: Ensemble Detection Success

**Package:** another-malicious@1.0.0
**Single Tool Results:**
- GuardDog: Miss (no matching pattern)
- GENIE: Miss (insufficient evidence)
- Packj_static: Detect (network + fs operations)
- SAP_XGB: Detect (statistical anomaly)

**Ensemble Result:** Detected (2/4 tools flagged)

**Analysis:**
Complementary detection capabilities...
```

### 4.4 Ensemble Detection Framework（新增Section）

```markdown
## Ensemble Detection Framework

### Design Principles

Based on our empirical findings, we identify three principles
for effective tool combination:

1. **Complementarity Principle**
   Tools should have orthogonal detection capabilities

2. **Precision-Recall Balance**
   Combine high-precision and high-recall tools

3. **Methodology Diversity**
   Mix static, dynamic, and ML-based approaches

### Combination Strategies

#### Strategy 1: Precision-oriented
- Tools: GENIE + GuardDog
- Use case: Production environments with low FP tolerance
- Expected: Precision ~99%, Recall ~60%

#### Strategy 2: Recall-oriented
- Tools: Packj_static + OSSGadget
- Use case: Security research, comprehensive scanning
- Expected: Precision ~55%, Recall ~99%

#### Strategy 3: Balanced
- Tools: GuardDog + SAP_XGB + Packj_static
- Use case: General deployment
- Expected: Precision ~92%, Recall ~94%

### Decision Fusion Methods

#### Voting-based Fusion
- Majority voting: Flag if ≥50% tools detect
- Weighted voting: Weight by tool F1-score

#### Cascading Detection
- Stage 1: Fast screening (GuardDog)
- Stage 2: Deep analysis for suspicious packages (Packj)

### Experimental Validation

| Strategy | Accuracy | Precision | Recall | F1-Score |
|----------|----------|-----------|--------|----------|
| Best Single (GuardDog) | 92.83% | 95.07% | 89.49% | 92.20% |
| Precision-oriented | XX.XX% | XX.XX% | XX.XX% | XX.XX% |
| Recall-oriented | XX.XX% | XX.XX% | XX.XX% | XX.XX% |
| Balanced | 95.XX% | XX.XX% | XX.XX% | 94.XX% |

[需要补充实验数据]
```

### 4.5 Discussion Section（大幅加强）

```markdown
## Discussion

### Implications for Detection Tool Development

基于我们的发现，我们为检测工具开发者提出以下建议：

1. **增强语义理解能力**
   - ML工具应加入代码语义特征，而非仅依赖统计特征
   - 静态工具应加入数据流分析

2. **改进混淆检测**
   - 加入deobfuscation预处理步骤
   - 使用AST级别的模式匹配

3. **扩展动态分析时间**
   - 当前300s超时无法捕获延时执行攻击
   - 建议至少600s或基于行为的动态超时

4. **建立持续更新机制**
   - ML模型需要定期重训练
   - 规则库需要持续更新

### Implications for Security Practitioners

1. **工具选择指南**

| 场景 | 推荐工具 | 原因 |
|------|----------|------|
| CI/CD集成 | GuardDog | 快速、平衡、低FP |
| 安全审计 | Packj_static | 高召回、全面覆盖 |
| 关键系统 | GENIE + GuardDog | 极低FP |
| 研究分析 | Ensemble | 最高准确率 |

2. **部署策略建议**
   - 分层检测：快速筛选 + 深度分析
   - 定期评估工具在新样本上的表现
   - 建立误报反馈机制

3. **成本-效益分析**

| 工具 | 时间/包 | 准确率 | 推荐场景 |
|------|---------|--------|----------|
| GuardDog | 2.55s | 92.83% | 大规模扫描 |
| Packj_trace | 17.90s | 64.09% | 深度分析 |
| SocketAI | 146.34s | 72.92% | 特定场景 |

### Implications for npm Ecosystem

1. **平台级建议**
   - 限制preinstall script权限
   - 强制安全扫描
   - 建立maintainer信誉系统

2. **开发者教育**
   - 提高对supply chain attack的awareness
   - 推广lockfile使用
   - 定期审计依赖

### Future Research Directions

1. **语义感知检测**
   - 利用LLM理解代码意图
   - 结合程序分析和ML

2. **自适应检测系统**
   - 持续学习新攻击模式
   - 自动更新检测规则

3. **跨生态系统研究**
   - 将方法扩展到PyPI、Maven等
   - 跨生态系统威胁情报共享

4. **轻量级动态分析**
   - 减少动态分析开销
   - 符号执行结合

5. **可解释检测**
   - 提供检测结果解释
   - 辅助人工审核
```

---

## 5. 需要补充的实验

### 5.1 Ensemble Detection实验

```markdown
实验设计：
- 数据集：原有13,571 packages
- 划分：80% train, 20% test（用于确定最优组合）
- 评估：5-fold cross-validation

实验内容：
1. 所有2-tool组合的性能
2. 所有3-tool组合的性能
3. 最优组合的参数敏感性（voting threshold）
4. 不同时间段数据上的稳定性
```

### 5.2 Ablation Study

```markdown
实验设计：
- 从最优ensemble中逐个移除工具
- 测量性能下降

预期结果表格：
| 配置 | Accuracy | Delta |
|------|----------|-------|
| Full Ensemble | 95.XX% | - |
| - GuardDog | XX.XX% | -X.XX% |
| - SAP_XGB | XX.XX% | -X.XX% |
| - Packj | XX.XX% | -X.XX% |
```

### 5.3 Complementarity Analysis

```markdown
实验设计：
- 分析不同工具检测的package overlap
- 计算互补性指标

可视化：
- Venn diagram of detected packages
- Heatmap of pairwise complementarity
```

---

## 6. 方法论细节补充

### 6.1 人工标注流程

```markdown
需要补充的内容：
1. 两位标注者的背景和资质
2. 标注指南（labeling guidelines）
3. 标注流程图
4. 分歧解决机制
5. Cohen's Kappa计算细节
```

### 6.2 关键词提取方法

```markdown
需要补充的内容：
1. TF-IDF具体参数
2. 为什么选择3-5个关键词
3. 阈值设定依据
4. 关键词到类别的映射规则
```

### 6.3 LLM使用细节

```markdown
需要补充的内容：
1. 使用的模型版本
2. Prompt模板
3. Temperature等参数
4. 输出格式要求
5. 质量控制措施
```

---

## 7. 图表改进

### 7.1 需要重新设计的图表

| 图表 | 问题 | 改进方案 |
|------|------|----------|
| Figure 2 (行为分布) | 字体太小 | 使用PDF格式，增大字体 |
| Figure 3 (检测率热力图) | 难以阅读 | 重新配色，增加数值标注 |
| 所有图表 | 使用PNG格式 | 改用PDF/SVG矢量格式 |

### 7.2 需要新增的图表

1. **Taxonomy构建流程图**
2. **Dataset构建Pipeline图**
3. **Ensemble Framework架构图**
4. **工具互补性Venn图**
5. **Case Study代码示例图**

---

## 8. 时间规划

| 阶段 | 内容 | 时间 | 产出 |
|------|------|------|------|
| Week 1-2 | Ensemble实验设计与执行 | 需要跑新实验 | 实验数据 |
| Week 2-3 | Case Study选择与深入分析 | 需要人工分析 | 3-5个case study |
| Week 3-4 | Root Cause Analysis写作 | 加强现有RQ | 修改后的RQ sections |
| Week 4-5 | Taxonomy + Discussion写作 | 全新内容 | 新章节 |
| Week 5-6 | Ensemble Framework写作 | 结合实验结果 | 新章节 |
| Week 6-7 | 图表重新设计 | 使用专业工具 | 高质量图表 |
| Week 7-8 | 整体修改、内部review | 最终打磨 | 完整论文 |

---

## 9. 审稿人可能的新问题及预防

| 可能的问题 | 预防措施 |
|------------|----------|
| Ensemble方法太简单 | 强调contribution是systematic study，ensemble是insight validation |
| 为什么这些组合策略有效 | 用complementarity analysis详细解释 |
| Ensemble的实用性 | 提供具体deployment guideline和runtime分析 |
| 仍然缺乏novelty | 强调taxonomy + deep analysis + validated framework的组合贡献 |
| 数据集会过时 | 承诺持续维护，提供update机制 |

---

## 10. Checklist

### 10.1 内容Checklist

- [ ] Taxonomy作为独立Section，包含15个类别的详细定义
- [ ] 每个RQ都有root cause analysis
- [ ] 至少3个详细的case study
- [ ] Ensemble Framework设计与验证
- [ ] 完整的Discussion Section
- [ ] 方法论细节补充（标注流程、关键词提取、LLM使用）
- [ ] Threats to Validity

### 10.2 实验Checklist

- [ ] Ensemble组合实验
- [ ] Ablation study
- [ ] Complementarity analysis
- [ ] Cross-validation
- [ ] Runtime分析

### 10.3 呈现Checklist

- [ ] 所有图表使用PDF/SVG格式
- [ ] 字体大小统一且可读
- [ ] 新增pipeline/架构图
- [ ] 代码示例格式统一
- [ ] 论文后半部分写作质量提升

### 10.4 Artifact Checklist

- [ ] 代码整理到Zenodo
- [ ] 数据集整理到Zenodo
- [ ] README完善
- [ ] 复现指南
