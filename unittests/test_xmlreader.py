import unittest
from xmlreader import XMLReader

class TestXMLReader(unittest.TestCase):

    # parse simulation
    def test_parse_simulation_legal(self):
        objects = XMLReader("../testfiles/settings.xml", "simulation").read()

        assert objects[0] == \
            ('robot',
             'Khepera3', 
             'khepera3.K3Supervisor', 
             (1.0, 1.0, 1.5708))
        assert objects[1] == \
            ('obstacle', 
             (1.0, 1.2, 0.0), 
             [(0.0, 0.0), (0.3, 0.0), (0.3, 0.3), (0.0, 0.3)])
        assert objects[2] == \
            ('obstacle', 
             (-0.5, 0.0, 0.7854), 
             [(0.0, 0.0), (0.3, 0.0), (0.3, 0.3), (0.0, 0.3)])
        assert objects[3] == \
            ('obstacle', 
             (0.65, 0.0, 0.7854), 
             [(0.0, 0.0), (0.3, 0.0), (0.3, 0.3), (0.0, 0.3)])
        assert objects[4] == \
            ('obstacle', 
             (0.2, 0.8, 0.0), 
             [(0.0, 0.0), (0.3, 0.0), (0.3, 0.3), (0.0, 0.3)])
        assert objects[5] == \
            ('obstacle', 
             (-1.0, -1.0, 0.0), 
             [(0.0, 0.0), (1.5, 0.0), (1.5, 0.3), (0.0, 0.3)]) 
        assert objects[6] == \
            ('obstacle', 
             (-1.6, -1.5, 0.0), 
             [(0.0, 0.0), (3.0, 0.0), (3.0, 0.1), (0.0, 0.1)])
        assert objects[7] == \
            ('obstacle', 
             (-1.5, -1.4, 1.5708), 
             [(0.0, 0.0), (3.0, 0.0), (3.0, 0.1), (0.0, 0.1)])
        assert objects[8] == \
            ('obstacle', 
             (1.5, -1.5, 1.5708), 
             [(0.0, 0.0), (3.0, 0.0), (3.0, 0.1), (0.0, 0.1)])
        assert objects[9] == \
            ('obstacle', 
             (-1.5, 1.5, 0.0), 
             [(0.0, 0.0), (3.0, 0.0), (3.0, 0.1), (0.0, 0.1)])
            
    def test_parse_simulation_bad_filename(self):
        self.assertRaises(Exception, XMLReader, "pysimiam_rules", "simulation")
        
    def test_parse_simulation_no_robot_supervisor(self):
        parser = XMLReader("../testfiles/no_robot_supervisor.xml", "simulation")
        self.assertRaises(Exception, parser.read)
    
    def test_parse_simulation_no_robot_pose(self):
        parser = XMLReader("../testfiles/no_robot_pose.xml", "simulation")
        self.assertRaises(Exception, parser.read)

    def test_parse_simulation_bad_robot_coordinate(self):
        parser = XMLReader("../testfiles/bad_robot_coord.xml", "simulation")
        self.assertRaises(Exception, parser.read)
                
    def test_parse_simulation_no_obstacle_pose(self):
        parser = XMLReader("../testfiles/no_obstacle_pose.xml", "simulation")
        self.assertRaises(Exception, parser.read)
        
    def test_parse_simulation_no_obstacle_geometry(self):
        parser = XMLReader("../testfiles/no_obstacle_geometry.xml", "simulation")
        self.assertRaises(Exception, parser.read)
        
    def test_parse_simulation_bad_obstacle_coordinate(self):
        parser = XMLReader("../testfiles/bad_obstacle_coord.xml", "simulation")
        self.assertRaises(Exception, parser.read)
        
    def test_parse_simulation_missing_obstacle_coordinate(self):
        parser = XMLReader("../testfiles/missing_obstacle_coord.xml", "simulation")
        self.assertRaises(Exception, parser.read)
        
    def test_parse_simulation_too_few_obstacle_points(self):
        parser = XMLReader("../testfiles/too_few_points.xml", "simulation")
        self.assertRaises(Exception, parser.read)


    # parse parameters
    def test_parse_parameters_legal(self):
        parameters = XMLReader("../testfiles/parameters.xml", "parameters").read()
        
        assert parameters == {'pid': {
                                     'goal': {'y': 10.0, 'x': 11.0}, 
                                     'angle': {'theta': 0.7854}, 
                                     'velocity': {'v': 0.1}, 
                                     ('gains', 'soft'): {'ki': 0.1, 'kp': 5.0, 'kd': 0.01}, 
                                     ('gains', 'hard'): {'ki': 0.1, 'kp': 5.0, 'kd': 0.01}
                                     }
                             }

    # validate parameters
    def test_validate_parameters_default(self):
        try:
            import lxml
        except ImportError:
            return True

        assert XMLReader("../testfiles/parameters.xml", "parameters").validate("../schemas/pid.xsd") == True   
    
    def test_validate_parameters_saved(self):
        try:
            import lxml
        except ImportError:
            return True

        assert XMLReader("../testfiles/parameters_saved.xml", "parameters").validate("../schemas/pid.xsd") == True   
    
if __name__ == "__main__":
    unittest.main()