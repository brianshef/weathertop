import argparse

from weathertop import app


_description = '''
An experimental early-warning system to be used with the game Foxhole. Named after the famous, ancient watchtower in Lord of the Rings.
'''
_epilog = '''
Best invoked like pipenv run python main.py OR
make run
'''
_defaultSourceDir = './assets'


def configure():
	parser = argparse.ArgumentParser(description=_description, epilog=_epilog)
	parser.add_argument('--source', '-s', default=_defaultSourceDir, required=False)
	return parser.parse_args()


def main():
	app.main(configure())


if __name__ == '__main__':
	main()

