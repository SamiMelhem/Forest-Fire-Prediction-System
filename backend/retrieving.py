import json
import os
import time
import threading

class LocationCache:
    def __init__(self, filename="cache.json", expiry_time=3600):
        self.filename = filename
        self.expiry_time = expiry_time
        self.cache = self.load_cache()

    def load_cache(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                try:
                    data = json.load(f)
                    return {k: v for k, v in data.items() if self.is_valid(v)}
                except json.JSONDecodeError:
                    return {}
        return {}

    def save_cache(self):
        with open(self.filename, "w") as f:
            json.dump(self.cache, f, indent=4)

    def is_valid(self, entry):
        return time.time() - entry["timestamp"] < self.expiry_time

    def set_location(self, user_id, location):
        self.cache[user_id] = {
            "location": location,
            "timestamp": time.time()
        }
        self.save_cache()

    def get_location(self, user_id):
        if user_id in self.cache and self.is_valid(self.cache[user_id]):
            return self.cache[user_id]["location"]
        return None

    def get_all_locations(self):
        return {user_id: data["location"] for user_id, data in self.cache.items()}

    def remove_user(self, user_id):
        if user_id in self.cache:
            del self.cache[user_id]
            self.save_cache()

    def refresh_cache(self):
        """Refreshes the cache every 10 minutes."""
        while True:
            print("Refreshing cache...")
            self.cache = self.load_cache()
            self.save_cache()
            time.sleep(600)

if __name__ == "__main__":
    cache = LocationCache()

    refresh_thread = threading.Thread(target=cache.refresh_cache, daemon=True)
    refresh_thread.start()

    cache.set_location("user_123", {"latitude": 40.7128, "longitude": -74.0060})
    cache.set_location("user_456", {"latitude": 37.7749, "longitude": -122.4194})

    print("User 123's Location:", cache.get_location("user_123"))
    print("All Locations:", cache.get_all_locations())

    cache.remove_user("user_456")
    print("After Removing User 456:", cache.get_all_locations())
