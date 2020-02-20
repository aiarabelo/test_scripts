x = [["423", "123"], ["123", "432"], ["903", "23"]]

x.sort(key=lambda y: int(y[1]))

print(x)