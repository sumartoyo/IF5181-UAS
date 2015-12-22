(function() {
	angular.module('app').constant('config', new Config());
	
	function Config() {
		this.links = [
			new Route('histogram', 'Histogram / Open File', 'red'),
			new Route('ekualisasi', 'Ekualisasi Histogram', 'green'),
			new Route('binary', 'Binary (Otsu)', 'blue'),
			new Route('derajat0', 'Konvolusi Derajat 0', 'red'),
			new Route('derajat1', 'Konvolusi Derajat 1', 'green'),
			new Route('derajat2', 'Konvolusi Derajat 2', 'blue'),
			new Route('gauss', 'Gaussian Blur', 'red'),
			'gutter1',
			new Route('chaincode', 'Chaincode / Kode Belok', 'green'),
			new Route('skeleton', 'Penulangan (Zhang Suen)', 'blue'),
			new Route('ocr', 'Pengenalan Huruf', 'red'),
			'gutter2',
			new Route('faceWarna', 'Wajah (Warna)', 'green'),
			new Route('faceBentuk', 'Wajah (Bentuk)', 'blue'),
			new Route('faceRecognition', 'Pengenalan Wajah', 'red'),
		];
		
		this.py = {
			defaultOptions: {
				pythonPath: 'WinPython\\python-2.7.10.amd64\\python.exe',
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