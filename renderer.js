//not sure if needed
// window.$ = window.jQuery = require('jquery');

function runPythonSync(){
    var pyshell =  require('python-shell');

    pyshell.PythonShell.run('./python/sync.py', function  (err, results)  {
      if  (err)  throw err;
      console.log('sync.py finished.');
    });
}

function loadNextPage(){
    var pyshell =  require('python-shell');
    var pjson = require('./package.json');

    let cmdDataLoad = {
      mode: 'text',
      pythonOptions: ['-u'],
      args: ["nextPage", pjson.version]
    }

    pyshell.PythonShell.run('./python/dbCMD.py', cmdDataLoad, function  (err, results)  {

      //append to table

      if(err)  throw err;
      console.log('loaded next page');
    });
}

function loadFirstPage(){
  var pyshell =  require('python-shell');
  var pjson = require('./package.json');

  let cmdDataLoad = {
    mode: 'text',
    pythonOptions: ['-u'],
    args: ["loaded", pjson.version]
  }

  pyshell.PythonShell.run('./python/dbCMD.py', cmdDataLoad, function  (err, results)  {
    
    let matchID = [];
    let filename = [];
    let players = [];
    let decknames = [];
    let p1Deck = [];
    let p2Deck = [];
    let turnOrder = [];
    let winList = [];
    let format = [];
    let type = [];
    let date = [];
    
    for (let inner = 1; inner < results.length; inner++){
      
    }
    
    for (let outer = 0; outer < results.length/11; outer++){
      document.getElementById(databaseContent).innerHTML = `
          <tr>
            <th class="matchID">${matchID}</th>
            <th class="filename">${filename}<button class="replaceImageFilename">...</button></th>
            <th class="players"><p class="replaceTextOpponent">${players}</p><button class="replaceImageOpponent">...</button></th>
            <th class="decknames"><p class="replaceText">${decknames}</p><button class="replaceImage">...</button></th>
            <th class="p1Deck"><p class="replaceTextDeck">${p1Deck}</p><button class="replaceImageDeck">...</button></th>
            <th class="p2Deck"><p class="replaceTextDeck">${p2Deck}</p><button class="replaceImageDeck">...</button></th>
            <th class="turnOrder"><p class="replaceTextExtra">${turnOrder}<button class="replaceImageExtra">...</button></th>
            <th class="winList"><p class="replaceTextExtra">${winList}</p><button class="replaceImageExtra">...</button></th>
            <th class="format">${format}</th>
            <th class="type">${type}</th>
            <th class="date">${date}</th>
          </tr>`
    }

    if(err)  throw err;
    console.log('loaded next page');
  });
}

document.querySelector('#pyBtnSync').addEventListener('click', () => {
    runPythonSync();
})

document.querySelector('#pyBtnNextPage').addEventListener('click', () => {
  loadNextPage();
})

document.addEventListener('DOMContentLoaded', () =>{
  loadFirstPage();
})
