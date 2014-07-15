function li_item(dt, vals) {
    var ts = [];
    for (i in vals){
        out0 = "<div class=\"dt\">" + dt + "</div>";
        out1 = "<div class=\"title\"><a href=\"" + vals[i].url + "\">" + vals[i].title + "</a></div>";
        out2 = "<div class=\"ps\">" + vals[i].ps.join("") + "</div>";
        ts.push("<div class=\"item\">" + out0 + out1 + out2 + "</div>");
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

// var url = "intriguing-things.json";
var url = "http://raw.githubusercontent.com/mobeets/intriguing-things/master/intriguing-things.json";
$(function() {
    console.log('Hello!');
    $.getJSON(url, add_to_list);
});
