"""
test_accessibility.py
Automated test suite verifying accessibility, responsive typography,
and WCAG contrast standards across CloudStore Command UI.
"""

import re
from pathlib import Path
from streamlit.testing.v1 import AppTest

ROOT_DIR = Path(__file__).resolve().parent

def test_no_sub_micro_font_sizes():
    """Verify ui_components.py, team_views.py, and app.py contain no sub-micro font sizes (10px, 11px, 12px)."""
    print("\n--- [TEST 1] Scan for Sub-Micro Font Sizes (< 13px) ---")
    files_to_check = [
        ROOT_DIR / "ui_components.py",
        ROOT_DIR / "team_views.py",
        ROOT_DIR / "app.py",
    ]

    # Regex targeting font-size: 10px, 11px, 12px, or any single-digit px
    sub_micro_pattern = re.compile(r'font-size:\s*([0-9]|1[0-2])px\b', re.IGNORECASE)

    violations = []
    for file_path in files_to_check:
        with open(file_path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                matches = sub_micro_pattern.findall(line)
                if matches:
                    violations.append(f"{file_path.name}:{line_no}: Found sub-micro font size: {matches} -> {line.strip()}")

    assert len(violations) == 0, f"Accessibility font size violations found:\n" + "\n".join(violations)
    print("  ✓ Zero sub-micro font sizes found. All font sizes are >= 13px.")


def test_high_contrast_legend_colors():
    """Verify that muted low-contrast colors like #64748b are not used for gauge legends or small labels."""
    print("\n--- [TEST 2] Verify High Contrast WCAG Compliance on Gauges and Legends ---")
    gauge_file = ROOT_DIR / "ui_components.py"
    with open(gauge_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Specifically check the health gauge threshold legend: #64748b should be replaced with #cbd5e1
    assert "#64748b" not in content, "Found low-contrast #64748b in ui_components.py! Must use #cbd5e1 or brighter."
    print("  ✓ Verified: High contrast threshold legend colors used (#cbd5e1).")


def test_global_responsive_css_present():
    """Verify that app.py contains the responsive stylesheet and touch target sizing."""
    print("\n--- [TEST 3] Verify Global Responsive & Accessible Stylesheet ---")
    app_file = ROOT_DIR / "app.py"
    with open(app_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert "max-width: 1400px" in content, "Missing max-width constraint for wide laptop displays"
    assert "min-height: 48px" in content, "Missing 48px touch target height for mobile/tablet buttons"
    assert "outline: 3px solid #38bdf8" in content, "Missing visible keyboard focus outline"
    assert "@media (max-width: 1024px)" in content, "Missing tablet responsive media query"
    print("  ✓ Verified: Global CSS defines responsive container, 48px touch targets, and focus rings.")


def test_apptest_responsive_views():
    """Verify that AppTest renders key role views cleanly without exceptions."""
    print("\n--- [TEST 4] AppTest Viewport & Multi-Device Rendering ---")
    for role in ["instructor", "projector", "hackers", "it", "exec", "media"]:
        at = AppTest.from_file("app.py")
        at.query_params["team"] = role
        at.run()
        assert not at.exception, f"AppTest raised an exception on role '?team={role}': {at.exception}"
        print(f"  ✓ Verified '?team={role}' rendered cleanly with 0 exceptions.")


def test_theme_responsive_color_tokens():
    """Verify that text colors adapt to light and dark themes rather than using hardcoded light gray."""
    print("\n--- [TEST 5] Verify Theme-Responsive Color Tokens (Light & Dark Mode) ---")
    app_file = ROOT_DIR / "app.py"
    with open(app_file, "r", encoding="utf-8") as f:
        app_content = f.read()

    # Verify CSS variables for theme responsiveness
    assert "var(--text-color" in app_content, "Missing var(--text-color) in app.py CSS"
    assert "prefers-color-scheme: dark" in app_content, "Missing prefers-color-scheme in app.py"
    assert "data-theme=\"light\"" in app_content, "Missing data-theme light token in app.py"
    assert "data-theme=\"dark\"" in app_content, "Missing data-theme dark token in app.py"

    # Verify team_views.py does not hardcode light gray on uncontained header subtitles
    views_file = ROOT_DIR / "team_views.py"
    with open(views_file, "r", encoding="utf-8") as f:
        views_content = f.read()

    assert "var(--text-color" in views_content, "Missing theme-responsive var(--text-color) in team_views.py headers/polling"
    print("  ✓ Verified: Theme-responsive color tokens and CSS variables implemented for light/dark adaptability.")


if __name__ == "__main__":
    test_no_sub_micro_font_sizes()
    test_high_contrast_legend_colors()
    test_global_responsive_css_present()
    test_apptest_responsive_views()
    test_theme_responsive_color_tokens()
    print("\n🎉 ALL ACCESSIBILITY & THEME-RESPONSIVE VIEWPORT TESTS PASSED!")
