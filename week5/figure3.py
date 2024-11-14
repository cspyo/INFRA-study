import matplotlib.pyplot as plt
import numpy as np

# kill되지 않은 경우와 kill된 경우의 데이터
acks = ['0', '1', 'all']
produce_count_no_kill = [1389883, 234180, 158171]
avg_no_kill = [3.7911158890736096e-05, 0.000249049256100216, 0.0003624987353069431]
produce_count_kill = [1374746, 226758, 143936]
avg_kill = [3.346063342618942e-05, 0.0002464525585561093, 0.00040166363080324944]

# 막대 너비
bar_width = 0.35
index = np.arange(len(acks))

# 그래프 설정
fig, ax1 = plt.subplots(figsize=(10, 6))

# kill되지 않은 경우 데이터
bar1 = ax1.bar(index - bar_width/2, produce_count_no_kill, bar_width, color='skyblue', label='No Kill')
# kill된 경우 데이터
bar2 = ax1.bar(index + bar_width/2, produce_count_kill, bar_width, color='lightgreen', label='Kill')

# 첫 번째 y 축 레이블
ax1.set_ylabel('Message Count')
ax1.set_xlabel('acks')
ax1.set_title('Comparison of Message Count and Avg Response Time (Leader Broker Kill vs No Kill)')
ax1.set_xticks(index)
ax1.set_xticklabels(acks)

# 두 번째 y 축 (오른쪽)
ax2 = ax1.twinx()
ax2.plot(index, avg_no_kill, color='orange', marker='o', linestyle='-', linewidth=2, label='Avg Response Time (No Kill)')
ax2.plot(index, avg_kill, color='red', marker='o', linestyle='-', linewidth=2, label='Avg Response Time (Kill)')
ax2.set_ylabel('Average Response Time (s)')

# 범례 설정
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

# 그래프 출력
plt.tight_layout()
plt.show()
