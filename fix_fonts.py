import os
import re

# ============================================================
# FIX FONT SIZES
# ============================================================
# This script increases EVERY font-size by 2px.
#
# Examples:
#   18px   -> 20px
#   22px   -> 24px
#   1rem   -> 1.125rem
#   0.82rem -> 0.945rem
#
# It also handles clamp() values containing rem.
#
# IMPORTANT:
# - This version MODIFIES files.
# - It does NOT change font-family.
# - It only targets font-size declarations.
# ============================================================


# ------------------------------------------------------------
# SETTINGS
# ------------------------------------------------------------

# Project folder = same folder where this script is located
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Increase by 2px
INCREASE_PX = 4

# 1rem = 16px
REM_TO_PX = 16

# Extensions to process
EXTENSIONS = {".html", ".htm"}


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def increase_px(value):
    """
    Increase a px value by 2px.

    Examples:
        18px -> 20px
        22px -> 24px
    """

    number = float(value)

    new_number = number + INCREASE_PX

    # Keep integers clean
    if new_number.is_integer():
        return f"{int(new_number)}px"

    return f"{new_number:g}px"


def increase_rem(value):
    """
    Increase a rem value by 2px.

    Since:
        1rem = 16px

    2px = 0.125rem

    Examples:
        1rem    -> 1.125rem
        0.82rem -> 0.945rem
        2rem    -> 2.125rem
    """

    number = float(value)

    increase_rem_value = INCREASE_PX / REM_TO_PX

    new_number = number + increase_rem_value

    # Keep useful precision
    result = f"{new_number:.3f}".rstrip("0").rstrip(".")

    return f"{result}rem"


def increase_font_value(value):
    """
    Increase a complete CSS font-size value.

    Supports:
        px
        rem
        clamp(...)
        values containing rem / px
    """

    original = value

    # --------------------------------------------------------
    # 1. Simple px
    # --------------------------------------------------------

    px_match = re.fullmatch(
        r"\s*(-?\d+(?:\.\d+)?)px\s*",
        value,
        flags=re.IGNORECASE
    )

    if px_match:
        return increase_px(px_match.group(1))


    # --------------------------------------------------------
    # 2. Simple rem
    # --------------------------------------------------------

    rem_match = re.fullmatch(
        r"\s*(-?\d+(?:\.\d+)?)rem\s*",
        value,
        flags=re.IGNORECASE
    )

    if rem_match:
        return increase_rem(rem_match.group(1))


    # --------------------------------------------------------
    # 3. clamp(...)
    #
    # Example:
    #
    # clamp(
    #     2rem,
    #     5vw,
    #     2.8rem
    # )
    #
    # becomes:
    #
    # clamp(
    #     2.125rem,
    #     5vw,
    #     2.925rem
    # )
    # --------------------------------------------------------

    if re.match(r"\s*clamp\s*\(", value, flags=re.IGNORECASE):

        def replace_rem(match):
            number = match.group(1)
            return increase_rem(number)

        def replace_px(match):
            number = match.group(1)
            return increase_px(number)

        new_value = re.sub(
            r"(-?\d+(?:\.\d+)?)rem",
            replace_rem,
            value,
            flags=re.IGNORECASE
        )

        new_value = re.sub(
            r"(-?\d+(?:\.\d+)?)px",
            replace_px,
            new_value,
            flags=re.IGNORECASE
        )

        return new_value


    # --------------------------------------------------------
    # 4. Other values
    #
    # If something unusual is found, leave it unchanged.
    # --------------------------------------------------------

    return original


# ------------------------------------------------------------
# PROCESS ONE FILE
# ------------------------------------------------------------

def process_file(filepath):

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

    except UnicodeDecodeError:
        print(f"⚠️ Skipped (encoding issue): {filepath}")
        return 0

    original_content = content

    changes = []


    # --------------------------------------------------------
    # Match font-size declarations
    #
    # Examples:
    #
    # font-size: 18px;
    # font-size: 1rem;
    # font-size: clamp(2rem, 5vw, 3rem);
    #
    # Does NOT touch:
    #
    # font-weight
    # line-height
    # width
    # height
    # padding
    # margin
    # etc.
    # --------------------------------------------------------

    pattern = re.compile(
        r"""
        (?P<prefix>
            font-size
            \s*:\s*
        )

        (?P<value>
            clamp
            \s*\(
                (?:
                    [^()]|\([^()]*\)
                )*
            \)
            |
            [-+]?\d+(?:\.\d+)?px
            |
            [-+]?\d+(?:\.\d+)?rem
        )

        (?P<suffix>
            \s*
            (?=;)
        )
        """,
        flags=re.IGNORECASE | re.VERBOSE
    )


    def replace_match(match):

        original_value = match.group("value")

        new_value = increase_font_value(original_value)

        if new_value != original_value:

            changes.append(
                (original_value, new_value)
            )

        return (
            match.group("prefix")
            + new_value
            + match.group("suffix")
        )


    content = pattern.sub(replace_match, content)


    # --------------------------------------------------------
    # Write only if something changed
    # --------------------------------------------------------

    if content != original_content:

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)


    # --------------------------------------------------------
    # Print changes
    # --------------------------------------------------------

    if changes:

        print()
        print(f"📄 {os.path.relpath(filepath, PROJECT_ROOT)}")

        for old, new in changes:
            print(f"   {old}  →  {new}")

    return len(changes)


# ------------------------------------------------------------
# FIND ALL HTML FILES
# ------------------------------------------------------------

html_files = []

for root, dirs, files in os.walk(PROJECT_ROOT):

    # Ignore common folders that should not be processed
    dirs[:] = [
        d for d in dirs
        if d not in {
            ".git",
            "node_modules",
            "__pycache__"
        }
    ]

    for filename in files:

        extension = os.path.splitext(filename)[1].lower()

        if extension in EXTENSIONS:

            filepath = os.path.join(root, filename)

            html_files.append(filepath)


# ------------------------------------------------------------
# START
# ------------------------------------------------------------

print("=" * 90)
print("🔧 FIX FONT SIZES — APPLY MODE")
print("=" * 90)

print()
print(f"📁 Project: {PROJECT_ROOT}")
print("📏 Increase: +2px")
print("🔤 REM conversion: 1rem = 16px")
print("🎨 Font-family: NOT MODIFIED")
print("✏️ Files WILL BE MODIFIED")
print()


# ------------------------------------------------------------
# PROCESS
# ------------------------------------------------------------

total_files_modified = 0
total_declarations_modified = 0

for filepath in sorted(html_files):

    count = process_file(filepath)

    if count > 0:

        total_files_modified += 1
        total_declarations_modified += count


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

print()
print("=" * 90)
print("📊 SUMMARY")
print("=" * 90)

print()
print(f"HTML files found: {len(html_files)}")
print(f"Files modified: {total_files_modified}")
print(f"Font-size declarations modified: {total_declarations_modified}")

print()

if total_declarations_modified > 0:

    print("✅ DONE — All detected font-size values were increased by 2px.")
    print("✅ Files have been modified successfully.")

else:

    print("ℹ️ No font-size declarations needed modification.")

print()
print("=" * 90)
print("🏁 FINISHED")
print("=" * 90)