import matplotlib.pyplot as plt
import numpy as np

# 브로커 3개와 7개일 때의 데이터
acks = ['0', '1', 'all']
produce_count_3 = [1389883, 234180, 158171]
avg_3 = [3.7911158890736096e-05, 0.000249049256100216, 0.0003624987353069431]
produce_count_7 = [1087695, 176514, 135134]
avg_7 = [4.961116912591948e-05, 0.00032707335276103234, 0.00042833968332517527]

# 막대 너비
bar_width = 0.35
index = np.arange(len(acks))

# 그래프 설정
fig, ax1 = plt.subplots(figsize=(10, 6))

# 브로커 3개 데이터
bar1 = ax1.bar(index - bar_width/2, produce_count_3, bar_width, color='skyblue', label='Broker 3')
bar2 = ax1.bar(index + bar_width/2, produce_count_7, bar_width, color='lightgreen', label='Broker 7')

# 첫 번째 y 축 레이블
ax1.set_ylabel('Message Count')
ax1.set_xlabel('acks')
ax1.set_title('Comparison of Message Count and Avg Response Time')
ax1.set_xticks(index)
ax1.set_xticklabels(acks)

# 두 번째 y 축 (오른쪽)
ax2 = ax1.twinx()
ax2.plot(index, avg_3, color='orange', marker='o', linestyle='-', linewidth=2, label='Avg Response Time (Broker 3)')
ax2.plot(index, avg_7, color='red', marker='o', linestyle='-', linewidth=2, label='Avg Response Time (Broker 7)')
ax2.set_ylabel('Average Response Time (s)')

# 범례 설정
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')

# 그래프 출력
plt.tight_layout()
plt.show()
