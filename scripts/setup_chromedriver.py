import os
import platform
import requests
import zipfile
import stat
from pathlib import Path

def setup_chromedriver():
    """M1/M2 Mac용 ChromeDriver 설치"""
    
    # Chrome 버전 확인 - 최신 버전 사용
    chrome_version = "138.0.7204.169"  # Chrome 138 버전용
    
    # 다운로드 URL
    if platform.machine() == "arm64":
        # M1/M2 Mac
        download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/mac-arm64/chromedriver-mac-arm64.zip"
    else:
        # Intel Mac
        download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/mac-x64/chromedriver-mac-x64.zip"
    
    # 드라이버 저장 경로
    driver_dir = Path.home() / ".chromedriver"
    driver_dir.mkdir(exist_ok=True)
    
    driver_path = driver_dir / "chromedriver"
    
    # 이미 존재하면 삭제
    if driver_path.exists():
        driver_path.unlink()
    
    print(f"ChromeDriver 다운로드 중: {download_url}")
    
    # 다운로드
    response = requests.get(download_url)
    zip_path = driver_dir / "chromedriver.zip"
    
    with open(zip_path, "wb") as f:
        f.write(response.content)
    
    # 압축 해제
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(driver_dir)
    
    # 압축 파일 삭제
    zip_path.unlink()
    
    # chromedriver 실행 파일 찾기
    for root, dirs, files in os.walk(driver_dir):
        for file in files:
            if file == "chromedriver":
                src = Path(root) / file
                if src != driver_path:
                    src.rename(driver_path)
                break
    
    # 실행 권한 부여
    driver_path.chmod(driver_path.stat().st_mode | stat.S_IEXEC)
    
    print(f"ChromeDriver 설치 완료: {driver_path}")
    return str(driver_path)

if __name__ == "__main__":
    driver_path = setup_chromedriver()
    print(f"ChromeDriver 경로: {driver_path}")