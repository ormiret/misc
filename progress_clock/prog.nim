include karax/prelude

import std/ [strformat, times]
import karax / [vstyles, kdom]

var progs : seq[tuple[label: string, prog: float64]] 
var timer: TimeOut
    
proc render(): VNode =
  proc setProgs() =
    var n = now()
    timer = setTimeout(setProgs, 1000-int(n.nanosecond/1e6.int))
    progs = @[("Minute", n.second/60), ("Hour", n.minute/60), ("Day", n.hour/24),
    ("Week", ord(n.weekDay)/ord(high(WeekDay))), ("Month", n.monthday/getDaysInMonth(n.month, n.year)),
    ("Year", n.yearday/getDaysInYear(n.year))]
    redraw()
  timer = setTimeout(setProgs, 10)

  result = buildHtml(tdiv(class="progress-clock")):
    for (label, prog) in progs:
      h4:
        text label
      tdiv(class="progress"):
        tdiv(class="meter"):
          span(style = fmt"width: {prog*100}%".toCss)

setRenderer render
