# We will do the imports required for this notebook here
# numpy provides import array and linear algebra utilities
import numpy as np
# the robotics toolbox provides robotics specific functionality
import roboticstoolbox as rtb
# spatial math provides objects for representing transformations
import spatialmath as sm
# arm ET
# arm ET

# E1 = rtb.ET.Rz()
# E2 = rtb.ET.tz(0.085)
# E3 = rtb.ET.Rx(-np.pi/2)
# E4 = rtb.ET.Rz()
# E41 = rtb.ET.Rz(np.pi/2)
# E5 = rtb.ET.tx(-0.095)
# E6 = rtb.ET.Rz()
# E7 = rtb.ET.tx(-0.095)
# E8 = rtb.ET.Rz()
# E81 = rtb.ET.Rz(-np.pi/2)
# E9 = rtb.ET.tx(-0.025)
# E10 = rtb.ET.Rx(np.pi/2)
# E11 = rtb.ET.Rz()
# E12 = rtb.ET.tz(0.175)

E1 = rtb.ET.Rz()
E2 = rtb.ET.Rz()
E3 = rtb.ET.Rx(-np.pi/2)
E4 = rtb.ET.Rz()
E5 = rtb.ET.tz(0.6)
E6 = rtb.ET.Rx(np.pi/2)
E7 = rtb.ET.Rz()
E8 = rtb.ET.tx(0.8)
arm = rtb.ETS([E1, E2, E3, E4, E5, E6, E7, E8])
t1 = rtb.ETS([E1])
t2 = rtb.ETS([E1,E2,E3])
t3 = rtb.ETS([E1,E2,E3,E4,E5,E6])
t4 = rtb.ETS([E1,E2,E3,E4,E5,E6,E7,E8])
print(arm)
# The ETS class has many usefull properties
# print the number of joints in the panda model
print(f"The arm has {arm.n} joints")

# print the number of ETs in the panda model
print(f"The arm has {arm.m} ETs")

# We can access an ET from an ETS as if the ETS were a Python list
print(f"The second ET in the ETS is {arm[1]}")

# When a variable ET is added to an ETS, it is assigned a jindex, which is short for joint index
# When given an array of joint coordinates (i.e. joint angles), the ETS will use the jindices of each
# variable ET to correspond with elements of the given joint coordiante array
print(f"The first variable joint has a jindex of {arm[0].jindex}, while the second has a jindex of {arm[3].jindex}")

# We can extract all of the variable ETs from the panda model as a list
print(f"\nAll variable liks in the arm ETS: \n{arm.joints()}")

# Using the above methodolgy, we can calculate the forward kinematics of our Panda model
# First, we must define the joint coordinates q, to calculate the forward kinematics at
q = np.array([np.deg2rad(30), np.deg2rad(25), np.deg2rad(15), np.deg2rad(50)])
Tep = arm.fkine(q)
Tep1 = t1.fkine(q)
Tep2 = t2.fkine(q)
Tep3 = t3.fkine(q)
Tep4 = t4.fkine(q)
print(f"Tep1: \n{Tep1}")
print(f"Tep2: \n{Tep2}")
print(f"Tep3: \n{Tep3}")
print(f"Tep4: \n{Tep4}")

# Note: The panda object which we have been using is an instance of the ETS class

# Calculate the world frame Jacobian using the ETS class
J0 = arm.jacob0(q)

# Calculate the end-effector frame Jacobian using the ETS class
Je = arm.jacobe(q)

# View our Jacobians
print(f"The manipulator Jacobian (world frame) is: \n{np.round(J0, 2)}")
print(f"\nThe manipulator Jacobian (end-effector frame) is: \n{np.round(Je, 2)}")

# Calculate the world frame Hessian using the ETS class
H0 = arm.hessian0(q)

# Calculate the end-effector frame Hessian using the ETS class
He = arm.hessiane(q)

# View our Hessians
print(f"The manipulator Hessian (world frame) is: \n{np.round(H0, 2)}")
print(f"\nThe manipulator Hessian (end-effector frame) is: \n{np.round(He, 2)}")


ev = [0.1, 0.0, 0.0, 0.0, 0.0, 0.0]

dq = np.linalg.pinv(J0) @ ev

# Visualise the results
print("dq")
print(np.round(dq, 4))

print("inverse")
print(arm.ik_NR(Tep,q))
