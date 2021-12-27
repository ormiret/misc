import sugar, json, strformat, karax/kajax, uri

include karax/prelude

var earthAge, desiredAge : float
var res : VNode

var planets: seq[tuple[name:string, period:float]]

proc loadPlanets(httpStatus: int, resp: cstring) =
  let planetsJ = parseJson($resp)
  for p in planetsJ["planets"]:
    let
      name = p{"name"}.getStr
      period = p{"period"}.getFloat
    if period > 0:
      planets.add((name, period))
  res = buildHtml:
        text fmt"Added {planets.len} planets"

ajaxGet("/img/planets.json", @[], loadPlanets)

proc findPlanet(earth: float, desired: float) : VNode = 
  let
    desired_ratio = earth/desired
  var
    bestName = ""
    bestDelta, bestPeriod: float
  bestDelta = +INF
  for (name, period) in planets:
    let
      ratio = period/365.25
      delta = abs(desired_ratio - ratio)
    if delta < bestDelta:
      bestName = name
      bestDelta = delta
      bestPeriod = period
  return buildHtml:
    tdiv(class="result"):
      text "Best match is "
      a(href="https://exoplanetarchive.ipac.caltech.edu/overview/" & bestName.encodeUrl(false),
        target="_blank"):
        text bestName
      text fmt" with a period of {bestPeriod} (earth) days ({bestDelta*100:.2f}% from target)"
      


proc render(): VNode =
  result = buildHtml(tdiv(class="planets-wrapper")):
    section(class="planets"):
      header(class="header"):
        h3:
          text "Age on other planets"
      p:
        text "Age in earth years: "
        input(class="age", onkeyup = (e: Event, n: VNode) => (earthage = n.value.parseFloat))
      p:
        text "Desired age: "
        input(class="age", onkeyup = (e: Event, n: VNode) => (desiredAge = n.value.parseFloat))
      p:
        button(onclick = () => (res = findPlanet(earthAge, desiredAge))):
          text "Calculate"
      p:
        res

setRenderer render
    
