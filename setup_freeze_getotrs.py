from cx_Freeze import setup, Executable

buildOptions = dict(
    compressed=True, append_script_to_exe=False, create_shared_zip=False
)
setup(
    name="getotrs",
    version="0.1",
    description="getotrs",
    options=dict(build_exe=buildOptions),
    # targets to build
    executables=[Executable("getotrs.py")],
)
