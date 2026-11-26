# Decision Framework for Project Prioritization

## Core Principles

1. **Evidence-Based Decisions**: Every decision must be based on verifiable data, not assumptions
2. **Systematic Evaluation**: Use structured criteria to evaluate all options before choosing
3. **Transparency**: Document the reasoning behind every decision
4. **Iterative Improvement**: Review and refine the framework based on outcomes

## Prioritization Criteria

### 1. Impact (High Priority)
- **Definition**: How much value does this project deliver?
- **Factors**:
  - User-facing improvements (immediate user value)
  - System-wide benefits (affects multiple components)
  - Strategic alignment (advances long-term goals)
  - Revenue/cost implications (if applicable)

**Scoring**: 1-10 scale
- 10: Transformative, system-wide benefit
- 7-9: Significant improvement
- 4-6: Moderate benefit
- 1-3: Minimal impact

### 2. Urgency (High Priority)
- **Definition**: How soon does this need to be addressed?
- **Factors**:
  - Blocking issues (prevents other work)
  - Time-sensitive opportunities
  - Dependencies (waiting on this blocks others)
  - Risk accumulation (delay increases risk)

**Scoring**: 1-10 scale
- 10: Blocking, immediate action required
- 7-9: High urgency
- 4-6: Medium urgency
- 1-3: Low urgency

### 3. Dependencies (Medium Priority)
- **Definition**: What other work depends on this project?
- **Factors**:
  - Pre-requisites (must complete before other work)
  - Dependencies (other projects depend on this)
  - Bottlenecks (this project is a choke point)
  - External dependencies (waiting on third-party work)

**Scoring**: 1-10 scale
- 10: Critical dependency, blocks multiple projects
- 7-9: Significant dependency
- 4-6: Moderate dependency
- 1-3: Minor dependency

### 4. Alignment with Goals (Medium Priority)
- **Definition**: Does this project advance stated goals?
- **Factors**:
  - Directly addresses project goals
  - Supports broader objectives
  - Aligns with long-term vision
  - No conflict with strategic priorities

**Scoring**: 1-10 scale
- 10: Directly advances core goals
- 7-9: Strong alignment
- 4-6: Moderate alignment
- 1-3: Misaligned or neutral

### 5. Effort/Complexity (Low Priority but Important)
- **Definition**: How much work is required to complete?
- **Factors**:
  - Lines of code / complexity
  - Testing requirements
  - Documentation needs
  - Risk of failure

**Scoring**: 1-10 scale (higher = more effort)
- 10: Very complex, high risk
- 7-9: Complex
- 4-6: Moderate effort
- 1-3: Simple

### 6. Technical Debt (Anti-Priority)
- **Definition**: Does this project reduce technical debt?
- **Factors**:
  - Fixes known bugs
  - Refactors complex code
  - Improves maintainability
  - Reduces technical debt

**Scoring**: 1-10 scale (higher = more debt reduction)
- 10: Eliminates significant technical debt
- 7-9: Reduces debt meaningfully
- 4-6: Minor debt reduction
- 1-3: No impact on debt

## Decision Matrix

### Scoring Formula

```
Priority Score = (Impact × 3) + (Urgency × 2) + (Dependencies × 1.5) + (Alignment × 1) - (Effort × 0.5) + (Technical Debt × 0.8)
```

**Interpretation**:
- Score > 20: High priority
- Score 15-20: Medium priority
- Score < 15: Low priority

### Example Calculation

**Project A**: New feature request
- Impact: 8
- Urgency: 4
- Dependencies: 3
- Alignment: 9
- Effort: 7
- Technical Debt: 2

```
Score = (8 × 3) + (4 × 2) + (3 × 1.5) + (9 × 1) - (7 × 0.5) + (2 × 0.8)
      = 24 + 8 + 4.5 + 9 - 3.5 + 1.6
      = 43.6
```

**Project B**: Bug fix
- Impact: 5
- Urgency: 9
- Dependencies: 7
- Alignment: 6
- Effort: 3
- Technical Debt: 8

```
Score = (5 × 3) + (9 × 2) + (7 × 1.5) + (6 × 1) - (3 × 0.5) + (8 × 0.8)
      = 15 + 18 + 10.5 + 6 - 1.5 + 6.4
      = 54.4
```

Project B gets higher priority because it's urgent and addresses technical debt.

## Example Decisions

### Example 1: Choosing Between Two Projects

**Scenario**: Two projects competing for limited time

**Project X**:
- Impact: 8, Urgency: 7, Dependencies: 4, Alignment: 9, Effort: 6, Technical Debt: 3
- Score: (8×3) + (7×2) + (4×1.5) + (9×1) - (6×0.5) + (3×0.8) = 24 + 14 + 6 + 9 - 3 + 2.4 = 52.4

**Project Y**:
- Impact: 6, Urgency: 9, Dependencies: 2, Alignment: 7, Effort: 4, Technical Debt: 6
- Score: (6×3) + (9×2) + (2×1.5) + (7×1) - (4×0.5) + (6×0.8) = 18 + 18 + 3 + 7 - 2 + 4.8 = 48.8

**Decision**: Project X has higher score (52.4 vs 48.8), so work on X first.
**Reasoning**: Higher impact and alignment outweigh slightly lower urgency, despite Y being more urgent.

### Example 2: Blocking Issue

**Scenario**: Critical bug preventing other work

**Bug Fix**:
- Impact: 5, Urgency: 10, Dependencies: 10, Alignment: 6, Effort: 4, Technical Debt: 7
- Score: (5×3) + (10×2) + (10×1.5) + (6×1) - (4×0.5) + (7×0.8) = 15 + 20 + 15 + 6 - 2 + 5.6 = 59.6

**Feature Implementation**:
- Impact: 8, Urgency: 4, Dependencies: 3, Alignment: 9, Effort: 7, Technical Debt: 2
- Score: (8×3) + (4×2) + (3×1.5) + (9×1) - (7×0.5) + (2×0.8) = 24 + 8 + 4.5 + 9 - 3.5 + 1.6 = 43.6

**Decision**: Bug fix first (Score 59.6 vs 43.6)
**Reasoning**: High urgency (10) and critical dependency (10) make it a blocker, despite lower alignment with long-term goals.

### Example 3: Technical Debt vs New Features

**Scenario**: Balance between fixing technical debt and adding features

**Refactoring**:
- Impact: 4, Urgency: 5, Dependencies: 6, Alignment: 7, Effort: 9, Technical Debt: 10
- Score: (4×3) + (5×2) + (6×1.5) + (7×1) - (9×0.5) + (10×0.8) = 12 + 10 + 9 + 7 - 4.5 + 8 = 41.5

**New Feature**:
- Impact: 9, Urgency: 6, Dependencies: 4, Alignment: 8, Effort: 5, Technical Debt: 2
- Score: (9×3) + (6×2) + (4×1.5) + (8×1) - (5×0.5) + (2×0.8) = 27 + 12 + 6 + 8 - 2.5 + 1.6 = 52.1

**Decision**: New feature first (Score 52.1 vs 41.5)
**Reasoning**: Higher impact and alignment with goals outweigh the debt reduction benefit, despite higher effort.

## Integration into Project Completion

When completing a project in PROJECT.md:

1. **Calculate the score** using the decision matrix
2. **Document the score** in the project completion section
3. **Include the reasoning** for the score
4. **Track the decision** in the run log
5. **Review and adjust** if circumstances change

### Template for Project Completion

```markdown
### Project Name ✅

**Objective:** [Project objective]

**Decision Framework Score:** [Score calculation details]
- Impact: [score] - [reasoning]
- Urgency: [score] - [reasoning]
- Dependencies: [score] - [reasoning]
- Alignment: [score] - [reasoning]
- Effort: [score] - [reasoning]
- Technical Debt: [score] - [reasoning]
- **Total Score:** [score]

**Decision:** [Why this project was prioritized]

**Done when:**
[Criteria listed in PROJECT.md]

**Completed:**
[Completed items with verification]
```

## Review and Refinement

This framework should be reviewed and refined periodically:

1. **Weekly**: Check if scoring decisions match outcomes
2. **Monthly**: Adjust weights based on what actually happened
3. **Quarterly**: Major review of the entire framework

**Refinement Principles**:
- Only change weights when data shows a pattern
- Document any changes to the framework
- Update examples if scoring decisions change
- Keep the framework simple and actionable
