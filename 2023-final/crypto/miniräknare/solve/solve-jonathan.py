with open("output.txt", "r") as data:
    e = int(data.readline().split(" = ")[1].strip())
    n = int(data.readline().split(" = ")[1].strip())
    c = int(data.readline().split(" = ")[1].strip())

# c = modp(m, 3, n)
# c = m*m*m*1 // 100 * n
# m**3 ≈ c * 100 / n

m_cubed = c * 100 // n

m_approx = m_cubed ** (1/3)

# Find exact value with Newton's method
m_guess = int(m_approx)

for i in range(10):
    m_guess = (2 * m_guess + m_cubed // m_guess**2) // 3

m_guess += 1 # mjau mjau mjau
print(m_guess.to_bytes(64, "big").lstrip(b"\x00").decode())
