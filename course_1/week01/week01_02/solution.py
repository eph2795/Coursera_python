import sys


if __name__ == '__main__':
	n = int(sys.argv[1])
	for i in range(n):
		print(' ' * (n - i - 1) + '#' * (i + 1))
