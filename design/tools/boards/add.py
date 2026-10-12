import json,sys
k,name,x,h,title=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]
p='root/project/canvas.json'
c=json.load(open(p))
c['boards'][name]={"x":x,"y":0,"w":1440,"h":h,"title":title,"expand":"fill"}
if name not in c['order']: c['order'].append(name)
json.dump(c,open(p,'w'),indent=2)
