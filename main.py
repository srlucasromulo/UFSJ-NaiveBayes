import pandas as pd


df = pd.read_csv('dataset.csv')
entry = pd.read_csv('entry.csv')
# rows, columns = df.shape
index = df.columns


if __name__ == '__main__':

	count_x = {i: None for i in index[1:]}
	for i in index[1:]:
		count_x[i] = df[i].value_counts().to_dict()
	count_y = df[index[0]].value_counts().to_dict()

	# class probability
	probabilities_y = df[index[0]].value_counts(normalize=True).to_dict()

	# xij probability
	probabilities_x = {i: {} for i in index[1:]}
	for i in index[1:]:
		for key in count_x[i].keys():
			probabilities_x[i].update({key: {}})
			for y in count_y.keys():
				prop = count_x[i][key] / count_y[y]
				prop = prop if prop < 1 else 1	# probability max = 1
				probabilities_x[i][key].update({y: prop})

	# classify entries
	for row in entry.iloc:
		result_entry = row[index[0]]
		result = {}
		for y in count_y.keys():
			result.update({y: None})
			calc = 1
			for i in index[1:]:
				calc *= probabilities_x[i][row[i]][y]
			result[y] = calc
		print(result)

	# for row in entry.itertuples(index=True):
	# 	print(type(row['age']))

	## just a remider
	# querys
	# data = df.loc[(df['Contact-lenses']=='soft') & (df['age']=='young')]
	# print(data)
