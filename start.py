import sys, os
import threading

if sys.platform.startswith("win32"):
    FETCH_PATH = "fetch_bin/fetch_windows_amd64.exe"
    DEL_COMMAND = "cd rd downloads/" #TODO: rendre ça compatible avec windows
elif sys.platform.startswith("linux"):
    FETCH_PATH = "fetch_bin/fetch_linux_amd64"
    os.system("chmod a+x " + FETCH_PATH)
elif sys.platform.startswith("darwin"):
    FETCH_PATH = "fetch_bin/fetch_darwin_amd64"
else:
    raise Exception("OS not compatible")

def repo_thread(repo_name:str, dyno:str):
    app_path = "downloads/" + repo_name
    if os.path.isdir(app_path):
        os.system("rm -r " + app_path)

    repo_url = os.environ["GITHUB_URL_START"] + repo_name
    os.system(FETCH_PATH + " --repo " + repo_url + " --github-oauth-token " + os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"] + " --branch master downloads/" + repo_name)

    # Install app requirements if exists
    if os.path.isfile(app_path + "/requirements.txt"):
        os.system("pip install -r " + app_path + "/requirements.txt")

    with open(app_path + "/Procfile", "r", encoding="utf-8") as f:
        data =  f.read().splitlines()

    procfile = {}
    for line in data:
        splitted = line.split(": ")
        procfile[splitted[0]] = splitted[1]

    os.system("cd downloads/" + repo_name + " ; " + procfile[dyno])

with open("reps.txt", "r", encoding="utf-8") as reps_f:
    data = reps_f.read().splitlines()

for line in data:
    if line.startswith("#") or not line:
        continue
    
    thread_data = line.split(" : ")
    thread = threading.Thread(target=repo_thread, args=thread_data)
    thread.start()