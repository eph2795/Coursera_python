import os
import tempfile
import argparse
import json


if __name__ == '__main__':
	storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
	parser = argparse.ArgumentParser()
	parser.add_argument('--key', type=str, default=None)
	parser.add_argument('--val', type=str, default=None)

	args = parser.parse_args()
	if os.path.exists(storage_path):
		with open(storage_path, 'r') as f:
			storage_content = f.read()
			j = json.loads(storage_content)
	else:
		j = dict()

	if args.key and args.val:
		if args.key in j:
			j[args.key].append(args.val)
		else:
			j[args.key] = [args.val]

		with open(storage_path, 'w') as f:
			json.dump(j, f)
	else:
		if args.key:
			val = j.get(args.key, ['None'])
			print(', '.join(val))
		else:
			raise Exception('Wrong arguments!')

