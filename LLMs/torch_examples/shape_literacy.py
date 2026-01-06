import torch

x = torch.randn(10)
y = x.unsqueeze(1)
print(x.shape,y.shape)

x = torch.randn(4, 1, 8)
y = x.squeeze()
print(x.shape,y.shape)

x = torch.randn(2,3,4)
print(x, x.shape)
# reshape to same number of elements, but different shape
y = x.view(12,2)
print(y, y.shape)
z = x.reshape(12,2)
print(z, z.shape)

x = torch.randn(5, 1)
z = x.expand(5,3)
print(x,y)
print(x.shape, z.shape)

# copies the data
y = x.repeat(1,3)
print(y)
print(y.shape)
y[0, 0] = 10
print("Y", y)


y2 = x.expand_as(torch.randn(5, 10))
# expanded size to match existing size at dim 0.
# expand doesn't allocate new memory, so changing y2 will change x
y3 = x.expand(5, 2)
y3[0, 0] = 20
print(y3)