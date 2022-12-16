import pip
f = open("requirments.txt" , "r")
lines = f.readlines()
for x in lines:
    pip.main(["install",x])