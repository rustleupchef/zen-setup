# About
This is some code I made to quickly setup the zen browser, so you can run code locally. The reason I made this is because the docs are mainly designed for windows, and even then the documentation can be a little trick, so I decided to make some code to automatically setup the zen-browser on both windows and linux.

## Mac
Mac support is currently in the work, but the code used to run windows should also work just fine with macs, but the code is not guaranteed to work on macs.

# Usage
First thing you need to do is go into the directory that you want to add the code
For example

    cd path/to/zen
You want to make sure this folder does or is going to contain the desktop repository
In this folder you want to git clone the setup code and move it back to your folder

## Linux
```bash
git clone https://github.com/rustleupchef/zen-setup.git
cd zen-setup
mv * ..
cd ..
rm -rf zen-setup/
```
## Windows
windows is essentially the exact same except their aren't any built in functions so you'll have to manually move all the files out of the clone repository.

## Dot env file
You want to edit the .env file placed to match your current setup
The file should contain:
```js
FORKED_REPO=https://github.com/rustleupchef/desktop
L10N_REPO=https://github.com/rustleupchef/l10n-packs
```
You NEED to change FORKED_REPO to your fork of the zen-browser, but if you don't have to assign L10N_REPO (as in you can leave it blank)
I would highly suggest that you fork it regardless, but if you really don't want to the code will just grab the official zen-browser repo for l10n-packs

## Run
Now that you setup up the file and environment variables you can run
And all you have to do is write
```bash
python main.py
```