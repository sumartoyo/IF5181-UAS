(function() {
	angular.module('app').controller('OcrController', OcrController);

	OcrController.$inject = ['config', 'fileService', 'pyService'];
	
	function OcrController(config, fileService, pyService) {
		
		var vm = this;
		
		vm.result = {};
		
		var init = function() {
			vm.src = config.srcEmpty;
			pyService.call('ocr-result.json', 'ocr').then(laksanakan);
		};
		
		var laksanakan = function() {
			vm.src = 'file://'+fileService.input;
			vm.result = require(fileService.dir()+'ocr-result.json');
		};
		
		init();
	}
})();