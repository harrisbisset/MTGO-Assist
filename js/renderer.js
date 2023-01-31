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
    args: ["loadFirstPage", pjson.version]
  }

  pyshell.PythonShell.run('./python/dbCMD.py', cmdDataLoad, function  (err, results)  {

    //append to table

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
