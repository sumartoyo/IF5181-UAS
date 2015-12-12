(function() {
	angular.module('app').constant('config', new Config());
	
	function Config() {
		this.links = [
			new Route('histogram', 'Histogram / Open File', 'red'),
			new Route('ekualisasi', 'Ekualisasi Histogram', 'orange'),
			new Route('binary', 'Binary (otsu)', 'aqua'),
			new Route('gauss', 'Gaussian Blur', 'aqua'),
		];
	};
	
	function Route(name, title, color) {
		this.name = name;
		this.title = title;
		this.color = color;
		
		this.when = '/'+name;
		this.templateUrl = 'app/'+name+'/'+name+'.html';
		this.controller = name[0].toUpperCase()+name.substr(1)+'Controller';
		this.controllerAs = 'vm';
	};
})();