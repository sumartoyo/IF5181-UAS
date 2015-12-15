(function() {
	angular.module('app').controller('EkualisasiController', EkualisasiController);
	
	EkualisasiController.$inject = ['config', 'fileService', 'pyService'];

	function EkualisasiController(config, fileService, pyService) {
		
		var vm = this;
		
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
			pyService.call('histogram_equalized.json', 'equalize').then(laksanakan);
		};
		
		var laksanakan = function() {
			
			var histGray = require(fileService.dir()+'histogram_gray.json');
			var histEqualized = require(fileService.dir()+'histogram_equalized.json');
			
			vm.chart.gray.data[0] = histGray;
			vm.chart.equalized.data[0] = histEqualized;
			
			vm.srcGray = 'file://'+fileService.dir()+'gray.jpg';
			vm.srcEqualized = 'file://'+fileService.dir()+'equalized.jpg';
		};
		
		init();
	}
})();