"""
ui_components.py
Reusable UI widgets for CloudStore Command: Cyber Attack Simulation
Includes Threatening Ticking Clock, Health Gauge, Polling Bars, and Briefings.
"""

import streamlit as st
import time
from typing import Dict, Any, List, Optional
from game_data import load_markdown_content

def render_threatening_clock(remaining_secs: int, total_secs: int, phase_name: str, is_paused: bool = False):
    """
    Renders an ominous, high-stakes ticking countdown clock.
    Features red/amber warning colors, digital typography, and pulse animations.
    """
    mins = max(0, remaining_secs) // 60
    secs = max(0, remaining_secs) % 60
    time_str = f"{mins:02d}:{secs:02d}"

    # Determine alert state
    is_urgent = remaining_secs <= 60 and not is_paused
    is_expired = remaining_secs <= 0

    if is_expired:
        border_color = "#ef4444"
        glow_color = "rgba(239, 68, 68, 0.6)"
        clock_color = "#f87171"
        status_label = "🚨 CRITICAL TIMEOUT — DECISION IMMEDIATE REQUIRED"
        anim_css = "animation: pulse-urgent 1s infinite;"
    elif is_urgent:
        border_color = "#f59e0b"
        glow_color = "rgba(245, 158, 11, 0.6)"
        clock_color = "#fbbf24"
        status_label = "⚠️ THREAT WINDOW RAPIDLY CLOSING"
        anim_css = "animation: pulse-urgent 1.2s infinite;"
    elif is_paused:
        border_color = "#64748b"
        glow_color = "rgba(100, 116, 139, 0.3)"
        clock_color = "#94a3b8"
        status_label = "⏸️ SIMULATION PAUSED BY GAME MASTER"
        anim_css = ""
    else:
        border_color = "#dc2626"
        glow_color = "rgba(220, 38, 38, 0.3)"
        clock_color = "#fca5a5"
        status_label = f"⏳ ACTIVE THREAT WINDOW — {phase_name.upper()} PHASE"
        anim_css = ""

    pct = max(0.0, min(100.0, (remaining_secs / max(1, total_secs)) * 100.0))

    html = f"""
    <style>
    @keyframes pulse-urgent {{
        0% {{ box-shadow: 0 0 8px {glow_color}; }}
        50% {{ box-shadow: 0 0 24px {glow_color}; }}
        100% {{ box-shadow: 0 0 8px {glow_color}; }}
    }}
    .threat-clock-container {{
        background: linear-gradient(180deg, #090d16 0%, #030712 100%);
        border: 2px solid {border_color};
        border-radius: 14px;
        padding: 14px 20px;
        margin: 10px 0 20px 0;
        text-align: center;
        box-shadow: 0 4px 20px {glow_color};
        {anim_css}
    }}
    .clock-title {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
        font-size: 11px;
        font-weight: 800;
        color: {clock_color};
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 4px;
    }}
    .clock-digits {{
        font-family: "Courier New", Courier, monospace;
        font-size: 38px;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: 0.08em;
        text-shadow: 0 0 12px {glow_color};
        line-height: 1.1;
    }}
    .clock-bar-bg {{
        background-color: #1e293b;
        height: 6px;
        border-radius: 999px;
        overflow: hidden;
        margin-top: 8px;
    }}
    .clock-bar-fill {{
        background: linear-gradient(90deg, {border_color}, {clock_color});
        width: {pct}%;
        height: 100%;
        border-radius: 999px;
        transition: width 0.5s ease;
    }}
    </style>
    <div class="threat-clock-container">
        <div class="clock-title">{status_label}</div>
        <div class="clock-digits">{time_str}</div>
        <div class="clock-bar-bg">
            <div class="clock-bar-fill"></div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_health_gauge(health: float, bankrupt_cutoff: int, win_cutoff: int):
    """Renders the primary unified Company Health Score gauge with calibrated thresholds."""
    val = max(0.0, min(100.0, float(health)))
    
    if val >= win_cutoff:
        status_text = "WINNING TIER (RESILIENT)"
        bar_color = "#10b981"  # Emerald
        glow = "rgba(16, 185, 129, 0.4)"
    elif val >= bankrupt_cutoff:
        status_text = "SURVIVING TIER (DAMAGED)"
        bar_color = "#f59e0b"  # Amber
        glow = "rgba(245, 158, 11, 0.4)"
    else:
        status_text = "BANKRUPTCY IMMINENT"
        bar_color = "#ef4444"  # Red
        glow = "rgba(239, 68, 68, 0.6)"

    html = f"""
    <div style="background-color: #030712; padding: 18px; border-radius: 14px; border: 1px solid #1e293b; box-shadow: 0 4px 18px {glow}; margin-bottom: 15px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-size: 13px; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em;">🏢 Unified Enterprise Health</span>
            <span style="font-size: 12px; font-weight: 800; color: {bar_color}; letter-spacing: 0.05em;">{status_text}</span>
        </div>
        <div style="display: flex; align-items: baseline; gap: 8px;">
            <span style="font-size: 40px; font-weight: 900; color: #f8fafc; font-family: monospace;">{val:.1f}</span>
            <span style="font-size: 16px; color: #64748b;">/ 100.0 HP</span>
        </div>
        <div style="background-color: #1e293b; height: 12px; border-radius: 999px; overflow: hidden; margin-top: 10px; position: relative;">
            <div style="background-color: {bar_color}; width: {val}%; height: 100%; border-radius: 999px; transition: width 0.4s ease;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 11px; color: #64748b; margin-top: 6px;">
            <span>💥 Bankrupt (&lt; {bankrupt_cutoff})</span>
            <span>🛡️ Survive ({bankrupt_cutoff} - {win_cutoff - 1})</span>
            <span>🏆 Win (&ge; {win_cutoff})</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_briefing_card(role: str, filename: str, fallback_title: str, fallback_desc: str):
    """Renders markdown scenario briefing from content/ with clean formatting."""
    md_content = load_markdown_content(role, filename)
    with st.expander(f"📖 Intelligence Dossier: {fallback_title}", expanded=True):
        if md_content:
            st.markdown(md_content)
        else:
            st.info(fallback_desc)
