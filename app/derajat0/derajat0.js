(function() {
	angular.module('app').controller('Derajat0Controller', Derajat0Controller);

	Derajat0Controller.$inject = ['config', 'fileService', 'pyService'];
	
	function Derajat0Controller(config, fileService, pyService) {
		
		var vm = this;
		
		var init = function() {
			vm.srcGray = config.srcEmpty;
			vm.srcAverage = config.srcEmpty;
			vm.srcHomogen = config.srcEmpty;
			vm.srcDifference = config.srcEmpty;
			pyService.call('derajat0-average.jpg', 'derajat0').then(laksanakan);
		};
		
		var laksanakan = function() {
			vm.srcGray = 'file://'+fileService.dir()+'gray.jpg';
			vm.srcAverage = 'file://'+fileService.dir()+'derajat0-average.jpg';
			vm.srcHomogen = 'file://'+fileService.dir()+'derajat0-homogen.jpg';
			vm.srcDifference = 'file://'+fileService.dir()+'derajat0-difference.jpg';
		};
		
		init();
	}
})();