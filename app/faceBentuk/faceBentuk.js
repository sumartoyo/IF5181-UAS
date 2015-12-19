(function() {
	angular.module('app').controller('FaceBentukController', FaceBentukController);

	FaceBentukController.$inject = ['config', 'fileService', 'pyService'];
	
	function FaceBentukController(config, fileService, pyService) {
		
		var vm = this;
		
		var init = function() {
			vm.srcLimatitik = config.srcEmpty;
			vm.srcTitikobjek = config.srcEmpty;
			pyService.call('face-limatitik.jpg', 'face-bentuk').then(laksanakan);
		};
		
		var laksanakan = function() {
			vm.srcLimatitik = 'file://'+fileService.dir()+'face-limatitik.jpg';
			vm.srcTitikobjek = 'file://'+fileService.dir()+'face-titikobject.jpg';
		};
		
		init();
	}
})();