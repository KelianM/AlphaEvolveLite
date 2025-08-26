def p(g,z=range):
 r,c=len(g),len(g[0])
 p=[(i,j,g[i][j])for i in z(r)for j in z(c)if g[i][j]]
 p.sort()
 if len(p)==2:
  a,b=p
  if a[0]==b[0]:
   i,n,H=a;T,N=b[1],b[2];d=abs(T-n)
   for x in z(r):g[x][n]=H;g[x][T]=N
   if d:
    j=max(n,T)+d;k=0;v=[H,N]
    if T<n:v=v[::-1]
    while j<c:
     for x in z(r):g[x][j]=v[k%2]
     j+=d;k+=1
  elif a[1]==b[1]:
   j,L,H=a[1],a[0],a[2];X,N=b[0],b[2];d=abs(X-L)
   for x in z(c):g[L][x]=H;g[X][x]=N
   if d:
    i=X+d;k=0;v=[H,N]
    while i<r:
     for x in z(c):g[i][x]=v[k%2]
     i+=d;k+=1
  elif a[0]==0and b[0]==r-1:
   L,n,H=a;X,T,N=b;d=abs(T-n)
   for x in z(r):g[x][n]=H;g[x][T]=N
   if d:
    j=T+d;k=0;v=[H,N]
    while j<c:
     for x in z(r):g[x][j]=v[k%2]
     j+=d;k+=1
  elif(a[1]==0and b[1]==c-1)or(b[1]==0and a[1]==c-1):
   if a[1]==0:L,n,H=a;X,T,N=b
   else:L,n,H=b;X,T,N=a
   d=abs(X-L)
   for x in z(c):g[L][x]=H;g[X][x]=N
   if d:
    i=max(L,X)+d;k=0;v=[H,N]
    if X<L:v=v[::-1]
    while i<r:
     for x in z(c):g[i][x]=v[k%2]
     i+=d;k+=1
 return g