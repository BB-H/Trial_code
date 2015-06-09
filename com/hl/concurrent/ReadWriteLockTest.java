package com.hl.concurrent;

import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class ReadWriteLockTest {

	public static void main(String[] args) {

	}

}


/**
 * 用ReadWriteLock来实现线程安全的共享数据访问。
 * 相比于使用synchronized来保证线程安全，使用ReadWriteLock可以免除不必要的互斥，从而提升线程的并发性。
 * 对共享数据的访问需要实现互斥，若使用synchronized关键字，则会实现如下互斥：(1).写与写之间的互斥；(2).读与写之间的互斥；(3).读与读之间的互斥。
 * 事实上以上(3)完全是多余不必要的，多个线程的读操作之间不存在线程安全问题，因此不需要互斥。
 * ReadWriteLock正是用来解决这个问题的，它可以实现以上(1),(2)而忽略(3).
 * 对于并发读非常多而写比较少的场景，使用ReadWriteLock可以明显提高性能.
 * @author hanl1   keepintouch_lei@163.com
 *
 */
class ThreadSafedFlag{
	
	private boolean flag = false;
	
	private final ReadWriteLock lock = new ReentrantReadWriteLock();
	
	
	public boolean getFlag(){
		//用readLock保护数据读取的操作
		lock.readLock().lock();
		try{
			return flag;
		}finally{
			lock.readLock().unlock();
		}
	}
	
	public void setFlag(boolean flag){
		//用writeLock保护数据写入的操作
		lock.writeLock().lock();
		try{
			this.flag = flag;
		}finally{
			lock.writeLock().unlock();
		}
	}
}
