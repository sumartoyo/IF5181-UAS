(function() {
	angular.module('app').controller('BinaryController', BinaryController);

	BinaryController.$inject = ['config', 'fileService', 'loadingService', 'pyService'];
	
	function BinaryController(config, fileService, loadingService, pyService) {
		
		var vm = this;
		
		var init = function() {
			
			vm.srcGray = config.srcEmpty;
			vm.srcBinary = config.srcEmpty;
			
			if (fileService.input != '') {
				
				fileService.isReadable('binary.jpg')
					.then(function() {
						laksanakan();
					})
					.catch(function(error) {
						
						var py = pyService.run([
							'otsu',
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
			
			vm.srcGray = 'file://'+fileService.dir()+'gray.jpg';
			vm.srcBinary = 'file://'+fileService.dir()+'binary.jpg';
			
			loadingService.hide();
		};
		
		init();
	}
})();