(function() {
	angular.module('app').controller('ChaincodeController', ChaincodeController);

	ChaincodeController.$inject = ['config', 'fileService', 'pyService'];
	
	function ChaincodeController(config, fileService, pyService) {
		
		var vm = this;
		
		vm.chaincode = [];
		vm.kodebelok = [];
		
		var init = function() {
			vm.srcBinary = config.srcEmpty;
			vm.srcKopong = config.srcEmpty;
			pyService.call('kodebelok.json', 'chaincode').then(laksanakan);
		};
		
		var laksanakan = function() {
			vm.srcBinary = 'file://'+fileService.dir()+'binary.jpg';
			vm.srcKopong = 'file://'+fileService.dir()+'kopong.jpg';
			vm.chaincode = require(fileService.dir()+'chaincode.json');
			vm.kodebelok = require(fileService.dir()+'kodebelok.json');
		};
		
		init();
	}
})();