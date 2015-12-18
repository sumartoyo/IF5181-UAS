(function() {
	angular.module('app').controller('Derajat1Controller', Derajat1Controller);

	Derajat1Controller.$inject = ['config', 'fileService', 'pyService'];
	
	function Derajat1Controller(config, fileService, pyService) {
		
		var vm = this;
		
		var init = function() {
			vm.srcGray = config.srcEmpty;
			vm.srcSobel = config.srcEmpty;
			vm.srcPrewitt = config.srcEmpty;
			pyService.call('derajat1-sobel.jpg', 'derajat1').then(laksanakan);
		};
		
		var laksanakan = function() {
			vm.srcGray = 'file://'+fileService.dir()+'gray.jpg';
			vm.srcSobel = 'file://'+fileService.dir()+'derajat1-sobel.jpg';
			vm.srcPrewitt = 'file://'+fileService.dir()+'derajat1-prewitt.jpg';
		};
		
		init();
	}
})();