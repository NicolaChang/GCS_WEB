from numpy import sin, cos, arccos, pi, round

class lon_transfer(): 
    def __init__():
        self.radians = radians
    def rad2deg(self):
        degrees = radians * 180 / pi
        return degrees

    def deg2rad(degrees):
        radians = degrees * pi / 180
        return radians

    def getDistanceBetweenPointsNew(latitude1, longitude1, latitude2, longitude2, unit = 'kilometers'):
        
        theta = longitude1 - longitude2
        
        distance = 60 * 1.1515 * rad2deg(
            arccos(
                (sin(deg2rad(latitude1)) * sin(deg2rad(latitude2))) + 
                (cos(deg2rad(latitude1)) * cos(deg2rad(latitude2)) * cos(deg2rad(theta)))
            )
        )
        
        if unit == 'miles':
            return round(distance, 15)
        if unit == 'kilometers':
            return round(distance * 1.609344, 2)