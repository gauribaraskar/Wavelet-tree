import matplotlib.pyplot as plt
import numpy as np

N = 6

naive_rank_times = []
jacobsons_rank_times = []

with open('time_naive.txt') as f:

    for i in range(N):
        time = f.readline()
        naive_rank_times.append(np.log(float(time)))

    for i in range(N):
        time = f.readline()
        jacobsons_rank_times.append(np.log(float(time)))

f.close()


fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(0, 10, 1)

#x = plt.gca()
#plt.gca().set_ylim()

ax.plot(naive_rank_times, color='blue', label='Naive rank')
ax.plot(jacobsons_rank_times, color='black', label='Jacobsons rank')

plt.show()
