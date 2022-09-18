window.$ = window.jQuery = require('jquery');

function runPythonSync(){
    var pyshell =  require('python-shell');

    pyshell.PythonShell.run('./python/sync.py', null, function  (err, results)  {

      //if 'unconnectedInt returned'
      if (results[1] == "unconnectedInt") {
        unInt()
      }
      if  (err)  throw err;
      console.log('sync.py finished.');
    });
}

function runPythonCreateUser(userName, userPass, mtgoName, mtgoPass){
  var pyshell =  require('python-shell');
  
  let opDataLoad = {
    mode: 'text',
    pythonOptions: ['-u'],
    args: ['createUser', userName, userPass, mtgoName, mtgoPass]
  }
  pyshell.PythonShell.run('./python/dbCMD.py', opDataLoad, function  (err, results)  {
      if  (err)  throw err;
      console.log('dbCMD.py finished.');
      console.log('results: ', results);
    });
}

function runPythonDB(){
    var pyshell =  require('python-shell');
    var pjson = require('./package.json');

    let opDataLoad = {
      mode: 'text',
      pythonOptions: ['-u'],
      args: ["loaded", pjson.version]
    }

    pyshell.PythonShell.run('./python/dbCMD.py', opDataLoad, function  (err, results)  {

      //if the table userDetails doesn't exist, then renderer.js prompts the user to enter them
      if (results[0] === "unconnectedDB"){
        const Dialogs = require('dialogs')
        const dialogs = Dialogs()
        dialogs.confirm('Please create account for MTGO Assist', ok => {
          console.log('result:', ok);
          if (ok !== undefined) {
            dialogs.prompt('Username', ok => {
              console.log('result:', ok);
              var userName = ok
              if (ok !== undefined) {
                dialogs.promptPassword('Password', ok => {
                  console.log('result:', ok);
                  var userPass = ok
                  if (ok !== undefined) {
                  dialogs.alert('Account Created', ok =>{

                    //linking an MTGO account is optional
                      dialogs.confirm('Would you like to link your MTGO account?', ok => {
                        console.log('result:', ok);
                        if (ok !== undefined) {
                          dialogs.prompt('Username', ok => {
                            console.log('result:', ok);
                            var mtgoName = ok
                            if (ok !== undefined) {
                              dialogs.promptPassword('Password', ok => {
                                console.log('result:', ok);
                                var mtgoPass = ok
                                dialogs.alert('Account Linked', ok =>{

                                  //sends data to db
                                  runPythonCreateUser(userName, userPass, mtgoName, mtgoPass);
                                });
                              });
                            };
                          });
                        }else if(ok === undefined){
                          runPythonCreateUser(userName, userPass, "", "");
                        }
                      });
                    });
                  };
                });
              };
            });
          };
        });
      };
      
      if (results[2] === "unconnectedInt"){
        unInt();
      }else if (results[2] === "connectedInt"){
        //hides reload button
        document.getElementById('#btnReload').style.display = "none";
      }

      if(err)  throw err;
      console.log('dbCMD.py finished.');
      console.log('results: ', results);
    });
}

function unInt(){
  //disables user's ability to run the main program, as it requires interent access, until internet connection is established
  document.getElementById('#pyBtnSync').style.display = "none";
  document.getElementById('#btnReload').style.display = "block";
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
