(function() {
	angular.module('app').controller('GaussController', GaussController);

	GaussController.$inject = ['mainService', 'pyService'];
	
	function GaussController(mainService, pyService) {
		var vm = this;
		
		var init = function() {
			vm.src = mainService.srcEmpty;
			vm.srcGauss = mainService.srcEmpty;
			
			if (mainService.file.input != '') {
				mainService.file.readable('gauss.jpg')
					.then(function() {
						laksanakan();
					})
					.catch(function(error) {
						var py = pyService.run([
							'gauss',
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
			vm.src = 'file://'+mainService.file.input;
			vm.srcGauss = 'file://'+mainService.file.dir()+'gauss.jpg';
			
			mainService.loading.hide();
		};
		
		init();
	}
})();