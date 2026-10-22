import sys
import os
from pathlib import Path

# Ensure UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

print("🧪 Starting updated PvZ Helper Bot test...")

# 1. Test Tracker
from services.playmarket_tracker import tracker
pvz2_info = tracker.get_pvz2_info()
assert pvz2_info is not None, "Failed to get PvZ 2 info"
print(f"✅ PvZ 2 Play Store Check: v{pvz2_info['version']} (Updated: {pvz2_info['updated_date']})")

pvz3_info = tracker.get_pvz3_info()
if pvz3_info:
    print(f"✅ PvZ 3 Play Store Check: v{pvz3_info['version']} ({pvz3_info['title']})")

# 2. Test Channel Post Builder
post_text, markup = tracker.build_channel_post(
    game_name="Plants vs. Zombies 2",
    version="13.5.1",
    changelog="Новые уровни!",
    play_url="https://play.google.com/store/apps/details?id=com.ea.game.pvz2_row",
)
assert "🌸 Новости франшизы PvZ 🍀" in post_text
assert "#НовостиPvZ2" in post_text

post_text_3, _ = tracker.build_channel_post(
    game_name="Plants vs. Zombies 3",
    version="34.0.27",
    changelog="Новые миссии!",
    play_url="https://play.google.com/store/apps/details?id=com.ea.gp.pvzn3xt",
)
assert "#НовостиPvZ3" in post_text_3
print("✅ Channel post format and hashtags verified.")

# 3. Test APK Downloader (Pure APK)
from services.apk_downloader import apk_downloader
from config import PVZ2_PACKAGE_ROW

play_url_2 = apk_downloader.get_play_store_url(PVZ2_PACKAGE_ROW)
assert "play.google.com" in play_url_2
print(f"✅ PvZ 2 Play Store link: {play_url_2}")

# 4. Test FileIdCache
from services.file_cache import file_cache
test_pkg = "com.test.game"
test_ver = "1.0.0"
file_cache.save_cached_parts(test_pkg, test_ver, [{"file_id": "TEST_FILE_ID_123", "filename": "test.apk", "size_mb": 15.0}])
cached = file_cache.get_cached_parts(test_pkg, test_ver)
assert cached is not None and len(cached) == 1
assert cached[0]["file_id"] == "TEST_FILE_ID_123"
# Check mismatch version returns None
assert file_cache.get_cached_parts(test_pkg, "1.0.1") is None
file_cache.clear(test_pkg)
assert file_cache.get_cached_parts(test_pkg, test_ver) is None
print("✅ FileIdCache service verified.")

# 5. Test Handlers Import
import handlers
import main
print("✅ main.py and all handlers imported cleanly.")

print("\n🎉 ALL TESTS PASSED! The bot with caching, progress bar, and daemon setup is ready.")
