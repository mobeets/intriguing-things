function dt2str(val) {
  var date = new Date(val*1000);
  var d1 = date.getDate();
  var d2 = date.getMonth() + 1;
  var d3 = date.getFullYear();
  return d3 + "-" + d2 + "-" + d1;
}
function li_item(key, dt, vals) {
    var ts = [];
    for (i in vals){
        out0 = "<div class=\"item-title\"><span class=\"dt\">" + dt2str(dt) + "</span>";
        out1 = "<span class=\"num\">#" + vals[i].number + "</span>";
        out2 = "<span class=\"src-url\"><a href=\"" + vals[i].src_url + "\">[source]</a></span></div>";
        out3 = "<div class=\"title\"><a href=\"" + vals[i].url + "\">" + vals[i].title + "</a></div>";
        out4 = "<div class=\"ps\">" + vals[i].ps.join("") + "</div>";
        ts.push("<div id=\"" + dt + "-" + vals[i].number + "\" class=\"item\">" + out0 + out1 + out2 + out3 + out4 + "</div>");
    }
    return ts.join("<hr>");
}

function add_to_list(data) {
  var out = [];
  $.each(data, function(key, val) {
    out.push(li_item(key, val[0], val[1]));
  });
 
  $("<div/>", {
    "id": "items",
    html: out.join("<hr>")
  }).appendTo(".container");
}

var url = "data.json";
$(function() {
    $.getJSON(url, add_to_list);
});
