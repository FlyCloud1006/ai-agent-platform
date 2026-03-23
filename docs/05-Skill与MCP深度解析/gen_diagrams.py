#!/usr/bin/env python3
"""
生成 Skill 与 MCP 技术架构图
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(2, 2, figsize=(16, 14))
fig.suptitle('Skill & MCP Architecture Diagrams', fontsize=20, fontweight='bold', y=0.98)

# ========== 图1: Skill 核心组成 ==========
ax1 = axes[0, 0]
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.set_title('Skill Core Components', fontsize=14, fontweight='bold', pad=10)
ax1.axis('off')

# SKILL.md box
skill_box = FancyBboxPatch((0.5, 6.5), 4, 2.5, boxstyle="round,pad=0.1", 
                           facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=2)
ax1.add_patch(skill_box)
ax1.text(2.5, 7.75, 'SKILL.md', ha='center', va='center', fontsize=12, fontweight='bold')
ax1.text(2.5, 7.2, 'description\nmetadata\nexecution logic', ha='center', va='center', fontsize=9)

# scripts folder
scripts_box = FancyBboxPatch((5.5, 6.5), 4, 2.5, boxstyle="round,pad=0.1",
                              facecolor='#FFF3E0', edgecolor='#FF9800', linewidth=2)
ax1.add_patch(scripts_box)
ax1.text(7.5, 7.75, 'scripts/', ha='center', va='center', fontsize=12, fontweight='bold')
ax1.text(7.5, 7.2, 'helper scripts\nautomation', ha='center', va='center', fontsize=9)

# references folder
ref_box = FancyBboxPatch((0.5, 3.5), 4, 2.5, boxstyle="round,pad=0.1",
                          facecolor='#E8F5E9', edgecolor='#4CAF50', linewidth=2)
ax1.add_patch(ref_box)
ax1.text(2.5, 4.75, 'references/', ha='center', va='center', fontsize=12, fontweight='bold')
ax1.text(2.5, 4.2, 'documentation\ntemplates', ha='center', va='center', fontsize=9)

# metadata.json
meta_box = FancyBboxPatch((5.5, 3.5), 4, 2.5, boxstyle="round,pad=0.1",
                           facecolor='#FCE4EC', edgecolor='#E91E63', linewidth=2)
ax1.add_patch(meta_box)
ax1.text(7.5, 4.75, 'metadata.json', ha='center', va='center', fontsize=12, fontweight='bold')
ax1.text(7.5, 4.2, 'config\ndependencies\nversion', ha='center', va='center', fontsize=9)

# Skill directory label
ax1.text(5, 1.5, 'my-skill/', ha='center', va='center', fontsize=14, 
         fontweight='bold', style='italic', color='#666666')
ax1.text(5, 0.8, 'Skill Directory Structure', ha='center', va='center', fontsize=10, color='#888888')

# arrows
ax1.annotate('', xy=(2.5, 6.5), xytext=(2.5, 6), 
             arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
ax1.annotate('', xy=(7.5, 6.5), xytext=(7.5, 6),
             arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))

# ========== 图2: Skill 与 MCP 关系 ==========
ax2 = axes[0, 1]
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.set_title('Skill & MCP Relationship', fontsize=14, fontweight='bold', pad=10)
ax2.axis('off')

# AI Agent circle
agent_circle = Circle((5, 7.5), 1.5, facecolor='#673AB7', edgecolor='#4527A0', linewidth=3)
ax2.add_patch(agent_circle)
ax2.text(5, 7.5, 'AI Agent', ha='center', va='center', fontsize=11, fontweight='bold', color='white')

# Skill box
skill_box2 = FancyBboxPatch((0.3, 3.5), 4, 3, boxstyle="round,pad=0.1",
                              facecolor='#E1BEE7', edgecolor='#7B1FA2', linewidth=2)
ax2.add_patch(skill_box2)
ax2.text(2.3, 5.8, 'Skill', ha='center', va='center', fontsize=12, fontweight='bold')
ax2.text(2.3, 5.2, '• Task encapsulation', ha='left', va='center', fontsize=9)
ax2.text(2.3, 4.7, '• Decision logic', ha='left', va='center', fontsize=9)
ax2.text(2.3, 4.2, '• Flow control', ha='left', va='center', fontsize=9)
ax2.text(2.3, 3.7, '• Multi-step execution', ha='left', va='center', fontsize=9)

# MCP Server box
mcp_box = FancyBboxPatch((5.7, 3.5), 4, 3, boxstyle="round,pad=0.1",
                           facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=2)
ax2.add_patch(mcp_box)
ax2.text(7.7, 5.8, 'MCP Server', ha='center', va='center', fontsize=12, fontweight='bold')
ax2.text(7.7, 5.2, '• Tool exposure', ha='left', va='center', fontsize=9)
ax2.text(7.7, 4.7, '• Protocol handler', ha='left', va='center', fontsize=9)
ax2.text(7.7, 4.2, '• API integration', ha='left', va='center', fontsize=9)
ax2.text(7.7, 3.7, '• Standardized interface', ha='left', va='center', fontsize=9)

# Tool boxes inside MCP
tool1 = FancyBboxPatch((5.9, 2.8), 1.5, 0.6, boxstyle="round,pad=0.05",
                        facecolor='#90CAF9', edgecolor='#1976D2', linewidth=1)
ax2.add_patch(tool1)
ax2.text(6.65, 3.1, 'Tool A', ha='center', va='center', fontsize=8)

tool2 = FancyBboxPatch((7.7, 2.8), 1.5, 0.6, boxstyle="round,pad=0.05",
                        facecolor='#90CAF9', edgecolor='#1976D2', linewidth=1)
ax2.add_patch(tool2)
ax2.text(8.45, 3.1, 'Tool B', ha='center', va='center', fontsize=8)

tool3 = FancyBboxPatch((6.8, 1.8), 1.5, 0.6, boxstyle="round,pad=0.05",
                        facecolor='#90CAF9', edgecolor='#1976D2', linewidth=1)
ax2.add_patch(tool3)
ax2.text(7.55, 2.1, 'Tool C', ha='center', va='center', fontsize=8)

# arrows
ax2.annotate('', xy=(2.3, 6.5), xytext=(3.5, 7),
             arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=2))
ax2.annotate('', xy=(7.7, 6.5), xytext=(6.5, 7),
             arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))

ax2.text(5, 0.5, 'Skill contains decision logic & calls MCP tools', 
         ha='center', va='center', fontsize=10, style='italic', color='#666666')

# ========== 图3: MCP 协议流程 ==========
ax3 = axes[1, 0]
ax3.set_xlim(0, 10)
ax3.set_ylim(0, 10)
ax3.set_title('MCP Protocol Flow', fontsize=14, fontweight='bold', pad=10)
ax3.axis('off')

# Client box
client_box = FancyBboxPatch((0.5, 5), 3, 3, boxstyle="round,pad=0.1",
                             facecolor='#C8E6C9', edgecolor='#388E3C', linewidth=2)
ax3.add_patch(client_box)
ax3.text(2, 7.5, 'MCP Client', ha='center', va='center', fontsize=12, fontweight='bold')
ax3.text(2, 6.8, '(Agent)', ha='center', va='center', fontsize=9)

# Server box
server_box = FancyBboxPatch((6.5, 5), 3, 3, boxstyle="round,pad=0.1",
                             facecolor='#FFCCBC', edgecolor='#E64A19', linewidth=2)
ax3.add_patch(server_box)
ax3.text(8, 7.5, 'MCP Server', ha='center', va='center', fontsize=12, fontweight='bold')
ax3.text(8, 6.8, '(External API)', ha='center', va='center', fontsize=9)

# Protocol label
ax3.text(5, 8.5, 'MCP Protocol', ha='center', va='center', fontsize=14, 
         fontweight='bold', color='#E91E63')

# Step boxes
steps = [
    ('1. list_tools', 0.5, 4.2),
    ('2. tool_list', 6.5, 4.2),
    ('3. call_tool', 0.5, 1.5),
    ('4. result', 6.5, 1.5),
]

colors = ['#E8F5E9', '#BBDEFB', '#E8F5E9', '#BBDEFB']
for i, (text, x, y) in enumerate(steps):
    box = FancyBboxPatch((x, y), 3, 1, boxstyle="round,pad=0.05",
                          facecolor=colors[i], edgecolor='gray', linewidth=1)
    ax3.add_patch(box)
    ax3.text(x+1.5, y+0.5, text, ha='center', va='center', fontsize=9)

# arrows
ax3.annotate('', xy=(6.5, 4.7), xytext=(3.5, 4.7),
             arrowprops=dict(arrowstyle='->', color='#388E3C', lw=2))
ax3.annotate('', xy=(3.5, 4.7), xytext=(6.5, 4.7),
             arrowprops=dict(arrowstyle='->', color='#E64A19', lw=2))
ax3.annotate('', xy=(6.5, 2), xytext=(3.5, 2),
             arrowprops=dict(arrowstyle='->', color='#388E3C', lw=2))
ax3.annotate('', xy=(3.5, 2), xytext=(6.5, 2),
             arrowprops=dict(arrowstyle='->', color='#E64A19', lw=2))

# ========== 图4: Skill 触发流程 ==========
ax4 = axes[1, 1]
ax4.set_xlim(0, 10)
ax4.set_ylim(0, 10)
ax4.set_title('Skill Trigger & Execution Flow', fontsize=14, fontweight='bold', pad=10)
ax4.axis('off')

# Flow boxes
flow_items = [
    ('User Input', 4, 9, '#E3F2FD', '#1976D2'),
    ('Intent Recognition', 4, 7.5, '#E1BEE7', '#7B1FA2'),
    ('Skill Matching', 4, 6, '#FFF3E0', '#FF9800'),
    ('Pre-check', 4, 4.5, '#E8F5E9', '#4CAF50'),
    ('Tool Execution', 4, 3, '#BBDEFB', '#1565C0'),
    ('Result Formatting', 4, 1.5, '#FCE4EC', '#E91E63'),
]

for text, x, y, fc, ec in flow_items:
    box = FancyBboxPatch((x-1.5, y-0.5), 3, 1, boxstyle="round,pad=0.05",
                          facecolor=fc, edgecolor=ec, linewidth=2)
    ax4.add_patch(box)
    ax4.text(x, y, text, ha='center', va='center', fontsize=10, fontweight='bold')

# arrows
for i in range(len(flow_items)-1):
    ax4.annotate('', xy=(flow_items[i+1][1], flow_items[i+1][2]+0.5),
                 xytext=(flow_items[i][1], flow_items[i][2]-0.5),
                 arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))

# Condition branches
ax4.text(7.5, 6, 'Trigger Conditions:', ha='left', va='center', fontsize=9, fontweight='bold')
ax4.text(7.5, 5.3, '• description matching', ha='left', va='center', fontsize=8)
ax4.text(7.5, 4.8, '• keyword detection', ha='left', va='center', fontsize=8)
ax4.text(7.5, 4.3, '• context analysis', ha='left', va='center', fontsize=8)

ax4.text(7.5, 3, 'Tool Types:', ha='left', va='center', fontsize=9, fontweight='bold')
ax4.text(7.5, 2.3, '• read/write files', ha='left', va='center', fontsize=8)
ax4.text(7.5, 1.8, '• exec commands', ha='left', va='center', fontsize=8)
ax4.text(7.5, 1.3, '• API calls', ha='left', va='center', fontsize=8)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('/root/ai-agent-platform/docs/05-Skill与MCP深度解析/skill-mcp-architecture.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("Diagram saved: skill-mcp-architecture.png")
