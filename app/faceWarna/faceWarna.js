(function() {
	angular.module('app').controller('FaceWarnaController', FaceWarnaController);

	FaceWarnaController.$inject = ['config', 'fileService', 'pyService'];
	
	function FaceWarnaController(config, fileService, pyService) {
		
		var vm = this;
		
		var init = function() {
			vm.srcMasker = config.srcEmpty;
			vm.srcKotak = config.srcEmpty;
			pyService.call('face-masker.jpg', 'face-warna').then(laksanakan);
		};
		
		var laksanakan = function() {
			vm.srcMasker = 'file://'+fileService.dir()+'face-masker.jpg';
			vm.srcKotak = 'file://'+fileService.dir()+'face-kotak.jpg';
		};
		
		init();
	}
})();