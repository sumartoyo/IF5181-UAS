(function() {
	angular.module('app').factory('pyService', pyService);
	
	function pyService(config, $q, fileService, loadingService) {
		
		return new (function() {
			
			var self = this;
			var PythonShell = require('python-shell');
			
			PythonShell.defaultOptions = config.py.defaultOptions;
			
			var run = function(args) {
				
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
			
			var kill = function(shell) {
				shell.childProcess.kill('SIGINT');
			};
			
			var done = function(resolve) {
				loadingService.hide();
				resolve();
			};
			
			self.call = function(fileCheck, command) {
				
				return $q(function(resolve, reject) {
					
					if (fileService.input != '') {
						
						fileService.isReadable(fileCheck)
							.then(function() {
								done(resolve)
							})
							.catch(function(error) {
								
								var py = run([
									command,
									fileService.input,
									fileService.id,
								]);
								
								py.promise
									.finally(function() {
										done(resolve)
									});
								
								loadingService.show()
									.catch(function() {
										kill(py.shell);
										reject();
									});
							});
					}
				});
			};
		})();
	}
})();