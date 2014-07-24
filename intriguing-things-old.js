var keys = [];

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

        cur_key = dt + "-" + vals[i].number;
        ts.push("<div id=\"" + cur_key + "\" class=\"item\">" + out0 + out1 + out2 + out3 + out4 + "</div>");
        keys.push(cur_key);
    }
    return ts.join("\n");
}

function add_to_list(data) {
  data.sort(function(a,b) { return parseFloat(b[0]) - parseFloat(a[0]) } );

  var out = [];
  $.each(data, function(key, val) {
    out.push(li_item(key, val[0], val[1]));
  });
 
  $("<div/>", {
    "id": "items",
    html: out.join("\n")
  }).appendTo(".container");
}

function show_random() {
  $("#items").hide("fast");
  $("#rand-items").show("fast");
  inds = [];
  i = 1;
  while (i < 6) {
    ind = Math.floor(Math.random() * keys.length);
    if ($.inArray(ind, inds)) {
      inds.push(ind);
      $("#rand-item-" + i).html($('#' + keys[ind]).html());
      i += 1;
    }
  }
}
function show_all() {
  $("#items").show("fast");
  $("#rand-items").hide("fast");
}

var url = "data.json";
$(function() {
    $.getJSON(url, add_to_list);
    $("#show-random").click(show_random);
    $("#show-all").click(show_all);
});
