f = open('name.txt','r')
file= f.read()
new= file.split('\n')
data = list(dict.fromkeys(new))
print('h')