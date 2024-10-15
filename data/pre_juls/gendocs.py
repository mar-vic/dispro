import subprocess
from pathlib import Path

in_dir = Path(".")
out_dir = Path("./docx/")

out_files = [file for file in out_dir.iterdir() if file.is_file()]
in_files = [
    file
    for file in in_dir.iterdir()
    if file.is_file()
    and file.stem not in [file.stem for file in out_files]
    and file.stem != "gendocs"
]

# print(in_files)
# print(len(in_files))

for file in in_files:
    subprocess.run(
        [
            "pandoc",
            file.name,
            "-f",
            "../../pandoc/readers/eltec.lua",
            "-t",
            "docx",
            "-o",
            f"./docx/{file.stem}.docx",
        ],
        capture_output=True,
    )
