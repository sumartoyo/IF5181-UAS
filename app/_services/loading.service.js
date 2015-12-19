(function() {
	angular.module('app').factory('loadingService', loadingService);
	
	function loadingService($q) {
		return new (function() {
			var self = this;
			
			var element = $('#modalLoading');
				
			var onCanceled = function() { };
			
			self.show = function() {
				$('#modalTitle').text('Loading...');
				$('#modalBody').css('display', 'none');
				$('#modalCancel').text('Cancel Operation');
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
			
			self.setText = function(title, body, cancel) {
				$('#modalTitle').text(title || 'Loading...');
				$('#modalBody').css('display', body ? 'block' : 'none');
				$('#modalBody p').text(body || '');
				$('#modalCancel').text(cancel || 'Cancel Operation');
			};
			
			$('#modalCancel').click(function() {
				onCanceled();
			});
		})();
	}
})();