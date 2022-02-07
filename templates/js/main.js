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
      radius: 7,
      borderOpacity: 1,
      borderColor: '#FFFFFF',
      borderWidth: 1,
      highlightFillColor: '#0000FF',
      highlightBorderWidth: 2,
      highlightBorderColor: 'rgba(0, 0, 0, 1)'
    }
});

function initRowsHoverListeners() {
    $('#results-table tbody tr').hover(
        function(e) {
            var settlementId = $(this).attr("data-settlement-id");
            var bubble = d3.select(`.datamaps-bubble[data-id="${settlementId}"]`);
            var previousAttributes = {
              'fill':  bubble.style('fill'),
              'stroke': bubble.style('stroke'),
              'stroke-width': bubble.style('stroke-width'),
              'fill-opacity': bubble.style('fill-opacity')
            };

            bubble
              .style('fill', map.options.bubblesConfig.highlightFillColor)
              .style('stroke', map.options.bubblesConfig.highlightBorderColor)
              .style('stroke-width', map.options.bubblesConfig.highlightBorderWidth)
              .style('fill-opacity', map.options.bubblesConfig.highlightFillOpacity)
              .attr('data-previousAttributes', JSON.stringify(previousAttributes));
        },
        function(e) {
            var settlementId = $(this).attr("data-settlement-id");
            var bubble = d3.select(`.datamaps-bubble[data-id="${settlementId}"]`);
            var previousAttributes = {
              'fill':  bubble.style('fill'),
              'stroke': bubble.style('stroke'),
              'stroke-width': bubble.style('stroke-width'),
              'fill-opacity': bubble.style('fill-opacity')
            };

            bubble
              .style('fill', map.options.fills.point)
              .style('stroke', map.options.bubblesConfig.borderColor)
              .style('stroke-width', map.options.bubblesConfig.borderWidth)
              .style('fill-opacity', map.options.bubblesConfig.fillOpacity)
              .attr('data-previousAttributes', JSON.stringify(previousAttributes));
        }
    )
}

function addResultsToTable(settlements) {
    $('#table-wrapper').show();

    var tableBody = $('#results-table tbody');
    tableBody.empty();

    for (var i=0; i < settlements.length; i++) {
        settlement = settlements[i];
        var settlementHtml = `
            <tr data-settlement-id="${settlement.id}">
                <td>${settlement.id}</td>
                <td>${settlement.name}</td>
                <td>${settlement.latitude}</td>
                <td>${settlement.longitude}</td>
            </tr>
        `;
        tableBody.append(settlementHtml)
    }
    initRowsHoverListeners();

}

function showBubbles(result) {
    map.bubbles(result, {
          popupTemplate: function (geo, data) {
                  return `<div class="hoverinfo">
                            ${data.name}<br/>
                            id:  ${data.id}
                          </div>`;
          }
    });
    $('.datamaps-bubble').each(function( index ) {
      $(this).attr('data-id', JSON.parse($(this).attr('data-info')).id);
    });
}

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

      showBubbles(result)

      addResultsToTable(result);
    }
  });

}

$("#submit-btn").on("click", function(event) {
  console.log("button click");
  searchSettlementsAndShowOnMap();
});

var searchInputElement = $('#settlement-name-regex');

searchInputElement.bind("enterKey",function(e){
  console.log("pressing enter");
  searchSettlementsAndShowOnMap();
});

searchInputElement.keyup(function(e){
    if(e.keyCode == 13)
    {
        $(this).trigger("enterKey");
    }
});

$('.disclaimer .examples ul li span').on("click", function(event) {
    event.preventDefault();
    var text = $(this).text().trim();
    searchInputElement.val(text);
    searchInputElement.trigger("enterKey");
});
