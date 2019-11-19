import os


def run():
    os.system('redis-server redis.windows.conf')

if __name__ == '__main__':
    run()