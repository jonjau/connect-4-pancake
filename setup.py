from cx_Freeze import setup, Executable

BUILD_EXE_OPTIONS = {"packages": ["numpy"]}

setup(
    name="Connect 4S+",
    version="0.1",
    description="A spin on Connect 4 :)",
    options={"build_exe": BUILD_EXE_OPTIONS},
    executables=[Executable("connect4plus.py")]
    )
