(function() {
	angular.module('app').constant('config', new Config());
	
	function Config() {
		this.links = [
			new Route('histogram', 'Histogram / Open File', 'red'),
			new Route('ekualisasi', 'Ekualisasi Histogram', 'orange'),
			new Route('binary', 'Binary (Otsu)', 'aqua'),
			new Route('derajat0', 'Konvolusi Derajat 0', 'aqua'),
			new Route('derajat1', 'Konvolusi Derajat 1', 'aqua'),
			new Route('derajat2', 'Konvolusi Derajat 2', 'aqua'),
			new Route('gauss', 'Gaussian Blur', 'aqua'),
			'gutter1',
			new Route('chaincode', 'Chaincode / Kode Belok', 'aqua'),
			new Route('skeleton', 'Penulangan (Zhang Suen)', 'aqua'),
			new Route('ocr', 'Pengenalan Huruf', 'aqua'),
			'gutter2',
			new Route('faceWarna', 'Wajah (Warna)', 'aqua'),
			new Route('faceBentuk', 'Wajah (Bentuk)', 'aqua'),
			new Route('faceRecognition', 'Pengenalan Wajah', 'aqua'),
		];
		
		this.py = {
			defaultOptions: {
				pythonPath: 'C:\\exe\\WinPython\\python-2.7.10.amd64\\python.exe',
				script: 'py\\api.py',
			}
		};
		
		this.srcEmpty = 'img/empty.png';
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