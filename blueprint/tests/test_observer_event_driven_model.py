#!/usr/bin/env python3

class Observer:
    def __init__(self):
        self.last={}
    def emit(self,key,message,full=False):
        if not key or not message:
            return False
        if full:
            self.last[key]=message
            return True
        if self.last.get(key)==message:
            return False
        self.last[key]=message
        return True

def main():
    o=Observer()
    assert o.emit("N1|GBPUSD","A")
    assert not o.emit("N1|GBPUSD","A")
    assert o.emit("N1|GBPUSD","B")
    assert o.emit("D10A|GBPUSD","A")
    assert not o.emit("D10A|GBPUSD","A")
    assert o.emit("N1|GBPUSD","B",full=True)
    assert o.emit("N1|GBPUSD","B",full=True)
    print("OBSERVER_EVENT_DRIVEN_MODEL=PASS")

if __name__=="__main__":
    main()
