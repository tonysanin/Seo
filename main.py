# coding: utf-8
import commands
import re
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from time import sleep, time
from datetime import datetime
from random import randint

proxies = []
threads_count = 0
tasks = -1

command = open("script.txt").readline()
if command.find("do (") != -1 and command.find (") times in (") != -1 and command.find(") threads"):
    tasks = re.findall("[(](\d+)[)]", command)[0]
    threads_count = re.findall("[(](\d+)[)]", command)[1]
else:
    print("Command do (x) times in (y) threads not found")
    exit(-1)
if int(threads_count) > int(tasks):
    print("Threads count must be less then tasks")
    exit(-1)


def MakeTask():
    with open("script.txt", encoding='utf-8') as f:
        for command in f:

            if command.find("do (") != -1 and command.find (") times in (") != -1 and command.find(") threads"):
                tasks = re.findall("[(](\d+)[)]", command)[0]
                threads_count = re.findall("[(](\d+)[)]", command)[1]

            if command.find("loadProxy()") != -1:
                lines = [line.rstrip('\n') for line in open('proxy.txt')]
                for line in lines:
                    proxies.append(line)

            if command.find("createBrowser(") != -1:
                params = str(re.findall("createBrowser\((.+)[\)]", command)).replace("['", '').replace("']", '')
                browser = commands.createBrowser(params, proxies)

            if command.find("findInGoogle(") != -1:
                params = str(re.findall("[\(\"](.*)[\)\"]", command)[0])
                if not commands.findInGoogle(browser, params):
                    return False

            if command.find("findInGoogleRandomQuery(") != -1:
                params = str(re.findall("[\(\"](.*)[\)\"]", command)[0])
                params = params.split(",")
                site = params[-1]
                params = params[:-1]
                rand = randint(0, len(params) - 1)
                params = str(params[rand].lstrip() + ',' + site)
                if not commands.findInGoogle(browser, params):
                    return False

            if command.find("wait(") != -1:
                params = int(re.findall("[\(\"](\d+)[\)\"]", command)[0])
                commands.wait(params)

            if command.find("scroll(") != -1:
                params = int(re.findall("[\(\"](.+)[\)\"]", command)[0])
                commands.scroll(browser, params)

            if command.find("clickOnElement(") != -1:
                params = str(re.findall("[\"](.+)[\"]", command)[0])
                commands.clickOnElement(browser, params)

            if command.find("openUrl(") != -1:
                params = str(re.findall("[\"](.+)[\"]", command)[0])
                commands.openUrl(browser, params)

            if command.find("closeBrowser()") != -1:
                print("close")
                browser.close()

            if command.find("makeScreenshot(") != -1:
                timestamp = datetime.timestamp(datetime.now())
                path = str(re.findall("[\"](.+)[\"]", command)[0] + " " + str(timestamp) + ".png")
                print(path)
                browser.save_screenshot(path)

    f.close()
    return True





MAX_WORKERS = int(threads_count)
TASK_COUNT = int(tasks)

def msg(text):
    if not hasattr(msg, 'lock'):
        msg.lock = Lock()
    with msg.lock:
        print(text)

def run_task(name, value):
    if MakeTask():
        return name, value // 5
    else:
        print("Remaking task")
        run_task(name, value)

def task_complete(task):
    name, res = task.result()
    elapsed = time() - start
    msg(f'+{elapsed:.2f}: {name} {res}')


if __name__ == '__main__':
    start = time()
    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    workers = []

    msg('creating tasks...')
    for i in range(TASK_COUNT):
        t = executor.submit(run_task, f'task{i}', i)
        t.add_done_callback(task_complete)
        workers.append(t)
        sleep(0.2)
    msg('done creating tasks')
    wait(workers)
    msg('done executing tasks')
    exit(0)
