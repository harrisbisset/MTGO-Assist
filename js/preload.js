window.addEventListener('DOMContentLoaded', () => {
    
    var pyshell =  require('python-shell');
    
    let args = {
      mode: 'text',
      pythonOptions: ['-u'],
      args: [checkUserExists]
    }
    
    pyshell.PythonShell.run('./python/dbCMD.py', args, function  (err, results)  {
      if  (err)  throw err;
      console.log('dbCMD.py finished.');
    });
    
    //i have no idea what this does
    const replaceText = (selector, text) => {
      const element = document.getElementById(selector)
      if (element) element.innerText = text
    }
  
    for (const type of ['chrome', 'node', 'electron']) {
      replaceText(`${type}-version`, process.versions[type])
    }

  })
  
