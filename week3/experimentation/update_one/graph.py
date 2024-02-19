import pandas as pd
import matplotlib.pyplot as plt

# 데이터를 DataFrame으로 읽어오기

df = pd.read_csv('./update_one.csv')

# 막대 그래프 그리기
plt.figure(figsize=(10, 6))
plt.bar(df['DB'], df['Time'], color='skyblue')
plt.xlabel('Database')
plt.ylabel('Time (seconds)')
plt.title('UPDATE passenger SET name = :name WHERE id = :id')
plt.show()
