def get_acad_version():
    for version in ["AutoCAD.Application.24", "AutoCAD.Application.23", "AutoCAD.Application.22"]:
        try:
            return win32com.client.Dispatch(version)
        except Exception as e:
            continue
    raise Exception("找不到可用的AutoCAD版本")

acad = get_acad_version()