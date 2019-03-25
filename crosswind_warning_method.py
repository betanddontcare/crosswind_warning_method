import math

#WEATHER PARAMETERS
windVelocity = 18
windAngle = 45
totalAirPressure = 983.0
temperature = 18.0
humidity = 0.1
isRainy = False

#TERRAIN PARAMETERS
terrRoughCoe = 0.05
altidude = 100
rollingResistanceCoe = 0.014

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
    
def computeAeroAngle(computeGustVelocity, vehVelocity, angleWindVeh, computeVehAngle, windAngle):
    aeroAngle = math.atan(windVelocity * math.sin(toRadians(angleWindVeh())) / (vehVelocity + windVelocity * math.cos(toRadians(angleWindVeh()))))
    if windAngle <= computeVehAngle() or windAngle >= computeVehAngle() + 180:
        if toDegrees(aeroAngle) >= 0:
            return toDegrees(aeroAngle)
        else:
            return 90 - toDegrees(aeroAngle)
    else:
        if toDegrees(aeroAngle) >= 0:
            return 180 + toDegrees(aeroAngle)
        else:
            return 270 - toDegrees(aeroAngle)

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
def computeSideCoe(computeAeroAngle):
    angle = computeAeroAngle(computeGustVelocity, vehVelocity, angleWindVeh, computeVehAngle, windAngle)
    if angle > 0 and angle <= 90:
        return 5.2 * math.sin(toRadians(angle))
    elif angle > 90 and angle <= 180:
        return 5.2 * math.sin(toRadians(180 - angle))
    elif angle > 180 and angle <= 270:
        return -5.2 * math.sin(toRadians(angle - 180))
    elif angle > 270 and angle <= 360:
        return -5.2 * math.sin(toRadians(360 - angle))

def computeLiftCoe(computeAeroAngle):
    angle = computeAeroAngle(computeGustVelocity, vehVelocity, angleWindVeh, computeVehAngle, windAngle)
    if angle > 0 and angle <= 90:
        return 1.1 * (1 - math.cos(4 * toRadians(angle)))
    elif angle > 90 and angle <= 180:
        return 1.1 * (1 - math.cos(4 * toRadians(180 - angle)))
    elif angle > 180 and angle <= 270:
        return 1.1 * (1 - math.cos(4 * toRadians(angle - 180)))
    elif angle > 270 and angle <= 360:
        return 1.1 * (1 - math.cos(4 * toRadians(360 - angle)))

def computeDragCoe(computeAeroAngle):
    angle = computeAeroAngle(computeGustVelocity, vehVelocity, angleWindVeh, computeVehAngle, windAngle)
    if angle > 0 and angle <= 90:
        return -0.5 * (1 + math.sin(toRadians(3 * angle)))
    elif angle > 90 and angle <= 180:
        return 0.5 * (1 + math.sin(toRadians(3 * (180 - angle))))
    elif angle > 180 and angle <= 270:
        return 0.5 * (1 + math.sin(toRadians(3 * (angle - 180))))
    elif angle > 270 and angle <= 360:
        return -0.5 * (1 + math.sin(toRadians(3 * (360 - angle))))

def computePitchingCoe(computeAeroAngle):
    angle = computeAeroAngle(computeGustVelocity, vehVelocity, angleWindVeh, computeVehAngle, windAngle)
    if angle > 0 and angle <= 90:
        return -2 * (1 - math.cos(toRadians(2 * angle)))
    elif angle > 90 and angle <= 180:
        return 2 * (1 - math.cos(toRadians(2 * (180 - angle))))
    elif angle > 180 and angle <= 270:
        return 2 * (1 - math.cos(toRadians(2 * (angle - 180))))
    elif angle > 270 and angle <= 360:
        return -2 * (1 - math.cos(toRadians(2 * (360 - angle))))
    
#FORCES AND MOMENTS
#Newton unit!
def dragForce(computeDragCoe, frontArea, computeAirDensity, appWindVelocity):
    airDensity = computeAirDensity(computeDryAirPressure, computeVaporPresure, temperature, totalAirPressure, humidity)
    dragCoe = computeDragCoe(computeAeroAngle)
    appWindVel = appWindVelocity(vehVelocity, windVelocity, angleWindVeh)
    return (dragCoe * frontArea * airDensity * (appWindVel ** 2)) / 2

def liftForce(computeLiftCoe, frontArea, computeAirDensity, appWindVelocity):
    airDensity = computeAirDensity(computeDryAirPressure, computeVaporPresure, temperature, totalAirPressure, humidity)
    liftCoe = computeLiftCoe(computeAeroAngle)
    appWindVel = appWindVelocity(vehVelocity, windVelocity, angleWindVeh)
    return (liftCoe * frontArea * airDensity * (appWindVel ** 2)) / 2

def pitchingMoment(computePitchingCoe, computeHightGravity, frontArea, computeAirDensity, appWindVelocity):
    airDensity = computeAirDensity(computeDryAirPressure, computeVaporPresure, temperature, totalAirPressure, humidity)
    pitchCoe = computePitchingCoe(computeAeroAngle)
    appWindVel = appWindVelocity(vehVelocity, windVelocity, angleWindVeh)
    height = computeHightGravity(computeFrontGravity, distanceAxles, totalWeight, scaleWeight, angleOfInclination, wheelRadius)
    return (pitchCoe * frontArea * airDensity * height * (appWindVel ** 2)) / 2

#TRACTION PARAMETERS
def traction(computeFrontGravity, computeRearGravity, dragForce, rollingResistanceCoe, liftForce, computeHightGravity, pitchingMoment, totalWeight):
    a = computeFrontGravity(rearAxleLoad, distanceAxles, totalWeight)
    b = computeRearGravity(computeFrontGravity, distanceAxles)
    h = computeHightGravity(computeFrontGravity, distanceAxles, totalWeight, scaleWeight, angleOfInclination, wheelRadius)
    drag = dragForce(computeDragCoe, frontArea, computeAirDensity, appWindVelocity)
    lift = liftForce(computeLiftCoe, frontArea, computeAirDensity, appWindVelocity)
    pitching = pitchingMoment(computePitchingCoe, computeHightGravity, frontArea, computeAirDensity, appWindVelocity)
    return ((a + b) * (drag + rollingResistanceCoe * (totalWeight * 1000 * 9.81 - lift))) / ((b + a) * (totalWeight * 1000 - lift))

def staticFriction(isRainy):
    if isRainy:
        return 0.35
    else:
        return 0.75

def computeFrictionCoePerAxle(staticFriction, rollingResistanceCoe, traction):
    q = traction(computeFrontGravity, computeRearGravity, dragForce, rollingResistanceCoe, liftForce, computeHightGravity, pitchingMoment, totalWeight)
    static = staticFriction(isRainy)
    return math.sqrt(static ** 2 - ((q - rollingResistanceCoe) ** 2))

#COMPUTING FINAL VELOCITIES
def appWindVelocity(vehVelocity, windVelocity, angleWindVeh):
    angle = angleWindVeh()
    return math.sqrt(((windVelocity + windVelocity * math.cos(toRadians(angle))) ** 2) + (windVelocity * math.sin(toRadians(angle))))

def computeSlideSlipVel(totalWeight, computeFrontGravity, computeRearGravity, frontArea, computeAirDensity, computeSideCoe, computeFrictionCoePerAxle, computeLiftCoe):
    static = computeFrictionCoePerAxle(staticFriction, rollingResistanceCoe, traction)
    a = computeFrontGravity(rearAxleLoad, distanceAxles, totalWeight)
    b = computeRearGravity(computeFrontGravity, distanceAxles)
    side = computeSideCoe(computeAeroAngle)
    lift = computeLiftCoe(computeAeroAngle)
    airDensity = computeAirDensity(computeDryAirPressure, computeVaporPresure, temperature, totalAirPressure, humidity)
    print(static, a, b, side, lift, airDensity, totalWeight, frontArea)
    print(math.sqrt((2 * totalWeight * 1000 * 9.81 * static * (a + b)) / ((frontArea * airDensity) * ((a + b) * side + static * lift * (a + b)))))

#CALCULATORS OF UNITS
def toDegrees(num):
    return num * 180 / math.pi

def toRadians(num):
    return num * math.pi / 180

def toKelvin(temp):
    return temp + 273.15
