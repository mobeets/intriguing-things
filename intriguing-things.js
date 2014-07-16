function dt2str(val) {
  var date = new Date(val*1000);
  var d1 = date.getDate();
  var d2 = date.getMonth() + 1; //Months are zero based
  var d3 = date.getFullYear();
  return d3 + "-" + d2 + "-" + d1;
}
function li_item(dt, vals) {
    var ts = [];
    for (i in vals){
        out0 = "<div class=\"item-title\"><span class=\"dt\">" + dt2str(dt) + "</span>";
        out1 = "<span class=\"num\">(" + vals[i].number + ")</span></div>";
        out2 = "<div class=\"title\"><a href=\"" + vals[i].url + "\">" + vals[i].title + "</a></div>";
        out3 = "<div class=\"ps\">" + vals[i].ps.join("") + "</div>";
        ts.push("<div class=\"item\">" + out0 + out1 + out2 + out3 + "</div>");
    }
    return ts.join("<hr>");
}

function add_to_list(data) {
  var out = [];
  $.each(data, function(key, val) {
    out.push(li_item(val[0], val[1]));
  });
 
  $("<div/>", {
    "id": "items",
    html: out.join("<hr>")
  }).appendTo(".container");
}

var url = "data.json";
// var url = "http://raw.githubusercontent.com/mobeets/intriguing-things/master/intriguing-things.json";
$(function() {
    console.log('Hello!');
    $.getJSON(url, add_to_list);
});
