from pathlib import Path
import traceback
import sys

class StaticManager:
    def __init__(self):
        print("StaticManager initializing...", end="")
        try:
            self.STATIC_DIR = Path('static')
            self.BOTTLES_DIR = self.STATIC_DIR / "bottles"
            self.DESC_DIR = self.STATIC_DIR / "descriptions"
            
            self.BOTTLES_DIR.mkdir(parents=True, exist_ok=True)
            self.DESC_DIR.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"    [FAIL] - {e}")
            traceback.print_exc()
            sys.exit(1)
        else:
            print("    [OK]")
        
    def bottle_path(self, wID):
        return self.BOTTLES_DIR / f"{wID}.jpg"
    
    def description_path(self, wID):
        return self.DESC_DIR / f"{wID}.webp"
    
    def save_bottle(self, wID, file):
        path = self.bottle_path(wID)
        file.save(path)
        return path
    
    def save_description(self, wID, file):
        path = self.description_path(wID)
        file.save(path)
        return path
    
    def delete_bottle(self, wID):
        path = self.bottle_path(wID)
        if path.exists():
            path.unlink()
            return True
        return False

    def delete_description(self, wID):
        path = self.description_path(wID)
        if path.exists():
            path.unlink()
            return True
        return False
    
    def has_bottle(self, wID):
        path = self.bottle_path(wID)
        return path.exists()
    
    def has_description(self, wID):
        path = self.description_path(wID)
        return path.exists()