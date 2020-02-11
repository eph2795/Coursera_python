import sys

if __name__ == '__main__':
	s = sys.argv[1]
	print(sum([int(a) for a in s]))
