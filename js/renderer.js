function runPythonSync(){
    var pyshell =  require('python-shell');

    pyshell.PythonShell.run('./python/sync.py', function  (err, results)  {
      if  (err)  throw err;
      console.log('sync.py finished.');
    });
}

//merge this and under

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
    mode: 'json',
    pythonOptions: ['-u'],
    args: ["loaded", pjson.version]
  }

  pyshell.PythonShell.run('./python/dbCMD.py', cmdDataLoad, function  (err, results)  {
    let leng = Object.keys(results[0]).length;
    for (let i = 0; i < leng; i++){
      
      let append = `<tr>
              <th class="matchID" id="row${leng-i}">${Object.keys(results[0])[leng-i-1]}</th>
              <th class="filename"><p class="hidden">${results[0][leng-i][0]['filename']}</p><button class="replaceImageFilename">...</button></th>
              <th class="players"><p class="replaceTextOpponent">${results[0][leng-i][0]['players']}</p><button class="replaceImageOpponent">...</button></th>
              <th class="decknames"><p class="replaceText">${JSON.stringify(results[0][leng-i][0]['deckNames'][0])}</p><button class="replaceImage">...</button></th>
              <th class="p1Deck"><p class="replaceTextDeck">${JSON.stringify(results[0][leng-i][0]['P1'][0])}</p><button class="replaceImageDeck">...</button></th>
              <th class="p2Deck"><p class="replaceTextDeck">${JSON.stringify(results[0][leng-i][0]['P2'][0])}</p><button class="replaceImageDeck">...</button></th>
              <th class="turnOrder"><p class="replaceTextExtra">${results[0][leng-i][0]['play']}</p><button class="replaceImageExtra">...</button></th>
              <th class="winList"><p class="replaceTextExtra">${results[0][leng-i][0]['winner']}</p><button class="replaceImageExtra">...</button></th>
              <th class="format">${results[0][leng-i][0]['format']}</th>
              <th class="type">${results[0][leng-i][0]['type']}</th>
              <th class="date">${results[0][leng-i][0]['date']}</th>
            </tr>`
      document.getElementById('databaseContent').insertAdjacentHTML('beforeend', append) ;
    }

    if(err)  throw err;
    console.log(results);
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
