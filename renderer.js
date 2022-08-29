function runPython(){
    var pyshell =  require('python-shell');

    pyshell.PythonShell.run('sync.py', null, function  (err, results)  {
      if  (err)  throw err;
      console.log('sync.py finished.');
    });
}

document.querySelector('#pyBtnSync').addEventListener('click', () => {
    //run pythonfile that grabs user preference data from db
    //runPython(autoLogin = T/F, userName = '', password = '', )
    runPython()
})
