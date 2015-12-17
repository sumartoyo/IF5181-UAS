(function() {
	angular.module('app').controller('SkeletonController', SkeletonController);

	SkeletonController.$inject = ['config', 'fileService', 'pyService'];
	
	function SkeletonController(config, fileService, pyService) {
		
		var vm = this;
		
		vm.identity = '';
		vm.chaincode = [];
		vm.kodebelok = [];
		
		var init = function() {
			vm.srcBinary = config.srcEmpty;
			vm.srcTulang = config.srcEmpty;
			pyService.call('tulang.jpg', 'skeleton').then(laksanakan);
		};
		
		var laksanakan = function() {
			
			vm.srcBinary = 'file://'+fileService.dir()+'binary.jpg';
			vm.srcTulang = 'file://'+fileService.dir()+'tulang.jpg';
			vm.chaincode = require(fileService.dir()+'tulang-chaincode.json');
			vm.kodebelok = require(fileService.dir()+'tulang-kodebelok.json');
			
			var identity = require(fileService.dir()+'tulang-identity.json')
			vm.identity = 'Identitas\n';
			vm.identity += '- Ujung ada '+identity.ujung.length+': ';
			identity.ujung.forEach(function(ujung) {
				vm.identity += '(x='+ujung[1]+', y='+ujung[0]+') ';
			});
			vm.identity += '\n- Simpangan ada '+identity.simpangan.length+': ';
			identity.simpangan.forEach(function(simpangan) {
				vm.identity += '(x='+simpangan[1]+', y='+simpangan[0]+') ';
			});
		};
		
		init();
	}
})();