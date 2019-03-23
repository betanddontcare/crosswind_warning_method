import math

#WEATHER PARAMETERS
windVelocity = 33.3
windAngle = 180
totalAirPressure = 983.0
temperature = 18.0
humidity = 0.1

#TERRAIN PARAMETERS
terrRoughCoe = 0.05
altidude = 100

#VEHCICLE PARAMETERS
vehVelocity = 13.88
frontArea = 11
distanceAxles = 5
totalWeight = 10
frontAxleLoad = 3
rearAxleLoad = 7
scaleWeight = 7
angleOfInclination = 30
wheelRadius = 0.5

#LOCATION PARAMETERS
p1 = [22, 23]
p2 = [21, 24]

#GUST VELOCITY
def computeGustVelocity(windVelocity, altidude, terrRoughCoe):
    return windVelocity*(1 + (2.28 / math.log(altidude/terrRoughCoe)))

#COMPUTING INITIAL BEARING
def computeLongRange(p1, p2):
    return abs(p1[1] - p2[1])

def computeAtanY():
    longrange = toRadians(computeLongRange(p1, p2))
    return math.sin(longrange) * math.cos(toRadians(p2[0]))

def computeAtanX():
    longrange = toRadians(computeLongRange(p1, p2))
    return math.cos(toRadians(p1[0])) * math.sin(toRadians(p2[0])) - math.sin(toRadians(p1[0])) * math.cos(toRadians(p2[0])) * math.cos(longrange)

def computeVehAngle():
    rawAtan = math.atan2(computeAtanY(), computeAtanX())
    return toDegrees(rawAtan)

#COMPUTING OTHER ANGLES
def angleWindVeh():
    return 180 - (computeVehAngle() - windAngle)

def computeAeroAngle(computeGustVelocity, vehVelocity, angleWindVeh):
    angle = math.atan(windVelocity * math.sin(angleWindVeh()) / (vehVelocity + windVelocity * math.cos(angleWindVeh())))
    return toDegrees(angle) #return angle from -pi/2 to pi/2 range

#AIR DENSITY
def computeVaporPresure(humidity, temperature):
    return ((6.1078 * 10 ** (7.5 * temperature/(temperature + 237.3))) * humidity) / 100

def computeDryAirPressure(totalAirPressure, computeVaporPresure):
    return totalAirPressure - computeVaporPresure(humidity, temperature)

def computeAirDensity(computeDryAirPressure, computeVaporPresure, temperature, totalAirPressure, humidity):
    temp = toKelvin(temperature)
    vapor = computeVaporPresure(humidity, temperature)
    dry = computeDryAirPressure(totalAirPressure, computeVaporPresure)
    return (((dry / (287.058 * temp)) + (vapor / (461.495 * temp)))  *100)

#LOCATION OF POINT OF MASS
def computeFrontGravity(rearAxleLoad, distanceAxles, totalWeight):
    return rearAxleLoad * distanceAxles/totalWeight

def computeRearGravity(computeFrontGravity, distanceAxles):
    return distanceAxles - computeFrontGravity(rearAxleLoad, distanceAxles, totalWeight)

def computeHightGravity(computeFrontGravity, distanceAxles, totalWeight, scaleWeight, angleOfInclination, wheelRadius):
    dist = computeFrontGravity(rearAxleLoad, distanceAxles, totalWeight)
    inclination = math.tan(angleOfInclination)
    return ((scaleWeight * distanceAxles - totalWeight * dist) / (totalWeight * inclination)) + wheelRadius

#AERODYNAMIC BAKER's COEFFICIENTS (1988)

#CALCULATORS OF UNITS
def toDegrees(num):
    return num * 180 / math.pi

def toRadians(num):
    return num * math.pi / 180

def toKelvin(temp):
    return temp + 273.15

