import java.util.Random;
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;



/**
 * 以一次田径比赛作为例子，演示CountdownLatch和CyclicBarrier的使用。
 * 场景描述：一组运动员在跑道上做准备，当所有运动员准备就绪则比赛开始；当所有运动员都跑完全程时比赛结束。
 * 用参赛运动员数目(integer n)作为参数创建CyclicBarrier实例。每个运动员在完成准备活动之后触发CyclicBarrier.await()并阻塞在此方法上，
 * 直到所有运动员都准备好（CyclicBarrier.await()被调用了n次），此时所有被阻塞的线程同时解除阻塞。所有运动员一起起跑。
 * 用参赛运动员数目(integer n)作为参数创建CountDownLatch实例。 每个运动员跑完全程后触发一个CountDownLatch.countDown()，
 * 当所有参赛运动员/线程都触发了countDown()方法，阻塞在CountDownLatch.await()上的赛事主办方/main线程宣布比赛结束。
 * @author hanl1
 *
 */
public class CountdownLatch_CyclicBarrierTest {

	public static void main(String[] args) throws InterruptedException {
		
		CyclicBarrier barrier = new CyclicBarrier(5, new Runnable() {
			
			//run方法中的代码会在所有被barrier.await()阻塞的线程解除阻塞之前的一刻被调用。
			@Override
			public void run() {
				System.out.println("All the players ready, GO!");
				
			}
		});
		CountDownLatch latch = new CountDownLatch(5);
		
		Racer r1 = new Racer(barrier,latch);
		Racer r2 = new Racer(barrier,latch);
		Racer r3 = new Racer(barrier,latch);
		Racer r4 = new Racer(barrier,latch);
		Racer r5 = new Racer(barrier,latch);
		
		System.out.println("Game START!");
		ExecutorService pool = Executors.newFixedThreadPool(5);
		pool.execute(r1);
		pool.execute(r2);
		pool.execute(r3);
		pool.execute(r4);
		pool.execute(r5);
		
		latch.await();
		System.out.println("Game OVER!");
		pool.shutdown();

	}

}

class Racer implements Runnable{
	
	private CyclicBarrier barrier;
	private CountDownLatch latch;

	public Racer(CyclicBarrier barrier,CountDownLatch latch) {
		this.barrier = barrier;
		this.latch = latch;
	}

	@Override
	public void run() {
		String racerName = Thread.currentThread().getName();
		System.out.println(racerName+" is preparing..");
		try {
			Thread.sleep(new Random().nextInt(500));
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		System.out.println(racerName+" is ready..");
		try {
			barrier.await();
		} catch (InterruptedException e) {
			e.printStackTrace();
		} catch (BrokenBarrierException e) {
			e.printStackTrace();
		}
		System.out.println(racerName+" is running..");
		try {
			Thread.sleep(new Random().nextInt(2000));
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.println(racerName+" is reached..");
		latch.countDown();
	}
	
}
