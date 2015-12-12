(function() {
	angular.module('app').controller('NavController', NavController);

	function NavController($route, config) {
		var vm = this;
		
		vm.$route = $route;
		vm.links = config.links;
	}
})();