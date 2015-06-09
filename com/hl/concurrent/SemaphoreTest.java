package com.hl.concurrent;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Semaphore;

public class SemaphoreTest {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}

/**
 * Semaphore可以用来控制对特定资源访问的并发线程数量。
 * 通过Semaphore.acquire()获得许可，通过Semaphore.release()释放许可。
 * 如果只获取(acquire)不释放(release)，则许可很快被耗尽，后续线程会被一直阻塞在Semaphore.acquire()上。
 * 
 * @author hanl1  keepintouch_lei@163.com
 *
 */
class MyObjPool{
	
	//既然是多线程并发访问(本例中限制并发数为5)资源对象，则资源对象本身需要是线程安全的.
	//本例中的pool对象可以创建为线程安全的集合， 也可以使用ArrayList等非线程安全的集合并通过代码来保证其线程安全性(访问pool时加synchronized或lock)。
	private List<Object> pool = Collections.synchronizedList(new ArrayList<Object>()) ;
	
	//访问本对象池的并发线程数设置为5
	private Semaphore semaphore = new Semaphore(5);
	
	public Object getObj() throws InterruptedException{
		semaphore.acquire();
		try{
			return pool.remove(pool.size()-1);
		}finally{
			semaphore.release();
		}
	}
	
	public void setObj(Object obj) throws InterruptedException{
		semaphore.acquire();
		try{
			pool.add(obj);
		}finally{
			semaphore.release();
		}
	}
}
