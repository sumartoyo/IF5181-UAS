(function() {
	angular.module('app').factory('fileService', fileService);
	
	function fileService($q) {
		return new (function() {
			var self = this;
			
			var fs = require('fs');
				
			self.clear = function() {
				self.id = '';
				self.input = '';
			};
			
			self.load = function(path) {
				self.id = (new Date()).getTime() + '.' + Math.random();
				self.input = path;
			};
			
			self.dir = function() {
				return (process.env.HOME || process.env.USERPROFILE) + '\\.IF5181\\' + self.id + '\\';
			};
			
			self.isReadable = function(name) {
				return $q(function(resolve, reject) {
					fs.access(self.dir()+name, fs.R_OK, function(error) {
						if (error) {
							reject(error);
						} else {
							resolve();
						}
					});
				});
			};
			
			self.clear();
		})();
	}
})();