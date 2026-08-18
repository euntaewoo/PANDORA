"""
===================================================================================
🌐 Multi-lingual_Text-In_Image_Translation_Engine.py (Root Legacy Wrapper)
-----------------------------------------------------------------------------------
• Main Core: multilingual_text_in_image_translation/multilingual_text_in_image_translation.py
===================================================================================
"""

import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_ENGINE = os.path.join(SCRIPT_DIR, "multilingual_text_in_image_translation", "multilingual_text_in_image_translation.py")

if __name__ == "__main__":
    cmd = [sys.executable, MAIN_ENGINE] + sys.argv[1:]
    sys.exit(subprocess.run(cmd).returncode)
