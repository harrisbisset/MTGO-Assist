function runPythonSync(){
    var pyshell =  require('python-shell');
    var pjson = require('./package.json');

    let options = {
      mode: 'text',
      pythonOptions: ['-u'],
      args: [pjson.version]
    }

    pyshell.PythonShell.run('./python/sync.py', options, function  (err, results)  {
      if (err)  throw err;
      console.log('sync.py finished.');
    });
}

//merge this and under

function loadNextPage(){
    var pyshell =  require('python-shell');
    var pjson = require('./package.json');

    let options = {
      mode: 'text',
      pythonOptions: ['-u'],
      args: ["nextPage", pjson.version]
    }

    pyshell.PythonShell.run('./python/dbCMD.py', options, function  (err, results)  {

      //append to table

      if(err)  throw err;
      console.log('loaded next page');
    });
}

function loadFirstPage(){
  var pyshell =  require('python-shell');
  var pjson = require('./package.json');

  let options = {
    mode: 'json',
    pythonOptions: ['-u'],
    args: ["loaded", pjson.version]
  }

  pyshell.PythonShell.run('./python/dbCMD.py', options, function  (err, results)  {
    console.log(results);
    let keys = Object.keys(results[0])
    if (results){
      let leng = Object.keys(results[0]).length;
      for (let i = 0; i < leng; i++){

        let append = `<tr>
                <th class="matchID" id="row${i}">${Object.keys(results[0])[i]}</th>
                <th class="filename"><p class="hidden">${results[0][keys[leng-i-1]][0]['filename']}</p><button class="replaceImageFilename">...</button></th>
                <th class="players"><p class="replaceTextOpponent">${results[0][keys[leng-i-1]][0]['players'][0]}</p><button class="replaceImageOpponent">...</button></th>
                <th class="decknames"><p class="replaceText">${JSON.stringify(results[0][keys[leng-i-1]][0]['deckNames'][0]).replace(/[[\]]|"|{|}/g, '').replace(/:/g, ': ').replace(/,/g, '<br>')}</p><button class="replaceImage">...</button></th>
                <th class="p1Deck"><p class="replaceTextDeck">${structureDecklist(results, keys, leng, i, 'P1')}</p><button class="replaceImageDeck">...</button></th>
                <th class="p2Deck"><p class="replaceTextDeck">${structureDecklist(results, keys, leng, i, 'P2')}</p><button class="replaceImageDeck">...</button></th>
                <th class="turnOrder"><p class="replaceTextExtra">${JSON.stringify(results[0][keys[leng-i-1]][0]['play']).replace(',','<br>').replace(/[[\]]|"/g, '')}</p><button class="replaceImageExtra">...</button></th>
                <th class="winList"><p class="replaceTextExtra">${JSON.stringify(results[0][keys[leng-i-1]][0]['winner']).replace(',','<br>').replace(/[[\]]|"/g, '')}</p><button class="replaceImageExtra">...</button></th>
                <th class="format">${results[0][keys[leng-i-1]][0]['format']}</th>
                <th class="type">${results[0][keys[leng-i-1]][0]['type']}</th>
                <th class="date">${JSON.stringify(results[0][keys[leng-i-1]][0]['date']).replace('"','').split(' ')[0]}</th>
              </tr>`
        document.getElementById('databaseContent').insertAdjacentHTML('beforeend', append);
      }
    }
    if(err) throw err;
  });
}

function structureDecklist(results, keys, leng, i, player){
  let deck = JSON.stringify(results[0][keys[leng-i-1]][0][player][0]).replace(/[[\]]|"|{|}/g, '').split(/:|,/g)
  let res = ''
  for (let b = 0; b < deck.length; b++){
    if (b % 2 == 0){
      res += deck[b+1] + ' ' + deck[b] + '<br>'
    }
  }
  return res
}

function loadProfile(){
  document.getElementById('mid').style.display = 'none';
  document.getElementById('bottom').style.display = 'none';
  document.getElementById('lowHeader').style.display = 'none';
  document.getElementById('profile').style.display = 'block';

  var pyshell =  require('python-shell');
  var pjson = require('./package.json');

  let options = {
    mode: 'json',
    pythonOptions: ['-u'],
    args: ["profile", pjson.version]
  }

  pyshell.PythonShell.run('./python/dbCMD.py', options, function  (err, results)  {
    
    if(err) throw err;
  });
}

function closeProfile(){
  document.getElementById('mid').style.display = 'block';
  document.getElementById('bottom').style.display = 'block';
  document.getElementById('lowHeader').style.display = 'block';
  document.getElementById('profile').style.display = 'none';
}

document.querySelector('#pyBtnProfile').addEventListener('click', () => {
  loadProfile();
})

document.querySelector('#close').addEventListener('click', () => {
  closeProfile();
})

document.querySelector('#pyBtnSync').addEventListener('click', () => {
  runPythonSync();
})

document.querySelector('#pyBtnNextPage').addEventListener('click', () => {
  loadNextPage();
})

document.addEventListener('DOMContentLoaded', () =>{
  loadFirstPage();
})
