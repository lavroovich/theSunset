import pyotp
from dotenv import load_dotenv
import os
import traceback
import sys

load_dotenv()

class TOTPctl:
    def __init__(self):
        print("TOTPctl initializing...", end="")
        try:
            self.secret = os.getenv("TOTP_SECRET")
            if not self.secret:
                print("secret will be generated and saved to .env file")
                self.secret = pyotp.random_base32()
                with open(".env", "a") as f:
                    f.write(f"\nTOTP_SECRET={self.secret}\n")
                    
            self.totp = pyotp.TOTP(self.secret)
        except Exception as e:
            print(f"    [FAIL] - {e}")
            traceback.print_exc()
            sys.exit(1)
        else:
            print("    [OK]")
        
    def get_uri(self, user):
        print(f"SECURITY LOG: generating TOTP URI for user {user}")
        return self.totp.provisioning_uri(name=user, issuer_name="CPWB theSunset")
    
    def verify(self, code):
        print(f"SECURITY LOG: verifying TOTP code")
        return self.totp.verify(code)
    
    
        