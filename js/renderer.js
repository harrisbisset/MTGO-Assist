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
    mode: 'text',
    pythonOptions: ['-u'],
    args: ["loaded", pjson.version]
  }

  pyshell.PythonShell.run('./python/dbCMD.py', cmdDataLoad, function  (err, results)  {
    let leng = results.length;

    for (let i = 0; i < results.length; i++){
      let append = `<tr>
              <th class="matchID" id="row${leng-i-1}">${results[leng-i-1][0]}</th>
              <th class="filename"><p class="hidden">${results[leng-i-1][1]}</p><button class="replaceImageFilename">...</button></th>
              <th class="players"><p class="replaceTextOpponent">${results[leng-i-1][2]}</p><button class="replaceImageOpponent">...</button></th>
              <th class="decknames"><p class="replaceText">${results[leng-i-1][3]}</p><button class="replaceImage">...</button></th>
              <th class="p1Deck"><p class="replaceTextDeck">${results[leng-i-1][4]}</p><button class="replaceImageDeck">...</button></th>
              <th class="p2Deck"><p class="replaceTextDeck">${results[leng-i-1][5]}</p><button class="replaceImageDeck">...</button></th>
              <th class="turnOrder"><p class="replaceTextExtra">${results[leng-i-1][6]}</p><button class="replaceImageExtra">...</button></th>
              <th class="winList"><p class="replaceTextExtra">${results[leng-i-1][7]}</p><button class="replaceImageExtra">...</button></th>
              <th class="format">${results[leng-i-1][8]}</th>
              <th class="type">${results[leng-i-1][9]}</th>
              <th class="date">${results[leng-i-1][10]}</th>
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
