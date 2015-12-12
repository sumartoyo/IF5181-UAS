(function() {
	angular.module('app').config(['$routeProvider', 'config', routing]);
	
	function routing($routeProvider, config) {
		config.links.forEach(function(link) {
			$routeProvider.when(link.when, link);
		});
		$routeProvider.otherwise({
			redirectTo: config.links[0].when
		});
	}
})();