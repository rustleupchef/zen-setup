from dotenv import load_dotenv, find_dotenv
import requests
import os
import sys
import shutil

load_dotenv(find_dotenv(), override=True)

def input_request(prompt = "Are you okay continuing?", 
                  yes = "Y", 
                  no = "n", 
                  yOutput="Continuing to final step", 
                  nOutput = "Not continuing to the next step") -> bool:
    yes = yes.lower()
    no = no.lower()

    while True:
        response = input(f"{prompt}\nPlease write either {yes.upper()}/{no}").lower()
        
        if response == yes:
            print(yOutput)
            return True
        
        if response == no:
            print(nOutput) 
            return False
        print("Invalid response. Please try again.")

def check_url(url: str) -> bool:
    print(url)
    try:
        return requests.head(url).status_code == 200
    except requests.ConnectionError:
        return False


def language_packs(source_path, dest_path, mozconfig, mozconfig_output_path) -> None:
    # currently only supports linux and windows
    if sys.platform == "linux":
        os.system("sh  scripts/update-en-US-packs.sh")
    shutil.copytree(source_path, dest_path, dirs_exist_ok=True);

    #editing mozconfig
    with open(mozconfig, 'r') as f:
        text = f.read().replace("$PWD", mozconfig_output_path)
        f.close()
    
    with open(mozconfig, 'w') as f:
        f.write(text)
        f.close()
    


def grab_repo_name(url: str) -> str:
    return url.split("/")[-1]

def main() -> None:

    FORKED_REPO = os.environ.get("FORKED_REPO").replace(".git", "") # getting the your fork of zen browser
    L10N_REPO = os.environ.get("L10N_REPO").replace(".git", "") # getting the l10n packs
    DESKTOP_DIR = os.path.join(os.getcwd(), grab_repo_name(FORKED_REPO)) # dir for forked repo
    #check if env variables are set
    if FORKED_REPO is None or FORKED_REPO == "":
        print("FORKED_REPO is not set");
        return
    if L10N_REPO is None or L10N_REPO == "": L10N_REPO = "https://github.com/zen-browser/l10n-packs"

    #grabbing language pack related files
    MOZ_CONF_DIR = os.path.join(DESKTOP_DIR, "configs", "common", "mozconfig") # dir for mozconfig
    MOZ_CONF_OUTPUT_DIR = os.path.join(DESKTOP_DIR, "engine", "browser", "locales") # output dir for mozconfig
    LANGUAGE_PACKS_DIR = os.path.join(DESKTOP_DIR, "l10n", "en-US", "browser", "browser") # dir for language packs
    LANGUAGE_PACKS_OUTPUT_DIR = os.path.join(MOZ_CONF_OUTPUT_DIR, "en-US", "browser") # output dir for language packs

    #check if url's are valid
    if not check_url(FORKED_REPO):
        print("FORKED_REPO is not a valid url")
        return 
    if not check_url(L10N_REPO):
        print("L10N_REPO is not a valid url")
        return
    
    # running commands
    if not os.path.exists(DESKTOP_DIR):
        os.system(f"git clone {FORKED_REPO}");
    os.system(f"git clone {L10N_REPO} \"{DESKTOP_DIR}/l10n/\"")
    os.system(f"cd \"{DESKTOP_DIR}\" && npm i && npm run init && npm run bootstrap")

    # copy language packs
    language_packs(LANGUAGE_PACKS_DIR, LANGUAGE_PACKS_OUTPUT_DIR, MOZ_CONF_DIR, MOZ_CONF_OUTPUT_DIR)

    if not input_request("Would you like to build the browser?"): return
    os.system(f"cd \"{DESKTOP_DIR}\" && npm run build")

if __name__ == "__main__":
    main()