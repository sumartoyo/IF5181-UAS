(function() {
	angular.module('app').controller('BinaryController', BinaryController);

	BinaryController.$inject = ['config', 'fileService', 'pyService'];
	
	function BinaryController(config, fileService, pyService) {
		
		var vm = this;
		
		var init = function() {
			vm.srcGray = config.srcEmpty;
			vm.srcBinary = config.srcEmpty;
			pyService.call('binary.jpg', 'otsu').then(laksanakan);
		};
		
		var laksanakan = function() {
			vm.srcGray = 'file://'+fileService.dir()+'gray.jpg';
			vm.srcBinary = 'file://'+fileService.dir()+'binary.jpg';
		};
		
		init();
	}
})();