
function init() {
  console.log("=== here in init")
  $.getJSON("report.json" , function(data) {
    build_content(data)
  }) 
}

function build_content(data) {
  var created_time = data['created_time']
  var rows = data['rows']
  var trs = []
  trs.push("<tr><th></th><th>Uploaded</th><th>Package</th></tr>")
  for (var i = 0; i < rows.length; i++) {
    var r = rows[i]
    var p = r["package"]
    var v = r["version"]
    var st = r["status"]
    var t = r["upload_time"]
    t = t.split(" ")[0]
    var url = "http://hackage.haskell.org/package/" + p + "-" + v
    var atag = '<a href="' + url + '">'
    var html = "<tr><td class=counter>" + (i+1) + "</td><td>" + t + "</td><td>" + atag + p + "-" + v + "</a></td></tr>"
    trs.push(html)
  }
  var joined = trs.join("")
  $("#tbl").html(joined)
  $("#preface").html("Report created at " + created_time)
}

$(document).ready(init)

