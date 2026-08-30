import os
import re
from collections import defaultdict, Counter

# ============================================================
# CHECK DESIGN SYSTEM
# ============================================================
# CHECK ONLY
#
# This script DOES NOT modify any files.
#
# It scans HTML files and reports visual/design differences
# across Vocabulary Games and Lessons/Sentences.
# ============================================================


# ------------------------------------------------------------
# SETTINGS
# ------------------------------------------------------------

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

HTML_EXTENSIONS = {".html", ".htm"}

# Folders / files to ignore
IGNORE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__"
}


# ------------------------------------------------------------
# DESIGN PROPERTIES TO CHECK
# ------------------------------------------------------------

CSS_PROPERTIES = [
    "font-family",
    "font-size",
    "font-weight",
    "line-height",
    "letter-spacing",

    "color",
    "background",
    "background-color",

    "border",
    "border-width",
    "border-style",
    "border-color",
    "border-radius",

    "box-shadow",

    "padding",
    "padding-top",
    "padding-right",
    "padding-bottom",
    "padding-left",

    "margin",
    "margin-top",
    "margin-right",
    "margin-bottom",
    "margin-left",

    "gap",
    "row-gap",
    "column-gap",

    "width",
    "max-width",
    "min-width",

    "height",
    "min-height",
    "max-height",

    "text-align",

    "display",
    "align-items",
    "justify-content",

    "cursor",

    "transition"
]


# ------------------------------------------------------------
# IMPORTANT SELECTORS
# ------------------------------------------------------------

IMPORTANT_SELECTORS = [
    "body",
    "header",
    "main",
    "footer",

    ".container",
    ".page",
    ".wrapper",
    ".content",

    ".header",
    ".page-header",
    ".section-header",
    ".section-title",
    ".section-title-wrap",

    ".game",
    ".game-container",
    ".game-card",

    ".question",
    ".question-card",
    ".question-text",

    ".answers",
    ".answer",
    ".answer-button",
    ".option",
    ".option-button",

    ".btn",
    ".button",
    "button",

    ".next",
    ".next-btn",

    ".back",
    ".back-btn",

    ".progress",
    ".progress-bar",
    ".score",

    ".card",

    ".lesson",
    ".lesson-container",
    ".lesson-card",

    ".pattern",
    ".pattern-box",

    ".example",
    ".examples",

    ".practice",
    ".practice-box",

    ".vocab",
    ".vocabulary",

    ".footer"
]


# ------------------------------------------------------------
# FILE CATEGORY
# ------------------------------------------------------------

def classify_file(filepath):

    relative = os.path.relpath(filepath, PROJECT_ROOT)

    normalized = relative.replace("\\", "/").lower()

    # Vocabulary games
    if "/vocabulary/" in f"/{normalized}/":
        if re.search(r"game\d+\.html$", normalized):
            return "VOCABULARY GAME"

    # Lessons / Sentences
    if (
        "/sentences/" in f"/{normalized}/"
        or "/lessons/" in f"/{normalized}/"
        or "lesson" in normalized
    ):
        return "LESSON"

    # Phrases / sentences page
    if "phrases-and-sentences.html" in normalized:
        return "LESSON"

    return None


# ------------------------------------------------------------
# EXTRACT CSS BLOCKS
# ------------------------------------------------------------

def extract_css(content):

    css_blocks = []

    # <style>...</style>
    style_pattern = re.compile(
        r"<style\b[^>]*>(.*?)</style>",
        re.IGNORECASE | re.DOTALL
    )

    for match in style_pattern.finditer(content):
        css_blocks.append(match.group(1))

    return "\n".join(css_blocks)


# ------------------------------------------------------------
# EXTRACT CSS RULES
# ------------------------------------------------------------

def extract_rules(css):

    rules = []

    # Basic CSS rule parser
    rule_pattern = re.compile(
        r"([^{}]+)\{([^{}]*)\}",
        re.DOTALL
    )

    for match in rule_pattern.finditer(css):

        selector = match.group(1).strip()
        declarations = match.group(2).strip()

        if not selector or not declarations:
            continue

        rules.append((selector, declarations))

    return rules


# ------------------------------------------------------------
# EXTRACT DECLARATIONS
# ------------------------------------------------------------

def extract_declarations(declarations):

    result = []

    for prop in CSS_PROPERTIES:

        pattern = re.compile(
            rf"{re.escape(prop)}\s*:\s*([^;}}]+)",
            re.IGNORECASE
        )

        for match in pattern.finditer(declarations):

            value = re.sub(
                r"\s+",
                " ",
                match.group(1).strip()
            )

            result.append((prop, value))

    return result


# ------------------------------------------------------------
# FIND IMPORTANT SELECTORS
# ------------------------------------------------------------

def selector_matches(selector, target):

    selector_lower = selector.lower()

    target_lower = target.lower()

    # Direct selector
    if target_lower in selector_lower:
        return True

    return False


# ------------------------------------------------------------
# FILE ANALYSIS
# ------------------------------------------------------------

def analyze_file(filepath):

    try:

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as f:

            content = f.read()

    except UnicodeDecodeError:

        return None

    css = extract_css(content)

    rules = extract_rules(css)

    data = {
        "all": defaultdict(list),
        "important": defaultdict(list),
        "selectors": Counter(),
        "fonts": Counter()
    }


    # --------------------------------------------------------
    # Analyze rules
    # --------------------------------------------------------

    for selector, declarations in rules:

        selector_clean = re.sub(
            r"\s+",
            " ",
            selector
        ).strip()

        data["selectors"][selector_clean] += 1

        extracted = extract_declarations(
            declarations
        )

        for prop, value in extracted:

            data["all"][prop].append(
                (selector_clean, value)
            )

            # Font tracking
            if prop == "font-family":

                data["fonts"][value] += 1

            # Important selector tracking
            for target in IMPORTANT_SELECTORS:

                if selector_matches(
                    selector_clean,
                    target
                ):

                    data["important"][
                        target
                    ].append(
                        (prop, value, selector_clean)
                    )

                    break

    return data


# ------------------------------------------------------------
# FORMAT VALUE
# ------------------------------------------------------------

def format_value(value):

    return re.sub(
        r"\s+",
        " ",
        value.strip()
    )


# ------------------------------------------------------------
# PRINT PROPERTY SUMMARY
# ------------------------------------------------------------

def print_property_summary(
    all_data,
    category_name
):

    print()
    print("=" * 90)

    print(
        f"🎨 {category_name} — DESIGN PROPERTY SUMMARY"
    )

    print("=" * 90)

    for prop in CSS_PROPERTIES:

        values = []

        for filepath, data in all_data.items():

            for selector, value in data["all"].get(
                prop,
                []
            ):

                values.append(
                    (
                        value,
                        filepath,
                        selector
                    )
                )

        if not values:
            continue

        counter = Counter(
            value
            for value, _, _ in values
        )

        print()
        print(
            f"🔹 {prop}: "
            f"{len(values)} occurrence(s), "
            f"{len(counter)} different value(s)"
        )

        # Show values
        for value, count in counter.most_common():

            print(
                f"   → {value} "
                f"({count} occurrence(s))"
            )

            # If there are many variants,
            # show where they occur
            if len(counter) > 1:

                examples = [
                    (
                        filepath,
                        selector
                    )
                    for val, filepath, selector
                    in values
                    if val == value
                ]

                shown = 0

                for filepath, selector in examples[:3]:

                    print(
                        f"      - "
                        f"{os.path.relpath(filepath, PROJECT_ROOT)}"
                        f" → {selector}"
                    )

                    shown += 1

                if len(examples) > shown:

                    print(
                        f"      ... "
                        f"+{len(examples) - shown} more"
                    )


# ------------------------------------------------------------
# PRINT IMPORTANT SELECTORS
# ------------------------------------------------------------

def print_selector_summary(
    all_data,
    category_name
):

    print()
    print("=" * 90)

    print(
        f"🧩 {category_name} — IMPORTANT SELECTORS"
    )

    print("=" * 90)

    for target in IMPORTANT_SELECTORS:

        occurrences = []

        for filepath, data in all_data.items():

            for prop, value, selector in data[
                "important"
            ].get(target, []):

                occurrences.append(
                    (
                        filepath,
                        prop,
                        value,
                        selector
                    )
                )

        if not occurrences:
            continue

        print()
        print(f"🔸 {target}")

        property_groups = defaultdict(list)

        for (
            filepath,
            prop,
            value,
            selector
        ) in occurrences:

            property_groups[prop].append(
                (
                    value,
                    filepath,
                    selector
                )
            )

        for prop, items in property_groups.items():

            values = Counter(
                value
                for value, _, _ in items
            )

            print(
                f"   {prop}: "
                f"{len(values)} value(s)"
            )

            for value, count in values.most_common():

                print(
                    f"      → {value} "
                    f"({count})"
                )


# ------------------------------------------------------------
# PRINT FONT REPORT
# ------------------------------------------------------------

def print_font_report(
    all_data,
    category_name
):

    print()
    print("=" * 90)

    print(
        f"🔤 {category_name} — FONT REPORT"
    )

    print("=" * 90)

    font_files = defaultdict(set)

    for filepath, data in all_data.items():

        for font, count in data["fonts"].items():

            font_files[font].add(filepath)

    if not font_files:

        print("No font-family declarations found.")

        return

    for font, files in sorted(
        font_files.items(),
        key=lambda x: (-len(x[1]), x[0])
    ):

        print()
        print(
            f"→ {font}"
        )

        print(
            f"   Used in {len(files)} file(s)"
        )

        for filepath in sorted(files)[:10]:

            print(
                f"   - "
                f"{os.path.relpath(filepath, PROJECT_ROOT)}"
            )

        if len(files) > 10:

            print(
                f"   ... "
                f"+{len(files) - 10} more"
            )


# ------------------------------------------------------------
# FIND OUTLIERS
# ------------------------------------------------------------

def print_outliers(
    all_data,
    category_name
):

    print()
    print("=" * 90)

    print(
        f"⚠️ {category_name} — POSSIBLE DESIGN OUTLIERS"
    )

    print("=" * 90)

    found = False

    for prop in [
        "font-family",
        "font-size",
        "font-weight",
        "line-height",
        "color",
        "background",
        "background-color",
        "border-radius",
        "box-shadow",
        "padding",
        "gap"
    ]:

        occurrences = []

        for filepath, data in all_data.items():

            for selector, value in data[
                "all"
            ].get(prop, []):

                occurrences.append(
                    (
                        filepath,
                        selector,
                        value
                    )
                )

        if len(occurrences) < 2:
            continue

        counter = Counter(
            value
            for _, _, value in occurrences
        )

        # If there are multiple values,
        # flag the least common ones.
        if len(counter) > 1:

            found = True

            print()
            print(
                f"🔹 {prop}"
            )

            for value, count in counter.most_common():

                if count <= 2:

                    print(
                        f"   ⚠️ {value} "
                        f"({count} occurrence(s))"
                    )

                    for (
                        filepath,
                        selector,
                        actual_value
                    ) in occurrences:

                        if actual_value == value:

                            print(
                                f"      - "
                                f"{os.path.relpath(filepath, PROJECT_ROOT)}"
                                f" → {selector}"
                            )

    if not found:

        print()
        print(
            "✅ No obvious low-frequency "
            "design outliers found."
        )


# ------------------------------------------------------------
# FIND HTML FILES
# ------------------------------------------------------------

files_by_category = {
    "VOCABULARY GAME": [],
    "LESSON": []
}

for root, dirs, files in os.walk(PROJECT_ROOT):

    dirs[:] = [
        d
        for d in dirs
        if d not in IGNORE_DIRS
    ]

    for filename in files:

        extension = os.path.splitext(
            filename
        )[1].lower()

        if extension not in HTML_EXTENSIONS:
            continue

        filepath = os.path.join(
            root,
            filename
        )

        category = classify_file(
            filepath
        )

        if category:

            files_by_category[
                category
            ].append(filepath)


# ------------------------------------------------------------
# START
# ------------------------------------------------------------

print("=" * 90)

print(
    "🔎 DESIGN SYSTEM CHECK — CHECK ONLY"
)

print("=" * 90)

print()
print(
    f"📁 Project: {PROJECT_ROOT}"
)

print()
print(
    "⚠️ IMPORTANT:"
)

print(
    "   This script DOES NOT modify files."
)

print(
    "   It only analyzes existing HTML/CSS."
)

print()


# ------------------------------------------------------------
# ANALYZE CATEGORIES
# ------------------------------------------------------------

all_category_data = {}

for category, files in files_by_category.items():

    print()
    print("-" * 90)

    print(
        f"📂 {category}"
    )

    print(
        f"   Files found: {len(files)}"
    )

    print("-" * 90)

    category_data = {}

    for filepath in sorted(files):

        data = analyze_file(
            filepath
        )

        if data:

            category_data[
                filepath
            ] = data

    all_category_data[
        category
    ] = category_data


# ------------------------------------------------------------
# PRINT REPORTS
# ------------------------------------------------------------

for category, data in all_category_data.items():

    if not data:
        continue

    print_property_summary(
        data,
        category
    )

    print_font_report(
        data,
        category
    )

    print_selector_summary(
        data,
        category
    )

    print_outliers(
        data,
        category
    )


# ------------------------------------------------------------
# CROSS-CATEGORY COMPARISON
# ------------------------------------------------------------

print()
print("=" * 90)

print(
    "🔄 CROSS-CATEGORY DESIGN COMPARISON"
)

print("=" * 90)


def collect_category_values(
    category_data,
    property_name
):

    values = Counter()

    for filepath, data in category_data.items():

        for selector, value in data[
            "all"
        ].get(property_name, []):

            values[value] += 1

    return values


properties_to_compare = [
    "font-family",
    "font-size",
    "font-weight",
    "line-height",
    "border-radius",
    "box-shadow",
    "padding",
    "gap"
]

for prop in properties_to_compare:

    print()
    print(
        f"🔹 {prop}"
    )

    for category, data in all_category_data.items():

        if not data:
            continue

        values = collect_category_values(
            data,
            prop
        )

        print()

        print(
            f"   {category}:"
        )

        if not values:

            print(
                "      No declarations found."
            )

            continue

        for value, count in values.most_common():

            print(
                f"      → {value} "
                f"({count})"
            )


# ------------------------------------------------------------
# FINAL SUMMARY
# ------------------------------------------------------------

print()
print("=" * 90)

print(
    "📊 FINAL SUMMARY"
)

print("=" * 90)

total_files = sum(
    len(files)
    for files in files_by_category.values()
)

print()
print(
    f"Total relevant HTML files checked: "
    f"{total_files}"
)

for category, files in files_by_category.items():

    print(
        f"   {category}: {len(files)} file(s)"
    )

print()
print(
    "CSS properties checked:"
)

print(
    f"   {len(CSS_PROPERTIES)} properties"
)

print()
print(
    "Important selectors checked:"
)

print(
    f"   {len(IMPORTANT_SELECTORS)} selectors"
)

print()
print(
    "✅ CHECK COMPLETE"
)

print(
    "❌ NO FILES WERE MODIFIED"
)

print()
print("=" * 90)