(function() {
	angular.module('app').controller('GaussController', GaussController);

	GaussController.$inject = ['config', 'fileService', 'loadingService', 'pyService'];
	
	function GaussController(config, fileService, loadingService, pyService) {
		
		var vm = this;
		
		var init = function() {
			
			vm.src = config.srcEmpty;
			vm.srcGauss = config.srcEmpty;
			
			if (fileService.input != '') {
				
				fileService.isReadable('gauss.jpg')
					.then(function() {
						laksanakan();
					})
					.catch(function(error) {
						
						var py = pyService.run([
							'gauss',
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
			
			vm.src = 'file://'+fileService.input;
			vm.srcGauss = 'file://'+fileService.dir()+'gauss.jpg';
			
			loadingService.hide();
		};
		
		init();
	}
})();