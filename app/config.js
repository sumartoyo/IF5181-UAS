(function() {
	angular.module('app').constant('config', new Config());
	
	function Config() {
		var Route = function(name, title, color) {
			this.name = name;
			this.title = title;
			this.color = color;
			
			this.when = '/'+name;
			this.templateUrl = 'app/'+name+'/'+name+'.html';
			this.controller = name[0].toUpperCase()+name.substr(1)+'Controller';
			this.controllerAs = 'vm';
		};
		
		this.links = [
			new Route('histogram', 'Histogram / Open File', 'red'),
			new Route('ekualisasi', 'Ekualisasi Histogram', 'orange'),
			new Route('binary', 'Binary (otsu)', 'aqua'),
			new Route('gauss', 'Gaussian Blur', 'aqua'),
		];
		
		this.py = {
			defaultOptions: {
				pythonPath: 'C:\\exe\\WinPython\\python-2.7.10.amd64\\python.exe',
				script: 'py\\api.py',
			}
		};
		
		this.srcEmpty = 'img/empty.png';
	};
})();