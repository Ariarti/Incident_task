import pandas as pd
import re


def comparison_incidents(w_file, dt, r_file):
    """ Создаёт .csv файл со столбцами инцидентов(id) и числом идентичных инцидентов(count) 
        по категориальным признакам, и заданной разнице по времени """

    pattern_w_file = r"\w+[.]{1}csv"
    pattern_r_file = r".+[.]{1}csv"
    if not re.match(pattern_w_file, w_file):
        print("Неверное имя выходного файла!")
    elif not re.match(pattern_r_file, r_file):
        print("Неверный формат входного файла!")
    else:
        try:
            dt = abs(float(dt))
            with open(r_file) as f:
                d = dict()
                for line in f:
                    line = line.rstrip()
                    s = line.split(",")
                    if len(s) != 4:
                        continue
                    # Записываем в словарь в качестве ключа строку со значениями 
                    # категориальных признаков, а в качестве значений кортеж
                    # со значением id и времени
                    try:
                        if str(s[1:-1]) not in d:
                            d[str(s[1:-1])] = list()
                            d[str(s[1:-1])].append((int(s[0]), float(s[3])))
                        else:
                            d[str(s[1:-1])].append((int(s[0]), float(s[3])))
                    except ValueError:
                        continue
        except FileNotFoundError:
            print("Такого файла не существует!")
        except ValueError:
            print("Неверный фомат dt")
        else:
            # Проходим по всем ключам d, если ключ содержит только одно значение, то
            # данный id не имеет пар.
            di = dict()
            for i in d:
                if len(d[i]) == 1:
                    di[d[i][0][0]] = 0
                else:
                    for k in d[i]:
                        for k1 in d[i]:
                            if 0 < (k[1] - k1[1]) < dt:
                                if k[0] not in di:
                                    di[k[0]] = 1
                                else:
                                    di[k[0]] += 1
                            else:
                                if k[0] not in di:
                                    di[k[0]] = 0

            dp = pd.DataFrame(di.items(), index=di.keys(), columns=['id', 'count'])
            dp.sort_index(inplace=True)
            dp.to_csv(w_file, index=False)
            print("The " + w_file + " file was created!")


if __name__ == "__main__":
    r_file = input("input file: ")
    w_file = input("output file: ")
    d_time = input("dtime: ")
    comparison_incidents(w_file, d_time, r_file)