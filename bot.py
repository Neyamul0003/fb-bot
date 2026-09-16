import requests
import pyotp

print("====================================")
print("      FACEBOOK AUTO-LOGIN BOT      ")
print("====================================\n")

email = input("১. Enter Email/Phone: ").strip()
password = input("২. Enter Password: ").strip()
secret_2fa = input("৩. Enter 2FA Secret Key: ").strip().replace(" ", "")

# OTP জেনারেট
totp = pyotp.TOTP(secret_2fa)
current_otp = totp.now()

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
})

print("\n[+] Logging in via HTTP Request...")

try:
    # লগইন রিকোয়েস্ট
    login_url = "https://m.facebook.com/login/device-based/regular/login/"
    payload = {
        'email': email,
        'pass': password
    }
    res = session.post(login_url, data=payload)

    # ২FA কোড সাবমিট
    if "checkpoint" in res.url or "approvals_code" in res.text:
        print(f"[+] 2FA Page detected. Submitting OTP: {current_otp}")
        otp_url = "https://m.facebook.com/login/checkpoint/"
        otp_payload = {
            'approvals_code': current_otp,
            'submit[Submit Code]': 'Submit Code'
        }
        res2 = session.post(otp_url, data=otp_payload)
        print("[+] OTP Submitted Successfully!")
    else:
        print("[+] Logged in without 2FA trigger.")

    print("[+] Operation Completed!")

except Exception as e:
    print("[-] Error:", e)
