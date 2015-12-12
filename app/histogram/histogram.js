(function() {
	angular.module('app').controller('HistogramController', HistogramController);

	HistogramController.$inject = ['$scope', 'mainService'];
	
	function HistogramController($scope, mainService) {
		var vm = this;
		var shell = {};
		
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
			if (mainService.file.input != '') {
				// setup loading
				mainService.loading.onCanceled = function() {
					$scope.$apply(function() {
						py.kill(shell);
						mainService.file.clear();
					});
				};
				
				// laksanakan
				function laksanakan() {
					$scope.$apply(function() {
						var histogram = require(mainService.file.dir()+'histogram.json');
						
						vm.chart.data[0] = histogram.r;
						vm.chart.data[1] = histogram.g;
						vm.chart.data[2] = histogram.b;
						
						$('#img').attr('src', 'file://'+mainService.file.input);
						
						mainService.loading.hide();
					});
				}
				
				// call python
				mainService.file.readable('histogram.json', function(err) {
					if (err) {
						mainService.loading.show();
						
						shell = py.run([
							'histogram',
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
		
		vm.onFileChanged = function() {
			$('#img').removeAttr('src');
			mainService.file.load(vm.path);
			init();
		};
		
		init();
	}
})();