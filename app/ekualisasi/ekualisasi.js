(function() {
	angular.module('app').controller('EkualisasiController', EkualisasiController);
	
	EkualisasiController.$inject = ['$scope', 'mainService'];

	function EkualisasiController($scope, mainService) {
		var vm = this;
		var shell = {};
		
		function createChart(name) {
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
		}
		
		vm.chart = {
			gray: new createChart('Grayscale'),
			equalized: new createChart('Equalized'),
		};
		
		var init = function() {
			vm.srcGray = mainService.srcEmpty;
			vm.srcEqualized = mainService.srcEmpty;
			
			if (mainService.file.input != '') {
				// setup loading
				mainService.loading.onCanceled = function() {
					py.kill(shell);
				};
				
				// laksanakan
				function laksanakan() {
					$scope.$apply(function() {
						var histGray = require(mainService.file.dir()+'histogram_gray.json');
						var histEqualized = require(mainService.file.dir()+'histogram_equalized.json');
						
						vm.chart.gray.data[0] = histGray;
						vm.chart.equalized.data[0] = histEqualized;
						
						vm.srcGray = 'file://'+mainService.file.dir()+'gray.jpg';
						vm.srcEqualized = 'file://'+mainService.file.dir()+'equalized.jpg';
						
						mainService.loading.hide();
					});
				}
				
				// call python
				mainService.file.readable('histogram_equalized.json', function(err) {
					if (err) {
						mainService.loading.show();
						
						shell = py.run([
							'equalize',
							mainService.file.input,
							mainService.file.id,
						], undefined, undefined, function() {
							laksanakan();
						});
					} else {
						laksanakan();
					}
				});
			}
		};
		
		init();
	}
})();