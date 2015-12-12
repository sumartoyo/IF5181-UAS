var py = new (function() {
	var PythonShell = require('python-shell');
	
	PythonShell.defaultOptions = {
		pythonPath: 'C:\\exe\\WinPython\\python-2.7.10.amd64\\python.exe',
		script: 'py\\api.py',
	};

	this.run = function(args, done, fail, always) {
		var shell = PythonShell.run(PythonShell.defaultOptions.script, {
			args: args
		}, function(err, results) {
			if (err) { // terjadi error
				if (!shell.childProcess.killed) { // not manually killed
					console.error(err);
					if (typeof fail === 'function') {
						fail(err);
					}
				}
			} else {
				if (typeof done === 'function') {
					done(results);
				}
			}
			
			if (typeof always === 'function') {
				always();
			}
		});
		
		return shell;
	}
	
	this.kill = function(shell) {
		shell.childProcess.kill('SIGINT');
	};
})();