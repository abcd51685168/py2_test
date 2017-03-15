# coding=utf-8

import os
import time
import json
import codecs
import multiprocessing
from multiprocessing import cpu_count
from collections import Counter

import pefile

CPU_COUNT = cpu_count()
json_file = r"C:/tmp/dict_cnt.json"
filename_list = []
exe_path = r"C:/tmp/virus"
CNT = Counter()


# pe_info = pe.dump_dict()
# with codecs.open(json_file, "w", "utf-8") as report:
#     json.dump(pe_info, report, ensure_ascii=False, sort_keys=False, indent=4, encoding="utf-8")


# get dll and api function
def get_dll_func(filename):
    dll_func = set()
    try:
        pe = pefile.PE(filename)
        if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                if entry.dll:
                    dll = entry.dll.lower()
                    dll_func.add(dll)

                for imp in entry.imports:
                    if imp.name:
                        func = imp.name.lower()
                        dll_func.add(func)
                        # print(dll, func)

            CNT.update(dll_func)
    except:
        return


def list_files(path, depth=1):
    os.chdir(path)
    for obj in os.listdir(os.curdir):
        if os.path.isfile(obj):
            filename_list.append(os.getcwd() + os.sep + obj)
        if os.path.isdir(obj):
            if depth > 1:
                list_files(obj, depth - 1)
                os.chdir(os.pardir)


if __name__ == "__main__":
    lock = multiprocessing.Lock()
    cwd = os.getcwd()
    list_files(exe_path)
    os.chdir(cwd)

    start = time.time()
    # work_manager = WorkManager(filename_list)
    # work_manager.wait_allcomplete()

    pool = multiprocessing.Pool(processes=CPU_COUNT, maxtasksperchild=400)
    for i, filename in enumerate(filename_list):
        get_dll_func(filename)
        print(i, filename)
        # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
        # pool.apply_async(get_dll_func, (filename, lock))
    # pool.close()
    # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    # pool.join()
    end = time.time()
    print("cost all time: %s seconds." % (end - start))
    # print(CNT)
    with codecs.open(json_file, "w", "utf-8") as report:
        json.dump(CNT, report, ensure_ascii=False, sort_keys=False, indent=4, encoding="utf-8")
