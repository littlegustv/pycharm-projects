from cx_Freeze import setup, Executable

setup(
    name="Lift",
    version="0.1",
    description="Self aware elevator simulator.",
    executables=[Executable("main.pyw")],
)
