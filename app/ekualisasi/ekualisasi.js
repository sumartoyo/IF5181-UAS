(function() {
	angular.module('app').controller('EkualisasiController', EkualisasiController);
	
	EkualisasiController.$inject = ['config', 'fileService', 'loadingService', 'pyService'];

	function EkualisasiController(config, fileService, loadingService, pyService) {
		
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
			
			vm.srcGray = config.srcEmpty;
			vm.srcEqualized = config.srcEmpty;
			
			if (fileService.input != '') {
				
				fileService.isReadable('histogram_equalized.json')
					.then(function() {
						laksanakan();
					})
					.catch(function(error) {
						
						var py = pyService.run([
							'equalize',
							fileService.input,
							fileService.id,
						]);
						
						py.promise.finally(function() {
							laksanakan();
						});
						
						loadingService.show()
							.catch(function() {
								pyService.kill(py.shell);
							});
					});
			}
		};
		
		var laksanakan = function() {
			
			var histGray = require(fileService.dir()+'histogram_gray.json');
			var histEqualized = require(fileService.dir()+'histogram_equalized.json');
			
			vm.chart.gray.data[0] = histGray;
			vm.chart.equalized.data[0] = histEqualized;
			
			vm.srcGray = 'file://'+fileService.dir()+'gray.jpg';
			vm.srcEqualized = 'file://'+fileService.dir()+'equalized.jpg';
			
			loadingService.hide();
		};
		
		init();
	}
})();