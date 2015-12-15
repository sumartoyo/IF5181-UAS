(function() {
	angular.module('app').factory('pyService', pyService);
	
	function pyService(config, $q) {
		return new (function() {
			var self = this;
			var PythonShell = require('python-shell');
			
			PythonShell.defaultOptions = config.py.defaultOptions;
			
			self.run = function(args) {
				var result = { };
				result.promise = $q(function(resolve, reject) {
					result.shell = PythonShell.run(PythonShell.defaultOptions.script, {
						args: args
					}, function(err, results) {
						if (err) { // terjadi error
							if (!result.shell.childProcess.killed) { // not manually killed
								console.error(err);
								reject(err);
							}
						} else {
							resolve(results);
						}
					});
				});
				return result;
			}
			
			self.kill = function(shell) {
				shell.childProcess.kill('SIGINT');
			};
		})();
	}
})();