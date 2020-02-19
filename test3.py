x = []
li = ["Cu", "O", "O"]
li.insert(0, '%s_B' % (li[0]))
wf = open("sdasd", "a+")

for i in range(len(li)):
    wf.write("%s " % (li[i]))

wf.write("\n ")
wf.write("dasdasd")
    
print(li)