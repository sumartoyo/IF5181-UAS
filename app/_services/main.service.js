var varMainService = {};

(function() {
	angular.module('app').factory('mainService', mainService);
	
	function mainService() {
		return new (function() {
			var self = this;
			varMainService = self;
			
			self.file = new (function() {
				var file = this;
				var os = require('os');
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
					// return os.tmpDir() + '\\' + file.id + '\\';
					return 'D:\\Kuliah\\pola\\uas\\py\\' + file.id + '\\';
				};
				
				file.readable = function(name, callback) {
					fs.access(file.dir()+name, fs.R_OK, callback);
				};
				
				file.clear();
			})();
			
			self.loading = new (function() {
				var loading = this;
				var element = $('#modalLoading');
				
				loading.onCanceled = function() { };
				
				loading.show = function() {
					element.modal('show');
				};
				
				loading.hide = function() {
					element.modal('hide');
				};
				
				$('#modalCancel').click(function() {
					var canceled = loading.onCanceled();
					
					if (canceled !== false) {
						loading.hide();
					}
				});
			})();
		})();
	}
})();