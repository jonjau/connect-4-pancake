from cx_Freeze import setup, Executable

BUILD_EXE_OPTIONS = {"packages": ["numpy"]}

# to prevent console from popping up
#EXE = [Executable("connect4pancake.py", base="Win32GUI")]

# linux
EXE = [Executable("connect4pancake.py")]

setup(
    name="Connect 4 Pancake",
    version="1.0",
    description="A spin on Connect 4 :)",
    options={"build_exe": BUILD_EXE_OPTIONS},
    executables=EXE
    )
