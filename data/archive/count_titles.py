from pathlib import Path

p = Path('.')
count = 0
dirs = sum([len([sd for sd in d.iterdir() if sd.is_dir()]) for d in p.iterdir() if d.is_dir()])

print(dirs)
# print("Hello World!")
