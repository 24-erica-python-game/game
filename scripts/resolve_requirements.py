import pip

if hasattr(pip, "main"):
    pip.main(["install", "-r", "../requirements.txt"])
else:
    pip._internal.main(["install", "-r", "../requirements.txt"])
