import string
import random
from django.core.cache import cache


def send_otp(phone, code):
    print(f"code send to {phone}...")

def check_limited(key, max_request, time):
    cache.add(key, 0, timeout=time)
    count = cache.incr(key)
    return count <= max_request

class OTPService:

    @staticmethod
    def generate_code():
        code = string.digits
        return "".join(random.choice(code) for _ in range(6))

    @staticmethod
    def send_otp_for_user(phone):
        code = OTPService.generate_code()
        cache.set(f"user_{phone}", code, timeout=120)
        send_otp(phone, code)
        return f"Phone {phone} Code Verify : {code}"

    def verify_otp(phone, code):
        otp = cache.get(f"user_{phone}")

        if otp and otp == code:
            print(f"Code Verified")
            cache.delete(otp)
            return True
        
        print(f"Code Invalid")
        return False


       