import os

FOLDER = "test-audio"

old_name = "2_ba_6e9c27ea-7390-4af2-a4d4-3f0a5ff41b99.mp3.mp3"
new_name = "ba.mp3"

old_path = os.path.join(FOLDER, old_name)
new_path = os.path.join(FOLDER, new_name)

if not os.path.exists(old_path):
    print(f"❌ Không tìm thấy: {old_name}")

elif os.path.exists(new_path):
    print(f"⚠️ {new_name} đã tồn tại, không đổi tên.")

else:
    os.rename(old_path, new_path)
    print(f"✅ {old_name} → {new_name}")