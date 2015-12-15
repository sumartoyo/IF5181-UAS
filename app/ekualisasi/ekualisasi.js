(function() {
	angular.module('app').controller('EkualisasiController', EkualisasiController);
	
	EkualisasiController.$inject = ['mainService', 'pyService'];

	function EkualisasiController(mainService, pyService) {
		var vm = this;
		var shell = {};
		
		var createChart = function(name) {
			this.series = [name];
			this.data = [[]];
			this.labels = [];
			
			for (var i = 0; i < 256; i++) {
				if (i == 0 || i == 64 || i == 128 || i == 192 || i == 255) {
					this.labels.push(i);
				} else {
					this.labels.push('');
				}
			}
		};
		
		vm.chart = {
			gray: new createChart('Grayscale'),
			equalized: new createChart('Equalized'),
		};
		
		var init = function() {
			vm.srcGray = mainService.srcEmpty;
			vm.srcEqualized = mainService.srcEmpty;
			
			if (mainService.file.input != '') {
				mainService.file.readable('histogram_equalized.json')
					.then(function() {
						laksanakan();
					})
					.catch(function(error) {
						var py = pyService.run([
							'equalize',
							mainService.file.input,
							mainService.file.id,
						]);
						
						py.promise.finally(function() {
							laksanakan();
						});
						
						mainService.loading.show()
							.catch(function() {
								pyService.kill(py.shell);
							});
					});
			}
		};
		
		var laksanakan = function() {
			var histGray = require(mainService.file.dir()+'histogram_gray.json');
			var histEqualized = require(mainService.file.dir()+'histogram_equalized.json');
			
			vm.chart.gray.data[0] = histGray;
			vm.chart.equalized.data[0] = histEqualized;
			
			vm.srcGray = 'file://'+mainService.file.dir()+'gray.jpg';
			vm.srcEqualized = 'file://'+mainService.file.dir()+'equalized.jpg';
			
			mainService.loading.hide();
		};
		
		init();
	}
})();