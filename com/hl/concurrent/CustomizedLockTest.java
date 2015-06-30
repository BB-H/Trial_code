package com.hl.concurrent;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.locks.LockSupport;

/** 
* 自定义的独占锁，实现方式是乐观的 
*/  
class OptimisticExclusiveLock  {  
  
    /** 
     * 独占锁标记 true 锁不可用 false 锁可用 
     */  
    private AtomicBoolean occupied = new AtomicBoolean(false);  
    List<Thread>          queue = new ArrayList<Thread>();//阻塞队列  
  
    public boolean lock() {  
        if (!occupied.get()&&occupied.compareAndSet(false, true)) {//取锁成功不会阻塞，程序会继续执行  
            return true; // 利用CAS  
        } else {  
            queue.add(Thread.currentThread());//加入阻塞队列  
            LockSupport.park();//阻塞线程  
            return false;  
        }  
    }  
  
    public boolean unLock() {  
        if (occupied.get()) {  
            queue.remove(Thread.currentThread());//从队列里移除  
            if (occupied.compareAndSet(true, false)) {// 利用CAS  
                if(!queue.isEmpty()){  
                    LockSupport.unpark(queue.get(0));//唤醒第一个等待线程  
                }  
                return true;  
            }  
            return false;  
        } else {  
            return false;  
        }  
    }  
}  



  
/** 
* 独占锁测试 
* 此例子中对锁的使用方式仍然是悲观的，就像使用synchronized时一样。
*/  
public class CustomizedLockTest {  
  
    public static OptimisticExclusiveLock lock = new OptimisticExclusiveLock(); // 独占锁  
    public static volatile int            i    = 0;                            // 保证可见性  
  
    public class Task implements Runnable {  
  
        @Override  
        public void run() {  
            while (true) {  
                try {  
                    lock.lock();//加锁  
                    i += 2;  
                    System.out.println("thread name:" + Thread.currentThread().getName() + " i=" + i);  
                } finally {  
                    lock.unLock();//释放锁  
                    try {  
                        Thread.currentThread().sleep(10);  
                    } catch (InterruptedException e) {  
                        // TODO Auto-generated catch block  
                        e.printStackTrace();  
                    }  
                }  
            }  
        }  
    }  
  
    public void runTask() {  
        for (int i = 0; i < 100; i++) {  
            Thread t = new Thread(new Task(), "thread" + i);  
            t.start();  
        }  
    }  
  
    public static void main(String[] args) {  
    	CustomizedLockTest test = new CustomizedLockTest();  
        test.runTask();  
  
    }  
}  