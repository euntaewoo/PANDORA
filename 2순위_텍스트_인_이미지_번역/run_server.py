import os
import sys
import subprocess

def run_2nd_priority_server():
    target_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
    if target_dir not in sys.path:
        sys.path.insert(0, target_dir)

    print("==================================================")
    print("🚀 2순위 배경 보존 텍스트 인 이미지 번역 웹 서버 구동 중...")
    print("==================================================")
    print("접속 주소: http://127.0.0.1:8000")
    print("종료하려면 Ctrl+C 키를 누르세요.\n")
    
    venv_py = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역\.venv\Scripts\python.exe"
    py_exec = venv_py if os.path.exists(venv_py) else sys.executable

    try:
        import uvicorn
        from backend.server import app
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except Exception as e:
        print(f"[INFO] 프로젝트 가상환경 uvicorn 구동: {e}")
        env = os.environ.copy()
        env["PYTHONPATH"] = target_dir
        subprocess.run([py_exec, "-m", "uvicorn", "backend.server:app", "--host", "127.0.0.1", "--port", "8000"], cwd=target_dir, env=env)

if __name__ == "__main__":
    run_2nd_priority_server()
