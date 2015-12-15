(function() {
	angular.module('app').controller('HistogramController', HistogramController);

	HistogramController.$inject = ['config', 'fileService', 'loadingService', 'pyService'];
	
	function HistogramController(config, fileService, loadingService, pyService) {
		
		var vm = this;
		var py = {};
		
		vm.path = '';
		
		vm.chart = new (function() {
			
			this.series = ['R', 'G', 'B'];
			this.data = [[], [], []];
			this.labels = [];
			
			for (var i = 0; i < 256; i++) {
				if (i == 0 || i == 64 || i == 128 || i == 192 || i == 255) {
					this.labels.push(i);
				} else {
					this.labels.push('');
				}
			}
		})();
		
		var init = function() {
			
			vm.src = config.srcEmpty;
			
			if (fileService.input != '') {
				
				fileService.isReadable('histogram.json')
					.then(function() {
						laksanakan();
					})
					.catch(function(error) {
						
						var py = pyService.run([
							'histogram',
							fileService.input,
							fileService.id,
						]);
						
						py.promise.finally(function() {
							laksanakan();
						});
						
						loadingService.show()
							.catch(function() {
								pyService.kill(py.shell);
								fileService.clear();
							});
					});
			}
		};
		
		var laksanakan = function() {
			
			var histogram = require(fileService.dir()+'histogram.json');
			
			vm.chart.data[0] = histogram.r;
			vm.chart.data[1] = histogram.g;
			vm.chart.data[2] = histogram.b;
			
			vm.path = fileService.input;
			vm.src = 'file://'+fileService.input;
			
			loadingService.hide();
		};
		
		vm.onFileChanged = function() {
			fileService.load(vm.path);
			init();
		};
		
		init();
	}
})();