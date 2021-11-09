import numpy as np

def angle_cal(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    #vector_calculation
    v_1 = np.array([a[0]-b[0],a[1]-b[1]])
    v_2 = np.array([c[0]-b[0],c[1]-b[1]])
    
    #magnitude = np.linalg.norm(v_1)
    #a.b = a*b*cos(q) dot product
    
    cos_theta = np.dot(v_1,v_2)/(np.linalg.norm(v_1)*np.linalg.norm(v_2))
    angle_radian = np.arccos(cos_theta)
    angle = int(np.abs(angle_radian*57.2958))
    
    if angle >180.0:
            angle = 360-angle
            
    return angle