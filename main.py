from scipy.stats import poisson
import numpy as np

N = 10000  # количество людей

lambda_tau = 5  # среднее время прихода человека
mu1_tau = 10  # средняя обработка запроса процессора
mu2_tau = 10

# Пуассоном заполняем 3 списка
lambda_array = poisson.rvs(lambda_tau, size=N)
mu1_array = poisson.rvs(mu1_tau, size=N)
mu2_array = poisson.rvs(mu2_tau, size=N)

total_time = np.sum(lambda_array)  # общее время - Т

# время работы каждого процессора
processor1_mu1 = []
processor2_mu2 = []

# указатели
current_time = 0
current_processor1_time = 0
current_processor2_time = 0

queue = 0  # отказы

# распределение людей по id
person_id = 0
id_processor1 = []
id_processor2 = []
id_queue = []

#________________________________________________
# Получаем списки людей и времени работы каждого процессора + отказы

for i in range(N):
  current_time += lambda_array[i]  # делаем шаг по лямбде
  person_id += 1  # id конкретного человека

  if current_processor1_time <= current_time:  # если указатель меньше настоящего времени
    processor1_mu1.append(mu1_array[i])  # записываем время работы
    id_processor1.append(person_id)  # записываем id человека
    current_processor1_time = current_time + mu1_array[i]  # обновляем указатель

  elif current_processor2_time <= current_time:
    processor2_mu2.append(mu2_array[i])
    id_processor2.append(person_id)
    current_processor2_time = current_time + mu2_array[i]

  else:  # если все уазатели больше чем настоящее время то отказываеем
    id_queue.append(person_id)
    queue += 1

#________________________________________________
total_time = max(current_processor1_time, current_processor2_time)  # находим общее время T вместе с самым большим временем последней работы процессоров

# списки для обозначения работы и отдыха процессоров (1 и 0)
work_mark_processor1 = [0 for i in range(total_time)]
work_mark_processor2 = [0 for i in range(total_time)]
#________________________________________________
# Получаем заполненные списки с состоянием процессоров

# указатели
current_time = 0
next_time = 0
for i in range(1, N+1):
  current_time += lambda_array[i-1]
  next_time += lambda_array[i-1]

  if i in id_processor1:  # если конкретный человек в списке этого процессора
    next_time += mu1_array[i-1]  # прибавляем ко второму указателю время работы
    for j in range(current_time-1, next_time):
      work_mark_processor1[j] = 1
    next_time -= mu1_array[i-1]

  elif i in id_processor2:
    next_time += mu2_array[i-1]
    for j in range(current_time-1, next_time):
      work_mark_processor2[j] = 1
    next_time -= mu2_array[i-1]
#________________________________________________

# счетчики
s_processor1 = 0
s_processor2 = 0
s_processor0 = 0

for i in range(total_time):
  if (work_mark_processor1[i] == 1 and work_mark_processor2[i] == 0) or (work_mark_processor1[i] == 0 and work_mark_processor2[i] == 1):
    s_processor1 += 1
  elif work_mark_processor1[i] == 1 and work_mark_processor2[i] == 1:
    s_processor2 += 1
  else:
    s_processor0 += 1
#________________________________________________
# Считааем вероятности

P1 = s_processor1 / total_time
P2 = s_processor2 / total_time
P0 = s_processor0 / total_time

avg_queue = queue / total_time  # в среднем отказываеют

#________________________________________________
# print(work_mark_processor1)
# print(work_mark_processor2)
print('_' * 70)
print('Общее время:', total_time)
print('Промежутки прихода людей:', lambda_array)
print()
print('Первый процессор работал времени:', s_processor1)
print('Первый процессор взял людей под №', id_processor1)
print('Первый процессор работал с каждым человеком (по времени):', processor1_mu1)
print('Вероятность работы первого процессора P1:', P1)
print()
print('Второй процессор работал времени:', s_processor2)
print('Второй процессор взял людей под №', id_processor2)
print('Второй процессор работал с каждым человеком (по времени):', processor2_mu2)
print('Вероятность работы второго процессора P2:', P2)
print()
print('Вероятность бездействия P0:', P0)
print()
print('Отказов:', s_processor0)
print('Было отказано людям с №', id_queue)
print('Вероятность отказа:', avg_queue)
print('')
print('Общая вероятность P0+P1+P2 = ', P0+P1+P2)
print('_' * 70)