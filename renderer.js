function runPython(){
    var pyshell =  require('python-shell');

    pyshell.PythonShell.run('sync.py', null, function  (err, results)  {
      if  (err)  throw err;
      console.log('sync.py finished.');
    });
}

document.querySelector('#pyBtnSync').addEventListener('click', () => {
    
    //
    document.getElementById('#pyBtnSync').style.display = "none"
    
    //run pythonfile that grabs user preference data from db
    //runPython(autoLogin = T/F, userName = '', password = '', )
    runPython()
    
    //
    document.getElementById('#pyBtnSync').style.display = "block"
})
