var map = new Datamap({
    scope: 'ukr',
    element: document.getElementById('container'),
    geographyConfig: {
        popupOnHover: false,
        highlightOnHover: false
    },
    projection: 'mercator',
    height: null, //if not null, datamaps will grab the height of 'element'
    width: null, //if not null, datamaps will grab the width of 'element'
    setProjection: function(element) {
        var projection = d3.geo.mercator()
          .center([31,49])
          .scale(2000)
          .translate([element.offsetWidth / 2, element.offsetHeight / 2]);
        var path = d3.geo.path()
          .projection(projection);

        return {path: path, projection: projection};
    },
    fills: {
        'point': '#0000FF',
        defaultFill: '#e87127'
    },
    bubblesConfig: {
      fillKey: 'point',
      fillOpacity: 1,
      radius: 5
    }
});

function searchSettlementsAndShowOnMap() {

  let nameRegex = $('#settlement-name-regex').val()
  console.log("name regex: " + nameRegex)

  $.ajax({
    url: "/api/settlements",
    type: "get",
    data: {
      settlement_name_regex: nameRegex
    },
    success: function(result) {
      console.log("Results:")
      console.log(result)

      map.bubbles(result, {
          popupTemplate: function (geo, data) {
                  return `<div class="hoverinfo">
                            ${data.name}<br/>
                            id:  ${data.id}
                          </div>`;
          }
      });
    }
  });

}

$("#submit-btn").on("click", function(event) {
  console.log("button click");
  searchSettlementsAndShowOnMap();
});

$('#settlement-name-regex').bind("enterKey",function(e){
  console.log("pressing enter");
  searchSettlementsAndShowOnMap();
});
$('#settlement-name-regex').keyup(function(e){
    if(e.keyCode == 13)
    {
        $(this).trigger("enterKey");
    }
});
