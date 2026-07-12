import numpy as np


def count_max_length_runs(L: int):
	lst = np.random.randint(0, 2, L)
	i = 1
	num_runs = 0
	curr_max = 0
	run = 1

	while i < L:
		if lst[i] == lst[i-1]:
			run += 1
		else:
			# only update number of runs if run ends
			if run > curr_max:
				curr_max = run
				num_runs = 1
			elif run == curr_max:
				num_runs += 1
			run = 1
		i += 1
	if run > curr_max:
		curr_max = run
		num_runs = 1
	elif run == curr_max:
		num_runs += 1
	return num_runs

def count_num_runs(L: int):
	lst = np.random.randint(0,2,L)
	runs = 1
	for i in range(1, L):
		if lst[i] != lst[i-1]:
			runs += 1
	return runs

s = 0
s_count_runs = 0
for _ in range(10000):
	s += count_max_length_runs(100)
	s_count_runs += count_num_runs(100)
print(s/10000)
print(s_count_runs/10000)
