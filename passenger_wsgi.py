import os 
import sys 
from pathlib import Path 
 
BASE_DIR = Path(__file__).resolve().parent 
sys.path.insert(0, str(BASE_DIR)) 
sys.path.insert(0, str(BASE_DIR / 'backend')) 
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.backend.settings') 
 
from django.core.wsgi import get_wsgi_application 
application = get_wsgi_application()
