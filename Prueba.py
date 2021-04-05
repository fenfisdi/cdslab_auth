import pyotp
from datetime import datetime

print(pyotp.TOTP('M5I7JS5U4BSXW6OZC654ICAYEV23ATKW').now())
