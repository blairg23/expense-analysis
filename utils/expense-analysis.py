import pandas as pd
import os
import calendar as cal
import numpy as np

month_names = [cal.month_name[i] for i in np.arange(1,13)]
months = pd.Series(np.arange(1,13), index=month_names)


def get_unique_types(dataframe=None):
	'''
	Get the unique types from the given dataframe.
	'''
	unique_types = set()
	for t in dataframe.Type:
		unique_types.add(t)
	return unique_types


def get_sum_dict(types=None, dataframe=None):
	'''
	Return a dict of sums, using the amounts from the dataframe.
	'''
	sum_dict = {}
	for type_string in types:
		sum_dict[str(type_string)] = round(dataframe.Amount[(dataframe.Type == type_string)].sum(), 2) # Round to 2 floating point digits
	return sum_dict


def process_csv(filename=None):
	'''
	Given the filename of a CSV, returns a dictionary of the expenses.
	'''
	expenses = pd.read_csv(os.path.join('../data', filename))
	
	types = get_unique_types(dataframe=expenses)
	return get_sum_dict(types=types, dataframe=expenses)


for filename in os.listdir('../data'):
	try:
		expenses = process_csv(filename=filename)
		stripped_filename = os.path.splitext(filename)[0]+'.txt'
		if not os.path.exists('../output'):
			os.makedirs('../output')
		with open(os.path.join('../output', stripped_filename), 'a+') as outfile:
			[outfile.write('{key}: {value}\n'.format(key=key, value=value)) for key, value in sorted(expenses.items())]
	except Exception as e:
		print('[ERROR]', e)