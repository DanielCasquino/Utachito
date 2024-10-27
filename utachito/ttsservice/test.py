import os

path = os.getcwd() + "/utachito.wav"
print(path)
os.system(f"vlc -I dummy --dummy-quiet --play-and-exit {path}")
