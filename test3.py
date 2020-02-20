overall_list_of_layers = []
list_of_layers = []

xq = ["I am on layer 0", "test", "23", "999"]
x1q = ["te23st", "22223", "922299"]
for x in range(7):
    l = []
    list_of_layers.append(l)

for x in range(2):
    overall_list_of_layers.append(list_of_layers)

print(overall_list_of_layers)
list_of_layers[0].append(xq)
print(list_of_layers)
# print(overall_list_of_layers)