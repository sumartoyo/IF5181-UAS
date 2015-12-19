(function() {
	angular.module('app').controller('FaceRecognitionController', FaceRecognitionController);

	FaceRecognitionController.$inject = ['config', 'fileService', 'pyService'];
	
	function FaceRecognitionController(config, fileService, pyService) {
		
		var vm = this;
		
		vm.result = {};
		
		var init = function() {
			vm.src = config.srcEmpty;
			pyService.call('face-result.json', 'face-recognition').then(laksanakan);
		};
		
		var laksanakan = function() {
			vm.src = 'file://'+fileService.input;
			vm.result = require(fileService.dir()+'face-result.json');
		};
		
		init();
	}
})();