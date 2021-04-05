import pyotp
from datetime import datetime

print(pyotp.TOTP('QO3HLQ3HHPSS2XFQQHXLBYKQIKY2FX5M').now())
