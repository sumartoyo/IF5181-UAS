(function() {
	angular.module('app').controller('BinaryController', BinaryController);

	BinaryController.$inject = ['$scope', 'mainService'];
	
	function BinaryController($scope, mainService) {
		var vm = this;
		
		var init = function() {
			if (mainService.file.input != '') {
				// setup loading
				mainService.loading.onCanceled = function() {
					py.kill(shell);
				};
				
				// laksanakan
				function laksanakan() {
					$('#imgGray').attr('src', 'file://'+mainService.file.dir()+'gray.jpg');
					$('#imgBinary').attr('src', 'file://'+mainService.file.dir()+'binary.jpg');
					
					mainService.loading.hide();
				}
				
				// call python
				mainService.file.readable('binary.jpg', function(err) {
					if (err) {
						mainService.loading.show();
						
						shell = py.run([
							'otsu',
							mainService.file.input,
							mainService.file.id,
						], undefined, undefined, function() {
							laksanakan();
						});
					} else {
						laksanakan();
					}
				});
			}
		};
		
		init();
	}
})();