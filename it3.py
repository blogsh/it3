from numpy import *
import matplotlib.pyplot as plt
import copy
import sys

if sys.version_info < (3, 0, 0):
	print("Python3 required")

def fsa(n):
	A = 1
	B = 2
	C = 3

	state = random.choice([A, B, C])

	for _ in range(n):
		if state == A:
			state = B
			yield 1
		elif state == B:
			if random.random() < 0.5:
				yield 0
			else:
				state = C
				yield 1
		elif state == C:
			state = A
			yield 1

def fsa2(n):
	for i in range(n):
		yield 1 - i % 2

def fsa3(n):
	for i in range(n):
		yield int(i % 4 < 2)

def fsa4(n):
	for i in range(n):
		yield int(i < 100)

def simulate():
	cols = 400
	rows = 200

	grid = zeros((rows, cols))
	grid[0, :] = [x for x in fsa2(cols)]
	grid = grid.astype(uint8)

	def rule(x):
		triplet = ''.join([str(xi) for xi in x])
		
		if triplet in ['110', '100', '000']: return 0
		return 1

	for t in range(1, rows):
		for x in range(1, cols - 1):
			grid[t, x] = rule(grid[t-1, x-1:x+2])

	return grid

if __name__ == '__main__':
	plt.figure()

	res = simulate()

	n = res.shape[1]

	p01 = sum(res[0,:] < 0.5) / n
	p11 = sum(res[0,:] > 0.5) / n
	p02 = sum(res[1,:] < 0.5) / n
	p12 = sum(res[1,:] > 0.5) / n
	p03 = sum(res[2,:] < 0.5) / n
	p13 = sum(res[2,:] > 0.5) / n

	print('Initial Distribution:', p01, p11)
	print('After 1 step:', p02, p12)
	print('After 2 steps:', p03, p13)

	plt.pcolor(res, cmap=plt.cm.binary)
	plt.gca().invert_yaxis()

	S0 = p01 * log2(1/p01) + p11 * log2(1/p11)
	S1 = p02 * log2(1/p02) + p12 * log2(1/p12)
	S2 = p03 * log2(1/p03) + p13 * log2(1/p13)

	plt.title('$S_0 = %.2f,\ \ S_1 = %.2f,\ \ S_2 = %.2f$' % (S0, S1, S2))

	plt.show()
