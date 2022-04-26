import sys, os

if sys.platform.startswith("win32"):
    FETCH_PATH = "fetch_bin/fetch_windows_amd64.exe"
elif sys.platform.startswith("linux"):
    FETCH_PATH = "fetch_bin/fetch_linux_amd64"
elif sys.platform.startswith("darwin"):
    FETCH_PATH = "fetch_bin/fetch_darwin_amd64"
else:
    raise Exception("")

def repo_thread(name:str, dyno:str):
    os.system(FETCH_PATH + " --github-oauth-token" + os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"))