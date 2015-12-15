(function() {
	angular.module('app').controller('HistogramController', HistogramController);

	HistogramController.$inject = ['mainService', 'pyService'];
	
	function HistogramController(mainService, pyService) {
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
			vm.src = mainService.srcEmpty;
			
			if (mainService.file.input != '') {
				mainService.file.readable('histogram.json')
					.then(function() {
						laksanakan();
					})
					.catch(function(error) {
						var py = pyService.run([
							'histogram',
							mainService.file.input,
							mainService.file.id,
						]);
						
						py.promise.finally(function() {
							laksanakan();
						});
						
						mainService.loading.show()
							.catch(function() {
								pyService.kill(py.shell);
								mainService.file.clear();
							});
					});
			}
		};
		
		var laksanakan = function() {
			var histogram = require(mainService.file.dir()+'histogram.json');
			
			vm.chart.data[0] = histogram.r;
			vm.chart.data[1] = histogram.g;
			vm.chart.data[2] = histogram.b;
			
			vm.path = mainService.file.input;
			vm.src = 'file://'+mainService.file.input;
			
			mainService.loading.hide();
		};
		
		vm.onFileChanged = function() {
			mainService.file.load(vm.path);
			init();
		};
		
		init();
	}
})();