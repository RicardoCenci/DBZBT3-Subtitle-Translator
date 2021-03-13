from cx_Freeze import setup, Executable

base = None    

executables = [Executable("main.py", base=base, targetName="dbzbt3sub.exe")]

packages = ["idna"]
options = {
    'build_exe': {
        'build_exe': '.././DBZBT3 Translation Tool',
        'packages':packages,
    },    
}

setup(
    name = "DBZBT3 Unk Translator",
    options = options,
    version = "0.9",
    description = 'A Simple console based program to open and translate .unk files from the game DBZ:BT3 for PS2',
    executables = executables
)