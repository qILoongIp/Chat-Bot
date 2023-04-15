import threading
import time

class MyThread(threading.Thread):
    def __init__(self, stop_event):
        threading.Thread.__init__(self)
        self.stop_event = stop_event

    def run(self):
        t1 = threading.Thread(target=self.run_1)
        t2 = threading.Thread(target=self.run_2)
        t1.start()
        t2.start()

    def run_1(self):
        while not self.stop_event.is_set():
            print("Thread_1 is running...")
            time.sleep(1)

        print("Thread_1 stopped.")

    def run_2(self):
        while not self.stop_event.is_set():
            print("Thread_2 is running...")
            time.sleep(1)

        print("Thread_2 stopped.")

if __name__ == '__main__':
    stop_event = threading.Event()
    print(stop_event.is_set())
    my_thread = MyThread(stop_event)
    my_thread.start()

    time.sleep(5)
    stop_event.set()
    print(stop_event.is_set())
