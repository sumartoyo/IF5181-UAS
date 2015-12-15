(function() {
	angular.module('app').controller('BinaryController', BinaryController);

	BinaryController.$inject = ['mainService', 'pyService'];
	
	function BinaryController(mainService, pyService) {
		var vm = this;
		
		var init = function() {
			vm.srcGray = mainService.srcEmpty;
			vm.srcBinary = mainService.srcEmpty;
			
			if (mainService.file.input != '') {
				mainService.file.readable('binary.jpg')
					.then(function() {
						laksanakan();
					})
					.catch(function(error) {
						var py = pyService.run([
							'otsu',
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
			vm.srcGray = 'file://'+mainService.file.dir()+'gray.jpg';
			vm.srcBinary = 'file://'+mainService.file.dir()+'binary.jpg';
			
			mainService.loading.hide();
		};
		
		init();
	}
})();