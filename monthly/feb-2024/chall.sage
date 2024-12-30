# kör sage online https://sagecell.sagemath.org/
# eller installera på linux/wsl https://repology.org/project/sagemath/versions
# eller på windows (om du måste) https://github.com/sagemath/sage-windows/releases
import struct
flag = b'SSM{[FLAG REDACTED!!!!]}'
mats = diagonal_matrix(struct.unpack('QQQ', flag))
A = random_matrix(ZZ, 3, 3, 'unimodular')
A *= mats*A**-1

print(A.trace())
A = 8*A**2 - 5*A + 16*A*A**-1
print(A.det())
A = 6*A**2 + 20*A - 3*A*A**-1
print(A.charpoly()[1])

# output:
# 19871028092746200562
# 31143324851076722529189336451008729704379858672550168591113427758662436634577754645297821879587920477504644205342388
# 2505012059114305215676710070948712689694988127376946853904378804219365586439603775933545874906865477558869980349977799844263386384888039947026300989062807975