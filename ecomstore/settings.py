"""
Django settings for ecomstore project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from ecomstore.settings_local import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/


ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Added
    'django.contrib.sites',
    'django.contrib.flatpages',
    'catalog',
    'utils',
    'cart',
    'checkout',
    'accounts',
    'search',
    'stats',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Added
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'ecomstore.SSLMiddleware.SSLRedirect',
]

SITE_ID = 1

ROOT_URLCONF = 'ecomstore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # We are telling django.template.loaders.filesystem.Loader:
            # to look into C:\virtualenvs\...\ecomstore\templates\(index.html)
            # The last part in brackets is generated from views.py - template_name
            os.path.join(BASE_DIR, "templates")
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'utils.context_processors.ecomstore',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecomstore.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "ecomstore_db",
        'USER': "root",
        'PASSWORD': "root",
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Kampala'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# STATIC_URL = '/static/'
# Set the static path to link to url pattern
STATIC_URL = "/r'^static/"

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'static')

# The URL that handles the media served from MEDIA_ROOT.
# Use a trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# default site name
SITE_NAME = 'Modern Musician'

# default site keywords
META_KEYWORDS = 'Music, instruments, music accessories, musician supplies'

# default site description
META_DESCRIPTION = 'Modern Musician is an online supplier of instruments, \
                    sheet music, and other accessories for musicians'

# session settings
SESSION_COOKIE_DAYS = 90

SESSION_COOKIE_AGE = 60*60*24*SESSION_COOKIE_DAYS

# Redirects to a custom page, after login
LOGIN_REDIRECT_URL = '/accounts/my_account/'

# search results
PRODUCTS_PER_PAGE = 12

# search results from the highest-ranking 3 words
PRODUCTS_PER_ROW = 4


# Handling performance - CACHE

CACHE_TIMEOUT = 60 * 60