(function() {
	angular.module('app').controller('GaussController', GaussController);

	GaussController.$inject = ['$scope', 'mainService'];
	
	function GaussController($scope, mainService) {
		var vm = this;
		
		var init = function() {
			vm.src = mainService.srcEmpty;
			vm.srcGauss = mainService.srcEmpty;
			
			if (mainService.file.input != '') {
				// setup loading
				mainService.loading.onCanceled = function() {
					py.kill(shell);
				};
				
				// laksanakan
				function laksanakan() {
					$scope.$apply(function() {
						vm.src = 'file://'+mainService.file.input;
						vm.srcGauss = 'file://'+mainService.file.dir()+'gauss.jpg';
						
						mainService.loading.hide();
					});
				}
				
				// call python
				mainService.file.readable('gauss.jpg', function(err) {
					if (err) {
						mainService.loading.show();
						
						shell = py.run([
							'gauss',
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