import numpy as np

label = np.array([1,2,3,4,5,6,7,8,9,10])
nums = np.array([[1,2,3,4,5,6,7,8,9,10],
                 [4,3,5,6,8,9,1,2,1,8]])

mask = (label >= 3) & (label <= 8)

print(mask)
print(nums[:, 0])

print(nums[1] - label[4])