package com.hl.concurrent;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

public class ReentrantLock_ConditionTest {

	public static void main(String[] args) {
		
	}

}

/**
 * 用synchronized+wait notify实现的生产者消费者.
 * 当多个线程在执行set/get方法时由于某种原因(容器空了或满了)调用了wait从而进入当前对象的阻塞队列中，线程被阻塞。
 * 在这个实现中只有一个线程阻塞队列，其中既有做get数据的线程(容器空，不能取),也有做set数据的线程(容器满，不能放)。
 * 当某个活跃的线程执行了notify/notifyAll的时候，所有的阻塞线程都(可能)被激活。事实上这是很低效的，因为：
 * 当某个活跃的set线程执行了notify，那么只应该激活某个(或全部)get数据的线程；
 * 反之，当某个活跃的get线程执行了notify，那么只应该激活某个(或全部)set数据的线程。
 * @author hanl1   keepintouch_lei@163.com
 *
 */
class Synchronized_Producer_Consumer {

	private List<Integer> container = new ArrayList<Integer>();

	private boolean isFull() {
		return this.container.size() >= 10;
	}

	private boolean isEmpty() {
		return this.container.size() == 0;
	}

	public synchronized int get() throws InterruptedException {
		while (this.isEmpty()) {
			this.wait();
		}
		int ret = this.container.remove(this.container.size() - 1);
		this.notifyAll();
		return ret;
	}

	public synchronized void set(int val) throws InterruptedException {
		while (this.isFull()) {
			this.wait();
		}
		this.container.add(val);
		this.notifyAll();
	}

}

/**
 * 用ReentrantLock和condition实现的生产者消费者.  比前一种实现方式(wait+notify)性能更好！
 * 使用ReentrantLock和两个condition，两个condition分别对应get和set阻塞队列。
 * 当活跃的线程读取数据(get)时，要么被阻塞在get_condition上(因为没有可用的数据)；要么读取数据成功然后通知set_condition上阻塞的线程可以继续set数据。
 * 反之，活跃线程set数据时亦然。
 * @author hanl1
 *
 */
class Lock_Condition_Producer_Consumer {
	
	private List<Integer> container = new ArrayList<Integer>();
	
	private final ReentrantLock lock = new ReentrantLock();
	
	private final Condition get_condition = lock.newCondition();
	private final Condition set_condition = lock.newCondition();
	
	private boolean isFull() {
		return this.container.size() >= 10;
	}

	private boolean isEmpty() {
		return this.container.size() == 0;
	}
	
	public int get() throws InterruptedException{
		lock.lock();
		try{
			while(this.isEmpty()){
				get_condition.await();
			}
			int ret = this.container.remove(this.container.size()-1);
			set_condition.signalAll();
			return ret;
		}finally{
			lock.unlock();
		}
	}

	public void set(int val) throws InterruptedException{
		this.lock.lock();
		try{
			while(this.isFull()){
				set_condition.await();
			}
			this.container.add(val);
			this.get_condition.signalAll();
		}finally{
			this.lock.unlock();
		}
	}
	
	
}







