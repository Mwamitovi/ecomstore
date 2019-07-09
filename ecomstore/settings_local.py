
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*ps!0$%4x+w+4dqunbt21i!^$(2u*yp*f9d$95ds@lx=(^tuuo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Change to true before deploying into production
ENABLE_SSL = False

# Google Checkout API credentials
GOOGLE_CHECKOUT_MERCHANT_ID = ''
GOOGLE_CHECKOUT_MERCHANT_KEY = ''
TEST_API_URL = \
    "https://sandbox.google.com/checkout/api/checkout/v2/merchantCheckout/Merchant/"
PRO_API_URL = \
    'https://checkout.google.com/api/checkout/v2/merchantCheckout/Merchant/'
# Use this for testing
GOOGLE_TEST_CHECKOUT_URL = TEST_API_URL + GOOGLE_CHECKOUT_MERCHANT_ID + '/diagnose'
# Use this in production
GOOGLE_REAL_CHECKOUT_URL = PRO_API_URL + GOOGLE_CHECKOUT_MERCHANT_ID

# Authorize.Net API Credentials
AUTHNET_POST_URL = 'test.authorize.net'
AUTHNET_POST_PATH = '/gateway/transact.dll'
AUTHNET_LOGIN = ''
AUTHNET_KEY = ''
