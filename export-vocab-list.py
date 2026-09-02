import json


INPUT_FILE = "categories.json"
OUTPUT_FILE = "vocabulary-list.txt"


# ============================================
# READ categories.json
# ============================================

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)


# ============================================
# BUILD TEXT
# ============================================

output = []

output.append("VIETNAMESE VOCABULARY LIST")
output.append("==========================")
output.append("")


for category_name, category in data.items():

    # Only vocabulary categories
    if (
        category.get("type") != "vocabulary"
        or not isinstance(category.get("vocab"), list)
    ):
        continue


    output.append(
        f"===== {category_name} ====="
    )

    output.append("")


    for topic in category["vocab"]:

        words = topic.get(
            "vocabulary",
            []
        )


        if not words:
            continue


        # Topic name
        if topic.get("topic"):

            output.append(
                f"-- {topic['topic']} --"
            )

            output.append("")


        # Vocabulary
        for word in words:

            if (
                isinstance(word, dict)
                and word.get("vietnamese")
            ):

                output.append(
                    word["vietnamese"]
                )


        output.append("")


    output.append("")


# ============================================
# WRITE TXT FILE
# ============================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "\n".join(output)
    )


print(
    f"Done! Created: {OUTPUT_FILE}"
)