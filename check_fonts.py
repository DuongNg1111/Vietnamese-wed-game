import os
import re
from collections import Counter, defaultdict

# ============================================================
# SETTINGS
# ============================================================

PROJECT_FOLDER = "."

EXTENSIONS = (".html", ".htm", ".css")

IGNORE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__"
}

# ============================================================
# FONT-SIZE DETECTION
# ============================================================

font_size_pattern = re.compile(
    r"""
    font-size
    \s*:\s*
    ([^;}{]+)
    """,
    re.IGNORECASE | re.VERBOSE
)

# ============================================================
# STORAGE
# ============================================================

all_sizes = Counter()
size_files = defaultdict(list)

file_results = []

# ============================================================
# SCAN
# ============================================================

for root, dirs, files in os.walk(PROJECT_FOLDER):

    dirs[:] = [
        d for d in dirs
        if d not in IGNORE_DIRS
    ]

    for filename in files:

        if not filename.lower().endswith(EXTENSIONS):
            continue

        filepath = os.path.join(root, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

        except UnicodeDecodeError:
            try:
                with open(filepath, "r", encoding="utf-8-sig") as f:
                    content = f.read()
            except Exception:
                print(f"⚠️ Cannot read: {filepath}")
                continue

        matches = font_size_pattern.findall(content)

        if not matches:
            continue

        relative_path = os.path.relpath(
            filepath,
            PROJECT_FOLDER
        )

        cleaned_sizes = []

        for size in matches:

            size = size.strip()

            all_sizes[size] += 1

            if relative_path not in size_files[size]:
                size_files[size].append(relative_path)

            if size not in cleaned_sizes:
                cleaned_sizes.append(size)

        file_results.append(
            (relative_path, cleaned_sizes)
        )

# ============================================================
# RESULT 1 — ALL FONT SIZES
# ============================================================

print()
print("=" * 80)
print("FONT-SIZE CHECK - VIETNAMESE GAME WEBSITE")
print("=" * 80)
print()

print("📌 ALL FONT-SIZE VALUES FOUND")
print("-" * 80)

if not all_sizes:

    print("❌ No font-size declarations found.")

else:

    for i, (size, count) in enumerate(
        all_sizes.most_common(),
        1
    ):

        print(
            f"{i:02d}. {size:<30} "
            f"→ {count} occurrence(s)"
        )

# ============================================================
# RESULT 2 — GROUP BY UNIT
# ============================================================

print()
print("=" * 80)
print("📐 FONT-SIZE BY UNIT")
print("=" * 80)

units = {
    "px": [],
    "rem": [],
    "em": [],
    "%": [],
    "vw": [],
    "vh": [],
    "other": []
}

for size in all_sizes:

    if size.endswith("px"):
        units["px"].append(size)

    elif size.endswith("rem"):
        units["rem"].append(size)

    elif size.endswith("em"):
        units["em"].append(size)

    elif size.endswith("%"):
        units["%"].append(size)

    elif size.endswith("vw"):
        units["vw"].append(size)

    elif size.endswith("vh"):
        units["vh"].append(size)

    else:
        units["other"].append(size)

for unit, sizes in units.items():

    if not sizes:
        continue

    print()
    print(f"🔹 {unit}")

    for size in sorted(sizes):
        print(
            f"   {size:<25} "
            f"→ {all_sizes[size]} occurrence(s)"
        )

# ============================================================
# RESULT 3 — FILE BY FILE
# ============================================================

print()
print("=" * 80)
print("📂 FONT-SIZE BY FILE")
print("=" * 80)

for filepath, sizes in file_results:

    print()
    print(f"📄 {filepath}")

    for size in sizes:

        print(
            f"   → {size} "
            f"({all_sizes[size]} total occurrence(s))"
        )

# ============================================================
# RESULT 4 — REM DETAILS
# ============================================================

print()
print("=" * 80)
print("🔎 REM FONT SIZES")
print("=" * 80)

rem_sizes = [
    size
    for size in all_sizes
    if size.endswith("rem")
]

if rem_sizes:

    for size in sorted(rem_sizes):

        print()
        print(
            f"REM: {size} "
            f"→ {all_sizes[size]} occurrence(s)"
        )

        for filepath in size_files[size]:

            print(f"   - {filepath}")

else:

    print("Không tìm thấy font-size dạng rem.")

# ============================================================
# RESULT 5 — SUMMARY
# ============================================================

print()
print("=" * 80)
print("📊 SUMMARY")
print("=" * 80)

print(
    f"Files containing font-size : {len(file_results)}"
)

print(
    f"Different font-size values : {len(all_sizes)}"
)

print(
    f"Total font-size declarations : {sum(all_sizes.values())}"
)

print()
print("=" * 80)
print("✅ CHECK ONLY — NO FILES WERE MODIFIED")
print("=" * 80)
print()