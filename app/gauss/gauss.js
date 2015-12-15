(function() {
	angular.module('app').controller('GaussController', GaussController);

	GaussController.$inject = ['config', 'fileService', 'pyService'];
	
	function GaussController(config, fileService, pyService) {
		
		var vm = this;
		
		var init = function() {
			vm.src = config.srcEmpty;
			vm.srcGauss = config.srcEmpty;
			pyService.call('gauss.jpg', 'gauss').then(laksanakan);
		};
		
		var laksanakan = function() {
			vm.src = 'file://'+fileService.input;
			vm.srcGauss = 'file://'+fileService.dir()+'gauss.jpg';
		};
		
		init();
	}
})();