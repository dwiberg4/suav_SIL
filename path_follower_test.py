import unittest
import algorithms as Algorithms
import numpy as np

class path_follower_test(unittest.TestCase):
    def test_straightCrosstrack(self):
        flag = 1
        r = np.array([[-1000,0,-500]]).T
        q = np.array([[0.7044,0.7044,0.0872]]).T
        p = np.array([[0,0,-500]]).T
        chi = 3.2687e-18
        chi_inf = 1.5708
        k_path = 0.02
        c = None
        rho = None
        lamb = None
        k_orbit = None
        example = Algorithms.Algorithms()
        cross, chi_c, h_c = example.pathFollower(flag,r,q,p,chi,chi_inf,k_path,c,rho,lamb,k_orbit)
        self.assertAlmostEqual(cross,-707.1068,4,''.join("Crosstrack Error should be -707.1068 but it is: "+str(cross)))

    def test_straightCommandChi(self):
        flag = 1
        r = np.array([[-1000,0,-500]]).T
        q = np.array([[0.7044,0.7044,0.0872]]).T
        p = np.array([[0,0,-500]]).T
        chi = 3.2687e-18
        chi_inf = 1.5708
        k_path = 0.02
        c = None
        rho = None
        lamb = None
        k_orbit = None
        example = Algorithms.Algorithms()
        cross, chi_c, h_c = example.pathFollower(flag,r,q,p,chi,chi_inf,k_path,c,rho,lamb,k_orbit)
        self.assertAlmostEqual(chi_c,2.2856,4,''.join("chi_c should be 2.2856 but it is: "+str(chi_c)))

    def test_straightCommandH(self):
        flag = 1
        r = np.array([[-1000,0,-500]]).T
        q = np.array([[0.7044,0.7044,0.0872]]).T
        p = np.array([[0,0,-500]]).T
        chi = 3.2687e-18
        chi_inf = 1.5708
        k_path = 0.02
        c = None
        rho = None
        lamb = None
        k_orbit = None
        example = Algorithms.Algorithms()
        cross, chi_c, h_c = example.pathFollower(flag,r,q,p,chi,chi_inf,k_path,c,rho,lamb,k_orbit)
        self.assertAlmostEqual(h_c,561.8638,1,''.join("h_c should be 561.8638 but it is: "+str(h_c)))

    def test_orbitCrosstrack(self):
        flag = 2
        r = np.array([[None,None,None]]).T
        q = np.array([[None,None,None]]).T
        p = np.array([[0.875,0,0]]).T
        chi = 0.0
        chi_inf = None
        k_path = None
        c = np.array([[0,1000,-600]]).T
        rho = 200
        lamb = 1
        k_orbit = 3
        example = Algorithms.Algorithms()
        cross, chi_c, h_c = example.pathFollower(flag,r,q,p,chi,chi_inf,k_path,c,rho,lamb,k_orbit)
        self.assertAlmostEqual(cross,800,3,''.join("Crosstrack error should be -800 but it is: "+str(cross)))

    def test_orbitCommandChi(self):
        flag = 2
        r = np.array([[None,None,None]]).T
        q = np.array([[None,None,None]]).T
        p = np.array([[0.875,0,0]]).T
        chi = 0.0
        chi_inf = None
        k_path = None
        c = np.array([[0,1000,-600]]).T
        rho = 200
        lamb = 1
        k_orbit = 3
        example = Algorithms.Algorithms()
        cross, chi_c, h_c = example.pathFollower(flag,r,q,p,chi,chi_inf,k_path,c,rho,lamb,k_orbit)
        self.assertAlmostEqual(chi_c,1.4877,2,''.join("chi_c should be 1.4877 but it is: "+str(chi_c)))

    def test_orbitCommandH(self):
        flag = 2
        r = np.array([[None,None,None]]).T
        q = np.array([[None,None,None]]).T
        p = np.array([[0.875,0,0]]).T
        chi = 0.0
        chi_inf = None
        k_path = None
        c = np.array([[0,1000,-600]]).T
        rho = 200
        lamb = 1
        k_orbit = 3
        example = Algorithms.Algorithms()
        cross, chi_c, h_c = example.pathFollower(flag,r,q,p,chi,chi_inf,k_path,c,rho,lamb,k_orbit)
        self.assertAlmostEqual(h_c,600,4,''.join("Crosstrack error should be 600 but it is: "+str(h_c)))

if __name__ == '__main__':
    unittest.main()
