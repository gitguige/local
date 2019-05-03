import os
import csv


def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def main():
    with open('result_summary.csv', 'w') as write_summary:
        write_summary.write('Scenario#,Fault#,Fault-line,Alerts,Hazards,T1,T2,T3\n')
    write_summary = open('result_summary.csv', 'a')

    with open('fault_list.txt', 'r') as read_file:
        for line in read_file:
            line = line.replace('\n', '')
            scene_num = line.split('_')
            print scene_num[0]
            
            file_name = '../' + line + '/' + 'summary.csv'
            with open(file_name, 'r') as summ_file:
                summ_file.readline()
                for lines in summ_file:
                    write_summary.writelines(lines)

    write_summary.close()



if __name__ == '__main__':
    #vision_summary()
    main()


