(function() {
	angular.module('app').factory('mainService', mainService);
	
	function mainService($q) {
		return new (function() {
			var self = this;
			
			self.srcEmpty = 'img/empty.png';
			
			self.file = new (function() {
				var file = this;
				var fs = require('fs');
				
				file.clear = function() {
					file.id = '';
					file.input = '';
				};
				
				file.load = function(path) {
					file.id = (new Date()).getTime() + '.' + Math.random();
					file.input = path;
				};
				
				file.dir = function() {
					return (process.env.HOME || process.env.USERPROFILE) + '\\.IF5181-dimas\\' + file.id + '\\';
				};
				
				file.readable = function(name) {
					return $q(function(resolve, reject) {
						fs.access(file.dir()+name, fs.R_OK, function(error) {
							if (error) {
								reject(error);
							} else {
								resolve();
							}
						});
					});
				};
				
				file.clear();
			})();
			
			self.loading = new (function() {
				var loading = this;
				var element = $('#modalLoading');
				
				loading.onCanceled = function() { };
				
				loading.show = function() {
					element.modal('show');
					
					return $q(function(resolve, reject) {
						loading.onCanceled = function() {
							loading.hide();
							reject();
						};
					});
				};
				
				loading.hide = function() {
					element.modal('hide');
				};
				
				$('#modalCancel').click(function() {
					loading.onCanceled();
				});
			})();
		})();
	}
})();