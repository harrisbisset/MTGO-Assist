
function runPythonSync(){
    var pyshell =  require('python-shell');

    pyshell.PythonShell.run('./python/sync.py', null, function  (err, results)  {
      if  (err)  throw err;
      console.log('sync.py finished.');
    });
}

function runPythonDB(){
    var pyshell =  require('python-shell');
    var pjson = require('./package.json');

    let opDataLoad = {
      args: ["loaded", pjson.version]
    }

    pyshell.PythonShell.run('./python/dbCMD.py', opDataLoad, function  (err, results)  {
      if (results == "createdDB"){
        const { BrowserWindow } = require('electron')
        const winInput = new BrowserWindow({ show: false })
        winInput.loadFile('./forms/inputUserData.html')
        winInput.once('ready-to-show', () => {
          winInput.show()
        })
      }

      if  (err)  throw err;
        console.log('dbCMD.py finished.');
    });
}

document.querySelector('#pyBtnSync').addEventListener('click', () => {
    //run pythonfile that grabs user preference data from db
    //runPython(autoLogin = T/F, userName = '', password = '', )
    runPythonSync()
})

document.addEventListener('DOMContentLoaded', () =>{
    runPythonDB()
})
