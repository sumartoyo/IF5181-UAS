(function() {
	angular.module('app').factory('loadingService', loadingService);
	
	function loadingService($q) {
		return new (function() {
			var self = this;
			
			var element = $('#modalLoading');
				
			var onCanceled = function() { };
			
			self.show = function() {
				element.modal('show');
				
				return $q(function(resolve, reject) {
					onCanceled = function() {
						self.hide();
						reject();
					};
				});
			};
			
			self.hide = function() {
				element.modal('hide');
			};
			
			$('#modalCancel').click(function() {
				onCanceled();
			});
		})();
	}
})();