
import argparse

from .directory import directory, default_experiment

class Arguments(object):
	def parse():

		parser = argparse.ArgumentParser()

		parser.add_argument('--experiment', type=str, default=default_experiment, choices=directory.keys())

		parser.add_argument('--batch_size', type=int, default=16)
		parser.add_argument('--epochs', type=int, default=100)
		parser.add_argument('--random-seed', type=int, default=None)
		parser.add_argument('--verbose', type=int, default=0)

		parser.add_argument('--golden', action='store_true')
		parser.add_argument('--lazy', action='store_true')
		parser.add_argument('--load-weights', action='store_true')


		parser.add_argument('--output-dir', type=str, default="./output")
		parser.add_argument('--data-dir', type=str, default="./data")

		return parser.parse_args()