import os

FOLDER_1 = "test-audio"
FOLDER_2 = "audio/vocabulary"

files_1 = {
    f for f in os.listdir(FOLDER_1)
    if f.lower().endswith(".mp3")
}

files_2 = {
    f for f in os.listdir(FOLDER_2)
    if f.lower().endswith(".mp3")
}

# =========================
# TRÙNG
# =========================

duplicate = sorted(files_1 & files_2)

# =========================
# CHỈ CÓ TRONG TEST-AUDIO
# =========================

only_test = sorted(files_1 - files_2)

# =========================
# CHỈ CÓ TRONG AUDIO/VOCABULARY
# =========================

only_vocab = sorted(files_2 - files_1)


# =========================
# RESULT
# =========================

print("\n==============================")
print("TRÙNG Ở CẢ 2 FOLDER")
print("==============================")

if duplicate:
    for f in duplicate:
        print(f)
else:
    print("Không có file trùng.")


print("\n==============================")
print("CHỈ CÓ TRONG test-audio")
print("==============================")

if only_test:
    for f in only_test:
        print(f)
else:
    print("Không có.")


print("\n==============================")
print("CHỈ CÓ TRONG audio/vocabulary")
print("==============================")

if only_vocab:
    for f in only_vocab:
        print(f)
else:
    print("Không có.")


print("\n==============================")
print("SUMMARY")
print("==============================")
print(f"test-audio:          {len(files_1)} files")
print(f"audio/vocabulary:    {len(files_2)} files")
print(f"Trùng nhau:          {len(duplicate)} files")
print(f"Chỉ test-audio:      {len(only_test)} files")
print(f"Chỉ vocabulary:      {len(only_vocab)} files")