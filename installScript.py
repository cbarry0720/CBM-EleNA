import pip
f = open("requirements.txt", "r")
lines = f.readlines()
for x in lines:
    pip.main(["install",x])