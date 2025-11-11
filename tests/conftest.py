import pytest
import subprocess
import time
import requests
import os

@pytest.fixture(scope='session')
def fastapi_server():
    """
    Fixture to start the FastAPI server before E2E tests and stop it after tests complete.
    """
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    env["PORT"] = "8010"  # ✅ Use a clean port

    print("🚀 Launching FastAPI server on port 8010...", flush=True)

    fastapi_process = subprocess.Popen(
        ['python', '-m', 'app.main'],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    server_url = 'http://127.0.0.1:8010/'
    timeout = 30
    start_time = time.time()
    server_up = False

    while time.time() - start_time < timeout:
        try:
            response = requests.get(server_url)
            if response.status_code == 200:
                server_up = True
                print("✅ FastAPI server is up and running.", flush=True)
                break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)

    if not server_up:
        try:
            stdout, stderr = fastapi_process.communicate(timeout=1)
            print("❌ FastAPI server failed to start.", flush=True)
            print("📤 Server stdout:\n", stdout.decode(errors="ignore"), flush=True)
            print("📥 Server stderr:\n", stderr.decode(errors="ignore"), flush=True)
        except Exception as e:
            print("⚠️ Failed to capture server logs:", str(e), flush=True)
        finally:
            fastapi_process.terminate()
        raise RuntimeError("FastAPI server failed to start within timeout period.")

    yield

    print("🛑 Shutting down FastAPI server...", flush=True)
    fastapi_process.terminate()
    fastapi_process.wait()
    print("✅ FastAPI server has been terminated.", flush=True)
