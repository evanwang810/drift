#!/usr/bin/env python3
"""
Decision Matrix Calculator for Project Prioritization

This script helps calculate priority scores for projects using the decision framework
defined in docs/decision-framework.md.

Usage:
    python scripts/decision_matrix.py

The script will interactively prompt for project criteria and calculate scores.
"""

import sys
import json
from datetime import datetime


def get_user_input(prompt, min_val=1, max_val=10, default=None):
    """Get user input with validation."""
    while True:
        if default is not None:
            prompt_with_default = f"{prompt} (default {default}): "
        else:
            prompt_with_default = f"{prompt}: "

        user_input = input(prompt_with_default).strip()

        if not user_input and default is not None:
            return default

        try:
            value = int(user_input)
            if min_val <= value <= max_val:
                return value
            print(f"Please enter a value between {min_val} and {max_val}")
        except ValueError:
            print(f"Please enter a valid number between {min_val} and {max_val}")


def calculate_score(impact, urgency, dependencies, alignment, effort, technical_debt):
    """
    Calculate priority score using the decision framework formula.

    Score = (Impact × 3) + (Urgency × 2) + (Dependencies × 1.5) + (Alignment × 1) - (Effort × 0.5) + (Technical Debt × 0.8)
    """
    score = (impact * 3) + (urgency * 2) + (dependencies * 1.5) + (alignment * 1) - (effort * 0.5) + (technical_debt * 0.8)
    return round(score, 2)


def interpret_score(score):
    """Interpret the score into priority level."""
    if score > 20:
        return "High Priority"
    elif score >= 15:
        return "Medium Priority"
    else:
        return "Low Priority"


def calculate_project(project_name):
    """Calculate score for a specific project."""
    print(f"\n{'='*60}")
    print(f"Project: {project_name}")
    print('='*60)

    # Get user input for each criterion
    impact = get_user_input("Impact (1-10): ", 1, 10, 5)
    urgency = get_user_input("Urgency (1-10): ", 1, 10, 5)
    dependencies = get_user_input("Dependencies (1-10): ", 1, 10, 5)
    alignment = get_user_input("Alignment with Goals (1-10): ", 1, 10, 5)
    effort = get_user_input("Effort/Complexity (1-10, higher = more effort): ", 1, 10, 5)
    technical_debt = get_user_input("Technical Debt (1-10, higher = more reduction): ", 1, 10, 5)

    # Calculate score
    score = calculate_score(impact, urgency, dependencies, alignment, effort, technical_debt)
    priority = interpret_score(score)

    # Print results
    print(f"\n{'='*60}")
    print("Decision Matrix Results")
    print('='*60)
    print(f"Impact:           {impact:2d} × 3 = {impact * 3:5.1f}")
    print(f"Urgency:          {urgency:2d} × 2 = {urgency * 2:5.1f}")
    print(f"Dependencies:     {dependencies:2d} × 1.5 = {dependencies * 1.5:5.1f}")
    print(f"Alignment:        {alignment:2d} × 1 = {alignment * 1:5.1f}")
    print(f"Effort:          -{effort:2d} × 0.5 = -{effort * 0.5:5.1f}")
    print(f"Technical Debt:   {technical_debt:2d} × 0.8 = {technical_debt * 0.8:5.1f}")
    print('-' * 60)
    print(f"Total Score:      {score:.1f}")
    print(f"Priority Level:   {priority}")
    print('='*60)

    # Generate recommendation
    print(f"\nRecommendation:")
    if score > 20:
        print(f"  HIGH PRIORITY: Work on this project soon")
    elif score >= 15:
        print(f"  MEDIUM PRIORITY: Consider this project for the current work cycle")
    else:
        print(f"  LOW PRIORITY: Consider for later or defer if other work is available")

    print(f"\nReasoning:")
    if impact >= 8:
        print(f"  - High impact: This project delivers significant value")
    if urgency >= 8:
        print(f"  - High urgency: This should be addressed soon")
    if dependencies >= 8:
        print(f"  - Critical dependencies: This project blocks other work")
    if alignment >= 8:
        print(f"  - Strong alignment: This advances core goals")
    if effort >= 8:
        print(f"  - High effort: Be prepared for significant work")
    if technical_debt >= 8:
        print(f"  - Strong debt reduction: This fixes important technical debt")

    return {
        "project": project_name,
        "impact": impact,
        "urgency": urgency,
        "dependencies": dependencies,
        "alignment": alignment,
        "effort": effort,
        "technical_debt": technical_debt,
        "score": score,
        "priority": priority,
        "timestamp": datetime.now().isoformat()
    }


def compare_projects(project1, project2):
    """Compare two projects and determine which should be prioritized."""
    print(f"\n{'='*60}")
    print(f"Comparison: {project1['project']} vs {project2['project']}")
    print('='*60)

    # Calculate scores
    score1 = calculate_project(project1['project'])
    score2 = calculate_project(project2['project'])

    # Reset input prompts
    print("\n" + "="*60)
    print("Comparison Results")
    print('='*60)
    print(f"{project1['project']}:")
    print(f"  Score: {project1['score']:.1f} ({project1['priority']})")
    print(f"{project2['project']}:")
    print(f"  Score: {project2['score']:.1f} ({project2['priority']})")
    print('='*60)

    # Determine winner
    if project1['score'] > project2['score']:
        print(f"\nWinner: {project1['project']}")
        print(f"Reason: Higher score ({project1['score']:.1f} vs {project2['score']:.1f})")
    elif project2['score'] > project1['score']:
        print(f"\nWinner: {project2['project']}")
        print(f"Reason: Higher score ({project2['score']:.1f} vs {project1['score']:.1f})")
    else:
        print(f"\nTie: Both projects have the same score")
        print("   Consider other factors like risk, resources, or timeline")

    # Save to JSON
    output = {
        "comparison": {
            "project1": project1,
            "project2": project2,
            "winner": project1['project'] if project1['score'] > project2['score'] else
                     (project2['project'] if project2['score'] > project1['score'] else "Tie")
        }
    }

    # Save to JSON file
    with open("scripts/decision_matrix_output.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: scripts/decision_matrix_output.json")

    return project1['score'] > project2['score']


def main():
    """Main function."""
    print("Decision Matrix Calculator")
    print("Calculate priority scores for projects using the decision framework")
    print("="*60)

    # Main menu
    while True:
        print("\nMain Menu:")
        print("1. Calculate score for a single project")
        print("2. Compare two projects")
        print("3. Exit")

        choice = input("\nSelect an option (1-3): ").strip()

        if choice == "1":
            project_name = input("Enter project name: ").strip()
            if project_name:
                calculate_project(project_name)
        elif choice == "2":
            print("\nProject 1:")
            project1_name = input("Enter project name: ").strip()
            if project1_name:
                project1_data = calculate_project(project1_name)
                print("\n" * 2)  # Double newline
                project2_name = input("Enter second project name: ").strip()
                if project2_name:
                    project2_data = calculate_project(project2_name)
                    compare_projects(project1_data, project2_data)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
