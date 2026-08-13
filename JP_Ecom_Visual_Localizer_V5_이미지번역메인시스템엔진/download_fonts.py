import os
import urllib.request
import zipfile

def download_noto_sans_jp():
    font_dir = r"D:\Users\euntaewoo\Desktop\JP_Ecom_Visual_Localizer_V3\fonts"
    os.makedirs(font_dir, exist_ok=True)
    
    # URL for Noto Sans JP from Google Fonts
    url = "https://fonts.google.com/download?family=Noto%20Sans%20JP"
    zip_path = os.path.join(font_dir, "NotoSansJP.zip")
    
    print("Downloading Noto Sans JP...")
    urllib.request.urlretrieve(url, zip_path)
    print("Download complete. Extracting...")
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(font_dir)
        
    print(f"Fonts extracted to {font_dir}")
    
    # Cleanup zip
    os.remove(zip_path)
    
if __name__ == "__main__":
    download_noto_sans_jp()
