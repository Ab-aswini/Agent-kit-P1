#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/UX Pro Max Core - BM25 search engine for UI/UX style guides
"""

import re
from pathlib import Path

# ============ CONFIGURATION ============
DATA_DIR = Path(__file__).parent.parent / "data"
MAX_RESULTS = 3

CSV_CONFIG = {
    "style": {
        "file": "styles.csv",
        "search_cols": ["Style Category", "Keywords", "Best For", "Type"],
        "output_cols": ["Style Category", "Type", "Keywords", "Primary Colors", "Effects & Animation", "Best For", "Performance", "Accessibility", "Framework Compatibility", "Complexity"]
    },
    "prompt": {
        "file": "prompts.csv",
        "search_cols": ["Style Category", "AI Prompt Keywords (Copy-Paste Ready)", "CSS/Technical Keywords"],
        "output_cols": ["Style Category", "AI Prompt Keywords (Copy-Paste Ready)", "CSS/Technical Keywords", "Implementation Checklist"]
    },
    "color": {
        "file": "colors.csv",
        "search_cols": ["Product Type", "Keywords", "Notes"],
        "output_cols": ["Product Type", "Keywords", "Primary (Hex)", "Secondary (Hex)", "CTA (Hex)", "Background (Hex)", "Text (Hex)", "Border (Hex)", "Notes"]
    },
    "chart": {
        "file": "charts.csv",
        "search_cols": ["Data Type", "Keywords", "Best Chart Type", "Accessibility Notes"],
        "output_cols": ["Data Type", "Keywords", "Best Chart Type", "Secondary Options", "Color Guidance", "Accessibility Notes", "Library Recommendation", "Interactive Level"]
    },
    "landing": {
        "file": "landing.csv",
        "search_cols": ["Pattern Name", "Keywords", "Conversion Optimization", "Section Order"],
        "output_cols": ["Pattern Name", "Keywords", "Section Order", "Primary CTA Placement", "Color Strategy", "Conversion Optimization"]
    },
    "product": {
        "file": "products.csv",
        "search_cols": ["Product Type", "Keywords", "Primary Style Recommendation", "Key Considerations"],
        "output_cols": ["Product Type", "Keywords", "Primary Style Recommendation", "Secondary Styles", "Landing Page Pattern", "Dashboard Style (if applicable)", "Color Palette Focus"]
    },
    "ux": {
        "file": "ux-guidelines.csv",
        "search_cols": ["Category", "Issue", "Description", "Platform"],
        "output_cols": ["Category", "Issue", "Platform", "Description", "Do", "Don't", "Code Example Good", "Code Example Bad", "Severity"]
    },
    "typography": {
        "file": "typography.csv",
        "search_cols": ["Font Pairing Name", "Category", "Mood/Style Keywords", "Best For", "Heading Font", "Body Font"],
        "output_cols": ["Font Pairing Name", "Category", "Heading Font", "Body Font", "Mood/Style Keywords", "Best For", "Google Fonts URL", "CSS Import", "Tailwind Config", "Notes"]
    },
    "icons": {
        "file": "icons.csv",
        "search_cols": ["Category", "Icon Name", "Keywords", "Best For"],
        "output_cols": ["Category", "Icon Name", "Keywords", "Library", "Import Code", "Usage", "Best For", "Style"]
    },
    "react": {
        "file": "react-performance.csv",
        "search_cols": ["Category", "Issue", "Keywords", "Description"],
        "output_cols": ["Category", "Issue", "Platform", "Description", "Do", "Don't", "Code Example Good", "Code Example Bad", "Severity"]
    },
    "web": {
        "file": "web-interface.csv",
        "search_cols": ["Category", "Issue", "Keywords", "Description"],
        "output_cols": ["Category", "Issue", "Platform", "Description", "Do", "Don't", "Code Example Good", "Code Example Bad", "Severity"]
    },
    "reasoning": {
        "file": "ui-reasoning.csv",
        "search_cols": ["UI_Category", "Style_Priority", "Color_Mood", "Key_Effects", "Dark_Mode_Strategy", "AI_Integration_Level"],
        "output_cols": ["UI_Category", "Recommended_Pattern", "Style_Priority", "Color_Mood", "Typography_Mood", "Key_Effects", "Decision_Rules", "Anti_Patterns", "Severity", "Dark_Mode_Strategy", "AI_Integration_Level", "Privacy_Tier", "Agent_Readiness", "Performance_Budget"]
    },
    "animations": {
        "file": "animations.csv",
        "search_cols": ["Category", "Pattern_Name", "Description", "Trigger", "Accessibility_Note"],
        "output_cols": ["Category", "Pattern_Name", "Description", "Duration", "Easing", "CSS_Code", "JS_Code", "Trigger", "Do", "Don't", "Severity", "Performance_Impact", "Accessibility_Note"]
    },
    "accessibility": {
        "file": "accessibility.csv",
        "search_cols": ["Category", "Pattern_Name", "Description", "WCAG_Level", "ARIA_Role", "Screen_Reader_Note"],
        "output_cols": ["Category", "Pattern_Name", "Description", "WCAG_Level", "Platform", "Do", "Don't", "Code_Good", "Code_Bad", "Severity", "ARIA_Role", "Screen_Reader_Note"]
    },
    "dark-mode": {
        "file": "dark-mode.csv",
        "search_cols": ["Category", "Pattern_Name", "Description", "CSS_Variable", "Token_Type"],
        "output_cols": ["Category", "Pattern_Name", "Description", "Light_Value", "Dark_Value", "CSS_Variable", "Do", "Don't", "Code_Good", "Code_Bad", "Severity", "Token_Type"]
    },
    "ai-patterns": {
        "file": "ai-patterns.csv",
        "search_cols": ["Category", "Pattern_Name", "Description", "AI_Model_Type", "User_Trust_Level"],
        "output_cols": ["Category", "Pattern_Name", "Description", "AI_Model_Type", "Do", "Don't", "Code_Good", "Code_Bad", "Severity", "User_Trust_Level", "Latency_Budget"]
    },
    "forms": {
        "file": "forms.csv",
        "search_cols": ["Category", "Pattern_Name", "Description", "Input_Type", "Validation_Strategy"],
        "output_cols": ["Category", "Pattern_Name", "Description", "Input_Type", "Do", "Don't", "Code_Good", "Code_Bad", "Severity", "Validation_Strategy", "A11y_Note"]
    },
    "error-states": {
        "file": "error-states.csv",
        "search_cols": ["Category", "Pattern_Name", "Description", "Error_Type", "Recovery_Action", "User_Emotion"],
        "output_cols": ["Category", "Pattern_Name", "Description", "Error_Type", "Do", "Don't", "Code_Good", "Code_Bad", "Severity", "Recovery_Action", "User_Emotion"]
    }
}

STACK_CONFIG = {
    "html-tailwind": {"file": "stacks/html-tailwind.csv"},
    "react": {"file": "stacks/react.csv"},
    "nextjs": {"file": "stacks/nextjs.csv"},
    "vue": {"file": "stacks/vue.csv"},
    "nuxtjs": {"file": "stacks/nuxtjs.csv"},
    "nuxt-ui": {"file": "stacks/nuxt-ui.csv"},
    "svelte": {"file": "stacks/svelte.csv"},
    "swiftui": {"file": "stacks/swiftui.csv"},
    "react-native": {"file": "stacks/react-native.csv"},
    "flutter": {"file": "stacks/flutter.csv"},
    "shadcn": {"file": "stacks/shadcn.csv"},
    "jetpack-compose": {"file": "stacks/jetpack-compose.csv"},
    "angular": {"file": "stacks/angular.csv"},
    "astro": {"file": "stacks/astro.csv"},
    "remix": {"file": "stacks/remix.csv"},
    "tauri": {"file": "stacks/tauri.csv"}
}

# Common columns for all stacks
_STACK_COLS = {
    "search_cols": ["Category", "Guideline", "Description", "Do", "Don't", "Dark_Mode_Strategy", "AI_Integration_Level", "Privacy_Tier", "Agent_Readiness"],
    "output_cols": ["Category", "Guideline", "Description", "Do", "Don't", "Code Good", "Code Bad", "Severity", "Docs URL", "Dark_Mode_Strategy", "AI_Integration_Level", "Privacy_Tier", "Agent_Readiness", "Performance_Budget"]
}

AVAILABLE_STACKS = list(STACK_CONFIG.keys())


DB_PATH = DATA_DIR / "ui_ux_knowledge.db"

def _sanitize_col_name(col):
    return col.replace(" ", "_").replace("/", "_").replace("&", "and").replace("(", "").replace(")", "").replace("-", "_").replace("'", "").lower()

def _search_db(domain, query, output_cols, max_results):
    """Core search function using SQLite FTS5"""
    if not DB_PATH.exists():
        return []

    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Sanitize query for FTS5 (basic fallback)
    # FTS5 matches tokens. If query has special chars, it might error. Keep it simple.
    clean_query = re.sub(r'[^\w\s]', ' ', query).strip()
    if not clean_query:
        return []
    
    # Optional OR queries across space-separated tokens
    tokens = clean_query.split()
    query_match = " OR ".join([f'"{t}"' for t in tokens])
    
    # FTS5 syntax: domain AND (word1 OR word2)
    fts_query = f'"{domain}" AND ({query_match})'

    try:
        cursor.execute('''
            SELECT table_name, record_id
            FROM search_index 
            WHERE search_index MATCH ?
            ORDER BY rank
            LIMIT ?
        ''', (fts_query, max_results))
        matches = cursor.fetchall()
    except sqlite3.OperationalError as e:
        # Fallback if FTS5 syntax fails
        print(f"FTS5 Error: {e}")
        try:
            cursor.execute('''
                SELECT table_name, record_id
                FROM search_index 
                WHERE content LIKE ? AND domain = ?
                LIMIT ?
            ''', (f"%{clean_query}%", domain, max_results))
            matches = cursor.fetchall()
        except Exception:
            matches = []

    results = []
    for table_name, record_id in matches:
        db_cols = [f'"{_sanitize_col_name(c)}"' for c in output_cols]
        query_sql = f"SELECT {', '.join(db_cols)} FROM {table_name} WHERE id = ?"
        
        try:
            cursor.execute(query_sql, (record_id,))
            row = cursor.fetchone()
            if row:
                res_dict = {output_cols[i]: row[i] or "" for i in range(len(output_cols))}
                results.append(res_dict)
        except sqlite3.Error:
            pass
            
    conn.close()
    return results


def detect_domain(query):
    """Auto-detect the most relevant domain from query"""
    query_lower = query.lower()

    domain_keywords = {
        "color": ["color", "palette", "hex", "#", "rgb"],
        "chart": ["chart", "graph", "visualization", "trend", "bar", "pie", "scatter", "heatmap", "funnel"],
        "landing": ["landing", "page", "cta", "conversion", "hero", "testimonial", "pricing", "section"],
        "product": ["saas", "ecommerce", "e-commerce", "fintech", "healthcare", "gaming", "portfolio", "crypto", "dashboard"],
        "prompt": ["prompt", "css", "implementation", "variable", "checklist", "tailwind"],
        "style": ["style", "design", "ui", "minimalism", "glassmorphism", "neumorphism", "brutalism", "flat", "aurora"],
        "ux": ["ux", "usability", "touch", "scroll", "navigation", "mobile", "cookie consent", "paywall", "skeleton", "optimistic", "a/b test"],
        "typography": ["font", "typography", "heading", "serif", "sans"],
        "icons": ["icon", "icons", "lucide", "heroicons", "symbol", "glyph", "pictogram", "svg icon"],
        "react": ["react", "next.js", "nextjs", "suspense", "memo", "usecallback", "useeffect", "rerender", "bundle", "waterfall", "barrel", "dynamic import", "rsc", "server component"],
        "web": ["aria", "focus", "outline", "semantic", "virtualize", "preconnect"],
        "reasoning": ["reasoning", "dark mode strategy", "ai integration", "privacy tier", "agent readiness", "performance budget", "decision rules", "anti-pattern", "ui category", "agent platform", "voice-first", "digital twin", "climate tech", "telemedicine", "compliance", "regulatory"],
        "animations": ["animation", "motion", "easing", "micro-interaction", "transition", "parallax", "stagger", "fade", "slide", "bounce", "spring", "gesture", "swipe", "drag"],
        "accessibility": ["accessibility", "a11y", "wcag", "screen reader", "keyboard", "focus", "aria", "alt text", "contrast", "caption", "reduced motion", "assistive"],
        "dark-mode": ["dark mode", "dark theme", "light mode", "theme toggle", "prefers-color-scheme", "color-scheme", "theme switch"],
        "ai-patterns": ["ai chat", "chatbot", "streaming", "llm", "prompt", "ai response", "hallucination", "confidence", "token", "human-in-loop", "ai safety"],
        "forms": ["form", "input", "validation", "text field", "select", "checkbox", "radio", "multi-step", "file upload", "autofill", "autocomplete", "submit"],
        "error-states": ["error", "404", "500", "empty state", "offline", "loading", "skeleton", "retry", "toast", "notification", "permission", "timeout"]
    }

    scores = {domain: sum(1 for kw in keywords if kw in query_lower) for domain, keywords in domain_keywords.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "style"


def search(query, domain=None, max_results=MAX_RESULTS):
    """Main search function with auto-domain detection"""
    if domain is None:
        domain = detect_domain(query)

    config = CSV_CONFIG.get(domain, CSV_CONFIG["style"])

    results = _search_db(domain, query, config["output_cols"], max_results)

    return {
        "domain": domain,
        "query": query,
        "file": config["file"],
        "count": len(results),
        "results": results
    }


def search_stack(query, stack, max_results=MAX_RESULTS):
    """Search stack-specific guidelines"""
    if stack not in STACK_CONFIG:
        return {"error": f"Unknown stack: {stack}. Available: {', '.join(AVAILABLE_STACKS)}"}

    results = _search_db(f"stack_{stack}", query, _STACK_COLS["output_cols"], max_results)

    return {
        "domain": "stack",
        "stack": stack,
        "query": query,
        "file": STACK_CONFIG[stack]["file"],
        "count": len(results),
        "results": results
    }
