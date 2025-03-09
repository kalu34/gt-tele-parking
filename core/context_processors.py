import os

def global_settings(request):
  return {
    'API_URL': os.environ.get('API_URL','http://127.0.0.1:8000')
  }
