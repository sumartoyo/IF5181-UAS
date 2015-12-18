(function() {
	angular.module('app').controller('Derajat2Controller', Derajat2Controller);

	Derajat2Controller.$inject = ['config', 'fileService', 'pyService'];
	
	function Derajat2Controller(config, fileService, pyService) {
		
		var vm = this;
		
		var init = function() {
			vm.srcGray = config.srcEmpty;
			vm.srcKirsch = config.srcEmpty;
			vm.srcPrewitt = config.srcEmpty;
			pyService.call('derajat2-kirsch.jpg', 'derajat2').then(laksanakan);
		};
		
		var laksanakan = function() {
			vm.srcGray = 'file://'+fileService.dir()+'gray.jpg';
			vm.srcKirsch = 'file://'+fileService.dir()+'derajat2-kirsch.jpg';
			vm.srcPrewitt = 'file://'+fileService.dir()+'derajat2-prewitt.jpg';
		};
		
		init();
	}
})();