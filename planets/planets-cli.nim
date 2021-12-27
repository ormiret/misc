import json, strformat, os, strutils

proc findPlanet(earth: int, desired: int) : string = 
  let
    planets = parseFile("planets.json")
    desired_ratio = earth.float/desired.float
  var
    bestName = ""
    bestDelta, bestPeriod: float
  bestDelta = +INF
  for p in planets["planets"]:
    let
      name = p{"name"}.getStr
      period = p{"period"}.getFloat 
    if period > 0:
      let
        ratio = period/365.25
        delta = abs(desired_ratio - ratio)
      if delta < bestDelta:
        bestName = name
        bestDelta = delta
        bestPeriod = period
  echo fmt"best delta: {bestDelta}"
  return fmt"{earth} earth years old would be {desired} on {bestName} where a year is {bestPeriod} (earth) days long"
      
if isMainModule:
  if paramCount() != 2:
    echo "Usage: ./planets <earth age> <desired age>"
  else:
    echo findPlanet(paramStr(1).parseInt, paramStr(2).parseInt)
