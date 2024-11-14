import matplotlib.pyplot as plt
import numpy as np

# 데이터
acks = ['0', '1', 'all']
produce_count_kill_3 = [1374746, 226758, 143936]
avg_kill_3 = [3.346063342618942e-05, 0.0002464525585561093, 0.00040166363080324944]
produce_count_kill_7 = [1040860, 167860, 120732]
avg_kill_7 = [5.228547087145047e-05, 0.00034475541577838565, 0.00047948147720313153]

# 막대 너비
bar_width = 0.35
index = np.arange(len(acks))

# 그래프 설정
fig, ax1 = plt.subplots(figsize=(10, 6))

# 브로커 3개 kill된 경우 데이터
bar1 = ax1.bar(index - bar_width/2, produce_count_kill_3, bar_width, color='skyblue', label='Broker 3')
# 브로커 7개 kill된 경우 데이터
bar2 = ax1.bar(index + bar_width/2, produce_count_kill_7, bar_width, color='lightgreen', label='Broker 7')

# 첫 번째 y 축 레이블
ax1.set_ylabel('Message Count')
ax1.set_xlabel('acks')
ax1.set_title('Comparison of Message Count and Avg Response Time (Broker Kill with Different Broker Counts)')
ax1.set_xticks(index)
ax1.set_xticklabels(acks)

# 두 번째 y 축 (오른쪽)
ax2 = ax1.twinx()
ax2.plot(index, avg_kill_3, color='orange', marker='o', linestyle='-', linewidth=2, label='Avg Response Time (Broker 3)')
ax2.plot(index, avg_kill_7, color='red', marker='o', linestyle='-', linewidth=2, label='Avg Response Time (Broker 7)')
ax2.set_ylabel('Average Response Time (s)')

# 범례 설정
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

# 그래프 출력
plt.tight_layout()
plt.show()
