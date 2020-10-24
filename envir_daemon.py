# Automation to check environment
# notice: signal api cannot founded in windows OS
import psutil as ps
import sys, os, time, signal

class system_detect:
	# monitor pid
	# monitor resources: battery, memory, cpu
	# case 0: default setting
	# case 1: graceful killer start and save ckpt
	def __init__(self,
				 pid = None, 
				 limit_mem = 70,
				 limit_cpu = 90):
		self.pid = pid
		self.limit_mem = limit_mem
		self.limit_cpu = limit_cpu

	def _behavior(self):
		# battery code block
		try:
			battery_status = ps.sensors_battery().percent
			power_plug = ps.sensors_battery().power_plugged
		except:
			power_plug = ps.sensors_battery().power_plugged
		# memory code block
		total_mem = ps.virtual_memory().total
		ava_mem = ps.virtual_memory().available
		usage_mem = ava_mem / total_mem
		# cpu code block
		cpu_core = ps.cpu_percent(interval = 1, percpu = True)
		cpu_average = sum(cpu_core) / len(cpu_core)
		# behavior settings
		# with battery
		if battery_status != False and battery_status <= 40 and power_plug != True:
			if self.limit_mem >= int(85 - usage_mem) or self.limit_cpu >= int(100 - cpu_average):
				GracefulKiller(pid = self.pid)
				if self.limit_mem >= int(100 - usage_mem) or self.limit_cpu >= int(100 - cpu_average):
					return True
		# without battery
		elif power_plug != False:
			if self.limit_mem >= int(85 - usage_mem) or self.limit_cpu >= int(100 - cpu_average):
				GracefulKiller(pid = self.pid)
				if self.limit_mem >= int(100 - usage_mem) or self.limit_cpu >= int(100 - cpu_average):
					return True
		else:
			return False

class GracefulKiller:
	def __init__(self, pid = None):
		self.pid = pid
		signal.signal(signal.SIGINT, self.exit_gracefully)
		signal.signal(signal.SIGTERM, self.exit_gracefully)
	# call ckpt to do something
	def exit_gracefully(self,signum, frame):
		print('Signal handler called with signal', signum)
		raise OSError("System Loading too high!")


if __name__ == "__main__":
	# daemon start
	while True:
		while os.path.exists("./tmp/train_pid.txt"):
			f = open("./tmp/train_pid.txt", "r")
			pid = f.read()
			pid = pid.strip().split(" ")
			pid = pid[1]
			if ps.pid_exists(int(pid)) == False:
				print(str(time.asctime(time.localtime(time.time()))) + ": Waiting...")
				os.remove("./tmp/train_pid.txt")
				break
			elif ps.pid_exists(int(pid)) == True:
				print(str(time.asctime(time.localtime(time.time()))) + ": Daemon start monitoring!")
				# record
				with open("daemon_log.txt", "w") as wf:
					wf.write(str(time.asctime(time.localtime(time.time()))) + ": monitoring...\n")
			if system_detect(int(pid)) == True:
				print(str(time.asctime(time.localtime(time.time()))) + ": Unstable situation!\n")
				with open("daemon_log.txt", "a") as wf:
					wf.write(str(time.asctime(time.localtime(time.time()))) + ": Unstable situation!\n")
				os.kill(int(pid), signal.SIGTERM)
				break
			else: 
				print(str(time.asctime(time.localtime(time.time()))) + ": Stable, training task is running...\n")
				with open("daemon_log.txt", "a") as wf:
					wf.write(str(time.asctime(time.localtime(time.time()))) + ": Stable, training task is running...\n")
				break

		print(str(time.asctime(time.localtime(time.time()))) + ": monitoring...\n")
		with open("daemon_log.txt", "a") as wf:
			wf.write(str(time.asctime(time.localtime(time.time()))) + ": monitoring...\n")
		time.sleep(10)
