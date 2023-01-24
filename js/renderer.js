//not sure if needed
window.$ = window.jQuery = require('jquery');

function runPythonSync(){
    var pyshell =  require('python-shell');
    var highestRecordID

    let syncDataLoad = {
      mode: 'text',
      pythonOptions: ['-u'],
      args: [highestRecordID]
    }

    pyshell.PythonShell.run('./python/sync.py', syncDataLoad, function  (err, results)  {

      //if 'unconnectedInt returned'
      if (results[0] === "unconnected") {
        
      } else if (results[0] === "license") {
        const Dialogs = require('dialogs')
        const dialogs = Dialogs()
        dialogs.alert('Please close the end user license agreement!', ok =>{})
      } else if (results[0] === "unOpened") {
        console.log(results[0])
        const Dialogs = require('dialogs')
        const dialogs = Dialogs()
        dialogs.alert('Please open the program!', ok =>{})
      }
      if  (err)  throw err;
      console.log('sync.py finished.');
    });
}

function runPythonDB(){
    var pyshell =  require('python-shell');
    var pjson = require('./package.json');

    let cmdDataLoad = {
      mode: 'text',
      pythonOptions: ['-u'],
      args: ["loaded", pjson.version]
    }

    pyshell.PythonShell.run('./python/dbCMD.py', cmdDataLoad, function  (err, results)  {
      
      if (results[2] === "unconnectedInt"){
        unInt();
      }else if (results[2] === "connectedInt"){
        //hides reload button
        document.getElementById('#btnReload').style.display = "none";
          
        //should also show sync button (set it to hidden first)
      }

      if(err)  throw err;
      console.log('dbCMD.py finished.');
      console.log('results: ', results);
    });
}

document.querySelector('#pyBtnSync').addEventListener('click', () => {
    //runs dbCMD that grabs user preference data from db
    //runPython(autoLogin = T/F, userName = '', password = '', )

    //runs main program
    runPythonSync();
})

document.querySelector('#btnReload').addEventListener('click', () => {
  runPythonDB();
})

document.addEventListener('DOMContentLoaded', () =>{
  runPythonDB();
})
