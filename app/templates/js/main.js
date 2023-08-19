const HistoryStateAction = {
  Push: 'Push',
  Replace: 'Replace',
  None: 'None'
};

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
          .scale(2400)
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

// this function is inspired by the `handleBubbles` function from datamaps source code
// https://github.com/markmarkoh/datamaps/blob/master/src/js/datamaps.js
function toggleBubbleHighlight(settlementId, isHoverEnterEvent) {
    var bubble = d3.select(`.datamaps-bubble[data-id="${settlementId}"]`);

    var previousAttributes = {
      'fill':  bubble.style('fill'),
      'stroke': bubble.style('stroke'),
      'stroke-width': bubble.style('stroke-width'),
      'fill-opacity': bubble.style('fill-opacity')
    };

    var newFill = isHoverEnterEvent ? map.options.bubblesConfig.highlightFillColor : map.options.fills.point;
    var newStroke = isHoverEnterEvent ? map.options.bubblesConfig.highlightBorderColor : map.options.bubblesConfig.borderColor;
    var newStrokeWidth = isHoverEnterEvent ? map.options.bubblesConfig.highlightBorderWidth : map.options.bubblesConfig.borderWidth;
    var newFillOpacity = isHoverEnterEvent ? map.options.bubblesConfig.highlightFillOpacity : map.options.bubblesConfig.fillOpacity;

    bubble
      .style('fill', newFill)
      .style('stroke', newStroke)
      .style('stroke-width', newStrokeWidth)
      .style('fill-opacity', newFillOpacity)
      .attr('data-previousAttributes', JSON.stringify(previousAttributes));
}

function initRowsHoverListeners() {
    $('#results-table tbody tr').hover(
        function(e) {
            var settlementId = $(this).attr("data-settlement-id");
            toggleBubbleHighlight(settlementId, true);
        },
        function(e) {
            var settlementId = $(this).attr("data-settlement-id");
            toggleBubbleHighlight(settlementId, false);
        }
    )
}

function pluralizeResults(size) {
    var lastDigit = size % 10;
    if (lastDigit == 1) {
        return "результат";
    } else if (lastDigit > 1 && lastDigit < 5) {
        return "результати";
    } else if (lastDigit == 0 || lastDigit > 4) {
        return "результатів"
    }
}

function addResultsToTable(settlements) {

    if (settlements && settlements.length > 0) {
        $('#table-wrapper .results-number').text(`Знайдено ${settlements.length} ${pluralizeResults(settlements.length)}`);

        var tableBody = $('#results-table tbody');
        tableBody.empty();

        for (var i = 0; i < settlements.length; i++) {
            settlement = settlements[i];
            var settlementHtml = `
                <tr data-settlement-id="${settlement.id}">
                    <td>${settlement.id}</td>
                    <td>${settlement.name}</td>
                    <td>${settlement.state}</td>
                    <td>${settlement.district}</td>
                    <td>${settlement.latitude}</td>
                    <td>${settlement.longitude}</td>
                </tr>
            `;
            tableBody.append(settlementHtml)
        }
        initRowsHoverListeners();
        $('#results-table').show();

    } else {
        $('#results-table').hide();
        $('#table-wrapper .results-number').text(`Не знайдено жодного результату`);
    }

}

function showBubbles(result) {
    map.bubbles(result, {
          popupTemplate: function (geo, data) {
                  return `<div class="hoverinfo">
                            ${data.name}<br/>
                            ${data.state}, ${data.district}, ${data.community}<br/>
                            id:  ${data.id}
                          </div>`;
          }
    });
    $('.datamaps-bubble').each(function( index ) {
      $(this).attr('data-id', JSON.parse($(this).attr('data-info')).id);
    });
}

function changeWindowHistoryState(nameRegex, historyStateAction) {
  if (historyStateAction &&
       (historyStateAction === HistoryStateAction.Push || historyStateAction === HistoryStateAction.Replace)
     ) {
     console.log(`${historyStateAction} new window state for ${nameRegex}`)
     const urlSearchParams = new URLSearchParams(window.location.search);
     urlSearchParams.set('q', encodeURIComponent(nameRegex));
     const newUrl = `${window.location.pathname}?${urlSearchParams.toString()}`;
     if (historyStateAction === HistoryStateAction.Push) {
       window.history.pushState({}, '', newUrl);
     } else if (historyStateAction === HistoryStateAction.Replace) {
        window.history.replaceState({}, '', newUrl);
     }
  }

}

function searchSettlementsAndShowOnMap(historyStateAction) {
  let nameRegex = $('#settlement-name-regex').val();
  console.log("searchSettlementsAndShowOnMap start. Regex: " + nameRegex);

  if (!nameRegex) {
    return;
  }

  if (historyStateAction) {
    changeWindowHistoryState(nameRegex, historyStateAction)
  }

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
  searchSettlementsAndShowOnMap(HistoryStateAction.Push);
});

var searchInputElement = $('#settlement-name-regex');

searchInputElement.bind("enterKey",function(e){
  searchSettlementsAndShowOnMap(HistoryStateAction.Push);
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

function processUrlQuery(historyStateAction) {
  const urlSearchParams = new URLSearchParams(window.location.search);
  const encodedQuery = urlSearchParams.get('q')
  if (encodedQuery) {
      query = decodeURIComponent(encodedQuery);
      searchInputElement.val(query);
      searchSettlementsAndShowOnMap(historyStateAction);
  }
}

function processInitialQuery() {
  processUrlQuery(HistoryStateAction.Replace);
}

processInitialQuery()

// handle history state change - browsers` 'back' and 'forward' buttons
window.onpopstate = function(e) {
    if(e.state){
        processUrlQuery(HistoryStateAction.None);
    } else {
        searchInputElement.val("");
        map.bubbles([]);
        $('#results-table tbody').empty();
        $('#results-table').hide();
        $('#table-wrapper .results-number').text('');
    }
};