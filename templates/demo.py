i = [[1,2,3],[4,5,6],[7,8,9],[10,11,12]]
p=[]
s = []
for j in range(3):
    s=[]
    for k in range(4):
        s.append(i[k][j])
    p.append(s)
print(p)


