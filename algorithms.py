import numpy as np
from mat import mat
from utils import in_half_plane, s_norm, Rz, angle, i2p
import math as m


class Algorithms:
    def __init__(self):
        print("WE HAVE INITIALIZED THE ALGY CLASS!!")
        self.i = 0
        self.state = 0

    def pathFollower(self, flag, r, q, p, chi, chi_inf, k_path, c, rho, lamb, k_orbit):
        """
        Input:
            flag = 1 for straight line, 2 for orbit
            r = origin of straight-line path in NED (m)
            q = direction of straight-line path in NED (m)
            p = current position of uav in NED (m)
            chi = course angle of UAV (rad)
            chi_inf = straight line path following parameter
            k_path = straight line path following parameter
            c = center of orbit in NED (m)
            rho = radius of orbit (m)
            lamb = direction of orbit, 1 clockwise, -1 counter-clockwise
            k_orbit = orbit path following parameter

        Outputs:
            e_crosstrack = crosstrack error (m)
            chi_c = commanded course angle (rad)
            h_c = commanded altitude (m)

        Example Usage
            e_crosstrack, chi_c, h_c = pathFollower(path)

        Reference: Beard, Small Unmanned Aircraft, Chapter 10, Algorithms 3 and 4
        Copyright 2018 Utah State University
        """

        if flag == 1:  # straight line
            pass
            # print(r)
            # print(r.shape)
            # print(q)
            # print(q.shape)
            # print(p)
            # print(p.shape)
            # print(c)
            # print(c.shape)
            # TODO Algorithm 3 goes here
            chi_q = float(m.atan2(q[1],q[0]))
            e_p_i = p - r
            k = np.array([[0],[0],[1]])
            n_cross = np.cross(q,k,axis=0)
            n = n_cross / (np.linalg.norm(n_cross))
            s_i = e_p_i - (float(np.dot(e_p_i.T,n)) * (n))

            qs = float(q[2] / np.sqrt((q[0]**2) + (q[1]**2)))
            h_c = float((-r[2]) - (np.sqrt((s_i[0]**2) + (s_i[1]**2)) * qs))

            if (chi_q - chi < -np.pi):
                chi_q = (chi_q + (2*np.pi))
            if (chi_q - chi > np.pi):
                chi_q = (chi_q - (2*np.pi))

            e_crosstrack = float((-np.sin(chi_q)*(p[0]-r[0]))  + (np.cos(chi_q)*(p[1]-r[1])))
            chi_c = chi_q - ( chi_inf * (2/np.pi) * np.arctan(k_path * e_crosstrack) )

        elif flag == 2:  # orbit following
            pass

            # TODO Algorithm 4 goes here
            # flag, r, q, p, chi, chi_inf, k_path, c, rho, lamb, k_orbit
            h_c = -(c[2])
            d = float(np.sqrt( ((p[0] - c[0])**2) + ((p[1] - c[1])**2) ))
            phi = m.atan2( (p[1] - c[1]) , (p[0] - c[0]) )

            if (phi - chi < -np.pi):
                phi = (phi + (2*np.pi))
            if (phi - chi > np.pi):
                phi = (phi - (2*np.pi))
            
            e_crosstrack = d - rho
            chi_c = phi + (lamb * ( (np.pi/2) + (np.arctan(k_orbit * ((d - rho) / rho) )) ))

        else:
            raise Exception("Invalid path type")

        return e_crosstrack, chi_c, h_c

    # followWpp algorithm left here for reference
    # It is not used in the final implementation
    def followWpp(self, w, p, newpath):
        """
        followWpp implements waypoint following via connected straight-line
        paths.

        Inputs:
            w = 3xn matrix of waypoints in NED (m)
            p = position of MAV in NED (m)
            newpath = flag to initialize the algorithm or define new waypoints

        Outputs
            r = origin of straight-line path in NED (m)
            q = direction of straight-line path in NED (m)

        Example Usage;
            r, q = followWpp(w, p, newpath)

        Reference: Beard, Small Unmanned Aircraft, Chapter 11, Algorithm 5
        Copyright 2018 Utah State University
        """

        if self.i is None:
            self.i = 0

        if newpath:
            # initialize index
            self.i = 1

        # check sizes
        m, N = w.shape
        assert N >= 3
        assert m == 3

        # calculate the q vector
        r = w[:, self.i - 1]
        qi1 = s_norm(w[:, self.i], -w[:, self.i - 1])

        # Calculate the origin of the current path
        qi = s_norm(w[:, self.i + 1], -w[:, self.i])

        # Calculate the unit normal to define the half plane
        ni = s_norm(qi1, qi)

        # Check if the MAV has crossed the half-plane
        if in_half_plane(p, w[:, self.i], ni):
            if self.i < (N - 2):
                self.i += 1
        q = qi1

        return r, q

    # followWppFillet algorithm left here for reference.
    # It is not used in the final implementation
    def followWppFillet(self, w, p, R, newpath):
        """
        followWppFillet implements waypoint following via straightline paths
        connected by fillets

        Inputs:
            W = 3xn matrix of waypoints in NED (m)
            p = position of MAV in NED (m)
            R = fillet radius (m)
            newpath = flag to initialize the algorithm or define new waypoints

        Outputs
            flag = flag for straight line path (1) or orbit (2)
            r = origin of straight-line path in NED (m)
            q = direction of straight-line path in NED (m)
            c = center of orbit in NED (m)
            rho = radius of orbit (m)
            lamb = direction or orbit, 1 clockwise, -1 counter clockwise

        Example Usage
            [flag, r, q, c, rho, lamb] = followWppFillet( w, p, R, newpath )

        Reference: Beard, Small Unmanned Aircraft, Chapter 11, Algorithm 6
        Copyright 2018 Utah State University
        """

        if self.i is None:
            self.i = 0
            self.state = 0
        if newpath:
            # Initialize the waypoint index
            self.i = 2
            self.state = 1

            # Check size of waypoints matrix
            m, N = w.shape  # Where 'N' is the number of waypoints and 'm' dimensions
            assert N >= 3
            assert m == 3
        else:
            [m, N] = w.shape
            assert N >= 3
            assert m == 3
        # Calculate the q vector and fillet angle
        qi1 = mat(s_norm(w[:, self.i], -w[:, self.i - 1]))
        qi = mat(s_norm(w[:, self.i + 1], -w[:, self.i]))
        e = acos(-qi1.T * qi)

        # Determine if the MAV is on a straight or orbit path
        if self.state == 1:
            c = mat([0, 0, 0]).T
            rho = 0
            lamb = 0

            flag = 1
            r = w[:, self.i - 1]
            q = q1
            z = w[:, self.i] - (R / (np.tan(e / 2))) * qi1
            if in_half_plane(p, z, qi1):
                self.state = 2

        elif self.state == 2:
            r = [0, 0, 0]
            q = [0, 0, 0]

            flag = 2
            c = w[:, self.i] - (R / (np.sin(e / 2))) * s_norm(qi1, -qi)
            rho = R
            lamb = np.sign(qi1(1) * qi(2) - qi1(2) * qi(1))
            z = w[:, self.i] + (R / (np.tan(e / 2))) * qi

            if in_half_plane(p, z, qi):
                if self.i < (N - 1):
                    self.i = self.i + 1
                self.state = 1

        else:
            # Fly north as default
            flag = -1
            r = p
            q = mat([1, 0, 0]).T
            c = np.nan(3, 1)
            rho = np.nan
            lamb = np.nan

        return flag, r, q, c, rho, lamb

    def findDubinsParameters(self, p_s, chi_s, p_e, chi_e, R):
        """
        findDubinsParameters determines the dubins path parameters

        Inputs:
        p_s = start position (m)
        chi_s = start course angle (rad)
        p_e = end position (m)
        chi_e = end course angle (rad)
        R = turn radius (m)

        Outputs
        dp.L = path length (m)
        dp.c_s = start circle origin (m)
        dp.lamb_s = start circle direction (unitless)
        dp.c_e = end circle origin (m)
        dp.lamb_e = end circle direction (unitless)
        dp.z_1 = Half-plane H_1 location (m)
        dp.q_12 = Half-planes H_1 and H_2 unit normals (unitless)
        dp.z_2 = Half-plane H_2 location (m)
        dp.z_3 = Half-plane H_3 location  (m)
        dp.q_3 = Half-plane H_3 unit normal (m)
        dp.case = case (unitless)

        Example Usage
        dp = findDubinsParameters( p_s, chi_s, p_e, chi_e, R )

        Reference: Beard, Small Unmanned Aircraft, Chapter 11, Algorithm 7
        Copyright 2018 Utah State University
        """

        # TODO Algorithm 7 goes here
        # Ensure that the configurations are far enough apart
        assert (np.linalg.norm(p_s[0:2] - p_e[0:2]) >= 3*R), "Start and end configurations are too close!"
        # Misc calcs
        e_1 = np.array([[1,0,0]]).T
        # Compute circle centers

        # print(float(chi_s))
        # print(type(float(chi_s)))
        # print(np.cos(float(chi_s)))
        # print(np.sin(float(chi_s)))
        # print(type(np.cos(float(chi_s))))
        # print(type(np.sin(float(chi_s))))
        # print(np.array([[np.cos(float(chi_s)),np.sin(float(chi_s)),0]]).T)
        # print(type(np.array([[np.cos(float(chi_s)),np.sin(float(chi_s)),0]]).T))


        c_rs = p_s + ( np.matmul((R * self.Rzm(np.pi/2)), np.array([[np.cos(float(chi_s)),np.sin(float(chi_s)),0]]).T) )
        c_ls = p_s + ( np.matmul((R * self.Rzm(-np.pi/2)), np.array([[np.cos(float(chi_s)),np.sin(float(chi_s)),0]]).T) )
        c_re = p_e + ( np.matmul((R * self.Rzm(np.pi/2)), np.array([[np.cos(float(chi_e)),np.sin(float(chi_e)),0]]).T) )
        c_le = p_e + ( np.matmul((R * self.Rzm(-np.pi/2)), np.array([[np.cos(float(chi_e)),np.sin(float(chi_e)),0]]).T) )

        # Compute path lengths
        # Case 1: R-S-R
        th = self.anglem(c_re - c_rs)
        ah = np.mod((th-(np.pi/2)),(2*np.pi))
        ba = np.mod((chi_s-(np.pi/2)),(2*np.pi))
        ca = np.mod(((2*np.pi)+ ah- ba),(2*np.pi))
        da = np.mod((chi_e-(np.pi/2)),(2*np.pi))
        eu = np.mod((th-(np.pi/2)),(2*np.pi))
        ef = np.mod(((2*np.pi)+ da- eu),(2*np.pi))
        L1 = (np.linalg.norm(c_rs - c_re)) + (R*ca) + (R*ef)

        # Case 2: R-S-L
        th = self.anglem(c_le - c_rs)
        ell = np.linalg.norm(c_le - c_rs)
        th2 = th - (np.pi/2) + m.asin((2*R)/ell)
        ah = np.mod(th2,(2*np.pi))
        ba = np.mod((chi_s-(np.pi/2)),(2*np.pi))
        ca = np.mod(((2*np.pi)+ ah- ba),(2*np.pi))
        da = np.mod((th2+np.pi),(2*np.pi))
        eu = np.mod((chi_e+(np.pi/2)),(2*np.pi))
        ef = np.mod(((2*np.pi)+ da- eu),(2*np.pi))
        ja = np.sqrt((ell**2)-(4*(R**2)))
        if (th2.imag != 0.0):
            L2 = nan # Will not be selected
        else:
            L2 = ja + (R*ca) + (R*ef)

        # Case 3: L-S-R
        th = self.anglem(c_re - c_ls)
        ell = np.linalg.norm(c_re - c_ls)
        th2 = m.acos((2*R)/ell)
        ah = np.mod((chi_s+(np.pi/2)),(2*np.pi))
        ba = np.mod((th+th2),(2*np.pi))
        ca = np.mod(((2*np.pi)+ ah- ba),(2*np.pi))
        da = np.mod((chi_e-(np.pi/2)),(2*np.pi))
        eu = np.mod((th+th2-np.pi),(2*np.pi))
        ef = np.mod(((2*np.pi)+ da- eu),(2*np.pi))
        ja = np.sqrt((ell**2)-(4*(R**2)))
        if (th2.imag != 0.0):
            L3 = nan # Will not be selected
        else:
            L3 = ja + (R*ca) + (R*ef)

        # Case 4: L-S-L
        th = self.anglem(c_le - c_ls)
        ah = np.mod((chi_s+(np.pi/2)),(2*np.pi))
        ba = np.mod((th+(np.pi/2)),(2*np.pi))
        ca = np.mod(((2*np.pi)+ ah- ba),(2*np.pi))
        da = np.mod((th+(np.pi/2)),(2*np.pi))
        eu = np.mod((chi_e+(np.pi/2)),(2*np.pi))
        ef = np.mod(((2*np.pi)+ da- eu),(2*np.pi))
        L4 = (np.linalg.norm(c_ls - c_le)) + (R*ca) + (R*ef)

        # Define the parameters for the minimum length path (i.e. Dubins path)
        (L,i_min) = self.min_i([L1, L2, L3, L4])
        #[L,i_min] = min([L1, L2, L3, L4])
        if (i_min == 0):
            c_s = c_rs
            lamb_s = 1
            c_e = c_re
            lamb_e = 1
            q_1 = (c_e - c_s) / (np.linalg.norm(c_e - c_s))
            z_1 = c_s + (np.matmul( (R * self.Rzm(-np.pi/2)), q_1))
            z_2 = c_e + (np.matmul( (R * self.Rzm(-np.pi/2)), q_1))
            ell = np.linalg.norm(c_s - c_e)
        elif (i_min == 1):
            c_s = c_rs
            lamb_s = 1
            c_e = c_le
            lamb_e = -1
            ell = np.linalg.norm(c_e - c_s)
            th = self.anglem(c_e - c_s)
            th2 = th - (np.pi/2) + m.asin((2*R)/ell)
            q_1 = np.matmul( (self.Rzm(th2+(np.pi/2))), e_1)
            z_1 = c_s + (np.matmul( (R * self.Rzm(th2)), e_1) )
            z_2 = c_e + (np.matmul( (R * self.Rzm(th2+np.pi)), e_1) )
        elif (i_min == 2):
            c_s = c_ls
            lamb_s = -1
            c_e = c_re
            lamb_e = 1
            ell = np.linalg.norm(c_e - c_s)
            th = self.anglem(c_e - c_s)
            th2 = m.acos((2*R)/ell)
            q_1 = np.matmul( (self.Rzm(th+th2-(np.pi/2))), e_1)
            z_1 = c_s + (np.matmul( (R * self.Rzm(th+th2)), e_1) )
            z_2 = c_e + (np.matmul( (R * self.Rzm(th+th2-np.pi)), e_1) )
        else: # i_min == 3
            c_s = c_ls
            lamb_s = -1
            c_e = c_le
            lamb_e = -1
            q_1 = (c_e - c_s) / (np.linalg.norm(c_e - c_s))
            z_1 = c_s + (np.matmul( (R * self.Rzm(np.pi/2)), q_1) )
            z_2 = c_e + (np.matmul( (R * self.Rzm(np.pi/2)), q_1) )
            ell = np.linalg.norm(c_s - c_e)

        z_3 = p_e
        q_3 = np.matmul( (self.Rzm(float(chi_e))), e_1)

        # package output into DubinsParameters class
        dp = DubinsParameters()

        # TODO populate dp members here
        # Package outputs into struct
        dp.L = L
        dp.c_s = c_s
        dp.lamb_s = lamb_s
        dp.c_e = c_e
        dp.lamb_e = lamb_e
        dp.z_1 = z_1
        dp.q_1 = q_1
        dp.z_2 = z_2
        dp.z_3 = z_3
        dp.q_3 = q_3
        dp.case = i_min
        dp.lengths = [L1, L2, L3, L4]
        dp.theta = th
        dp.ell = ell
        dp.c_rs = c_rs
        dp.c_ls = c_ls
        dp.c_re = c_re
        dp.c_le = c_le

        return dp

    def min_i(self,Ls):
        i = 0
        val = Ls[0]
        for j in range(len(Ls)):
            if Ls[j] < val:
                val = Ls[j]
                i = j
        return (val,i)


    def Rzm(self,th):
        out = np.array([\
            [np.cos(th), -np.sin(th), 0],\
            [np.sin(th), np.cos(th), 0],\
            [0,0,1]])
        return out
    

    def anglem(self,v):
        out = m.atan2(v[1],v[0])
        return out
    

    def followWppDubins(self, W, Chi, p, R, newpath):
        """
        followWppDubins implements waypoint following via Dubins paths

        Inputs:
            W = list of waypoints in NED (m)
            Chi = list of course angles at waypoints in NED (rad)
            p = mav position in NED (m)
            R = fillet radius (m)
            newpath = flag to initialize the algorithm or define new waypoints

        Outputs
            flag = flag for straight line path (1) or orbit (2)
            r = origin of straight-line path in NED (m)
            q = direction of straight-line path in NED (m)
            c = center of orbit in NED (m)
            rho = radius of orbit (m)
            lamb = direction or orbit, 1 clockwise, -1 counter clockwise
            self.i = waypoint number
            dp = dubins path parameters

        Example Usage
            flag, r, q, c, rho, lamb = followWppDubins(W, Chi, p, R, newpath)

        Reference: Beard, Small Unmanned Aircraft, Chapter 11, Algorithm 8
        Copyright 2018 Utah State University
        """

        # TODO Algorithm 8 goes here
        
        try:
            self.i
        except NameError:
            print("THIS VAR IS NOT YET DEFINED!")
            self.i = 0
        else:
            print("YEUP, IT'S ALREADY DEFINED")
        try:
            self.state 
        except NameError:
            print("STATE: THIS VAR IS NOT YET DEFINED!")
            self.state = 0
        else:
            print("STATE: YEP, ALREADY BEUNO.")
        
        print("\nNEWPATH IS: ",newpath)
        if newpath:
            print("\nARE we GETting in here???")
            self.i = 1   # This value has been decreased from 2 for MATLAB->Python indexing
            self.state = 1   # This value has been kept the same
            (m,N) = W.shape
            assert (N >= 3), "Not enough vehicle configurations."
            assert (m == 3)
        else:
            print("\nARe we getting into this else statement?")
            (m,N) = W.shape
            assert (N >= 3), "Not enough vehicle configurations."
            assert (m == 3)
        # Determine the Dubins path parameters
        ps = W[:,self.i-1]
        chis = Chi[self.i-1]
        pe = W[:,self.i]
        chie = Chi[self.i]
        dp = self.findDubinsParameters( ps, chis, pe, chie, R )
        # L = dp.L
        c_s = dp.c_s
        lamb_s = dp.lamb_s
        c_e = dp.c_e
        lamb_e = dp.lamb_e
        z_1 = dp.z_1
        q_1 = dp.q_1
        z_2 = dp.z_2
        z_3 = dp.z_3
        q_3 = dp.q_3
        if (self.state == 1):
            #Follow start orbit until on the correct side of H1
            print("\nSTATE: 1; Follow start orbit until on the correct side of H1")
            flag = 2
            c = c_s
            rho = R
            lamb = lamb_s
            if in_half_plane(p,z_1,-q_1):
                self.state = 2
            r = p
            q = np.array([[1, 0, 0]]).T
        elif (self.state == 2):
            #Continue following the start orbit until in H1
            print("\nSTATE: 2; Continue following the start orbit until in H1")
            if in_half_plane(p,z_1,q_1):
                self.state = 3
            flag = 2
            r = p
            q = np.array([[1, 0, 0]]).T
            c = c_s
            rho = R
            lamb = lamb_s
        elif (self.state == 3):
            #Transition to straight-line path until in H2
            print("\nSTATE: 3; Transition to straight-line path until in H2")
            flag = 1
            r = z_1
            q = q_1
            if in_half_plane(p,z_2,q_1):
                self.state = 4
            c = np.zeros((3,1))
            rho = 0
            lamb = 0
        elif (self.state == 4):
            #Follow the end orbit until on the correct side of H3
            print("\nSTATE: 4; Follow the end orbit until on the correct side of H3")
            flag = 2
            c = c_e
            rho = R
            lamb = lamb_e
            if in_half_plane(p,z_3,-q_3):
                self.state = 5
            r = p
            q = np.array([[1, 0, 0]]).T
        else: #state == 5
            #Continue following the end orbit until in H3
            print("\nSTATE: 5; Continue following the end orbit until in H3")
            flag = 2
            r = p
            q = np.array([[1, 0, 0]]).T
            c = c_e
            rho = R
            lamb = lamb_e
            if in_half_plane(p,z_3,q_3):
                self.state = 1
                if (self.i < N):
                    self.i = (self.i+1)

        return flag, r, q, c, rho, lamb, self.i, dp


class DubinsParameters:
    def __init__(self):
        """
        Member Variables:
            L = path length (m)
            c_s = start circle origin (m)
            lamb_s = start circle direction (unitless)
            c_e = end circle origin (m)
            lamb_e = end circle direction (unitless)
            z_1 = Half-plane H_1 location (m)
            q_1 = Half-planes H_1 and H_2 unit normals (unitless)
            z_2 = Half-plane H_2 location (m)
            z_3 = Half-plane H_3 location  (m)
            q_3 = Half-plane H_3 unit normal (m)
            case = case (unitless)
        """

        self.L = 0
        self.c_s = mat([0, 0, 0]).T
        self.lamb_s = -1
        self.c_e = mat([0, 0, 0]).T
        self.lamb_e = 1
        self.z_1 = mat([0, 0, 0]).T
        self.q_1 = mat([0, 0, 0]).T
        self.z_2 = mat([0, 0, 0]).T
        self.z_3 = mat([0, 0, 0]).T
        self.q_3 = mat([0, 0, 0]).T
        self.case = 0
        self.lengths = np.array([[0, 0, 0, 0]])
        self.theta = 0
        self.ell = 0
        self.c_rs = mat([0, 0, 0]).T
        self.c_ls = mat([0, 0, 0]).T
        self.c_re = mat([0, 0, 0]).T
        self.c_le = mat([0, 0, 0]).T
