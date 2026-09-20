"""Lambda entry points; application imports stay inside the scripts directory."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))
from cloud_bot import api, worker
