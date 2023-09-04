from threading import Thread
from queue import Queue
import time
import logging
import random
import mmap
import re
import os

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)
posts = []
BUF_SIZE = 500
q = Queue(BUF_SIZE)

class ProducerThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThread,self).__init__()
        self.target = target
        self.name = name
        self.fname = '../lichess_db_standard_rated_2016-11.pgn'
        self.chunkSize = 4096

    def run(self):
        try:
            fileEnd = os.path.getsize(self.fname)
            with open(self.fname, mode="r", encoding="utf-8") as file_obj:
                while file_obj:
                    if not q.full():
                        chunkEnd = file_obj.tell()
                        if chunkEnd < fileEnd:
                            chunkStart = chunkEnd
                            file_obj.seek(self.chunkSize, 0)
                            content = file_obj.read(self.chunkSize)
                            chunkEnd = file_obj.tell()
                            q.put(content)
                            file_obj.flush()
                        else:
                            mmap_obj.close()
                            break
        except IOError as io_err:
            print(io_err)
        return

class ConsumerThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread,self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        while True:
            if not q.empty():
                content = q.get()

                regex = r'\[Site\s\"\w+\S+\w+.\w+\/\S+'
                compiled_regex = re.compile(regex)
                re_result = compiled_regex.findall(content)
                for i in re_result:
                    r = re.findall("[a-zA-Z0-9]{8}", i)
                    if r:
                        posts.append(r[0])

                logging.debug('Getting files: ' + ' : ' + str(q.qsize()) + ' items in queue')
        return

def main():
    print(posts)


if __name__ == '__main__':

    p1 = ProducerThread(name='producer')
    c1 = ConsumerThread(name='consumer1')
    c2 = ConsumerThread(name='consumer1')
    c3 = ConsumerThread(name='consumer1')
    c4 = ConsumerThread(name='consumer1')
    c5 = ConsumerThread(name='consumer1')
    c6 = ConsumerThread(name='consumer1')
    c7 = ConsumerThread(name='consumer1')
    c8 = ConsumerThread(name='consumer1')
    c9 = ConsumerThread(name='consumer1')
    c10 = ConsumerThread(name='consumer1')
    c11 = ConsumerThread(name='consumer1')
    c12 = ConsumerThread(name='consumer1')

    p1.start()
    time.sleep(2)

    c1.start()
    c2.start()
    c3.start()
    c4.start()
    c5.start()
    c6.start()
    c7.start()
    c8.start()
    c9.start()
    c10.start()
    c11.start()
    c12.start()
    time.sleep(2)
    main()
