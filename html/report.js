
function init() {
  console.log("=== here in init")
  $.getJSON("report.json" , function(data) {
    build_content(data)
  }) 
}

function first_word(s) {
  return s.split(" ")[0]
}

function td_(s) {
  return '<td>' + s + '</td>'
}

function atag(url) {
  return '<a href="' + url + '">'
}

function contents_link(pkg, vers, body) {
  var url = "http://hackage.haskell.org/package/" + pkg + "-" + vers
  return atag(url) + body + "</a>"
}

function build_content(data) {
  var created_time = data['created_time']
  var rows = data['rows']
  console.log("first row:", rows[0])
  console.log("row count: " + rows.length)
  var trs = []
  trs.push("<tr><th></th><th>Uploaded</th><th>Package</th><th>Prev Upload Time</th><th>Prev Version</th><th>Prev Status</th></tr>")
  var fields = "upload_time package version last_version last_upload_time last_status".split(" ")
  for (var i = 0; i < rows.length; i++) {
    var r = rows[i]
    var p = r["package"]
    var v = r["version"]
    var t0 = first_word( r["upload_time"] )
    var t1 = first_word( r['last_upload_time'] || "--" )
    var url = "http://hackage.haskell.org/package/" + p + "-" + v
    var atag = '<a href="' + url + '">'
    var lst = r["last_status"] || "--"
    lst = lst.replace(/\[ *build log.*/, "")
    lst = lst.replace(/ *Build status unknown.*/, "")
    var lvers = r['last_version'] || "--"
    var lvers;
    if (r['last_version']) {
      lvers = contents_link(p, r['last_version'], r['last_version'])
    } else {
      lvers = "--"
    }
    var cols = [ '<td class=counter>' + (i+1) + '</td>'
               , td_( t0 )
               , td_( atag + p + '</a>' )
               , td_( t1 )
               , td_( lvers )
               , td_( lst  )
               ]
    var tr = "<tr>" + cols.join('') + "</tr>"
    trs.push(tr)
  }
  var joined = trs.join("")
  $("#tbl").html(joined)
  $("#preface").html("Report created at " + created_time)
}

$(document).ready(init)

