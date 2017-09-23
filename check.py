import pypot.dynamixel
from math import degrees,atan,sqrt,acos,pi
import time


class Hand(object):
	def __init__(self) :
		self.l1=300.00
		self.l2=600.00
		#pygame.init() 
		#self.scr=pygame.display.set_mode((760,760))
		ports=pypot.dynamixel.get_available_ports()
		print(ports)
		if not ports :
			raise IOError("no ports found bruh!")

		print "Connecting to ",ports[0]

		self.dxl=pypot.dynamixel.DxlIO(ports[0])
		self.ids=self.dxl.scan(range(20))
		print self.ids
		#for i in self.ids:
		#	self.dxl.set_moving_speed({i:20})
		self.dxl.set_goal_position({self.ids[2]:-37})
		self.pen_down(False)
		self.circle()
		self.eye_lip()
		

	def circle(self):
		x=0.0
		flag=True
		self.pen_down(True)
		while x>=0:
			if x>=199.99:
				flag=False
			if not flag:
				x-=0.1
			else:
				x+=0.1
			#deg1=float(raw_input("angle1:"))
			#deg2=float(raw_input("angle2:"))
			#x=float(raw_input("x:"))
			#y=float(raw_input("y:"))
			try:
				if flag:
					y=700+self.sqrrt(200.0*x-x*x)
				else:
					y=700-self.sqrrt(200.0*x-x*x)
				self.move(x,y)
			except ValueError:
				pass
		self.pen_down(False)

	def eye_lip(self):
		x=31
		y=740
		time.sleep(1)
		self.move(30,740)
		self.pen_down(True)
		
		while x>30 and x<75:
			self.move(x,y)
			x = x+0.02
			print "abc"

		self.pen_down(False)
		
		y=740
		x=126
		self.move(125,740)
		self.pen_down(True)
		
		while x>125 and x<170:
			print "ac"
			self.move(x,y)
			x = x+0.02
		self.pen_down(False)
	
		y=660
		x=31
		self.move(30,660)
		self.pen_down(True)
		
		while x>30 and x<170:
			self.move(x,y)
			print "bc"
			x=x+0.02
		self.pen_down(False)

	def sqrrt(self,n):
		if n>0:
			return sqrt(n)
		elif n>-0.1:
			return 0
		else:
			raise ValueError('math domain error')

	def get_th(self,x,y):
			d1=float(atan(y/x))
			dist=float(sqrt(x*x+y*y))
			d2=float(acos((dist*dist + self.l1*self.l1 - self.l2*self.l2 )/(2*self.l1*dist)))
			th1=pi/2-(d1+d2)
			th2=pi-float(acos((self.l1*self.l1 + self.l2*self.l2 - dist*dist )/(2*self.l1*self.l2)))
			return (th1,th2)

	def move(self,x,y):
		print x,y
		th=self.get_th(x,y)
		print degrees(th[0]),degrees(th[1])
		self.dxl.set_goal_position({self.ids[0]:-degrees(th[0])})
		time.sleep(0.01)
		self.dxl.set_goal_position({self.ids[1]:-degrees(th[1])})
		time.sleep(0.01)

	def pen_down(self,down):
		if down:
			self.dxl.set_goal_position({self.ids[3]:154.42})
			self.dxl.set_moving_speed({self.ids[0]:1024})
			self.dxl.set_moving_speed({self.ids[1]:1024})
		else:
			self.dxl.set_goal_position({self.ids[3]:151})
			self.dxl.set_moving_speed({self.ids[0]:50})
			self.dxl.set_moving_speed({self.ids[1]:50})
	
h=Hand()
