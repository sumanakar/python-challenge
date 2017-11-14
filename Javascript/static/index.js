// Get references to the tbody element, input field and button
var $tbody = document.querySelector("tbody");
var $dateInput = document.querySelector("#dateId");
var $cityInput = document.querySelector("#city");
var $stateInput = document.querySelector("#state");
var $countryInput = document.querySelector("#country");
var $shapeInput = document.querySelector("#shape");
var $searchBtn = document.querySelector("#search");
var $clearBtn = document.querySelector("#clear");
var $btnload = document.querySelector("#nextData");
var $btnprev = document.querySelector("#prevData");
var $page = document.querySelector("#pages");
//var total = dataSet.length;
var count = 0;
var data = dataSet;
var resultPerPage=100;

function capitalize(str) {
  if(str instanceof String || typeof str === 'string')
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

function createPage(startPage){
  var total = data.length%100;

  if(total!=0){
    total=Math.floor(data.length/100)+1;
  }  
  else{
    total=Math.floor(data.length/100)
  }

  while ($page.hasChildNodes()) {   
    $page.removeChild($page.firstChild);
  } 
  if( startPage > 0 ) {
    var pagelist= document.createElement("li");
    var prev= document.createElement("a");
    prev.setAttribute('href','#');
    prev.setAttribute("aria-label","Previous");
    prev.setAttribute("onClick","createPage("+(startPage-10)+")");
    span= document.createElement("span");
    span.setAttribute("aria-hidden","true");
    span.innerHTML="&laquo";
    prev.appendChild(span);
    pagelist.appendChild(prev);
    $page.appendChild(pagelist);
  }

  var remainCount = total - startPage;
  
  var loopCount = 10;
  
  if (remainCount < 10){
    loopCount = remainCount;
  }

  for(var k=startPage+1; k<=startPage+loopCount; k++) {    
    var pagelist= document.createElement("li");
    var pcount= document.createElement("a");

    pcount.innerText=k;
    pcount.setAttribute('href','#');
    pcount.setAttribute("onClick","onClickPage("+k+")");
    pagelist.appendChild(pcount);
    $page.appendChild(pagelist);
      
  }

  if( remainCount > 10 ) {

    var pagelist= document.createElement("li");
    var next= document.createElement("a");
    next.setAttribute('href','#');
    next.setAttribute("aria-label","Next");
    next.setAttribute("onClick","createPage("+(startPage+10)+")");
    span= document.createElement("span");
    span.setAttribute("aria-hidden","true");
    span.innerHTML="&raquo;";
    next.appendChild(span);
    pagelist.appendChild(next);
    $page.appendChild(pagelist);
  }
}

$searchBtn.addEventListener("click", handleSearchButtonClick);
$clearBtn.addEventListener("click", handleClearButtonClick);


// renderTable renders the filteredAddresses to the tbody
function renderTable(startIndex) {
  $tbody.innerHTML="";
  var endingIndex=startIndex+resultPerPage;
  var sliceData=data.slice(startIndex,endingIndex);

  for (var i = 0; i < sliceData.length; i++) {
    // Get get the current address object and its fields
    var fullData = sliceData[i];
    var fields = Object.keys(fullData);
    // Create a new row in the tbody, set the index to be i + startingIndex
    var $row = $tbody.insertRow(i);
    for (var j = 0; j < fields.length; j++) {
      // For every field in the address object, create a new cell at set its inner text to be the current value at the current address's field
      var field = fields[j];
      var $cell = $row.insertCell(j);
      if(field === "state" || field === "country"){

        $cell.innerText = fullData[field].toUpperCase();

      }
      else{

        $cell.innerText = capitalize(fullData[field]);

      } 
    }
  }
}

function  isMatch(filter,data) {
    return filter.length === 0 || filter.toLowerCase() === data.toLowerCase()
}

function handleSearchButtonClick() {
  var filterDate = $dateInput.value.trim();
  var filterCity = $cityInput.value.trim();
  var filterState = $stateInput.value.trim();
  var filterCountry = $countryInput.value.trim();
  var filterShape = $shapeInput.value.trim();

  // Set filteredAddresses to an array of all addresses whose "state" matches the filter
  data = dataSet.filter(function(inputData) {
    var dateSearch = inputData.datetime;
    var city = inputData.city;
    var state = inputData.state;
    var country = inputData.country;
    var shape = inputData.shape;
    return isMatch(filterDate,dateSearch) && isMatch(filterCity,city) && isMatch(filterState,state) && isMatch(filterCountry,country) && isMatch(filterShape,shape)
  });
  renderTable(0);
  createPage(0);

}

function handleClearButtonClick(){
    $dateInput.value="";
    data=dataSet;
    $dateInput.value="";
    $cityInput.value="";
    $stateInput.value="";
    $countryInput.value="";
    $shapeInput.value="";
    renderTable(0);
    createPage(0);

}


function onClickPage(arg){
  var startIndex=(parseInt(arg)-1)*100;
  renderTable(startIndex);
}


// Render the table for the first time on page load
renderTable(0);
createPage(0);


